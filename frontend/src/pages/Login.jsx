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
    // Track input of each password field
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    // Check if both password fields have been entered and don't match
    const passwordMismatch = confirmPassword.length > 0 && password !== confirmPassword

    // If passwords don't match, show alert
    const handleSubmit = (event) => {
        event.preventDefault()
        if (password !== confirmPassword) {
            alert("Passwords do not match")
            return
        }
    }

    return (
        <form onSubmit={handleSubmit}>
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
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                    />
                </div>
                <div className="grid gap-2">
                    <Label className="text-gray-700" htmlFor="confirm-password">Confirm Password</Label>
                    <Input
                    id="confirm-password"
                    type="password"
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                    required
                    />
                    {/* Show error message as soon as there is a mismatch */}
                    {passwordMismatch && (
                        <p className="text-xs text-red-500">Passwords do not match</p>
                    )}
                </div>
                <Button type="submit" disabled={passwordMismatch}>Create Account</Button>
            </div>
        </form>
    )
}

function Login() {
    // Controls whether the sign up dialog is open or closed
    const [signUp, setSignUp] = useState(false)

    return (
        <div className="flex min-h-screen items-center justify-center">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle>Login to your account</CardTitle>
                    <CardAction>
                        {/* Opens sign up dialog when clicked */}
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
            {/* Sign up dialog */}
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