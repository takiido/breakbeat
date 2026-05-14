"use server";

import {cookies} from "next/headers";
import { redirect } from "next/navigation";
import { LoginData, RegisterData, RefreshData, TokenPair } from "@/lib/types";
import { post } from "@/lib/api";

const ACCESS_TOKEN_MAX_AGE: number = parseInt(process.env.ACCESS_TOKEN_EXPIRE_MINUTES ?? "0") * 60;
const REFRESH_TOKEN_MAX_AGE: number = parseInt(process.env.REFRESH_TOKEN_EXPIRE_DAYS ?? "0") * 24 * 60 * 60;

export async function getTokenPair(): Promise<TokenPair> {
    const cookieStore = await cookies();
    const accessToken = cookieStore.get("access_token")?.value;
    const refreshToken = cookieStore.get("refresh_token")?.value;
    if (!accessToken || !refreshToken) {
        throw new Error("Access or refresh token not found");
    }
    return { access_token: accessToken, refresh_token: refreshToken } as TokenPair;
}

async function setTokenPair(tokenPair: TokenPair) {
    const cookieStore = await cookies();
    cookieStore.set("access_token", tokenPair.access_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        maxAge: ACCESS_TOKEN_MAX_AGE,
    });
    cookieStore.set("refresh_token", tokenPair.refresh_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        maxAge: REFRESH_TOKEN_MAX_AGE,
    });
}

export async function register(data: RegisterData): Promise<void> {
    const tokenPair = await post("/auth/register", data) as TokenPair;
    await setTokenPair(tokenPair);
    redirect("/calendar");
}

export async function login(data: LoginData): Promise<void> {
    const tokenPair = await post("/auth/login", data) as TokenPair;
    await setTokenPair(tokenPair);
    redirect("/calendar");
}

export async function refresh(data: RefreshData): Promise<void> {
    try {
        const tokenPair = await post("/auth/refresh", data);
        await setTokenPair(tokenPair as TokenPair);
    } catch {
        redirect("/auth?mode=login");
    }
}