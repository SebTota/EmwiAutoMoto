import type { IMedia } from "@/interfaces/media";
import type { IProduct, IProductCreate, IProductList } from "@/interfaces/product";

export interface IVehicle extends IProduct {
  year: number;
  make: string;
  model: string;
  vin: string | null;
  odometer: number;
  color: string;
}

export interface IVehicleWithContent extends IVehicle {
  media: IMedia[];
}

export interface IVehicleCreate extends IProductCreate {
  year: number;
  make: string;
  model: string;
  vin: string | null;
  odometer: number;
  color: string;
}

export interface IVehicleList extends IProductList {
  page: number;
  has_next_page: boolean;
  products: IVehicle[];
}
