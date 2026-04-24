// Name: Paula Tica
// Date: 4/19/2026
// Edited: Zilin Xu on 4/22/2026
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

const today = new Date();
const in3Days = new Date();
in3Days.setDate(today.getDate() + 3);

function PantryTable({ items }) {
    return (
        <table className="w-full text-sm">
        <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Brand</th>
            <th className="px-4 py-3 text-left">Category</th>
            <th className="px-4 py-3 text-left">Barcode</th>
            </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
            {items.length === 0 ? (
            <tr>
                <td colSpan={4} className="px-4 py-3 text-center text-gray-400">No items</td>
            </tr>
            ) : (
            items.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{item.name}</td>
                <td className="px-4 py-3 text-gray-500">{item.brand ?? "—"}</td>
                <td className="px-4 py-3">{item.category ?? "—"}</td>
                <td className="px-4 py-3">{item.barcode ?? "—"}</td>
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
                if (!response.ok) {
                    throw new Error(`Error ${response.status}: ${response.statusText}`);
                }
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

    if (loading) {
        return (
            <div className="p-6 max-w-5xl mx-auto text-center text-gray-500">
                Loading food items...
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-6 max-w-5xl mx-auto text-center text-red-500">
                Failed to load food items: {error}
            </div>
        );
    }

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
        <h1 className="text-center text-4xl font-semibold text-gray-900">Smart Grocery Housekeeping</h1>

        {/* Food Items Table */}
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
            <PantryTable items={foodItems} />
        </div>

        {/* Recipes Section */}
        <div className="rounded-lg border bg-white">
            <div className="p-4 border-b bg-mist-200 flex items-center justify-between">
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
