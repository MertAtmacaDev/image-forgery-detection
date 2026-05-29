import { useState, useEffect } from 'react';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);

  // Load logs from localStorage when page mounts
  useEffect(() => {
    const logs = JSON.parse(localStorage.getItem('forgery_history') || '[]');
    setHistory(logs);
  }, []);

  const handleClearHistory = () => {
    if (window.confirm("Are you sure you want to wipe all local analysis logs?")) {
      localStorage.removeItem('forgery_history');
      setHistory([]);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 py-4">
      {/* Header Info Banner */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Analysis History Log</h2>
          <p className="text-gray-400 text-xs mt-0.5">Audit log of previously executed forensic evaluations cached on this machine.</p>
        </div>
        {history.length > 0 && (
          <button
            type="button"
            onClick={handleClearHistory}
            className="text-xs bg-red-50 text-red-600 hover:bg-red-100 font-semibold px-4 py-2 rounded-xl transition-colors border border-red-100"
          >
            Clear All Logs
          </button>
        )}
      </div>

      {/* Main Table Interface */}
      <div className="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden">
        {history.length === 0 ? (
          <div className="text-center py-16 space-y-3">
            <div className="text-4xl">📁</div>
            <p className="text-gray-700 font-semibold">No historical data recorded yet</p>
            <p className="text-gray-400 text-xs max-w-xs mx-auto">Run a full image analysis from the dashboard to initialize the local browser storage log.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100 text-xs font-bold text-gray-400 tracking-wider uppercase">
                  <th className="py-4 px-6">Timestamp</th>
                  <th className="py-4 px-6">Source Filename</th>
                  <th className="py-4 px-6 text-right">System Verdict</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50 text-sm font-medium text-gray-600">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50/50 transition-colors">
                    <td className="py-4 px-6 text-gray-400 font-normal">{item.date}</td>
                    <td className="py-4 px-6 text-gray-800 font-semibold max-w-xs truncate">{item.filename}</td>
                    <td className="py-4 px-6 text-right">
                      <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-bold tracking-wide
                        ${item.overallResult === 'Suspicious'
                          ? 'bg-red-50 text-red-600 border border-red-100'
                          : 'bg-green-50 text-green-600 border border-green-100'
                        }`}
                      >
                        {item.overallResult === 'Suspicious' ? '⚠️ Suspicious' : '✅ Clean'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}