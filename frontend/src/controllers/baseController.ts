
export function postFormData(url: string, formData: FormData) {
    let headers: any = {}
    // if (localStorage.getItem('emwi-auto-moto-access-token') !== null) {
    //     headers['Authorization'] = `Bearer ${localStorage.getItem('emwi-auto-moto-access-token')}`;
    // }

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


function deAuthUser() {
    console.log('Received an unauthorized request. Removing signed in user and redirecting to login page.');
    localStorage.removeItem('emwi-auto-moto-access-token');
    window.location.href = '/login';
}

// Export post data