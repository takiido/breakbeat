export interface TokenPair {
    access_token: string;
    refresh_token: string;
};

export interface RegisterData {
    email: string;
    username: string;
    password: string;
};

export interface LoginData {
    email: string;
    password: string;
};

export interface RefreshData {
    refresh_token: string;
};