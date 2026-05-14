"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { LoginData, RegisterData } from "@/lib/types";
import { register, login } from "@/actions/auth";
import styles from "./styles.module.scss";

export default function AuthPage() {
  const searchParams = useSearchParams();
  const [mode, setMode] = useState<string | null>(null);

  const [registerData, setRegisterData] = useState<RegisterData>({
    email: "",
    username: "",
    password: "",
  });
  const [loginData, setLoginData] = useState<LoginData>({
    email: "",
    password: "",
  });
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (mode === "register") {
      await register(registerData);
    }
    if (mode === "login") {
      await login(loginData);
    }
  }

  useEffect(() => {
    setMode(searchParams.get("mode"));
  }, [searchParams]);

  return(
    <div> 
      {
        mode === "register" ?
          <form className={styles.register_form} onSubmit={handleSubmit}>
            <label htmlFor="reg-username">Username:</label>
            <input 
              name="reg-username" 
              type="text" 
              required 
              placeholder="Username"
              value={registerData.username}
              onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })}
            />

            <label htmlFor="reg-email">Email:</label>
            <input 
              name="reg-email" 
              type="email" 
              required 
              placeholder="Email"
              value={registerData.email}
              onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })}
            />
        
            <label htmlFor="reg-password">Password:</label>
            <input 
              name="reg-password" 
              type="password" 
              required 
              placeholder="Password"
              value={registerData.password}
              onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
            />

            <button type="submit">Register</button>
            <button onClick={() => setMode("login")}>Already registered? Sign in</button>
          </form>
      :
        <form className={styles.register_form} onSubmit={handleSubmit}>
          <label htmlFor="reg-email">Email:</label>
          <input 
            name="reg-email" 
            type="email" 
            required 
            placeholder="Email"
            value={loginData.email}
            onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
          />
        
          <label htmlFor="reg-password">Password:</label>
          <input 
            name="reg-password" 
            type="password" 
            required 
            placeholder="Password"
            value={loginData.password}
            onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
          />

          <button type="submit">Sign in</button>
          <button onClick={() => setMode("register")}>Don't have account? Register</button>
        </form>
      }
    </div>
  )
}
