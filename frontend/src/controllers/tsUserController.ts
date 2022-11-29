// @ts-ignore
import { HOST, ROUTES } from '../constants'
import {postFormData} from "./baseController";


export function login(username: string, password: string) {
    const data = new FormData();
    data.append('username', username);
    data.append('password', password);
    return postFormData(HOST + ROUTES.USER_LOGIN, data);
}
