import axios from 'axios';
import {apiUrl} from '@/env'
import type {IUser} from "@/interfaces/user";
import type {IToken} from "@/interfaces/token";
import type {IMotorcycleList} from "@/interfaces/motorcycle";
import {handleDates} from "@/utils/dates";

const client = axios.create({ baseURL: apiUrl });

client.interceptors.response.use(originalResponse => {
  handleDates(originalResponse.data);
  return originalResponse;
});

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

    return client.post<IToken>(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async refreshToken(refreshToken: string) {
    const body = {
      'refresh_token': refreshToken
    }
    return client.post<IToken>(`${apiUrl}/api/v1/users/refresh-token`);
  },
  async getMe(token: string) {
    return client.get<IUser>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async getMotorcycles(page: number) {
    const params = new URLSearchParams();
    params.append('page', page.toString());

    return client.get<IMotorcycleList>(`${apiUrl}/api/v1/motorcycles`, { params });
  }
};