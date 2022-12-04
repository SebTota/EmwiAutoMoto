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
    images: IImage[] | null
}

export interface IMotorcycleList {
    page: number | null,
    has_next_page: boolean,
    motorcycles: IMotorcycle[]
}
