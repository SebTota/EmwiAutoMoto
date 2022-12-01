
const LOCAL_STORAGE_NAME_AUTH_TOKEN: string = 'emwi-auto-moto-token';

export class Token {
    token_type: string;
    access_token: string;
    access_token_expires: Date;
    refresh_token: string;
    refresh_token_expires: Date;

    constructor(token_type: string, access_token: string, access_token_expires: Date,
                refresh_token: string, refresh_token_expires: Date) {
        this.token_type = token_type;
        this.access_token = access_token;
        this.access_token_expires = access_token_expires;
        this.refresh_token = refresh_token;
        this.refresh_token_expires = refresh_token_expires;
    }

    toObject() {
        return {
            "token_type": this.token_type,
            "access_token": this.access_token,
            "access_token_expires": this.access_token_expires,
            "refresh_token": this.refresh_token,
            "refresh_token_expires": this.refresh_token_expires
        }
    }

    serialize() {
        return JSON.stringify(this.toObject());
    }

    static fromSerialized(serialized: string) {
        const token: ReturnType<Token["toObject"]> = JSON.parse(serialized);

        return new Token(
            token.token_type,
            token.access_token,
            new Date(token.access_token_expires),
            token.refresh_token,
            new Date(token.refresh_token_expires)
        );
    }

    /**
     * Check if the refresh token is still valid
     */
    isValid() {
        const now = new Date();
        now.setHours(now.getHours() + 6);  // Allow for a six-hour buffer
        return this.access_token_expires > now;
    }

    /**
     * Check if a refresh token is still valid to request a new access token
     */
    canRefreshToken() {
        const now = new Date();
        now.setHours(now.getHours() + 1);  // Allow for a one-hour buffer
        return this.refresh_token_expires > now;
    }

}
