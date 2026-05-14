import { NextRequest, NextResponse } from "next/server";

export const config = {
    matcher: [
        "/auth/:path*",
        "/calendar/:path*",
    ],
};

export default function proxy(request: NextRequest) {
    const accessToken = request.cookies.get("access_token")?.value;
    const isAuth = !!accessToken;
    const isAuthPage = request.nextUrl.pathname.startsWith("/auth");

    if (isAuth && isAuthPage) {
        return NextResponse.redirect(new URL("/calendar", request.url));
    }
    if (!isAuth && !isAuthPage) {
        return NextResponse.redirect(new URL("/auth?mode=login", request.url));
    }
    return NextResponse.next();
}