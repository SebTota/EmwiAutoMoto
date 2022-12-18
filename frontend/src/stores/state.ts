import {defineStore} from "pinia";
import type {IUser} from "@/interfaces/user";
import {api} from "@/api";
import {getLocalToken, removeLocalToken, saveLocalToken} from "@/utils/token";
import router from "@/router";
import type {IToken} from "@/interfaces/token";
import axios from "axios";
import type {IMotorcycle, IMotorcycleCreate, IMotorcycleList} from "@/interfaces/motorcycle";
import {ProductStatusEnum} from "@/enums/productStatusEnum";


export interface MainState {
    token: IToken | null;
    isLoggedIn: boolean | null;
    isAdmin: boolean | null;
    loginError: string | null;
    user: IUser | null;
}


export const useMainStore = defineStore('mainState', {
    state: (): MainState => {
        return {
            token: null,
            isLoggedIn: false,
            isAdmin: false,
            loginError: null,
            user: null
        }
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
                    this.actionLogout();
                }
            } catch (error) {
                console.error('Failed to log in user.');
                this.loginError = 'Failed to sign in. Please try again.';
                this.actionLogout();
            }
            if (this.loginError) {
                throw Error(this.loginError);
            }
        },
        async actionGetUserProfile() {
            if (!this.isLoggedIn) {
                this.actionLogout();
            }

            await this.refreshToken();

            if (this.token) {
                try {
                    const response = await api.getMe(this.token.access_token);
                    if (response.data) {
                        this.user = response.data;
                        this.isAdmin = response.data.is_superuser;
                    }
                } catch (error) {
                    console.error('Failed to retrieve signed in user information.', error);
                    this.actionCheckApiError(error);
                }
            } else {
                this.actionLogout();
            }
        },
        async actionCheckLoggedIn() {
            if (!this.isLoggedIn && !this.token) {
                const localToken = getLocalToken();
                if (localToken) {
                    this.token = localToken;
                }
            }

            if (this.token) {
                await this.refreshToken();
            }

            if (!this.isLoggedIn && this.token) {
                try {
                    const response = await api.getMe(this.token.access_token);
                    this.isLoggedIn = true;
                    this.user = response.data;
                    this.isAdmin = response.data.is_superuser;
                } catch (error) {
                    console.error('Failed to retrieve signed in user information.', error);
                    await this.actionRemoveLogIn();
                }
            } else if (!this.token) {
                await this.actionRemoveLogIn();
            }
        },
        actionLogout() {
            this.actionRemoveLogIn();
            this.actionRouteLogOut();
        },
        actionCheckApiError(payload: any) {
            if (axios.isAxiosError(payload)) {
                if (payload.response!.status === 401) {
                    this.actionLogout();
                }
            }
        },
        async refreshToken() {
            if (this.token) {
                // Refresh token if it expires within 7 days
                const tokenExp: Date = this.token.refresh_token_expires;
                const sevenDays: number = 24 * 7;
                const sevenDaysIntoTheFuture: Date = new Date();
                sevenDaysIntoTheFuture.setHours(sevenDaysIntoTheFuture.getHours() + sevenDays);
                const shouldRefresh: boolean = tokenExp < sevenDaysIntoTheFuture;

                if (shouldRefresh && this.refreshTokenIsValid()) {
                    console.debug('Refreshing auth token');
                    try {
                        const response = await api.refreshToken(this.token.refresh_token);
                        if (response.data) {
                            this.token = response.data;
                        }
                    } catch (error) {
                        console.error('Failed to refresh valid user token.', error);
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
            if (router.currentRoute.value.path === '/login') {
                // Nav using href after login to refresh header auth check
                window.location.href = '/';
            }
        },
        actionRouteLogOut() {
            if (router.currentRoute.value.path !== '/login') {
                router.push({path: '/login'});
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
        async getMotorcycles(page: number, status: ProductStatusEnum[] = [ProductStatusEnum.active, ProductStatusEnum.inactive]): Promise<IMotorcycleList> {
            let token;
            if (this.token && this.tokenIsValid()) {
                token = this.token.access_token;
            }
            try {
                const response = await api.getMotorcycles(page, status, token);
                return response.data;
            } catch (error) {
                console.error('Failed to retrieve motorcycle list.', error);
                throw Error('Failed to retrieve motorcycle list.');
            }
        },
        async getMotorcycle(id: string): Promise<IMotorcycle> {
            try {
                const response = await api.getMotorcycle(id);
                return response.data;
            } catch (error) {
                console.error(error);
                throw Error('Failed to retrieve motorcycle details.');
            }
        },
        async createMotorcycle(motorcycle: IMotorcycleCreate): Promise<IMotorcycle> {
            if (this.token && this.tokenIsValid()) {
                try {
                    const response = await api.createMotorcycle(this.token.access_token, motorcycle);
                    return response.data;
                } catch (error) {
                    console.error(error);
                    this.actionCheckApiError(error);
                    throw Error('Failed to create motorcycle.');
                }
            } else {
                this.actionLogout();
                throw Error('User can not perform this action. Not signed in.');
            }
        },
        async updateMotorcycle(motorcycleId: string, motorcycle: IMotorcycleCreate): Promise<IMotorcycle> {
            if (this.token && this.tokenIsValid()) {
                try {
                    const response = await api.updateMotorcycle(this.token.access_token, motorcycleId, motorcycle);
                    return response.data;
                } catch (error) {
                    console.error(error);
                    this.actionCheckApiError(error);
                    throw Error('Failed to create motorcycle.');
                }
            } else {
                this.actionLogout();
                throw Error('User can not perform this action. Not signed in.');
            }
        },
        async addImageToMotorcycle(motorcycleId: string, file: File) {
            if (this.token && this.tokenIsValid()) {
                try {
                    const response = await api.addImageToMotorcycle(this.token.access_token, motorcycleId, file);
                    return response.data;
                } catch (error) {
                    console.error(error);
                    this.actionCheckApiError(error);
                    throw Error('Failed to add image to motorcycle.');
                }
            } else {
                this.actionLogout();
                throw Error('User can not perform this action. Not signed in.');
            }
        }
    }

});
