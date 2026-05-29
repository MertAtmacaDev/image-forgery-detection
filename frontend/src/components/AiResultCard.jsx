export default function AiResultCard({ model, prediction, confidence }) {
  const isTampered = prediction.toLowerCase() === 'tampered';
  const percentage = Math.round(confidence * 100);

  return (
    <div className="bg-white rounded-xl shadow-xs border border-gray-100 p-5 space-y-4 flex flex-col justify-between">
      {/* Header Info */}
      <div className="flex justify-between items-start">
        <div>
          <h4 className="text-base font-bold text-gray-800 tracking-tight">{model}</h4>
          <p className="text-xs text-gray-400 mt-0.5">Deep Learning Network</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wider capitalize
          ${isTampered 
            ? 'bg-red-100 text-red-700 border border-red-200' 
            : 'bg-green-100 text-green-700 border border-green-200'
          }`}
        >
          {prediction}
        </span>
      </div>

      {/* Confidence Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs font-semibold">
          <span className="text-gray-500">Model Confidence</span>
          <span className={isTampered ? 'text-red-600' : 'text-green-600'}>{percentage}%</span>
        </div>
        <div className="w-full bg-gray-100 h-2.5 rounded-full overflow-hidden">
          <div 
            className={`h-full rounded-full transition-all duration-500
              ${isTampered ? 'bg-red-500' : 'bg-green-500'}`}
            style={{ width: `${percentage}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}