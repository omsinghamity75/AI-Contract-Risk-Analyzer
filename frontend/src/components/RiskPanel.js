import { Shield, Warning, CheckCircle, Clock, CurrencyDollar, Users } from '@phosphor-icons/react';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';

const RiskPanel = ({ analysis, isAnalyzing, selectedClauseIndex, onClauseSelect }) => {
  if (isAnalyzing) {
    return (
      <div className="h-full flex items-center justify-center p-6">
        <div className="text-center">
          <div className="w-12 h-12 border-2 border-slate-900 border-t-transparent animate-spin mx-auto mb-4"></div>
          <p className="text-sm text-slate-500">Processing...</p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return null;
  }

  const getRiskLevel = (score) => {
    if (score >= 60) return { label: 'HIGH RISK', color: 'high', textColor: 'text-red-600' };
    if (score >= 30) return { label: 'MEDIUM RISK', color: 'medium', textColor: 'text-amber-600' };
    return { label: 'LOW RISK', color: 'safe', textColor: 'text-green-600' };
  };

  const riskLevel = getRiskLevel(analysis.risk_score);

  const riskCounts = {
    high: analysis.clauses.filter((c) => c.risk_level === 'high').length,
    medium: analysis.clauses.filter((c) => c.risk_level === 'medium').length,
    safe: analysis.clauses.filter((c) => c.risk_level === 'safe').length
  };

  const categoryIcons = {
    Termination: <Clock size={16} weight="regular" />,
    Liability: <Warning size={16} weight="regular" />,
    Payment: <CurrencyDollar size={16} weight="regular" />,
    Confidentiality: <Shield size={16} weight="regular" />,
    Indemnity: <Warning size={16} weight="regular" />,
    General: <CheckCircle size={16} weight="regular" />
  };

  return (
    <ScrollArea className="h-full">
      <div className="p-6 space-y-6">
        {/* Risk Score */}
        <div data-testid="risk-score-section">
          <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500">
            OVERALL RISK SCORE
          </span>
          <div className="mt-4">
            <div className="flex items-end gap-3 mb-3">
              <span className="font-heading text-5xl font-bold text-slate-900">
                {analysis.risk_score}
              </span>
              <span className="text-slate-500 mb-2">/100</span>
            </div>
            <div className="risk-gauge mb-2">
              <div
                className={`risk-gauge-fill ${riskLevel.color}`}
                style={{ width: `${analysis.risk_score}%` }}
              ></div>
            </div>
            <p className={`text-xs uppercase tracking-[0.2em] font-bold ${riskLevel.textColor}`}>
              {riskLevel.label}
            </p>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="border-t border-slate-200 pt-6">
          <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500 mb-4 block">
            RISK DISTRIBUTION
          </span>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">High Risk</span>
              <span className="font-bold text-red-600">{riskCounts.high}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">Medium Risk</span>
              <span className="font-bold text-amber-600">{riskCounts.medium}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">Safe</span>
              <span className="font-bold text-green-600">{riskCounts.safe}</span>
            </div>
          </div>
        </div>

        {/* Entities */}
        {(analysis.entities.parties.length > 0 ||
          analysis.entities.organizations.length > 0 ||
          analysis.entities.dates.length > 0 ||
          analysis.entities.money.length > 0) && (
          <div className="border-t border-slate-200 pt-6">
            <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500 mb-4 block">
              EXTRACTED ENTITIES
            </span>
            <div className="space-y-3">
              {analysis.entities.organizations.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Users size={14} weight="regular" className="text-slate-500" />
                    <span className="text-xs font-bold text-slate-500">PARTIES</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {analysis.entities.organizations.map((entity, idx) => (
                      <Badge key={idx} variant="outline" className="rounded-none font-mono text-xs">
                        {entity}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              {analysis.entities.dates.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Clock size={14} weight="regular" className="text-slate-500" />
                    <span className="text-xs font-bold text-slate-500">DATES</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {analysis.entities.dates.slice(0, 5).map((entity, idx) => (
                      <Badge key={idx} variant="outline" className="rounded-none font-mono text-xs">
                        {entity}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              {analysis.entities.money.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <CurrencyDollar size={14} weight="regular" className="text-slate-500" />
                    <span className="text-xs font-bold text-slate-500">AMOUNTS</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {analysis.entities.money.slice(0, 5).map((entity, idx) => (
                      <Badge key={idx} variant="outline" className="rounded-none font-mono text-xs">
                        {entity}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Clauses List */}
        <div className="border-t border-slate-200 pt-6">
          <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500 mb-4 block">
            CLAUSE ANALYSIS
          </span>
          <div className="space-y-3">
            {analysis.clauses.map((clause, index) => (
              <div
                key={index}
                data-testid={`risk-card-${index}`}
                onClick={() => onClauseSelect(index)}
                className={`bg-white border transition-colors duration-150 cursor-pointer ${
                  selectedClauseIndex === index
                    ? 'border-slate-900 ring-2 ring-slate-900'
                    : 'border-slate-200 hover:border-slate-400'
                } p-4`}
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-slate-400">
                      {String(index + 1).padStart(2, '0')}
                    </span>
                    <span className="text-xs font-bold uppercase tracking-wide text-slate-700">
                      {clause.category}
                    </span>
                  </div>
                  <Badge
                    variant="outline"
                    className={`rounded-none text-xs ${
                      clause.risk_level === 'high'
                        ? 'border-red-200 bg-red-50 text-red-600'
                        : clause.risk_level === 'medium'
                        ? 'border-amber-200 bg-amber-50 text-amber-600'
                        : 'border-green-200 bg-green-50 text-green-600'
                    }`}
                  >
                    {clause.risk_level.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-sm text-slate-700 mb-2 line-clamp-2">{clause.text}</p>
                {clause.explanation && (
                  <p className="text-xs text-slate-500 mb-2">{clause.explanation}</p>
                )}
                {clause.suggestion && (
                  <div className="bg-slate-50 border-l-2 border-slate-900 p-2 mt-2">
                    <p className="text-xs text-slate-700">
                      <span className="font-bold">Suggestion:</span> {clause.suggestion}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </ScrollArea>
  );
};

export default RiskPanel;