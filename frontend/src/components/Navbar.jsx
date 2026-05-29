import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Left Side: Brand Logo/Name */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-extrabold text-blue-600 tracking-tight">
              🛡️ Forgery<span className="text-gray-800">Detector</span>
            </Link>
          </div>

          {/* Right Side: Navigation Links */}
          <div className="flex space-x-8">
            <Link 
              to="/" 
              className="text-gray-600 hover:text-blue-600 font-medium transition-colors"
            >
              Analyze Image
            </Link>
            <Link 
              to="/results" 
              className="text-gray-600 hover:text-blue-600 font-medium transition-colors"
            >
              Latest Results
            </Link>
            <Link 
              to="/history" 
              className="text-gray-600 hover:text-blue-600 font-medium transition-colors"
            >
              History Log
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}