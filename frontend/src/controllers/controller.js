
export  function post(url = '', data = {}, file = null) {
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
                reject(response.json());
            } else if (response.status >= 200 && response.status < 300) {
                resolve(response.json())
            } else {
                reject(response.json())
            }
        }).catch((err) => {
            reject(err);
        })
    });
}
