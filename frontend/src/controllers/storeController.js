import {Motorcycle} from "../models/Motorcycle";
import { HOST, ROUTES } from '../constants'
import { post } from "./controller"


export function getMotorcycles() {
    return new Promise((resolve, _) => {
        fetch(HOST + ROUTES.GET_MOTORCYCLES).then(response => {
            return response.json()
        }).then(data => {
            let motorcycles = [];
            for (let i = 0; i < data.items.length; i++) {
                motorcycles.push(new Motorcycle(data.items[i]));
            }
            resolve(motorcycles);
        })
    });
}


export function getMotorcycle(id) {
    return new Promise((resolve, _) => {
        fetch(HOST + ROUTES.GET_MOTORCYCLE.replace('{id}', id)).then(response => {
            return response.json()
        }).then(data => {
            resolve(new Motorcycle(data));
        })
    });
}


export function updateMotorcycle(id, changes) {
    return post(HOST + ROUTES.UPDATE_MOTORCYCLE.replace('{id}', id), changes)
}
