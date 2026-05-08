// Name: Paula Tica
// Date: 4/19/2026, updated 4/29/2026
// Citation:
// Adapted code from shadcn docs
// grocery.png is from Flaticon
// URL: https://ui.shadcn.com/docs/components/radix/typography
// URL: https://ui.shadcn.com/colors
// URL: https://ui.shadcn.com/blocks
// URL: https://www.flaticon.com/free-icon/grocery_1261052?term=groceries&page=1&position=2&origin=tag&related_id=1261052

import { NavLink } from 'react-router-dom'
import logo from '@/assets/grocery.png'

const navItems = [
    { label: 'Dashboard', path: '/' },
    { label: 'Add Item', path: '/additem' },
    { label: 'Scan', path: '/item_detection' },
    { label: 'Barcode', path: '/barcode_scanner' },
    { label: 'Current Items', path: '/current_items' },
    { label: 'Recipes', path: '/recipes' },
    { label: 'Reports', path: '/reports' },
    { label: 'Profile', path: '/profile' },
]

function Navbar() {

    return (
        <nav className="h-screen w-48 bg-stone-100 border-r flex flex-col p-4 gap-1">
            <img src={logo} alt="logo" className="w-24 mb-8 ml-8" />
            {navItems.map((item) => (
                // Highlight current page name
                <NavLink
                    key={item.path}
                    to={item.path}
                    className={({isActive}) => 
                        `px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                            isActive
                                ? 'bg-white text-gray-900 shadow-sm'
                                : 'text-gray-600 hover:bg-white hover:text-gray-900'
                        }`
                    }
                >
                    {item.label}
                </NavLink>
            ))}
            <div className="mt-auto pt-4 border-t text-xs text-muted-foreground">
                <a href="https://www.flaticon.com/free-icon/grocery_1261052?term=groceries&page=1&position=2&origin=tag&related_id=1261052" target="_blank" rel="noopener noreferrer" className="hover:text-gray-600">
                    Groceries icon created by monkik - Flaticon
                </a>
            </div>
        </nav>
    )
}
export default Navbar