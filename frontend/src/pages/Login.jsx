// Name: Paula Tica
// Date: 05/12/2026
// This is the login and registration page
// Citation:
// Adapted code from shadcn
// URL: https://ui.shadcn.com/docs/components/radix/card
// URL: https://ui.shadcn.com/docs/components/radix/dialog

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import SignUpForm from "@/components/ui/SignUpForm"

function Login() {
    // Controls whether the sign up dialog is open or closed
    const [signUp, setSignUp] = useState(false)

    return (
        <div className="p-6 flex min-h-screen items-center justify-center">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle className="text-base text-xl">Login to your account</CardTitle>
                </CardHeader>
                <CardContent>
                    <form id="login-form">
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-2">
                                <Label className="text-gray-700" htmlFor="email">
                                    Email<span className="text-red-500">*</span>
                                </Label>
                                <Input
                                id="email"
                                type="email"
                                placeholder="example@email.com"
                                className="placeholder:text-gray-400"
                                required
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label className="text-gray-700" htmlFor="password">
                                    Password<span className="text-red-500">*</span>
                                </Label>
                                <Input 
                                id="password" 
                                type="password" 
                                required 
                                />
                            </div>
                        </div>
                    </form>
                </CardContent>
                <CardFooter className="flex-col gap-2 bg-blue-100">
                    <p className="text-base md:text-sm">
                        Don't have an account?{' '}
                        <span
                            onClick={() => setSignUp(true)}
                            className="text-base md:text-sm font-bold cursor-pointer text-blue-900 hover:text-blue-800"
                        >
                        Sign Up
                        </span>
                    </p>
                    <Button type="submit" form="login-form" className="w-full text-lg text-medium font-bold">Log In</Button>
                </CardFooter>
            </Card>
            {/* Sign up dialog */}
            <Dialog open={signUp} onOpenChange={setSignUp}>
                <DialogContent className="max-w-sm bg-white">
                    <DialogHeader>
                        <DialogTitle className="text-base text-xl">Create an account</DialogTitle>
                        <DialogDescription className="text-base md:text-sm">Please enter your information below.</DialogDescription>
                    </DialogHeader>
                    <SignUpForm/>
                </DialogContent>
            </Dialog>
        </div>
    )
}

export default Login