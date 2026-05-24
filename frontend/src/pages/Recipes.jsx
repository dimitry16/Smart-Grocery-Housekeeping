// Name: Paula Tica
// Date: 4/29/2026, updated 5/21/2026
// Citation:
// Adapted code from shadcn
// Adapted code from tailwindcss
// URL: https://ui.shadcn.com/docs/components/radix/card 
// URL: https://ui.shadcn.com/colors
// URL: https://tailwindcss.com/docs/grid-template-columns 

import { Button } from "@/components/ui/button"
import { Card, CardAction, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

// Mock recipes used as placeholders
// images to be added once Spoonacular API is implemented 
const mockRecipes = [
    {id: 1, title: "Salmon Alfredo", image: null},
    {id: 2, title: "Blueberry Waffles", image: null},
    {id: 3, title: "Caesar Salad", image: null},
    {id: 4, title: "Cajun Chicken and Rice", image: null},
    {id: 5, title: "Veggie Scramble", image: null},
    {id: 6, title: "Grilled Cheese Sandwich", image: null},
]

function Recipes() {

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
            <h1 className="text-center text-4xl font-semibold text-gray-900">Recipes</h1>
            {/* Responsive grid layout */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockRecipes.map((recipe) => (
                    // Display a card for each recipe
                    // Each card includes an image, header, title, and footer
                    <Card key={recipe.id} className="relative mx-auto w-full pt-0">
                        <div className="absolute inset-0 z-30 aspect-video bg-black/10" />
                        <img
                            src={recipe.image ?? "https://placehold.co/640x360"}
                            alt={recipe.title}
                            className="relative z-20 aspect-video w-full object-cover brightness-60 grayscale dark:brightness-40"
                        />
                        <CardHeader>
                            <CardTitle>{recipe.title}</CardTitle>
                        </CardHeader>
                        <CardFooter className="flex justify-between bg-neutral-200">
                            <Button type="submit" variant="outline" className="bg-white text-base md:text-sm">View Recipe</Button>
                            <Button type="submit" className="bg-emerald-500 hover:bg-emerald-500 text-white text-base md:text-sm">Save</Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

        </div>
    )
}

export default Recipes