export function isAdmin() {
    return localStorage.getItem('emwi-auto-moto-username') !== null;
}