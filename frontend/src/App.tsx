import React from 'react';
import { useAnalysis } from './hooks/useAnalysis';
import { UploadZone } from './components/UploadZone';
import { DamageSummary } from './components/DamageSummary';
import { RecommendationCard } from './components/RecommendationCard';
import { MapDisplay } from './components/MapDisplay';
import { Loader2, AlertCircle } from 'lucide-react';

function App() {
  const { state, result, error, upload } = useAnalysis();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-6 font-sans">
      <header className="flex items-center justify-between mb-8 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-black tracking-tighter text-white">DISASTER<span className="text-blue-500">RESPONSE</span> AI</h1>
          <p className="text-slate-500 text-sm uppercase tracking-widest">Nepal Emergency Command Center</p>
        </div>
        <div className="flex items-center gap-3">
          <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
            state === 'COMPLETED' ? 'bg-green-500/20 text-green-500' :
            state === 'PROCESSING' ? 'bg-blue-500/20 text-blue-500 animate-pulse' :
            'bg-slate-800 text-slate-500'
          }`}>
            System Status: {state}
          </div>
        </div>
      </header>

      <main className="grid grid-cols-12 gap-6 h-[calc(100vh-160px)]">
        {/* Left Column: Controls & Stats */}
        <div className="col-span-4 flex flex-col gap-6 overflow-y-auto pr-2">
          <section>
            <h2 className="text-sm font-bold text-slate-400 mb-3 uppercase tracking-wider">Image Analysis</h2>
            <UploadZone onUpload={upload} state={state} />
          </section>

          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-center gap-3 text-red-400">
              <AlertCircle className="w-5 h-5" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          {state === 'COMPLETED' && result && (
            <section className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h2 className="text-sm font-bold text-slate-400 mb-3 uppercase tracking-wider">Damage Assessment</h2>
              <DamageSummary data={result} />
            </section>
          )}

          {state === 'PROCESSING' && (
            <div className="flex flex-col items-center justify-center p-12 text-center">
              <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
              <p className="text-slate-400 animate-pulse">Analyzing satellite imagery...</p>
              <p className="text-slate-600 text-xs mt-2">Consulting RAG Guidelines</p>
            </div>
          )}
        </div>

        {/* Right Column: Map & Intelligence */}
        <div className="col-span-8 flex flex-col gap-6">
          <section className="flex-1 relative">
             <h2 className="absolute top-4 left-4 z-10 text-sm font-bold text-white bg-slate-900/80 px-3 py-1 rounded-full border border-slate-700 uppercase tracking-wider">
               Geospatial Analysis
             </h2>
             {state === 'COMPLETED' && result ? (
               <MapDisplay imageUrl={`http://localhost:8000/uploads/${result.location}`} />
             ) : (
               <div className="h-full w-full bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-center text-slate-600 italic">
                 Upload imagery to initialize geospatial view
               </div>
             )}
          </section>

          {state === 'COMPLETED' && result && (
            <section className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <RecommendationCard text={result.recommendation} />
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
