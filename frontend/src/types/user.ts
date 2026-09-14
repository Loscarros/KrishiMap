
export interface UserProfile {
  name: string;
  email: string;
  password: string;

  state: string;
  district: string;
  area: string;
}

export interface AuthUser {
  name: string;
  email: string;
  state: string;
  district: string;
  area: string;
}