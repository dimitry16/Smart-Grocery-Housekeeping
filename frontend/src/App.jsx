// Name: Paula Tica
// Date: 4/19/2026, updated 4/29/2026, updated 5/12/2026
// Edited: Zilin Xu on 4/22/2026
// Citation:
// Code adapted from React Router
// URL: https://reactrouter.com/start/framework/routing

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Navbar from '@/components/ui/navbar'
import AddItem from './pages/AddItem';
import CurrentItems from './pages/CurrentItems';
import Recipes from './pages/Recipes';
import SavedRecipes from './pages/SavedRecipes';
import Reports from './pages/Reports';
import Login from './pages/Login';
import BarcodeScanner from './pages/BarcodeScanner';
import ObjectScanner from './pages/ObjectScanner';
import { AuthGate } from './components/auth/AuthGate';

function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Navbar />
        <main className="flex-1 md:ml-48">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route element={<AuthGate />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/additem" element={<AddItem />} />
              <Route path="/scan-barcode" element={<BarcodeScanner />} />
              <Route path="/scan-object" element={<ObjectScanner />} />
              <Route path="/current_items" element={<CurrentItems />} />
              <Route path="/recipes" element={<Recipes/>} />
              <Route path="/savedrecipes" element={<SavedRecipes/>} />
              <Route path="/reports" element={<Reports/>} />
            </Route>
            <Route path="/login" element={<Login/>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App;
