import axios from 'axios';
import {apiUrl} from '@/env'
import type {IUser} from "@/interfaces/user";
import type {IToken} from "@/interfaces/token";
import type {IMotorcycleList} from "@/interfaces/motorcycle";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post<IToken>(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async refreshToken(refreshToken: string) {
    const body = {
      'refresh_token': refreshToken
    }
    return axios.post<IToken>(`${apiUrl}/api/v1/users/refresh-token`);
  },
  async getMe(token: string) {
    return axios.get<IUser>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async getMotorcycles(page: number) {
    const params = new URLSearchParams();
    params.append('page', page.toString());

    return axios.get<IMotorcycleList>(`${apiUrl}/api/v1/motorcycles`, { params });
  }
};