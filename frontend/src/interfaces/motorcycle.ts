import type {IImage} from "@/interfaces/image";

export interface IMotorcycle {
    id: string,
    date_created: Date,
    date_last_updated: Date,
    year: number,
    make: string,
    model: string,
    odometer: number,
    odometer_measurement: string,
    color: string,
    price: number,
    description: string,
    sold: boolean,
    status: string,
    thumbnail_url: string | null,
    medium_thumbnail_url: string | null,
    images: IImage[] | null
}

export interface IMotorcycleCreate {
    year: number,
    make: string,
    model: string,
    odometer: number,
    odometer_measurement: string,
    color: string,
    price: number,
    description: string,
    sold: boolean,
    status: string
}

export interface IMotorcycleList {
    page: number,
    has_next_page: boolean,
    total_count: number
    motorcycles: IMotorcycle[]
    count: number
}
