import { Routes, Route, Link } from 'react-router-dom'
import { BrowserRouter } from 'react-router-dom'
import HomePage from './pages/HomePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="*" element={
          <div className="min-h-screen bg-gray-50 flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Page Not Found</h1>
              <p className="text-gray-600 mb-8">This feature is coming soon!</p>
              <Link to="/" className="bg-teal-600 text-white px-6 py-3 rounded-md hover:bg-teal-700">
                Go Home
              </Link>
            </div>
          </div>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
