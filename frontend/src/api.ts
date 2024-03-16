import axios from "axios";
import { apiUrl } from "@/env";
import type { IUser } from "@/interfaces/user";
import type { IToken } from "@/interfaces/token";
import type { IProductCreate } from "@/interfaces/product";
import { handleDates } from "@/utils/dates";
import type { ProductStatusEnum } from "@/enums/productStatusEnum";
import type { IMedia } from "@/interfaces/media";
import type { IMotorcycleList, IMotorcycleWithContent } from "@/interfaces/motorcycle";
import type { IMowerList, IMowerWithContent } from "@/interfaces/mower";
import type { IPartList, IPartWithContent } from "@/interfaces/parts";

const client = axios.create({ baseURL: apiUrl });

client.interceptors.response.use((originalResponse) => {
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
    params: {},
    headers: {},
  };

  config.params = params;

  if (auth) {
    config.headers = auth.headers;
  }

  return config;
}

function createSearchParamsForGetProductsRequest(page: number, status: ProductStatusEnum[]): URLSearchParams {
  const params = new URLSearchParams();
  params.append("page", page.toString());
  status.forEach((s) => {
    params.append("show_status", s);
  });
  return params;
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return client.post<IToken>(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async refreshToken(refreshToken: string) {
    const body = {
      refresh_token: refreshToken,
    };
    return client.post<IToken>(`${apiUrl}/api/v1/users/refresh-token`, body);
  },
  async getMe(token: string) {
    return client.get<IUser>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async getMotorcycles(page: number, status: ProductStatusEnum[], token: string | null = null) {
    const auth: { headers: { Authorization: string } } | null = token ? authHeaders(token) : null;
    const config = configFromAuthHeadersAndParams(auth, createSearchParamsForGetProductsRequest(page, status));
    return client.get<IMotorcycleList>(`${apiUrl}/api/v1/products/motorcycles`, config);
  },
  async getMowers(page: number, status: ProductStatusEnum[], token: string | null = null) {
    const auth: { headers: { Authorization: string } } | null = token ? authHeaders(token) : null;
    const config = configFromAuthHeadersAndParams(auth, createSearchParamsForGetProductsRequest(page, status));
    return client.get<IMowerList>(`${apiUrl}/api/v1/products/mowers`, config);
  },
  async getParts(page: number, status: ProductStatusEnum[], token: string | null = null) {
    const auth: { headers: { Authorization: string } } | null = token ? authHeaders(token) : null;
    const config = configFromAuthHeadersAndParams(auth, createSearchParamsForGetProductsRequest(page, status));
    return client.get<IPartList>(`${apiUrl}/api/v1/products/parts`, config);
  },
  async getMotorcycle(id: string) {
    return client.get<IMotorcycleWithContent>(`${apiUrl}/api/v1/products/motorcycles/${id}`);
  },
  async getMower(id: string) {
    return client.get<IMowerWithContent>(`${apiUrl}/api/v1/products/mowers/${id}`);
  },
  async getPart(id: string) {
    return client.get<IPartWithContent>(`${apiUrl}/api/v1/products/parts/${id}`);
  },
  async createMotorcycle(token: string, product: IProductCreate) {
    return client.post<IMotorcycleWithContent>(`${apiUrl}/api/v1/products/motorcycles`, product, authHeaders(token));
  },
  async createMower(token: string, product: IProductCreate) {
    return client.post<IMowerWithContent>(`${apiUrl}/api/v1/products/mowers`, product, authHeaders(token));
  },
  async createPart(token: string, product: IProductCreate) {
    return client.post<IPartWithContent>(`${apiUrl}/api/v1/products/parts`, product, authHeaders(token));
  },
  async updateMotorcycle(token: string, productId: string, product: IProductCreate) {
    return client.put<IMotorcycleWithContent>(
      `${apiUrl}/api/v1/products/motorcycles/${productId}`,
      product,
      authHeaders(token)
    );
  },
  async uploadProductImages(token: string, files: FileList) {
    const formData = new FormData();
    Array.from(files).forEach((file, index) => {
      formData.append("files", file);
    });
    return client.post<[IMedia]>(`${apiUrl}/api/v1/products/images`, formData, authHeaders(token));
  },
};
