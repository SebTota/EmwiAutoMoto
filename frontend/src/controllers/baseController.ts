
export function postFormData(url: string, formData: FormData) {
    let headers: any = {}

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: formData
        }).then((response) => {
            if (response.status === 401) {
                deAuthUser();
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 400) {
                resolve(response.json())
            } else {
                reject(response.statusText)
            }
        }).catch((err) => {
            reject(err);
        })
    });
}

// export function postJsonData(url: string, data: any) {
//     // return postJsonDataWithAuthHeader()
// }

export function postJsonDataWithAuthHeader(url: string, data: any, authHeaderValue: string | null) {
    const body = JSON.stringify(data);
    let headers: any = {};
    headers['Content-Type'] = 'application/json';
    if (authHeaderValue)
        headers['Authorization'] = `Bearer ${authHeaderValue}`;

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: body
        }).then((response) => {
            if (response.status === 401) {
                deAuthUser();
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 400) {
                resolve(response.json())
            } else {
                reject(response.statusText)
            }
        }).catch((err) => {
            reject(err);
        })
    });
}

export function get(url: string) {
    return getWithAuthHeader(url, null);
}


export function getWithAuthHeader(url: string, authHeaderValue: string | null) {
    let headers: any = {};
    if (authHeaderValue)
        headers['Authorization'] = `Bearer ${authHeaderValue}`;

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'GET',
            headers: headers
        }).then(response => {
            return response.json()
        }).then(data => {
            resolve(data);
        }).catch((err) => {
            reject(err);
        })
    });
}


function deAuthUser() {
    console.log('Received an unauthorized request. Removing signed in user and redirecting to login page.');
    localStorage.removeItem('emwi-auto-moto-auth');
    window.location.href = '/login';
}

// Export post data