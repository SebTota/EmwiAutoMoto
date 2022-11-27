import { HOST, ROUTES } from '../constants'
import {fetchDelete, post} from "./controller"


export function getMotorcycles(showSold = false, show_status = 'active', page = 1) {
    return new Promise((resolve, _) => {
        fetch(HOST + ROUTES.GET_MOTORCYCLES.replace('{show_sold}', showSold)
            .replace('{show_status}', show_status)
            .replace('{page}', page)).then(response => {
            return response.json()
        }).then(data => {
            resolve(data);
        })
    });
}


export function getMotorcycle(id) {
    return new Promise((resolve, _) => {
        fetch(HOST + ROUTES.GET_MOTORCYCLE.replace('{id}', id)).then(response => {
            return response.json()
        }).then(data => {
            resolve(data);
        })
    });
}


export function updateMotorcycle(id, changes) {
    return post(HOST + ROUTES.UPDATE_MOTORCYCLE.replace('{id}', id), changes)
}

export function createMotorcycle(motorcycle) {
    return post(HOST + ROUTES.CREATE_MOTORCYCLE, motorcycle);
}

export function uploadImage(image) {
    return post(HOST + ROUTES.UPLOAD_IMAGE, {}, image);
}

export function deleteMotorcycle(id) {
    return fetchDelete(HOST + ROUTES.DELETE_MOTORCYCLE.replace('{id}', id));
}