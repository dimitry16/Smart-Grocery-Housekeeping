// Name: Paula Tica
// Date: 05/23/2026

import { useState, useEffect } from "react";

let listeners = [];
let state = {
    user: JSON.parse(localStorage.getItem("user")),
    token: localStorage.getItem("token"),
};

function setState(newState) {
    state = { ...state, ...newState };
    listeners.forEach((l) => l(state));
}

export function useAuth() {
    const [, rerender] = useState(0);

    useEffect(() => {
        const listener = () => rerender((n) => n + 1);
        listeners.push(listener);
        return () => { listeners = listeners.filter((l) => l !== listener); };
    }, []);

    const login = async (credentials) => {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials),
        });
        const { accessToken, user } = await res.json();
        localStorage.setItem("token", accessToken);
        localStorage.setItem("user", JSON.stringify(user));
        setState({ token: accessToken, user });
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setState({ token: null, user: null });
    };

    const isAuthenticated = () => !!state.token;

    const deleteMeForceLogin = () => {
        const accessToken = "abcd";
        const user = "john";
        localStorage.setItem("token", accessToken);
        localStorage.setItem("user", JSON.stringify(user));
        setState({ token: accessToken, user });
    }

    return { login, logout, isAuthenticated, user: state.user, token: state.token, deleteMeForceLogin };
}