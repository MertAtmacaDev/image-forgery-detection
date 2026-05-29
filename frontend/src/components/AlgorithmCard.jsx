export default function AlgorithmCard({ name, keypointCount, matchCount, isForged, resultImage }) {
  return (
    <div className="bg-white rounded-xl shadow-xs border border-gray-100 overflow-hidden flex flex-col">
      {/* Visual Result Output */}
      <div className="bg-gray-900 h-48 flex items-center justify-center relative border-b border-gray-100">
        {resultImage ? (
          <img 
            src={resultImage} 
            alt={`${name} match layout`} 
            className="w-full h-full object-contain"
          />
        ) : (
          <div className="text-gray-500 text-xs">No image visualization available</div>
        )}
        
        {/* Status Badge */}
        <span className={`absolute top-3 right-3 px-2.5 py-1 rounded-full text-xs font-bold tracking-wide shadow-sm
          ${isForged 
            ? 'bg-red-50 text-red-600 border border-red-200' 
            : 'bg-green-50 text-green-600 border border-green-200'
          }`}
        >
          {isForged ? '⚠️ Forgery Detected' : '✅ Match Clean'}
        </span>
      </div>

      {/* Card Metadata Details */}
      <div className="p-4 space-y-3 flex-grow flex flex-col justify-between">
        <div>
          <h4 className="text-base font-bold text-gray-800 tracking-tight">{name} Descriptor</h4>
          <p className="text-xs text-gray-400 mt-0.5">Keypoint analysis metrics</p>
        </div>

        <div className="grid grid-cols-2 gap-4 bg-gray-50 p-2.5 rounded-lg text-center">
          <div>
            <p className="text-xs text-gray-400 font-medium">Keypoints</p>
            <p className="text-sm font-bold text-gray-700 mt-0.5">{keypointCount}</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 font-medium">Valid Matches</p>
            <p className="text-sm font-bold text-gray-700 mt-0.5">{matchCount}</p>
          </div>
        </div>
      </div>
    </div>
  );
}