export default function LoadingSpinner({ message = "Analyzing image..." }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="relative w-16 h-16">
        {/* Outer spinning ring */}
        <div className="absolute inset-0 border-4 border-blue-100 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-blue-600 rounded-full animate-spin border-t-transparent"></div>
      </div>
      <p className="text-gray-600 font-medium animate-pulse text-sm tracking-wide">
        {message}
      </p>
    </div>
  );
}