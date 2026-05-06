// Name: Paula Tica
// Date: 4/19/2026
// Last Edited: Zilin Xu on 5/6/2026
// Citation:
// Code adapted from React Router
// URL: https://reactrouter.com/start/framework/routing

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Navbar from '@/components/ui/navbar'
import AddItem from './pages/AddItem';
import CurrentItems from './pages/CurrentItems';
import BarcodeScanner from './pages/BarcodeScanner';

function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/additem" element={<AddItem />} />
            <Route path="/scan" element={<BarcodeScanner />} />
            <Route path="/barcode" element={<BarcodeScanner />} />
            <Route path="/current_items" element={<CurrentItems />} />
            <Route path="/recipes" element={<div className="p-6"></div>} />
            <Route path="/profile" element={<div className="p-6"></div>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App;