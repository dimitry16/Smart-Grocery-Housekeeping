// Name: Paula Tica
// Date: 4/19/2026, updated 4/29/2026, 5/20/2026
// Citation:
// Adapted code from shadcn docs and tailwindcss
// Adapted code from Mastering Tailwind CSS: Overcome Styling Conflicts with Tailwind Merge and clsx
// grocery.png is from Flaticon
// URL: https://ui.shadcn.com/docs/components/radix/typography
// URL: https://ui.shadcn.com/colors
// URL: https://ui.shadcn.com/blocks
// URL: https://www.flaticon.com/free-icon/grocery_1261052?term=groceries&page=1&position=2&origin=tag&related_id=1261052
// URL: https://tailwindcss.com/docs/responsive-design
// URL: https://dev.to/sheraz4194/mastering-tailwind-css-overcome-styling-conflicts-with-tailwind-merge-and-clsx-1dol 

import { NavLink } from 'react-router-dom'
import logo from '@/assets/grocery.png'
import { useState } from 'react'
import clsx from 'clsx'


const navItems = [
    { label: 'Dashboard', path: '/' },
    { label: 'Add Item', path: '/additem' },
    { label: 'Scan', path: '/item_detection' },
    { label: 'Barcode', path: '/barcode_scanner' },
    { label: 'Current Items', path: '/current_items' },
    { label: 'Recipes', path: '/recipes' },
    { label: 'Reports', path: '/reports' },
    { label: 'Log In', path: '/login' },
]

function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const handleNavClick = () => setIsOpen(false);

    return (
        <>
            {/* Backdrop when navigation bar is open in mobile */}
            {isOpen && (
                <div 
                className="fixed inset-0 bg-black/50 z-[100] md:hidden" 
                onClick={() => setIsOpen(false)}
                />
            )}

            {/* Hamburger button - visible when closed */}
            {!isOpen && (
                <button
                className="fixed top-4 left-4 z-[300] bg-stone-100 p-2 rounded-md md:hidden text-xl"
                onClick={() => setIsOpen(true)}
                >
                    ☰        
                </button>
            )}

            {/* Toggling based on state */}
            <nav className={clsx(
                'fixed top-0 left-0 h-screen w-48 bg-stone-100 border-r flex flex-col p-4 gap-1 transition-transform duration-300 z-[200] md:translate-x-0',
                isOpen ? 'translate-x-0' : '-translate-x-full'
            )}>

                <button onClick={() => setIsOpen(false)} className="self-end mb-2 md:hidden">✕</button>
                    <img src={logo} alt="logo" className="w-24 mb-8 ml-8" />
                    {navItems.map((item) => (
                        // Highlight current page name
                        <NavLink
                            key={item.path}
                            to={item.path}
                            onClick={handleNavClick}
                            className={({isActive}) => 
                                `px-4 py-2 rounded-lg text-base md:text-sm font-medium transition-colors ${
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
        </>
    )
}
export default Navbar