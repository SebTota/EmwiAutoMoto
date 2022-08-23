import {Motorcycle} from "../models/Motorcycle";
import { HOST, ROUTES } from './constants'


function getMotorcycles() {
    return new Promise((resolve, _) => {
        fetch(HOST + ROUTES.GET_MOTORCYCLES).then(response => {
            return response.json()
        }).then(data => {
            let motorcycles = [];
            for (let i = 0; i < data.num_items; i++) {
                motorcycles.push(new Motorcycle(data.items[i]));
            }

            resolve(motorcycles);
        })
    });
}


export default getMotorcycles;
