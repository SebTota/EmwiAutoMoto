import { HOST, ROUTES } from '../constants'


export function login(username, password) {
    return new Promise((resolve, reject) => {
        fetch(HOST + ROUTES.USER_LOGIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'username': username,
                'password': password
            })
        }).then((response) => {
            if (response.status === 401) {
                reject(response.json());
            } else {
                resolve(response.json())
            }
        }).catch((err) => {
            reject(err);
        })
    });
}
