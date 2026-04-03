import { useRef, useState } from 'react';
import axios from 'axios';
import { Upload, FileText } from '@phosphor-icons/react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const UploadSection = ({ onAnalysisStart, onAnalysisComplete }) => {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFile = async (file) => {
    if (!file) return;

    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pdf') && !file.name.toLowerCase().endsWith('.docx')) {
      toast.error('Please upload a PDF or DOCX file');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }

    onAnalysisStart();
    toast.info('Analyzing contract...', { duration: 2000 });

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 120000 // 2 minutes
      });

      toast.success('Analysis complete!');
      onAnalysisComplete(response.data);
    } catch (error) {
      console.error('Upload failed:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed. Please try again.');
      onAnalysisComplete(null);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  return (
    <div className="h-full flex items-center justify-center p-6 sm:p-8">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-8">
          <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500">
            UPLOAD CONTRACT
          </span>
          <h2 className="font-heading text-2xl sm:text-3xl tracking-tight leading-tight font-bold text-slate-900 mt-4 mb-4">
            Analyze Your Legal Contract
          </h2>
          <p className="text-base leading-relaxed text-slate-700">
            Upload a PDF or DOCX file to get started. Our AI will analyze every clause
            and identify potential risks.
          </p>
        </div>

        <div
          data-testid="upload-dropzone"
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-2 border-dashed p-12 text-center transition-colors duration-150 ${
            dragActive
              ? 'border-slate-900 bg-slate-50'
              : 'border-slate-300 bg-white hover:border-slate-400'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx"
            onChange={handleChange}
            className="hidden"
            data-testid="file-input"
          />

          <div className="flex flex-col items-center gap-4">
            <div className="w-16 h-16 border border-slate-900 flex items-center justify-center">
              <Upload size={32} weight="regular" className="text-slate-900" />
            </div>
            <div>
              <p className="text-base text-slate-700 mb-2">
                <span className="font-bold">Drop your contract here</span> or
              </p>
              <Button
                data-testid="browse-button"
                onClick={() => fileInputRef.current?.click()}
                className="rounded-none bg-slate-900 text-white hover:bg-slate-800 font-medium tracking-wide"
              >
                Browse Files
              </Button>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <FileText size={16} weight="regular" />
              <span>Supported formats: PDF, DOCX (Max 10MB)</span>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-slate-50 border border-slate-200 p-6">
          <h4 className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500 mb-4">
            WHAT WE ANALYZE
          </h4>
          <ul className="space-y-2 text-sm text-slate-700">
            <li className="flex items-start gap-2">
              <span className="text-slate-900 font-bold">•</span>
              <span>Clause classification (Termination, Liability, Payment, etc.)</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-slate-900 font-bold">•</span>
              <span>Risk level detection (High, Medium, Safe)</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-slate-900 font-bold">•</span>
              <span>Entity extraction (Parties, Dates, Monetary values)</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-slate-900 font-bold">•</span>
              <span>Overall risk score and actionable suggestions</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default UploadSection;