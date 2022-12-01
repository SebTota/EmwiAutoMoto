import {UserState} from "../models/UserState";

export async function isAdmin(): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {
        const userState: UserState | null = UserState.getFromLocalStorage();
        if (userState) {
            if (userState.token.isValid()) {
                resolve(userState.user.is_superuser);
            } else {
                // Todo: Try to refresh auth credentials
                resolve(false);
            }
        }
        resolve(false);
    })
}

export function isSignedIn(): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {
        const userState: UserState | null = UserState.getFromLocalStorage();
        if (userState) {
            if (userState.token.isValid()) {
                resolve(true);
            } else {
                // Todo: Try to refresh auth credentials
                resolve(false);
            }
        }
        resolve(false);
    })
}
