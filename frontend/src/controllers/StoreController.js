import {Motorcycle} from "../models/Motorcycle";
import { HOST, ROUTES } from './constants'


function getMotorcycles() {
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


function getMotorcycle(id: String) {}



export default getMotorcycles;
