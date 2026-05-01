// Name: Paula Tica
// Date: 4/19/2026
// Edited: Zilin Xu on 4/22/2026
// Edited: Paula Tica on 4/29/2026
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
import { Badge } from "@/components/ui/badge"
import { Card, CardAction, CardHeader, CardTitle } from "@/components/ui/card"

const BASE_URL = `${import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"}/v1/food-items`;

const today = new Date();
const in3Days = new Date();
in3Days.setDate(today.getDate() + 3);

// Mock recipes used as placeholders
// images to be added once Spoonacular API is implemented 
const mockRecipes = [
    { id: 1, title: "Salmon Alfredo", image: null, category: "Dinner" },
    { id: 2, title: "Blueberry Waffles", image: null, category: "Breakfast" },
    { id: 3, title: "Caesar Salad", image: null, category: "Lunch" },
    { id: 4, title: "Cajun Chicken and Rice", image: null, category: "Dinner" },
    { id: 5, title: "Veggie Scramble", image: null, category: "Breakfast" },
    { id: 6, title: "Grilled Cheese Sandwich", image: null, category: "Lunch" },
]

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
            <div className="p-4 border-b bg-emerald-100 flex items-center justify-between">
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
            <div className="p-4 border-b bg-olive-200 flex items-center justify-between">
                <h2 className="text-2xl font-semibold text-gray-900">Recipes</h2>
                <Link to="/recipes">
                    <Button variant="outline" size="sm">View All</Button>
                </Link>
            </div>    
            <div className="p-4 grid grid-cols-1 sm:grid-cols-3 gap-4"> 
                {/* Display only the first three recipes */}
                {mockRecipes.slice(0, 3).map((recipe) => (
                    <Card key={recipe.id} className="relative mx-auto w-full pt-0">
                        <div className="absolute inset-0 z-30 aspect-video bg-black/10" />
                        <img
                            src={recipe.image}
                            alt={recipe.title}
                            className="relative z-20 aspect-video w-full object-cover brightness-60 grayscale dark:brightness-40"
                        />
                        <CardHeader>
                            <CardAction>
                                <Badge variant="secondary">{recipe.category}</Badge>
                            </CardAction>
                            <CardTitle className="text-sm">{recipe.title}</CardTitle>
                        </CardHeader>
                    </Card>
                ))}
            </div>
        </div>

    </div>
    );
}

export default Dashboard;
