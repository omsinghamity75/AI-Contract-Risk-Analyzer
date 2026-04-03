import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from '@phosphor-icons/react';
import { Button } from '@/components/ui/button';
import UploadSection from '@/components/UploadSection';
import DocumentViewer from '@/components/DocumentViewer';
import RiskPanel from '@/components/RiskPanel';

const AnalyzerPage = () => {
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedClauseIndex, setSelectedClauseIndex] = useState(null);

  const handleAnalysisComplete = (analysisData) => {
    setAnalysis(analysisData);
    setIsAnalyzing(false);
  };

  const handleNewAnalysis = () => {
    setAnalysis(null);
    setSelectedClauseIndex(null);
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-slate-200">
        <div className="px-6 sm:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                data-testid="back-button"
                onClick={() => navigate('/')}
                variant="ghost"
                className="rounded-none hover:bg-slate-100 p-2"
              >
                <ArrowLeft size={24} weight="regular" />
              </Button>
              <h1 className="font-heading text-2xl font-bold tracking-tight text-slate-900">
                CONTRACT<span className="text-slate-500">ANALYZER</span>
              </h1>
            </div>
            {analysis && (
              <Button
                data-testid="new-analysis-button"
                onClick={handleNewAnalysis}
                className="rounded-none bg-slate-900 text-white hover:bg-slate-800 font-medium tracking-wide"
              >
                New Analysis
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="h-[calc(100vh-89px)]">
        {!analysis && !isAnalyzing ? (
          <UploadSection
            onAnalysisStart={() => setIsAnalyzing(true)}
            onAnalysisComplete={handleAnalysisComplete}
          />
        ) : (
          <div className="h-full flex" data-testid="analysis-view">
            {/* Left Pane - Document Viewer */}
            <div className="flex-1 overflow-auto border-r border-slate-200">
              <DocumentViewer
                analysis={analysis}
                isAnalyzing={isAnalyzing}
                selectedClauseIndex={selectedClauseIndex}
                onClauseClick={setSelectedClauseIndex}
              />
            </div>

            {/* Right Pane - Risk Panel */}
            <div className="w-96 overflow-auto bg-slate-50">
              <RiskPanel
                analysis={analysis}
                isAnalyzing={isAnalyzing}
                selectedClauseIndex={selectedClauseIndex}
                onClauseSelect={setSelectedClauseIndex}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalyzerPage;