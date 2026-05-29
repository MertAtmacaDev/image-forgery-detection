import { useRef } from 'react';

export default function DropZone({ file, onFileSelect }) {
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleAreaClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  // Helper to format file size nicely
  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      {/* Hidden File Input */}
      <input 
        type="file" 
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        className="hidden"
      />

      {/* Drag & Drop Main Area */}
      <div 
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleAreaClick}
        className={`border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer transition-all bg-white shadow-xs
          ${file 
            ? 'border-blue-400 bg-blue-50/10' 
            : 'border-gray-300 hover:border-blue-500 hover:bg-gray-50/50'
          }`}
      >
        {!file ? (
          <div className="text-center space-y-3">
            <div className="text-4xl text-gray-400">📥</div>
            <p className="text-gray-700 font-semibold text-base">
              Drag and drop your image here, or <span className="text-blue-600 underline">browse</span>
            </p>
            <p className="text-gray-400 text-xs">
              Supports PNG, JPG, JPEG, TIFF (Max 10MB)
            </p>
          </div>
        ) : (
          <div className="w-full flex flex-col items-center space-y-4">
            {/* Live Preview Image */}
            <img 
              src={URL.createObjectURL(file)} 
              alt="Preview" 
              className="max-h-64 rounded-lg shadow-sm object-contain border border-gray-100"
            />
            <div className="text-center">
              <p className="text-gray-800 font-medium text-sm truncate max-w-md">
                {file.name}
              </p>
              <p className="text-gray-400 text-xs mt-0.5">
                {formatBytes(file.size)}
              </p>
            </div>
            <button 
              type="button"
              onClick={(e) => {
                e.stopPropagation(); // Prevents triggering input click
                onFileSelect(null);
              }}
              className="text-xs text-red-500 hover:text-red-700 font-medium bg-red-50 px-3 py-1.5 rounded-full transition-colors"
            >
              Remove Image
            </button>
          </div>
        )}
      </div>
    </div>
  );
}