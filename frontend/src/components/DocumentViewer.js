import { useEffect, useRef } from 'react';
import { FileText } from '@phosphor-icons/react';

const DocumentViewer = ({ analysis, isAnalyzing, selectedClauseIndex, onClauseClick }) => {
  const viewerRef = useRef(null);

  useEffect(() => {
    if (selectedClauseIndex !== null && viewerRef.current) {
      const element = viewerRef.current.querySelector(`[data-clause-index="${selectedClauseIndex}"]`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, [selectedClauseIndex]);

  if (isAnalyzing) {
    return (
      <div className="h-full flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="w-16 h-16 border-2 border-slate-900 border-t-transparent animate-spin mx-auto mb-6"></div>
          <h3 className="font-heading text-xl font-bold text-slate-900 mb-2">
            Analyzing Contract...
          </h3>
          <p className="text-sm text-slate-500">
            Extracting text, segmenting clauses, and detecting risks with AI.
            This may take a moment.
          </p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  const renderClauseWithHighlight = (clause) => {
    let text = clause.text;

    // Highlight risky keywords
    if (clause.keywords && clause.keywords.length > 0) {
      clause.keywords.forEach((keyword) => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
        text = text.replace(
          regex,
          (match) => `<mark class="entity-highlight">${match}</mark>`
        );
      });
    }

    return <span dangerouslySetInnerHTML={{ __html: text }} />;
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'high':
        return 'high-risk';
      case 'medium':
        return 'medium-risk';
      case 'safe':
      default:
        return 'safe';
    }
  };

  return (
    <div ref={viewerRef} className="p-6 sm:p-8 max-w-4xl mx-auto">
      {/* Document Header */}
      <div className="mb-8 pb-6 border-b border-slate-200">
        <div className="flex items-start gap-3 mb-4">
          <FileText size={24} weight="regular" className="text-slate-900 mt-1" />
          <div>
            <h2 className="font-heading text-xl sm:text-2xl tracking-tight font-medium text-slate-900">
              {analysis.filename}
            </h2>
            <p className="text-sm text-slate-500 mt-1">
              {analysis.clauses.length} clauses analyzed
            </p>
          </div>
        </div>
      </div>

      {/* Clauses */}
      <div className="space-y-4 font-body">
        {analysis.clauses.map((clause, index) => (
          <div
            key={index}
            data-testid={`clause-${index}`}
            data-clause-index={index}
            onClick={() => onClauseClick(index)}
            className={`clause-highlight ${getRiskColor(clause.risk_level)} ${
              selectedClauseIndex === index ? 'ring-2 ring-slate-900 ring-offset-2' : ''
            } p-4 transition-colors duration-150`}
          >
            <div className="flex items-start gap-3">
              <span className="text-xs font-mono font-bold text-slate-400 mt-1">
                {String(index + 1).padStart(2, '0')}
              </span>
              <p className="text-base leading-relaxed text-slate-700 flex-1">
                {renderClauseWithHighlight(clause)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentViewer;