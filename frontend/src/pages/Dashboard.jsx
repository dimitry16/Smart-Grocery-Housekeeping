// Name: Paula Tica
// Date: 4/19/2026
// Citation:
// Adapted code from shadcn docs
// Adapted code from Create Future And Past Dates From Today
// URL: https://ui.shadcn.com/docs/components/radix/typography
// URL: https://ui.shadcn.com/colors
// URL: https://ui.shadcn.com/blocks
// URL: https://github.com/jbranchaud/til/blob/master/javascript/create-future-and-past-dates-from-today.md


import { Button } from "@/components/ui/button"

const mockPantryItems = [
    { id: 1, name: "Milk", brand: "Organic Valley", category: "Dairy", quantity: 1, unit: "gallon", expiration_date: "04-25-2026" },
    { id: 2, name: "Bread", brand: "Dave's Killer Bread", category: "Bakery", quantity: 1, unit: "loaf", expiration_date: "04-22-2026" },
    { id: 3, name: "Apples", brand: null, category: "Produce", quantity: 3, unit: "count", expiration_date: "04-24-2026" },
    { id: 4, name: "Broccoli", brand: null, category: "Produce", quantity: 2, unit: "crowns", expiration_date: "04-24-2026" },
    { id: 5, name: "Bananas", brand: null, category: "Produce", quantity: 1, unit: "bunch", expiration_date: "04-23-2026" },
];

const today = new Date();
const in3Days = new Date();
in3Days.setDate(today.getDate() + 3);

// Items where expiration date is on or less than 3 days from now
const expiringSoon = mockPantryItems.filter(item => {
    const exp = new Date(item.expiration_date);
    return exp <= in3Days;
});

// Items where expiration date is more than 3 days from now
const currentItems = mockPantryItems.filter(item => {
    const exp = new Date(item.expiration_date);
    return exp > in3Days;
});

function PantryTable({ items }) {
    return (
        <table className="w-full text-sm">
        <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Brand</th>
            <th className="px-4 py-3 text-left">Category</th>
            <th className="px-4 py-3 text-left">Quantity</th>
            <th className="px-4 py-3 text-left">Expiration Date</th>
            </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
            {items.length === 0 ? (
            <tr>
                <td colSpan={5} className="px-4 py-3 text-center text-gray-400">No items</td>
            </tr>
            ) : (
            items.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{item.name}</td>
                <td className="px-4 py-3 text-gray-500">{item.brand ?? "—"}</td>
                <td className="px-4 py-3">{item.category}</td>
                <td className="px-4 py-3">{item.quantity} {item.unit}</td>
                <td className="px-4 py-3">{item.expiration_date}</td>
                </tr>
            ))
            )}
        </tbody>
        </table>
    );
}

function Dashboard() {
    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
        <h1 className="text-center text-4xl font-semibold text-gray-900">Smart Grocery Housekeeping</h1>

        {/* Expiring Soon Table */}
        <div className="rounded-lg border border-red-400 bg-white">
            <div className="p-4 border-b border-red-400 bg-red-200 flex items-center justify-between">
            <div>
                <h2 className="text-2xl font-semibold text-gray-900">Expiring Soon</h2>
                <p className="text-sm text-red-500">Expiring within 3 days</p>
            </div>
            <Button variant="outline" size="sm">View All</Button>
            </div>
            <PantryTable items={expiringSoon} />
        </div>

        {/* Current Items Table */}
        <div className="rounded-lg border bg-white">
            <div className="p-4 border-b bg-emerald-200 flex items-center justify-between">
            <h2 className="text-2xl font-semibold text-gray-900">Current Items</h2>
            <div className="flex gap-2">
                <Button variant="outline" size="sm">Add Item</Button>
                <Button variant="outline" size="sm">View All</Button>
            </div>
            </div>
            <PantryTable items={currentItems} />
        </div>

        {/* Recipes Table */}
        <div className="rounded-lg border bg-white">
            <div className="p-4 border-b bg-mist-200 flex items-center justify-between">
            <h2 className="text-2xl font-semibold text-gray-900">Recipes</h2>
            <Button variant="outline" size="sm">View All</Button>
            </div>
            <p className="p-4 text-sm text-gray-400">Recipes coming soon.</p>
        </div>

        </div>
    );
}

export default Dashboard;