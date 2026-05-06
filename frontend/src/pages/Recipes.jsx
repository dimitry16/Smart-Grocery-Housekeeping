// Name: Paula Tica
// Date: 4/29/2026
// Citation:
// Adapted code from shadcn
// Adapted code from tailwindcss
// URL: https://ui.shadcn.com/docs/components/radix/card 
// URL: https://ui.shadcn.com/colors
// URL: https://tailwindcss.com/docs/grid-template-columns 

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardAction, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useState } from "react"

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

// Categories used for the filter feature
const CATEGORIES = ["All", "Breakfast", "Lunch", "Dinner"]

function Recipes() {
    // Track which filter button is currently active
    const [selectedCategory, setSelectedCategory] = useState("All")

    // Display all recipes or display only recipes whose category matches the selected category
    const filteredRecipes = selectedCategory === "All"
        ? mockRecipes
        : mockRecipes.filter(recipe => recipe.category === selectedCategory)

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
            <h1 className="text-center text-4xl font-semibold text-gray-900">Recipes</h1>

            {/* Category Filter Buttons */}
            {/* Change appearance of button depending on whether it's clicked/active */}
            <div className="flex gap-2 flex-wrap">
                {CATEGORIES.map(category => (
                    <Button
                        key={category}
                        variant={selectedCategory === category ? "default" : "outline"}
                        size="sm"
                        onClick={() => setSelectedCategory(category)}
                    >
                        {category}
                    </Button>
                ))}
            </div>
            {/* Responsive grid layout */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Only show filtered recipes */}
                {filteredRecipes.map((recipe) => (
                    // Display a card for each recipe
                    // Each card includes an image, header, content, and footer
                    <Card key={recipe.id} className="relative mx-auto w-full pt-0">
                        <div className="absolute inset-0 z-30 aspect-video bg-black/10" />
                        <img
                            src={recipe.image ?? "https://placehold.co/640x360"}
                            alt={recipe.title}
                            className="relative z-20 aspect-video w-full object-cover brightness-60 grayscale dark:brightness-40"
                        />
                        <CardHeader>
                            <CardAction>
                                <Badge variant="secondary">{recipe.category}</Badge>
                            </CardAction>
                            <CardTitle>{recipe.title}</CardTitle>
                        </CardHeader>
                        <CardFooter className="bg-olive-200">
                            <Button className="w-full">View Recipe</Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

        </div>
    )
}

export default Recipes