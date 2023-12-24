import type { IImage } from "@/interfaces/image";
import type { ProductStatusEnum } from "@/enums/productStatusEnum";

export interface IMotorcycle {
  id: string;
  date_created: Date;
  date_last_updated: Date;
  year: number;
  make: string;
  model: string;
  odometer_miles: number;
  color: string;
  price: number;
  description: string;
  status: ProductStatusEnum;
  thumbnail_url: string;
  medium_thumbnail_url: string;
}

export interface IMotorcycleWithImages extends IMotorcycle {
  images: IImage[];
}

export interface IMotorcycleCreate {
  year: number;
  make: string;
  model: string;
  odometer_miles: number;
  color: string;
  price: number;
  description: string;
  status: ProductStatusEnum;
  images: IImage[];
}

export interface IMotorcycleList {
  page: number;
  has_next_page: boolean;
  motorcycles: IMotorcycle[];
}
