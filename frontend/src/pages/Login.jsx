// Name: Paula Tica
// Date: 05/12/2026
// This is the login and registration page
// Citation:
// Adapted code from shadcn
// URL: https://ui.shadcn.com/docs/components/radix/card

import { Button } from "@/components/ui/button"
import { Card, CardAction, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

function Login() {
    return (
        <div className="flex min-h-screen items-center justify-center">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle>Login to your account</CardTitle>
                    <CardAction>
                        <Button variant="link">Sign Up</Button>
                    </CardAction>
                </CardHeader>
                <CardContent>
                    <form>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-2">
                                <Label className="text-gray-700" htmlFor="email">Email</Label>
                                <Input
                                id="email"
                                type="email"
                                placeholder="example@email.com"
                                className="placeholder:text-gray-400"
                                required
                                />
                            </div>
                            <div className="grid gap-2">
                                <div className="flex items-center">
                                    <Label className="text-gray-700" htmlFor="password">Password</Label>
                                    <a
                                        href="#"
                                        className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                                    >
                                    </a>
                                </div>
                                <Input id="password" type="password" required />
                            </div>
                        </div>
                    </form>
                </CardContent>
                <CardFooter className="flex-col gap-2 bg-blue-300">
                    <Button type="submit" className="w-full">
                        Log In
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}

export default Login