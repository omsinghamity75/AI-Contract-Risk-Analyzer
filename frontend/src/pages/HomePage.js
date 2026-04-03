import { useNavigate } from 'react-router-dom';
import { FileText, Shield, ChartLineUp, CheckCircle } from '@phosphor-icons/react';
import { Button } from '@/components/ui/button';

const HomePage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <FileText size={32} weight="regular" />,
      title: 'Document Analysis',
      description: 'Upload PDF or DOCX contracts for comprehensive analysis'
    },
    {
      icon: <Shield size={32} weight="regular" />,
      title: 'Risk Detection',
      description: 'AI-powered identification of unfair and risky clauses'
    },
    {
      icon: <ChartLineUp size={32} weight="regular" />,
      title: 'Risk Scoring',
      description: 'Get an overall risk score from 0-100 with detailed breakdown'
    },
    {
      icon: <CheckCircle size={32} weight="regular" />,
      title: 'Smart Suggestions',
      description: 'Actionable recommendations to improve contract safety'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-6">
          <div className="flex items-center justify-between">
            <h1 className="font-heading text-2xl font-bold tracking-tight text-slate-900">
              CONTRACT<span className="text-slate-500">ANALYZER</span>
            </h1>
            <Button
              data-testid="nav-analyze-button"
              onClick={() => navigate('/analyzer')}
              className="rounded-none bg-slate-900 text-white hover:bg-slate-800 font-medium tracking-wide"
            >
              START ANALYSIS
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 sm:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-block mb-4">
              <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500">
                AI-POWERED LEGAL ANALYSIS
              </span>
            </div>
            <h2 className="font-heading text-4xl sm:text-5xl lg:text-6xl tracking-tight leading-none font-bold text-slate-900 mb-6">
              Detect Contract Risks Before You Sign
            </h2>
            <p className="text-base leading-relaxed text-slate-700 mb-8 max-w-prose">
              Upload your legal contracts and let our AI analyze every clause.
              Identify risky terms, get risk scores, and receive actionable suggestions
              to protect your interests.
            </p>
            <Button
              data-testid="hero-get-started-button"
              onClick={() => navigate('/analyzer')}
              className="rounded-none bg-slate-900 text-white hover:bg-slate-800 px-8 py-6 text-base font-bold uppercase tracking-wide"
            >
              Analyze Contract Now
            </Button>
          </div>
          <div className="relative">
            <img
              src="https://images.pexels.com/photos/7821573/pexels-photo-7821573.jpeg"
              alt="Contract analysis"
              className="w-full h-[500px] object-cover border border-slate-200"
            />
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-slate-50 border-t border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-20">
          <div className="text-center mb-16">
            <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500">
              FEATURES
            </span>
            <h3 className="font-heading text-2xl sm:text-3xl tracking-tight leading-tight font-bold text-slate-900 mt-4">
              Comprehensive Contract Intelligence
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white border border-slate-200 p-6 hover:border-slate-400 transition-colors duration-150"
                data-testid={`feature-card-${index}`}
              >
                <div className="text-slate-900 mb-4">{feature.icon}</div>
                <h4 className="text-lg font-bold uppercase tracking-wide text-slate-900 mb-2">
                  {feature.title}
                </h4>
                <p className="text-sm text-slate-500">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="max-w-7xl mx-auto px-6 sm:px-8 py-20">
        <div className="text-center mb-16">
          <span className="text-xs uppercase tracking-[0.2em] font-bold text-slate-500">
            PROCESS
          </span>
          <h3 className="font-heading text-2xl sm:text-3xl tracking-tight leading-tight font-bold text-slate-900 mt-4">
            How It Works
          </h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { step: '01', title: 'Upload Contract', description: 'Upload your PDF or DOCX contract file' },
            { step: '02', title: 'AI Analysis', description: 'Our AI analyzes clauses and detects risks' },
            { step: '03', title: 'Get Insights', description: 'Review risk scores and actionable suggestions' }
          ].map((item, index) => (
            <div key={index} className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 border-2 border-slate-900 text-slate-900 font-heading font-bold text-2xl mb-4">
                {item.step}
              </div>
              <h4 className="text-lg font-bold uppercase tracking-wide text-slate-900 mb-2">
                {item.title}
              </h4>
              <p className="text-sm text-slate-500">{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-20 text-center">
          <h3 className="font-heading text-2xl sm:text-3xl tracking-tight leading-tight font-bold mb-6">
            Ready to Analyze Your Contract?
          </h3>
          <p className="text-base text-slate-300 mb-8 max-w-2xl mx-auto">
            Get instant AI-powered insights into your legal agreements
          </p>
          <Button
            data-testid="cta-start-button"
            onClick={() => navigate('/analyzer')}
            className="rounded-none bg-white text-slate-900 hover:bg-slate-100 px-8 py-6 text-base font-bold uppercase tracking-wide"
          >
            Start Analysis
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-8">
          <p className="text-sm text-slate-500 text-center">
            © 2026 Contract Analyzer. AI-powered contract risk analysis.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;