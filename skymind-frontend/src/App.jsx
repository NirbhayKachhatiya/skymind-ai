import React, { useState } from 'react';
import { Plane, Search, ShieldCheck, Clock, Sliders, AlertCircle, Compass, RefreshCw, ArrowRight, User, MapPin } from 'lucide-react';

export default function App() {
  const [userId, setUserId] = useState('U01');
  const [origin, setOrigin] = useState('BOM');
  const [destination, setDestination] = useState('LHR');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const handleFetchRecommendations = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: String(userId).trim(),
          origin: String(origin).toUpperCase().trim(),
          destination: String(destination).toUpperCase().trim()
        })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to fetch recommendations.');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 antialiased p-4 sm:p-8 flex flex-col justify-between selection:bg-indigo-500/40">
      
      {/* Glow Effects */}
      <div className="absolute top-0 left-1/3 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-fuchsia-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div className="max-w-6xl w-full mx-auto space-y-8 flex-grow">
        {/* --- Header --- */}
        <header className="flex items-center justify-between border-b border-slate-800 pb-5">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-tr from-indigo-500 to-fuchsia-500 p-2.5 rounded-xl shadow-lg text-white">
              <Plane className="h-5 w-5 transform -rotate-45" />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-wide bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                SkyMind<span className="text-indigo-400 font-bold">.ai</span>
              </h1>
              <p className="text-[10px] text-slate-500 font-mono tracking-widest uppercase">Flight Optimization Cluster</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 bg-slate-900/80 border border-slate-800 rounded-full text-xs text-cyan-400 font-mono shadow-sm">
            <span className="h-2 w-2 rounded-full bg-cyan-400 shadow-md animate-pulse"></span>
            Online
          </div>
        </header>

        {/* --- Dynamic Grid Matrix --- */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* === Control Input Panel === */}
          <div className="lg:col-span-4 bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 shadow-xl relative backdrop-blur-sm self-start">
            <div className="flex items-center gap-2.5 mb-6 border-b border-slate-800 pb-3">
              <Compass className="h-4 w-4 text-indigo-400" />
              <h2 className="font-bold text-sm uppercase text-slate-200 tracking-wider">Search Hub</h2>
            </div>

            <form onSubmit={handleFetchRecommendations} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1.5">Traveler ID</label>
                <div className="relative">
                  <User className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-indigo-400" />
                  <input 
                    type="text" 
                    value={userId} 
                    onChange={(e) => setUserId(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white font-mono transition-colors"
                    placeholder="e.g. U01"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">Origin</label>
                  <div className="relative">
                    <MapPin className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-fuchsia-400" />
                    <input 
                      type="text" 
                      value={origin} 
                      onChange={(e) => setOrigin(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-3 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white font-bold tracking-wide uppercase text-center transition-colors"
                      placeholder="BOM"
                      maxLength={3}
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1.5">Destination</label>
                  <div className="relative">
                    <MapPin className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-cyan-400" />
                    <input 
                      type="text" 
                      value={destination} 
                      onChange={(e) => setDestination(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-3 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white font-bold tracking-wide uppercase text-center transition-colors"
                      placeholder="LHR"
                      maxLength={3}
                      required
                    />
                  </div>
                </div>
              </div>

              <button 
                type="submit" 
                disabled={loading}
                className="w-full mt-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-fuchsia-600 hover:opacity-90 text-white rounded-xl py-3.5 text-xs font-bold uppercase tracking-widest transition-all shadow-md active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-40"
              >
                {loading ? (
                  <>
                    <RefreshCw className="h-4 w-4 animate-spin" />
                    Optimizing Vectors...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    Search Paths
                  </>
                )}
              </button>
            </form>

            {error && (
              <div className="mt-4 bg-rose-500/10 border border-rose-500/20 rounded-xl p-4 flex items-start gap-3 text-rose-200">
                <AlertCircle className="h-4 w-4 text-rose-400 shrink-0 mt-0.5" />
                <p className="text-xs font-mono break-all leading-relaxed">{error}</p>
              </div>
            )}
          </div>

          {/* === Recommendations Workspace Display Panel === */}
          <div className="lg:col-span-8 space-y-6">
            {data ? (
              <>
                {/* Profile Header Metadata Summary Card */}
                <div className="bg-gradient-to-r from-slate-900 to-indigo-950/40 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <span className="text-[10px] font-mono font-bold tracking-wider text-indigo-400 uppercase block mb-1">Active Traveler Target</span>
                    <h3 className="text-xl font-black text-white">{data.traveler_name}</h3>
                    <div className="flex items-center gap-2 mt-2 text-xs text-slate-400 font-mono">
                      <span className="bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800 text-indigo-300 font-bold">{data.origin}</span>
                      <ArrowRight className="h-3 w-3 text-slate-600" />
                      <span className="bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800 text-fuchsia-300 font-bold">{data.destination}</span>
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <div className="bg-slate-950/80 border border-slate-800 px-4 py-2 rounded-xl text-center min-w-[110px]">
                      <span className="text-[9px] text-slate-500 font-mono uppercase tracking-wider block mb-1">Budget Bias</span>
                      <span className="text-xs font-mono font-bold text-indigo-400">{(data.metrics_applied.budget_sensitivity).toFixed(2)}</span>
                    </div>
                    <div className="bg-slate-950/80 border border-slate-800 px-4 py-2 rounded-xl text-center min-w-[110px]">
                      <span className="text-[9px] text-slate-500 font-mono uppercase tracking-wider block mb-1">Comfort Bias</span>
                      <span className="text-xs font-mono font-bold text-fuchsia-400">{(data.metrics_applied.convenience_priority).toFixed(2)}</span>
                    </div>
                  </div>
                </div>

                {/* Recommendations Results List Feed */}
                <div className="space-y-4">
                  {data.recommendations.map((rec) => {
                    const flightLeg = rec.itinerary.flights[0];
                    const isTopRank = rec.rank === 1;
                    return (
                      <div 
                        key={rec.rank}
                        className={`bg-slate-900/40 border rounded-2xl shadow-lg overflow-hidden transition-all duration-200 ${
                          isTopRank ? 'border-fuchsia-500/40 shadow-fuchsia-500/[0.02] ring-1 ring-fuchsia-500/10' : 'border-slate-800/80'
                        }`}
                      >
                        <div className={`px-5 py-2.5 flex items-center justify-between border-b ${
                          isTopRank ? 'bg-fuchsia-950/20 border-fuchsia-500/20' : 'bg-slate-950/50 border-slate-800'
                        }`}>
                          <span className="text-xs font-bold font-mono tracking-wider uppercase text-slate-300">
                            Route Proposal 0{rec.rank}
                          </span>
                          {isTopRank && (
                            <span className="text-[9px] bg-gradient-to-r from-fuchsia-500 to-purple-600 text-white font-black px-2.5 py-0.5 rounded-full uppercase tracking-wider shadow-sm">
                              Optimal Solution
                            </span>
                          )}
                        </div>

                        <div className="p-5 space-y-4">
                          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/60 pb-4">
                            
                            <div className="flex items-center gap-4 sm:gap-6 flex-wrap min-w-0">
                              <div>
                                <div className="text-xl font-bold font-mono tracking-wide text-white">{flightLeg.origin}</div>
                                <div className="text-[11px] text-indigo-400 font-mono mt-0.5">
                                  {new Date(flightLeg.departure_time).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                                </div>
                              </div>

                              <div className="flex flex-col items-center w-24 sm:w-28 shrink-0">
                                <span className="text-[10px] font-mono text-purple-300 flex items-center gap-1 mb-1">
                                  <Clock className="h-3 w-3" /> {rec.itinerary.total_duration_minutes}m
                                </span>
                                <div className="w-full h-[1px] bg-gradient-to-r from-indigo-500 via-purple-500 to-fuchsia-500 relative flex items-center justify-center">
                                  <div className="absolute h-1.5 w-1.5 rounded-full bg-fuchsia-400"></div>
                                </div>
                                <span className="text-[10px] text-slate-500 font-mono mt-1.5 uppercase tracking-wide">
                                  {rec.itinerary.total_stops === 0 ? 'Non-Stop' : `${rec.itinerary.total_stops} stop`}
                                </span>
                              </div>

                              <div>
                                <div className="text-xl font-bold font-mono tracking-wide text-white">{flightLeg.destination}</div>
                                <div className="text-[11px] text-cyan-400 font-mono mt-0.5">
                                  {new Date(flightLeg.arrival_time).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                                </div>
                              </div>
                            </div>

                            <div className="min-w-[120px] border-l border-slate-800 pl-4">
                              <span className="text-[9px] text-slate-500 font-mono uppercase tracking-wider block">Carrier</span>
                              <div className="text-xs font-bold text-slate-300 mt-0.5 truncate">{flightLeg.airline}</div>
                              <div className="text-[10px] text-slate-500 font-mono">ID: {flightLeg.flight_id}</div>
                            </div>

                            <div className="bg-slate-950 border border-slate-800 px-4 py-2 rounded-xl text-left md:text-right shrink-0 min-w-[115px] flex items-center md:inline-block justify-between shadow-inner">
                              <span className="text-[9px] text-slate-500 font-mono uppercase block">Computed Cost</span>
                              <span className="text-xl font-bold font-mono text-emerald-400 md:mt-0.5 block">${rec.itinerary.total_price.toFixed(2)}</span>
                            </div>

                          </div>

                          <div className="bg-slate-950/60 border border-slate-800/50 rounded-xl p-4 flex items-start gap-3">
                            <Sliders className="h-4 w-4 text-indigo-400 shrink-0 mt-0.5" />
                            <div className="space-y-1">
                              <span className="text-[10px] font-bold tracking-wider text-indigo-400 font-mono block uppercase">AI Alignment Rationale</span>
                              <p className="text-xs text-slate-300 leading-relaxed text-justify font-normal break-words">{rec.recommendation_rationale}</p>
                            </div>
                          </div>

                        </div>
                      </div>
                    );
                  })}
                </div>
              </>
            ) : (
              /* Ready State Standby Box Display Canvas */
              <div className="h-[430px] border border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-center p-6 bg-slate-900/10 backdrop-blur-[1px]">
                <div className="bg-gradient-to-tr from-indigo-500 to-fuchsia-500 p-3.5 rounded-xl text-white mb-4 shadow-md">
                  <ShieldCheck className="h-6 w-6" />
                </div>
                <h3 className="text-sm font-bold tracking-wide uppercase text-slate-300">Telemetry Channel Standby</h3>
                <p className="text-xs text-slate-500 max-w-xs mt-2 leading-relaxed font-normal">
                  Provide cataloged traveler identity specifications and destination targets in the control layout panel to compute recommendations.
                </p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}