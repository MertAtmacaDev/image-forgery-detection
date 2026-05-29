import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DropZone from '../components/DropZone';
import LoadingSpinner from '../components/LoadingSpinner';
import { uploadImage, analyzeClassical, analyzeAI } from '../services/api';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const navigate = useNavigate();

  const handleStartAnalysis = async () => {
    if (!file) return;

    setLoading(true);
    try {
      setLoadingMessage("Uploading image to secure server...");
      const uniqueFilename = await uploadImage(file);

      setLoadingMessage("Running Classical Computer Vision algorithms (SIFT, ORB...)...");
      const classicalData = await analyzeClassical(uniqueFilename);

      setLoadingMessage("Invoking Deep Learning models and Error Level Analysis (ELA)...");
      const aiData = await analyzeAI(uniqueFilename);

      const classicalFakeVotes = Object.keys(classicalData).filter(
        (key) => classicalData[key].is_forged
      ).length;

      const resnetFakeVote = aiData.resnet18_prediction?.prediction === "tampered" ? 1 : 0;
      const cnnLstmFakeVote = aiData.cnn_lstm_prediction?.prediction === "tampered" ? 1 : 0;

      const totalFakeVotes = classicalFakeVotes + resnetFakeVote + cnnLstmFakeVote;

      const overallVerdict = totalFakeVotes >= 3 ? "Suspicious" : "Clean";

      const newLog = {
        id: Date.now(),
        date: new Date().toLocaleString(),
        filename: file.name,
        overallResult: overallVerdict
      };
      const existingHistory = JSON.parse(localStorage.getItem('forgery_history') || '[]');
      localStorage.setItem('forgery_history', JSON.stringify([newLog, ...existingHistory]));

      const previewUrl = URL.createObjectURL(file);
      const latestAnalysisPayload = { classicalData, aiData, previewUrl };
      localStorage.setItem('latest_analysis', JSON.stringify(latestAnalysisPayload));

      navigate('/results', { state: latestAnalysisPayload });

    } catch (error) {
      console.error("Pipeline breakdown:", error);
      alert("Analysis failed! Please ensure backend servers are active and try again.");
    } finally {
      setLoading(false);
      setLoadingMessage('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">
          Advanced Image Forgery Detection
        </h2>
        <p className="text-gray-500 max-w-xl mx-auto text-sm">
          Analyze image authenticity using a combined framework of localized metadata compression (ELA) and keypoint structure matchings.
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
        {loading ? (
          <LoadingSpinner message={loadingMessage} />
        ) : (
          <div className="space-y-6">
            <DropZone file={file} onFileSelect={setFile} />
            
            {file && (
              <div className="flex justify-center pt-2">
                <button
                  type="button"
                  onClick={handleStartAnalysis}
                  className="w-full max-w-xs bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl shadow-sm transition-all transform active:scale-98 text-sm"
                >
                  🚀 Launch Full Analysis
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}