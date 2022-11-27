import { HOST, ROUTES } from '../constants'
import { post } from "./controller"


export function login(username, password) {
    return post(HOST + ROUTES.USER_LOGIN, {
                'username': username,
                'password': password
            })
}
