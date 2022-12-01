// @ts-ignore
import { HOST, ROUTES } from '../constants'
import {Token} from "../models/Token";
import {User} from "../models/User";
import {UserState} from "../models/UserState";


async function getAuthBearerToken(): Promise<string | null> {
    const userState: UserState | null = UserState.getFromLocalStorage();

    if (userState) {
        if (userState.token.isValid()) {
            return userState.token.access_token;
        } else if (userState.token.canRefreshToken()) {
            const refreshedAuth = await refreshAuthCredentials();
            return refreshedAuth.access_token;
        }
    }

    return null;
}


/**
 * Refresh the user credentials of an already signed-in user.
 * @return Promise<Auth> a promise containing the refreshed user auth.
 */
export function refreshAuthCredentials(): Promise<Token> {
    return new Promise<Token>((resolve, reject) => {
        // Only use getWithAuthHeader here to avoid a possible infinite loop
        getWithAuthHeader(HOST + ROUTES.REFRESH_TOKEN, null).then(tokenData => {
            const token: Token = Token.fromSerialized(JSON.stringify(tokenData));
            getUserDetailsUsingToken(token).then(user => {
                const userState: UserState = new UserState(token, user);
                userState.saveToLocalStorage();
            }).catch(err => {
                console.error('Refreshed auth token, but failed at retrieving user data', err);
                reject();
            })
        }).catch(err => {
            console.error("Failed to refresh user credentials.", err);
            reject();
        })
    });
}


export function getUserDetailsUsingToken(token: Token): Promise<User> {
    return new Promise<User>((resolve, reject) => {
        getWithAuthHeader(HOST + ROUTES.USER_DETAILS, token.access_token).then((userData) => {
            const user: User = User.fromSerialized(JSON.stringify(userData));
            resolve(user);
        }).catch(err => {
            console.error("Failed to get information on signed in user.", err);
            reject("Uh oh. An error occurred when trying to get the signed in user details.\n" + err);
        })
    })
}


export function postFormData(url: string, formData: FormData) {
    return new Promise<any>((resolve, reject) => {
        getAuthBearerToken().then(token => {
            postFormDataWithAuthHeader(url, formData, token).then(d => {
                resolve(d);
            }).catch(e => {
                reject(e);
            })
        }).catch(_ => {
            postFormDataWithAuthHeader(url, formData, null).then(d => {
                resolve(d);
            }).catch(e => {
                reject(e);
            })
        });
    })
}

export async function postJsonData(url: string, data: any) {
    return new Promise<any>((resolve, reject) => {
        getAuthBearerToken().then(token => {
            postJsonDataWithAuthHeader(url, data, token).then(d => {
                resolve(d);
            }).catch(e => {
                reject(e);
            })
        }).catch(_ => {
            postJsonDataWithAuthHeader(url, data, null).then(d => {
                resolve(d);
            }).catch(e => {
                reject(e);
            })
        });
    })
}

export function get(url: string) {
    return new Promise<any>((resolve, reject) => {
        getAuthBearerToken().then(token => {
            getWithAuthHeader(url, token).then(d => {
                resolve(d);
            }).catch(e => {
                reject(e);
            })
        }).catch(_ => {
            getWithAuthHeader(url, null).then(d => {
                resolve(d);
            }).catch(e => {
                reject(e);
            })
        });
    })
}

export function postFormDataWithAuthHeader(url: string,
                                           formData: any,
                                           authHeaderValue: string | null): Promise<any> {
    let headers: any = {};
    if (authHeaderValue)
        headers['Authorization'] = `Bearer ${authHeaderValue}`;

    return new Promise<any>((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: formData
        }).then(response => {
            if (response.status === 401) {
                deAuthUser();
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 400) {
                return response.json();
            } else {
                reject(response.statusText)
            }
        }).then(data => {
            resolve(data);
        }).catch(err => {
            reject(err);
        })
    });
}

export function postJsonDataWithAuthHeader(url: string,
                                           data: any,
                                           authHeaderValue: string | null): Promise<any> {
    const body = JSON.stringify(data);

    let headers: any = {};
    headers['Content-Type'] = 'application/json';
    if (authHeaderValue)
        headers['Authorization'] = `Bearer ${authHeaderValue}`;

    return new Promise<any>((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: body
        }).then(response => {
            if (response.status === 401) {
                deAuthUser();
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 400) {
                return response.json();
            } else {
                console.error(`Request to ${url} resulted in response code: ${response.statusText}`);
                reject(response.statusText)
            }
        }).then(data => {
            resolve(data);
        }).catch(err => {
            reject(err);
        })
    });
}


export function getWithAuthHeader(url: string,
                                  authHeaderValue: string | null): Promise<any> {
    let headers: any = {};
    if (authHeaderValue)
        headers['Authorization'] = `Bearer ${authHeaderValue}`;

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'GET',
            headers: headers
        }).then(response => {
            if (response.status === 401) {
                deAuthUser();
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 400) {
                return response.json();
            } else {
                reject(response.statusText)
            }
        }).then(data => {
            resolve(data);
        }).catch(err => {
            reject(err);
        })
    });
}


function deAuthUser() {
    console.log('Received an unauthorized request. Removing signed in user and redirecting to login page.');
    localStorage.removeItem('emwi-auto-moto-auth');
    window.location.href = '/login';
}

// Export post data