
import { AuthUser } from "@/types/user";
import { api } from "@/lib/api";

const TOKEN_KEY = "krishimap-token";

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface BackendUser {
  id: number;
  name: string;
  email: string;
  state: string;
  district: string;
  area: string;
  latitude?: number | null;
  longitude?: number | null;
  location_updated_at?: string | null;
}

export function saveToken(token: string) {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.setItem(
    TOKEN_KEY,
    token
  );
}

export function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem(
    TOKEN_KEY
  );
}

export function clearToken() {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.removeItem(
    TOKEN_KEY
  );
}

export function isAuthenticated(): boolean {
  return Boolean(getToken());
}

export async function loginUser(
  email: string,
  password: string
): Promise<boolean> {
  const formData =
    new URLSearchParams();

  formData.append(
    "username",
    email.trim().toLowerCase()
  );

  formData.append(
    "password",
    password
  );

  try {
    const response =
      await api.post<LoginResponse>(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
        }
      );

    saveToken(
      response.data.access_token
    );

    return true;
  } catch (error) {
    console.error(
      "Login failed:",
      error
    );

    return false;
  }
}

export async function getCurrentUser(): Promise<AuthUser | null> {
  try {
    const response =
      await api.get<BackendUser>(
        "/auth/me"
      );

    const user =
      response.data;

    return {
      name: user.name,
      email: user.email,
      state: user.state,
      district: user.district,
      area: user.area,
    };
  } catch (error) {
    console.error(
      "Failed to get current user:",
      error
    );

    return null;
  }
}

export async function getCurrentUserDetails(): Promise<BackendUser | null> {
  try {
    const response =
      await api.get<BackendUser>(
        "/auth/me"
      );

    return response.data;
  } catch (error) {
    console.error(
      "Failed to get current user:",
      error
    );

    return null;
  }
}

export function logoutUser() {
  clearToken();
}