// Name: Paula Tica
// Date: 05/12/2026
// This is the login and registration page
// Citation:
// Adapted code from shadcn
// URL: https://ui.shadcn.com/docs/components/radix/card
// URL: https://ui.shadcn.com/docs/components/radix/dialog

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardAction, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

function SignUpForm() {
    return (
        <form>
            <div className="flex flex-col gap-4">
                <div className="grid gap-2">
                    <Label className="text-gray-700" htmlFor="signup-name">Name</Label>
                    <Input 
                    id="signup-name" 
                    type="text"
                    required
                    />
                </div>
                <div className="grid gap-2">
                    <Label className="text-gray-700" htmlFor="signup-email">Email</Label>
                    <Input
                    id="signup-email"
                    type="email"
                    placeholder="example@email.com"
                    className="placeholder:text-gray-400"
                    required
                    />
                </div>
                <div className="grid gap-2">
                    <Label className="text-gray-700" htmlFor="signup-password">Password</Label>
                    <Input
                    id="signup-password"
                    type="password"
                    required
                    />
                </div>
                <Button type="submit">Create Account</Button>
            </div>
        </form>
    )
}

function Login() {
    const [signUp, setSignUp] = useState(false)

    return (
        <div className="flex min-h-screen items-center justify-center">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle>Login to your account</CardTitle>
                    <CardAction>
                        <Button variant="outline" className="rounded-full" onClick={() => setSignUp(true)}>
                            Sign Up
                        </Button>
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
                                <Label className="text-gray-700" htmlFor="password">Password</Label>
                                <Input 
                                id="password" 
                                type="password" 
                                required 
                                />
                            </div>
                        </div>
                    </form>
                </CardContent>
                <CardFooter className="flex-col gap-2 bg-blue-300">
                    <Button type="submit" className="w-full">Log In</Button>
                </CardFooter>
            </Card>
            <Dialog open={signUp} onOpenChange={setSignUp}>
                <DialogContent className="max-w-sm bg-white">
                    <DialogHeader>
                        <DialogTitle>Create an account</DialogTitle>
                    </DialogHeader>
                    <SignUpForm/>
                </DialogContent>
            </Dialog>
        </div>
    )
}

export default Login