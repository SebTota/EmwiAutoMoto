import {defineStore} from "pinia";
import type {IUser} from "@/interfaces/user";
import {api} from "@/api";
import {getLocalToken, saveLocalToken, removeLocalToken} from "@/utils";
import router from "@/router";
import type {IToken} from "@/interfaces/token";
import axios from "axios";
import type {IMotorcycleList} from "@/interfaces/motorcycle";


export interface MainState {
    token: IToken | null;
    isLoggedIn: boolean | null;
    loginError: string | null;
    user: IUser | null;
}


export const useMainStore = defineStore('mainState', {
    state: (): MainState => {
        return {
            token: null,
            isLoggedIn: false,
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
                await this.refreshToken();
                try {
                    const response = await api.getMe(this.token.access_token);
                    this.isLoggedIn = true;
                    this.user = response.data;
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
                }
            } else {
                console.debug('Logging out due to no token being present during token refresh.');
                this.actionLogout();
            }
        },
        actionRemoveLogIn() {
            removeLocalToken();
            this.token = null;
            this.user = null;
            this.isLoggedIn = false;
        },
        actionRouteLoggedIn() {
            if (router.currentRoute.value.path === '/login') {
                router.push({path: '/'});
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
        async getMotorcycles(page: number): Promise<IMotorcycleList> {
            try {
                const response = await api.getMotorcycles(page);
                return response.data;
            } catch (error) {
                console.error('Failed to retrieve motorcycle list.', error);
                throw Error('Failed to retrieve motorcycle list.');
            }
        }
    }

});
