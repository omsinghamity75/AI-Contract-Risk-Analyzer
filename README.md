 📄 AI Contract Risk Analyzer

An intelligent AI-powered tool that analyzes legal contracts and identifies potential risks, clauses, and key entities. This project helps users quickly understand complex agreements using NLP and AI.

---

## 🚀 Features

* 🔍 **Contract Analysis** – Upload PDF contracts and extract meaningful insights
* ⚠️ **Risk Detection** – Identifies risky clauses and highlights potential issues
* 🧠 **AI-Powered Insights** – Uses NLP and AI models for smart interpretation
* 📑 **Clause Segmentation** – Breaks contracts into readable sections
* 🏷️ **Named Entity Recognition (NER)** – Detects entities like names, dates, organizations
* 📊 **User-Friendly UI** – Built with Streamlit for easy interaction

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Libraries Used:**

  * `streamlit`
  * `spacy`
  * `pdfplumber`
  * `openai`
  * `pandas`
  * `python-dotenv` 

---

## 📂 Project Structure

```
AI-Contract-Risk-Analyzer/
│
├── app/
│   └── app.py                # Main Streamlit app
│
├── src/
│   ├── preprocess.py        # Text cleaning & preprocessing
│   ├── clause_splitter.py   # Splits contract into clauses
│   ├── analyzer.py          # Risk analysis logic
│   ├── ner.py               # Named Entity Recognition
│   └── risk_scoring.py      # Risk scoring system
│
├── requirements.txt         # Dependencies
├── .env                     # API keys
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI-Contract-Risk-Analyzer.git
cd AI-Contract-Risk-Analyzer
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

* Windows:

```bash
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory and add your API key:

```
OPENAI_API_KEY=your_api_key_here
```

(Required for AI-based analysis) 

---

## ▶️ Run the Application

```bash
streamlit run app/app.py
```

Then open:

```
http://localhost:8501
```

---

## 📌 How It Works

1. Upload a contract PDF
2. Extract text using `pdfplumber`
3. Preprocess and clean the text
4. Split into clauses
5. Apply NLP + AI models
6. Identify risks and entities
7. Display results in UI

---

## ⚠️ Challenges

* Handling complex legal language
* Accurate clause segmentation
* Risk classification precision
* Processing large documents efficiently

---

## 🔮 Future Improvements

* ✅ Better AI models for risk prediction
* 📊 Visualization dashboards
* 🌐 Multi-language support
* 🔐 Enhanced data security
* 📁 Support for more file formats (DOCX, TXT)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make changes
4. Submit a pull request

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Om Singh**
AI & Full Stack Enthusiast




