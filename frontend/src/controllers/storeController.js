import {Motorcycle} from "../models/Motorcycle";
import { HOST, ROUTES } from '../constants'
import { post } from "./controller"


export function getMotorcycles() {
    return new Promise((resolve, _) => {
        fetch(HOST + ROUTES.GET_MOTORCYCLES).then(response => {
            return response.json()
        }).then(data => {
            resolve(data.items);
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

export function uploadImage(image) {
    return post(HOST + ROUTES.UPLOAD_IMAGE, {}, image);
}