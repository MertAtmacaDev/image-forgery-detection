import { useLocation, Link } from 'react-router-dom';
import AlgorithmCard from '../components/AlgorithmCard';
import AiResultCard from '../components/AiResultCard';

export default function ResultsPage() {
  const location = useLocation();

  let classicalData = location.state?.classicalData;
  let aiData = location.state?.aiData;
  let previewUrl = location.state?.previewUrl;

  if (!classicalData || !aiData) {
    const savedAnalysis = JSON.parse(localStorage.getItem('latest_analysis') || '{}');
    classicalData = savedAnalysis.classicalData;
    aiData = savedAnalysis.aiData;
    previewUrl = savedAnalysis.previewUrl;
  }

  if (!classicalData || !aiData) {
    return (
      <div className="text-center py-12 space-y-4">
        <div className="text-5xl">🔍</div>
        <h3 className="text-lg font-bold text-gray-700">No active analysis data discovered</h3>
        <p className="text-gray-400 text-sm max-w-sm mx-auto">Please upload an image first from the dashboard to populate live framework reports.</p>
        <Link to="/" className="inline-block bg-blue-600 text-white font-medium text-sm px-5 py-2.5 rounded-xl shadow-xs hover:bg-blue-700 transition-colors">
          Go to Analyzer
        </Link>
      </div>
    );
  }

  const classicalKeys = Object.keys(classicalData);
  const totalClassicalDetected = classicalKeys.filter(key => classicalData[key].is_forged).length;

  const resnetVote = aiData.resnet18_prediction?.prediction === "tampered" ? 1 : 0;
  const cnnLstmVote = aiData.cnn_lstm_prediction?.prediction === "tampered" ? 1 : 0;
  
  const totalSystemVotes = totalClassicalDetected + resnetVote + cnnLstmVote;
  const finalSystemVerdict = totalSystemVotes >= 3 ? "SUSPICIOUS" : "CLEAN";

  return (
    <div className="space-y-8 py-4">
      {/* TOP SECTION: Preview and Summary Overview */}
      <div className="bg-white rounded-2xl shadow-md border border-gray-100 p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left: Input Image Imagebox */}
        <div className="md:col-span-1 bg-gray-50 rounded-xl p-3 flex items-center justify-center border border-gray-100">
          <img 
            src={previewUrl} 
            alt="Analyzed target" 
            className="max-h-56 rounded-lg object-contain shadow-xs"
          />
        </div>

        {/* Right: Automated Overview Verdict */}
        <div className="md:col-span-2 flex flex-col justify-between py-1">
          <div className="space-y-3">
            <h3 className="text-2xl font-extrabold text-gray-900 tracking-tight">Executive Report Overview</h3>
            <p className="text-gray-500 text-sm leading-relaxed">
              The verification pipeline has successfully finished evaluating cross-matching validation and structural artifact compressions. Below are the isolated details from both pipelines.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
            <div className="border border-gray-100 bg-gray-50/50 p-4 rounded-xl">
              <span className="text-xs font-semibold text-gray-400 tracking-wider block uppercase">Metadata Pipeline</span>
              <p className="text-lg font-black text-gray-700 mt-1">
                {totalClassicalDetected} / {classicalKeys.length} <span className="text-xs font-medium text-gray-400">Algos Flags</span>
              </p>
            </div>
            
            {/* Oylama Sonucu Çıkan Adil Ortak Karar Rozeti */}
            <div className="border border-gray-100 bg-gray-50/50 p-4 rounded-xl">
              <span className="text-xs font-semibold text-gray-400 tracking-wider block uppercase">
                System Consensus Verdict (6 Algos)
              </span>
              <p className={`text-lg font-black mt-1 uppercase ${finalSystemVerdict === 'SUSPICIOUS' ? 'text-red-600' : 'text-green-600'}`}>
                {finalSystemVerdict}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* MID SECTION: Classical Algorithms Grid Output */}
      <div className="space-y-3">
        <h3 className="text-xl font-extrabold text-gray-800 tracking-tight">1. Classical Feature Matching Reports</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {classicalKeys.map((key) => {
            const algo = classicalData[key];
            return (
              <AlgorithmCard 
                key={key}
                name={key.toUpperCase()}
                keypointCount={algo.keypoint_count}
                matchCount={algo.match_count}
                isForged={algo.is_forged}
                resultImage={algo.result_image_base64}
              />
            );
          })}
        </div>
      </div>

      {/* LOWER SECTION: Deep Learning Models Section */}
      <div className="space-y-3">
        <h3 className="text-xl font-extrabold text-gray-800 tracking-tight">2. Deep Learning Neural Evaluations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AiResultCard 
            model={aiData.resnet18_prediction?.model || "ResNet18 Transfer"}
            prediction={aiData.resnet18_prediction?.prediction || "N/A"}
            confidence={aiData.resnet18_prediction?.confidence || 0}
          />
          <AiResultCard 
            model={aiData.cnn_lstm_prediction?.model || "CNN-LSTM Hybrid"}
            prediction={aiData.cnn_lstm_prediction?.prediction || "N/A"}
            confidence={aiData.cnn_lstm_prediction?.confidence || 0}
          />
        </div>
      </div>
    </div>
  );
}