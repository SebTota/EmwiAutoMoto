
export function post(url, data = {}, file = null) {
    let headers = {}
    if (localStorage.getItem('emwi-auto-moto-access-token') !== null) {
        headers['Authorization'] = `Bearer ${localStorage.getItem('emwi-auto-moto-access-token')}`;
    }

    let body;
    if (file !== null) {
        let formData = new FormData();
        formData.append('file', file);
        body = formData;
    } else {
        body = JSON.stringify(data);
        headers['Content-Type'] = 'application/json'
    }

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: body
        }).then((response) => {
            if (response.status === 401) {
                localStorage.removeItem('emwi-auto-moto-access-token')
                localStorage.removeItem('emwi-auto-moto-username')
                window.location.href = '/login';
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 300) {
                resolve(response.json())
            } else {
                reject(response.statusText)
            }
        }).catch((err) => {
            reject(err);
        })
    });
}

export function fetchDelete(url, data = {}) {
    let headers = {}
    headers['Content-Type'] = 'application/json'
    if (localStorage.getItem('emwi-auto-moto-access-token') !== null) {
        headers['Authorization'] = `Bearer ${localStorage.getItem('emwi-auto-moto-access-token')}`;
    }

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'DELETE',
            headers: headers,
            body: JSON.stringify(data)
        }).then((response) => {
            if (response.status === 401) {
                localStorage.removeItem('emwi-auto-moto-access-token')
                localStorage.removeItem('emwi-auto-moto-username')
                window.location.href = '/login';
                reject(response.statusText);
            } else if (response.status >= 200 && response.status < 300) {
                resolve(response.json())
            } else {
                reject(response.statusText)
            }
        }).catch((err) => {
            reject(err);
        })
    });
}
