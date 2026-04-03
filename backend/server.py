from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import requests
import pdfplumber
import docx
import spacy
import re
from emergentintegrations.llm.chat import LlmChat, UserMessage
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Storage configuration
STORAGE_URL = "https://integrations.emergentagent.com/objstore/api/v1/storage"
EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY")
APP_NAME = "contract-analyzer"
storage_key = None

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Storage functions
def init_storage():
    """Initialize storage and return storage key"""
    global storage_key
    if storage_key:
        return storage_key
    try:
        resp = requests.post(
            f"{STORAGE_URL}/init",
            json={"emergent_key": EMERGENT_KEY},
            timeout=30
        )
        resp.raise_for_status()
        storage_key = resp.json()["storage_key"]
        logger.info("Storage initialized successfully")
        return storage_key
    except Exception as e:
        logger.error(f"Storage initialization failed: {e}")
        raise

def put_object(path: str, data: bytes, content_type: str) -> dict:
    """Upload file to storage"""
    key = init_storage()
    resp = requests.put(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key, "Content-Type": content_type},
        data=data,
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()

def get_object(path: str) -> tuple:
    """Download file from storage"""
    key = init_storage()
    resp = requests.get(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key},
        timeout=60
    )
    resp.raise_for_status()
    return resp.content, resp.headers.get("Content-Type", "application/octet-stream")

# Document processing functions
def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF"""
    from io import BytesIO
    text = ""
    with pdfplumber.open(BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text.strip()

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX"""
    from io import BytesIO
    doc = docx.Document(BytesIO(file_content))
    text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()

def segment_clauses(text: str) -> List[Dict[str, Any]]:
    """Segment contract into clauses using spaCy"""
    doc = nlp(text)
    clauses = []
    current_clause = []
    
    for sent in doc.sents:
        sent_text = sent.text.strip()
        if not sent_text:
            continue
        
        current_clause.append(sent_text)
        
        # Split on clause boundaries (numbered sections, new paragraphs, etc.)
        if len(current_clause) >= 2 or re.match(r'^\d+\.', sent_text):
            clause_text = " ".join(current_clause)
            if len(clause_text) > 20:  # Filter out very short clauses
                clauses.append({
                    "text": clause_text,
                    "index": len(clauses)
                })
                current_clause = []
    
    # Add remaining clause
    if current_clause:
        clause_text = " ".join(current_clause)
        if len(clause_text) > 20:
            clauses.append({
                "text": clause_text,
                "index": len(clauses)
            })
    
    return clauses

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract named entities from text"""
    doc = nlp(text)
    entities = {
        "parties": [],
        "dates": [],
        "money": [],
        "organizations": []
    }
    
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            if ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            else:
                entities["parties"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
        elif ent.label_ == "MONEY":
            entities["money"].append(ent.text)
    
    # Deduplicate
    for key in entities:
        entities[key] = list(set(entities[key]))
    
    return entities

async def analyze_clauses_with_gpt(clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze clauses using GPT-5.2"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=str(uuid.uuid4()),
            system_message="You are a legal contract analysis expert. Analyze contract clauses and identify risks."
        ).with_model("openai", "gpt-5.2")
        
        # Analyze in batches to avoid token limits
        batch_size = 5
        analyzed_clauses = []
        
        for i in range(0, len(clauses), batch_size):
            batch = clauses[i:i + batch_size]
            clauses_text = "\n\n".join([f"Clause {c['index'] + 1}: {c['text']}" for c in batch])
            
            prompt = f"""Analyze these contract clauses and for each clause provide:
1. Category (Termination, Liability, Payment, Confidentiality, Indemnity, General, Other)
2. Risk Level (safe, medium, high)
3. Risk Explanation (why it's risky or safe)
4. Risky Keywords (list of concerning terms found)
5. Suggestion (how to improve or what to watch out for)

Clauses:
{clauses_text}

Respond in JSON format as an array of objects with fields: clause_index, category, risk_level, explanation, keywords, suggestion."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse JSON response
            try:
                # Extract JSON from markdown code blocks if present
                response_text = response.strip()
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                batch_analysis = json.loads(response_text)
                analyzed_clauses.extend(batch_analysis)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse GPT response: {e}")
                # Fallback analysis
                for c in batch:
                    analyzed_clauses.append({
                        "clause_index": c["index"],
                        "category": "General",
                        "risk_level": "safe",
                        "explanation": "Analysis temporarily unavailable",
                        "keywords": [],
                        "suggestion": "Review manually"
                    })
        
        # Merge analysis with original clauses
        for clause in clauses:
            analysis = next(
                (a for a in analyzed_clauses if a.get("clause_index") == clause["index"]),
                None
            )
            if analysis:
                clause.update({
                    "category": analysis.get("category", "General"),
                    "risk_level": analysis.get("risk_level", "safe"),
                    "explanation": analysis.get("explanation", ""),
                    "keywords": analysis.get("keywords", []),
                    "suggestion": analysis.get("suggestion", "")
                })
            else:
                clause.update({
                    "category": "General",
                    "risk_level": "safe",
                    "explanation": "No analysis available",
                    "keywords": [],
                    "suggestion": ""
                })
        
        return clauses
    except Exception as e:
        logger.error(f"GPT analysis failed: {e}")
        # Return clauses with default analysis
        for clause in clauses:
            clause.update({
                "category": "General",
                "risk_level": "safe",
                "explanation": "Analysis failed",
                "keywords": [],
                "suggestion": "Review manually"
            })
        return clauses

def calculate_risk_score(clauses: List[Dict[str, Any]]) -> int:
    """Calculate overall risk score (0-100)"""
    if not clauses:
        return 0
    
    risk_weights = {
        "high": 10,
        "medium": 5,
        "safe": 0
    }
    
    total_risk = sum(risk_weights.get(c.get("risk_level", "safe"), 0) for c in clauses)
    max_possible_risk = len(clauses) * risk_weights["high"]
    
    if max_possible_risk == 0:
        return 0
    
    risk_score = int((total_risk / max_possible_risk) * 100)
    return min(100, risk_score)

# Models
class ContractAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    storage_path: str
    content_type: str
    file_size: int
    extracted_text: str
    clauses: List[Dict[str, Any]]
    entities: Dict[str, List[str]]
    risk_score: int
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    filename: str
    risk_score: int
    clauses: List[Dict[str, Any]]
    entities: Dict[str, List[str]]
    created_at: str

# Routes
@api_router.get("/")
async def root():
    return {"message": "AI Contract Risk Analyzer API"}

@api_router.post("/upload", response_model=AnalysisResponse)
async def upload_contract(file: UploadFile = File(...)):
    """Upload and analyze a contract"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_content)
        else:
            extracted_text = extract_text_from_docx(file_content)
        
        if not extracted_text or len(extracted_text) < 50:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from document")
        
        # Upload to storage
        ext = file.filename.split(".")[-1]
        storage_path = f"{APP_NAME}/uploads/{uuid.uuid4()}.{ext}"
        storage_result = put_object(storage_path, file_content, file.content_type or "application/octet-stream")
        
        # Segment clauses
        clauses = segment_clauses(extracted_text)
        
        # Extract entities
        entities = extract_entities(extracted_text)
        
        # Analyze clauses with GPT
        analyzed_clauses = await analyze_clauses_with_gpt(clauses)
        
        # Calculate risk score
        risk_score = calculate_risk_score(analyzed_clauses)
        
        # Create analysis record
        analysis = ContractAnalysis(
            filename=file.filename,
            storage_path=storage_result["path"],
            content_type=file.content_type or "application/octet-stream",
            file_size=storage_result["size"],
            extracted_text=extracted_text,
            clauses=analyzed_clauses,
            entities=entities,
            risk_score=risk_score
        )
        
        # Save to database
        doc = analysis.model_dump()
        await db.contract_analyses.insert_one(doc)
        
        return AnalysisResponse(
            id=analysis.id,
            filename=analysis.filename,
            risk_score=analysis.risk_score,
            clauses=analysis.clauses,
            entities=analysis.entities,
            created_at=analysis.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@api_router.get("/analyses", response_model=List[AnalysisResponse])
async def get_analyses():
    """Get all analyses"""
    analyses = await db.contract_analyses.find({}, {"_id": 0, "extracted_text": 0, "storage_path": 0}).to_list(100)
    return analyses

@api_router.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    """Get specific analysis"""
    analysis = await db.contract_analyses.find_one({"id": analysis_id}, {"_id": 0, "extracted_text": 0, "storage_path": 0})
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@app.on_event("startup")
async def startup():
    try:
        init_storage()
        logger.info("Storage initialized")
    except Exception as e:
        logger.error(f"Storage init failed: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)