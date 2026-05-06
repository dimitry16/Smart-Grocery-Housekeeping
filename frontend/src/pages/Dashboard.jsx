// Name: Paula Tica
// Date: 4/19/2026
// Last Edited: Zilin Xu on 5/5/2026
// Citation:
// Adapted code from shadcn docs
// Adapted code from Create Future And Past Dates From Today
// URL: https://ui.shadcn.com/docs/components/radix/typography
// URL: https://ui.shadcn.com/colors
// URL: https://ui.shadcn.com/blocks
// URL: https://github.com/jbranchaud/til/blob/master/javascript/create-future-and-past-dates-from-today.md

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const BASE_URL = `${import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"}/v1/food-items`;

// Returns days until expiration (negative = already expired)
function daysUntilExpiry(dateStr) {
    if (!dateStr) return null;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const exp = new Date(dateStr);
    exp.setHours(0, 0, 0, 0);
    return Math.round((exp - today) / (1000 * 60 * 60 * 24));
}

function ExpiryBadge({ dateStr }) {
    const days = daysUntilExpiry(dateStr);
    if (days === null) return <span className="text-gray-400 text-xs">No date</span>;

    if (days < 0) {
        return <span className="inline-block rounded-full bg-red-100 text-red-700 text-xs font-medium px-2 py-0.5">Expired</span>;
    }
    if (days === 0) {
        return <span className="inline-block rounded-full bg-red-100 text-red-700 text-xs font-medium px-2 py-0.5">Expires today</span>;
    }
    if (days <= 3) {
        return <span className="inline-block rounded-full bg-yellow-100 text-yellow-700 text-xs font-medium px-2 py-0.5">Expires in {days}d</span>;
    }
    return <span className="inline-block rounded-full bg-green-100 text-green-700 text-xs font-medium px-2 py-0.5">Expires in {days}d</span>;
}

function rowColor(dateStr) {
    const days = daysUntilExpiry(dateStr);
    if (days === null) return "";
    if (days < 0) return "bg-red-50";
    if (days <= 3) return "bg-yellow-50";
    return "";
}

function PantryTable({ items }) {
    return (
        <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
                <tr>
                    <th className="px-4 py-3 text-left">Name</th>
                    <th className="px-4 py-3 text-left">Brand</th>
                    <th className="px-4 py-3 text-left">Category</th>
                    <th className="px-4 py-3 text-left">Barcode</th>
                    <th className="px-4 py-3 text-left">Expiration</th>
                </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
                {items.length === 0 ? (
                    <tr>
                        <td colSpan={5} className="px-4 py-3 text-center text-gray-400">No items</td>
                    </tr>
                ) : (
                    items.map((item) => (
                        <tr key={item.id} className={`hover:brightness-95 ${rowColor(item.expiration_date)}`}>
                            <td className="px-4 py-3 font-medium">{item.name}</td>
                            <td className="px-4 py-3 text-gray-500">{item.brand ?? "—"}</td>
                            <td className="px-4 py-3">{item.category ?? "—"}</td>
                            <td className="px-4 py-3">{item.barcode ?? "—"}</td>
                            <td className="px-4 py-3">
                                <ExpiryBadge dateStr={item.expiration_date} />
                            </td>
                        </tr>
                    ))
                )}
            </tbody>
        </table>
    );
}

function Dashboard() {
    const [foodItems, setFoodItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchFoodItems() {
            try {
                const response = await fetch(BASE_URL);
                if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
                const data = await response.json();
                setFoodItems(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchFoodItems();
    }, []);

    if (loading) return <div className="p-6 max-w-5xl mx-auto text-center text-gray-500">Loading food items...</div>;
    if (error) return <div className="p-6 max-w-5xl mx-auto text-center text-red-500">Failed to load items: {error}</div>;

    const expiringSoon = foodItems.filter(item => {
        const days = daysUntilExpiry(item.expiration_date);
        return days !== null && days <= 3;
    });

    const currentItems = foodItems.filter(item => {
        const days = daysUntilExpiry(item.expiration_date);
        return days === null || days > 3;
    });

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
            <h1 className="text-center text-4xl font-semibold text-gray-900">Smart Grocery Housekeeping</h1>

            {/* Expiring Soon Table */}
            <div className="rounded-lg border border-red-400 bg-white">
                <div className="p-4 border-b border-red-400 bg-red-200 flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-900">Expiring Soon</h2>
                        <p className="text-sm text-red-500">Expiring within 3 days or already expired</p>
                    </div>
                    <Link to="/current_items">
                        <Button variant="outline" size="sm">View All</Button>
                    </Link>
                </div>
                <PantryTable items={expiringSoon} />
            </div>

            {/* Current Items Table */}
            <div className="rounded-lg border bg-white">
                <div className="p-4 border-b bg-emerald-200 flex items-center justify-between">
                    <h2 className="text-2xl font-semibold text-gray-900">Current Items</h2>
                    <div className="flex gap-2">
                        <Link to="/additem">
                            <Button variant="outline" size="sm">Add Item</Button>
                        </Link>
                        <Link to="/current_items">
                            <Button variant="outline" size="sm">View All</Button>
                        </Link>
                    </div>
                </div>
                <PantryTable items={currentItems} />
            </div>

            {/* Recipes */}
            <div className="rounded-lg border bg-white">
                <div className="p-4 border-b flex items-center justify-between">
                    <h2 className="text-2xl font-semibold text-gray-900">Recipes</h2>
                    <Link to="/recipes">
                        <Button variant="outline" size="sm">View All</Button>
                    </Link>
                </div>
                <p className="p-4 text-sm text-gray-400">Recipes coming soon.</p>
            </div>
        </div>
    );
}

export default Dashboard;
