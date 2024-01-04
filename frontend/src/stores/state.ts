import { defineStore } from "pinia";
import type { IUser } from "@/interfaces/user";
import { api } from "@/api";
import { getLocalToken, removeLocalToken, saveLocalToken } from "@/utils/token";
import router from "@/router";
import type { IToken } from "@/interfaces/token";
import axios from "axios";
import type {
  IProductCreate,
  IProductList,
  IProductWithImages,
} from "@/interfaces/product";
import { ProductStatusEnum } from "@/enums/productStatusEnum";

export interface MainState {
  token: IToken | null;
  isLoggedIn: boolean | null;
  isAdmin: boolean | null;
  loginError: string | null;
  user: IUser | null;
}

export const useMainStore = defineStore("mainState", {
  state: (): MainState => {
    return {
      token: null,
      isLoggedIn: false,
      isAdmin: false,
      loginError: null,
      user: null,
    };
  },

  actions: {
    async actionLogIn(username: string, password: string) {
      try {
        const response = await api.logInGetToken(username, password);
        const token: IToken = response.data;
        if (token) {
          saveLocalToken(token);
          this.token = token;
          this.isLoggedIn = true;
          this.loginError = null;
          await this.actionGetUserProfile();
          this.actionRouteLoggedIn();
          return this.user;
        } else {
          this.actionLogoutAndNavigateToLogin();
        }
      } catch (error) {
        console.error("Failed to log in user.", error);
        this.loginError = "Failed to sign in. Please try again.";
        this.actionLogoutAndNavigateToLogin();
      }
      if (this.loginError) {
        throw Error(this.loginError);
      }
    },
    async actionGetUserProfile() {
      if (!this.isLoggedIn) {
        this.actionLogoutAndNavigateToLogin();
      }

      // await this.refreshToken();

      if (this.token) {
        try {
          const response = await api.getMe(this.token.access_token);
          if (response.data) {
            this.user = response.data;
            this.isAdmin = response.data.is_superuser;
          }
        } catch (error) {
          console.error(
            "Failed to retrieve signed in user information.",
            error
          );
          this.actionCheckApiError(error);
        }
      } else {
        this.actionLogoutAndNavigateToLogin();
      }
    },
    async actionCheckLoggedIn() {
      if (!this.isLoggedIn && !this.token) {
        const localToken = getLocalToken();
        if (localToken) {
          this.token = localToken;
        }
      }

      // if (this.token) {
      //     await this.refreshToken();
      // }

      if (!this.isLoggedIn && this.token) {
        try {
          const response = await api.getMe(this.token.access_token);
          this.isLoggedIn = true;
          this.user = response.data;
          this.isAdmin = response.data.is_superuser;
        } catch (error) {
          console.error(
            "Failed to retrieve signed in user information.",
            error
          );
          await this.actionRemoveLogIn();
        }
      } else if (!this.token) {
        await this.actionRemoveLogIn();
      }
    },
    actionLogoutAndNavigateToLogin() {
      this.actionRemoveLogIn();
      this.actionRouteLogOut();
    },
    actionLogout() {
      this.actionRemoveLogIn();
    },
    actionCheckApiError(payload: any) {
      if (axios.isAxiosError(payload)) {
        if (payload.response!.status === 401) {
          this.actionLogoutAndNavigateToLogin();
        }
      }
    },
    async refreshToken() {
      if (this.token) {
        // Refresh token if it expires within 7 days
        const tokenExp: Date = this.token.refresh_token_expires;
        const sevenDays: number = 24 * 7;
        const sevenDaysIntoTheFuture: Date = new Date();
        sevenDaysIntoTheFuture.setHours(
          sevenDaysIntoTheFuture.getHours() + sevenDays
        );
        const shouldRefresh: boolean = tokenExp < sevenDaysIntoTheFuture;

        if (shouldRefresh && this.refreshTokenIsValid()) {
          console.debug("Refreshing auth token");
          try {
            const response = await api.refreshToken(this.token.refresh_token);
            if (response.data) {
              this.token = response.data;
            }
          } catch (error) {
            console.error("Failed to refresh valid user token.", error);
          }
        } else if (!this.refreshTokenIsValid()) {
          this.actionRemoveLogIn();
        }
      }
    },
    actionRemoveLogIn() {
      this.token = null;
      this.user = null;
      this.isLoggedIn = false;
      this.isAdmin = false;
      removeLocalToken();
    },
    actionRouteLoggedIn() {
      if (router.currentRoute.value.path === "/login") {
        // Nav using href after login to refresh header auth check
        window.location.href = "/";
      }
    },
    actionRouteLogOut() {
      if (router.currentRoute.value.path !== "/login") {
        router.push({ path: "/login" });
      }
    },
    tokenIsValid(): boolean {
      if (this.token) {
        const tokenExp: Date = this.token.access_token_expires;
        tokenExp.setHours(tokenExp.getHours() - 1);
        return tokenExp > new Date();
      }
      return false;
    },
    refreshTokenIsValid(): boolean {
      if (this.token) {
        const refreshTokenExp: Date = this.token.refresh_token_expires;
        refreshTokenExp.setHours(refreshTokenExp.getHours() - 1);
        return refreshTokenExp > new Date();
      }
      return false;
    },
    async getProducts(
      page: number,
      status: ProductStatusEnum[] = [ProductStatusEnum.FOR_SALE]
    ): Promise<IProductList> {
      let token;
      if (this.token && this.tokenIsValid()) {
        token = this.token.access_token;
      }
      try {
        const response = await api.getProducts(page, status, token);
        return response.data;
      } catch (error) {
        console.error("Failed to retrieve product list.", error);
        throw Error("Failed to retrieve product list.");
      }
    },
    async getProduct(id: string): Promise<IProductWithImages> {
      try {
        const response = await api.getProduct(id);
        return response.data;
      } catch (error) {
        console.error(error);
        throw Error("Failed to retrieve product details.");
      }
    },
    async createProducts(
      product: IProductCreate
    ): Promise<IProductWithImages> {
      if (this.token && this.tokenIsValid()) {
        try {
          const response = await api.createProduct(
            this.token.access_token,
            product
          );
          return response.data;
        } catch (error) {
          console.error(error);
          this.actionCheckApiError(error);
          throw Error("Failed to create product.");
        }
      } else {
        this.actionLogoutAndNavigateToLogin();
        throw Error("User can not perform this action. Not signed in.");
      }
    },
    async updateProducts(
      productId: string,
      product: IProductCreate
    ): Promise<IProductWithImages> {
      if (this.token && this.tokenIsValid()) {
        try {
          const response = await api.updateProduct(
            this.token.access_token,
            productId,
            product
          );
          return response.data;
        } catch (error) {
          console.error(error);
          this.actionCheckApiError(error);
          throw Error("Failed to create product.");
        }
      } else {
        this.actionLogoutAndNavigateToLogin();
        throw Error("User can not perform this action. Not signed in.");
      }
    },
    async uploadProductImage(files: FileList) {
      if (this.token && this.tokenIsValid()) {
        try {
          const response = await api.uploadProductImages(
            this.token.access_token,
            files
          );
          return response.data;
        } catch (error) {
          console.error(error);
          this.actionCheckApiError(error);
          throw Error("Failed to add image to product.");
        }
      } else {
        this.actionLogoutAndNavigateToLogin();
        throw Error("User can not perform this action. Not signed in.");
      }
    },
  },
});
