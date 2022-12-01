export const HOST = 'http://localhost:9000';
export const ROUTES = {
    GET_MOTORCYCLES: '/api/v1/motorcycles?show_sold={show_sold}&show_status={show_status}&page={page}',
    GET_MOTORCYCLE: '/api/v1/motorcycles/{id}',
    UPDATE_MOTORCYCLE: '/api/v1/motorcycles/{id}',
    CREATE_MOTORCYCLE: '/api/v1/motorcycles',
    DELETE_MOTORCYCLE: '/api/v1/motorcycles/{id}',
    USER_LOGIN: '/api/v1/login/access-token',
    REFRESH_TOKEN: '/api/v1/login/refresh-token',
    USER_DETAILS: '/api/v1/users/me'
}

export const UI_ROUTERS = {
    LOGIN: '/login'
}