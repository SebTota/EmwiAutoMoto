import axios from 'axios';
import {apiUrl} from '@/env'
import type {IUser} from "@/interfaces/user";
import type {IToken} from "@/interfaces/token";
import type {IMotorcycle, IMotorcycleCreate, IMotorcycleList, IMotorcycleUpdate} from "@/interfaces/motorcycle";
import {handleDates} from "@/utils/dates";
import type {ProductStatusEnum} from "@/enums/productStatusEnum";
import type {IImage} from "@/interfaces/image";

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

function configFromAuthHeadersAndParams(auth: { headers: { Authorization: string } } | null, params: URLSearchParams) {
  const config: any = {
    'params': {},
    'headers': {}
  };

  config.params = params;

  if (auth) {
    config.headers = auth.headers
  }

  return config;
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
    return client.post<IToken>(`${apiUrl}/api/v1/users/refresh-token`, body);
  },
  async getMe(token: string) {
    return client.get<IUser>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async getMotorcycles(page: number, status: ProductStatusEnum[], token: string | null = null) {
    const params = new URLSearchParams();
    params.append('page', page.toString());
    status.forEach(s => {
      params.append('show_status', s)
    })

    const auth: { headers: { Authorization: string } } | null = token ? authHeaders(token) : null;
    const config = configFromAuthHeadersAndParams(auth, params);
    return client.get<IMotorcycleList>(`${apiUrl}/api/v1/motorcycles`, config);
  },
  async getMotorcycle(id: string) {
    return client.get<IMotorcycle>(`${apiUrl}/api/v1/motorcycles/${id}`);
  },
  async createMotorcycle(token: string, motorcycle: IMotorcycleCreate) {
    return client.post<IMotorcycle>(`${apiUrl}/api/v1/motorcycles`, motorcycle, authHeaders(token));
  },
  async updateMotorcycle(token: string, motorcycleId: string, motorcycle: IMotorcycleUpdate) {
    return client.put<IMotorcycle>(`${apiUrl}/api/v1/motorcycles/${motorcycleId}`, motorcycle, authHeaders(token));
  },
  async addImageToMotorcycle(token: string, motorcycleId: string, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return client.post<IImage>(`${apiUrl}/api/v1/motorcycles/${motorcycleId}/productImage`, formData, authHeaders(token));
  },
  async sendEmail(first_name: string, last_name: string, email: string, phone_number: string, email_body: string) {
    const body = {
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'phone_number': phone_number,
      'message': email_body
    }
    return client.post(`${apiUrl}/api/v1/contact/email`, body)
  }
};