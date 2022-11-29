import {Token} from './Token'

export class User {
    id: number;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    auth_token: Token;

    constructor(id: number, first_name: string, last_name: string, username: string,
                email: string, is_active: boolean, is_superuser: boolean, auth_token: Token) {
        this.id = id;
        this.first_name = first_name;
        this.last_name = last_name;
        this.username = username;
        this.email = email;
        this.is_active = is_active;
        this.is_superuser = is_superuser;
        this.auth_token = auth_token;
    }

    private toObject() {
        return {
            "id": this.id,
            "first_name": this.first_name,
            "last_name": this.last_name,
            "username": this.username,
            "email": this.email,
            "is_active": this.is_active,
            "is_superuser": this.is_superuser,
            "auth_token": this.auth_token.toObject()
        }
    }

    serialize() {
        return JSON.stringify(this.toObject());
    }

    static fromSerialized(serialized: string) {
        const user: ReturnType<User["toObject"]> = JSON.parse(serialized);

        return new User(
          user.id,
          user.first_name,
          user.last_name,
          user.username,
          user.email,
          user.is_active,
          user.is_superuser,
          new Token(user.auth_token.token_type,
              user.auth_token.access_token,
              user.auth_token.access_token_expires,
              user.auth_token.refresh_token,
              user.auth_token.refresh_token_expires)
        );
    }

}
