import {User} from "./User";
import {Token} from "./Token";

const LOCAL_STORAGE_NAME_USER_STATE: string = 'emwi-auto-moto-user-state';

export class UserState {
    user: User
    token: Token
    lastRefresh: number  // ms since epoch

    constructor(token: Token, user: User) {
        this.token = token;
        this.user = user;
        this.lastRefresh = Date.now();
    }

    private toObject() {
        return {
            "token": this.token.serialize(),
            "user": this.user.serialize(),
            "lastRefresh": this.lastRefresh
        }
    }

    serialize() {
        return JSON.stringify(this.toObject());
    }

    static fromSerialized(serialized: string) {
        const userState: ReturnType<UserState["toObject"]> = JSON.parse(serialized);

        const state: UserState = new UserState(
            Token.fromSerialized(userState.token),
            User.fromSerialized(userState.user)
        );
        state.lastRefresh = userState.lastRefresh;

        return state;
    }


    static getFromLocalStorage() {
        const serializedAuthObj: string | null = localStorage.getItem(LOCAL_STORAGE_NAME_USER_STATE);
        if (serializedAuthObj)
            return UserState.fromSerialized(serializedAuthObj);
        else
            return null;
    }

    saveToLocalStorage() {
        localStorage.setItem(LOCAL_STORAGE_NAME_USER_STATE, this.serialize());
    }

    removeFromLocalStorage() {
        localStorage.removeItem(LOCAL_STORAGE_NAME_USER_STATE);
    }

}
