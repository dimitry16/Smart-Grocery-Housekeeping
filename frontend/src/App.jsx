// Name: Paula Tica
// Date: 4/19/2026
// Citation:
// Code adapted from React Router
// URL: https://reactrouter.com/start/framework/routing

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Navbar from '@/components/ui/navbar'

function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/additem" element={<div className="p-6"></div>} />
            <Route path="/scan" element={<div className="p-6"></div>} />
            <Route path="/barcode" element={<div className="p-6"></div>} />
            <Route path="/currentitems" element={<div className="p-6"></div>} />
            <Route path="/recipes" element={<div className="p-6"></div>} />
            <Route path="/profile" element={<div className="p-6"></div>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App;