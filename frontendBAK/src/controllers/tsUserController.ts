// @ts-ignore
import { HOST, ROUTES } from '../constants'
import {getUserDetailsUsingToken, postFormData} from "./baseController";
import {Token} from "../models/Token";


export function login(username: string, password: string) {
    const data = new FormData();
    data.append('username', username);
    data.append('password', password);
    return postFormData(HOST + ROUTES.USER_LOGIN, data);
}


/**
 * This method is used on login when we do not yet have a stored Auth object we can authorize our requests with.
 */
export function getUserDetailWithAuthToken(token: Token) {
    return getUserDetailsUsingToken(token);
}
