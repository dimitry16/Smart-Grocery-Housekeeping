// Name: Paula Tica
// Date: 05/08/2026
// This page provides data on the following:
// items frequently used
// items frequently left unused
// items frequently spoiled
// Citation:
// URL: https://lucide.dev/icons/categories

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Utensils } from "lucide-react"


// Placeholder data for frequently used food items
const usedItems = [
    {name: "Whole milk"},
    {name: "Chicken breast"},
    {name: "Eggs (dozen)"},
]

// Displays a list of the items within each report
function ItemList({items}) {
    return (
    <div className="flex flex-col gap-2">
        {items.map((item) => (
            <div key={item.name} className="flex justify-between items-center">
                <div className="flex justify-between items-baseline">
                    <span className="text-sm text-foreground">{item.name}</span>
                    {/* Display the raw count and unit */}
                    <span className="text-xs text-muted-foreground ml-2 whitespace-nowrap">
                        {item.count} {item.unit}
                    </span>
                </div>
            </div>
        ))}
    </div>
    )
}

// The three report cards
const reports = [
    {
        title: "Frequently Used",
        description: "Restocked most often in the last 60 days",
        icon: <Utensils className="w-4 h-4" style={{ color: "#3B6D11" }} />,
        iconBg: "#EAF3DE",
        items: usedItems,
    },
]

function Reports() {
    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
            <h1 className="text-center text-4xl font-semibold text-gray-900">Reports</h1>

            {/* Responsive grid: 1 column on mobile, 2 on tablet, 3 on desktop */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {reports.map((report) => (
                    <Card key={report.title} className="mx-auto w-full">
                        <CardHeader>
                            {/* Icon and badge at the top of the card */}
                        <div className="flex items-center justify-between">
                            <div
                                className="w-8 h-8 rounded-md flex items-center justify-center"
                                style={{ backgroundColor: report.iconBg }}
                            >
                                {report.icon}
                            </div>
                        </div>
                        <CardTitle>{report.title}</CardTitle>
                        <p className="text-xs text-green-600">{report.description}</p>
                        </CardHeader>
                        <CardContent>
                            <ItemList items={report.items}/>
                        </CardContent>
                        <CardFooter className="bg-olive-200">
                            <Button className="w-full">View Details</Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>
        </div>
    )
}

export default Reports