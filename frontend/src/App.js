import { BrowserRouter, Routes, Route } from 'react-router-dom';
import '@/App.css';
import HomePage from '@/pages/HomePage';
import AnalyzerPage from '@/pages/AnalyzerPage';
import { Toaster } from '@/components/ui/sonner';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/analyzer" element={<AnalyzerPage />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;