import {User} from "./User";
import {Token} from "./Token";


export class Auth {
    user: User
    token: Token

    constructor(user: User, token: Token) {
        this.user = user;
        this.token = token;
    }

    setUser(user: User) {
        this.user = user;
    }

    private toObject() {
        return {
            "user": this.user.serialize(),
            "token": this.token.serialize()
        }
    }

    serialize() {
        return JSON.stringify(this.toObject());
    }

    static fromSerialized(serialized: string) {
        const auth: ReturnType<Auth["toObject"]> = JSON.parse(serialized);
        return new Auth(User.fromSerialized(auth.user), Token.fromSerialized(auth.token));
    }

    saveAuthToLocalStorage() {
        localStorage.setItem('emwi-auto-moto-auth', this.serialize());
    }

    static getAuthFromLocalStorage() {
        const serializedAuthObj: string | null = localStorage.getItem('emwi-auto-moto-auth');
        if (serializedAuthObj)
            return Auth.fromSerialized(serializedAuthObj);
        else
            return null;
    }
}