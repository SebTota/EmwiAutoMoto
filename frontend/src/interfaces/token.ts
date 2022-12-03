
export interface IToken {
    token_type: string,
    access_token: string,
    access_token_expires: Date,
    refresh_token: string,
    refresh_token_expires: Date
}
