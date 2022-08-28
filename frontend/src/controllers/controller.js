
export  function post(url = '', data = {}) {
    let headers =
        {
            'Content-Type': 'application/json'
        }
    if (localStorage.getItem('emwi-auto-moto-access-token') !== null) {
        headers['Authorization'] = `Bearer ${localStorage.getItem('emwi-auto-moto-access-token')}`;
    }

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(data)
        }).then((response) => {
            if (response.status === 401) {
                window.location.href = '/login';
                reject(response.json());
            } else {
                resolve(response.json())
            }
        }).catch((err) => {
            reject(err);
        })
    });
}
