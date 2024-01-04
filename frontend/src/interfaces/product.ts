import type { IImage } from "@/interfaces/image";
import type { ProductStatusEnum } from "@/enums/productStatusEnum";

export interface IProduct {
  id: string;
  date_created: Date;
  date_last_updated: Date;
  year: number;
  make: string;
  model: string;
  vin: string | null;
  odometer_miles: number;
  color: string;
  price: number | null;
  description: string | null;
  status: ProductStatusEnum;
  thumbnail_url: string;
  medium_thumbnail_url: string;
}

export interface IProductWithImages extends IProduct {
  images: IImage[];
}

export interface IProductCreate {
  year: number;
  make: string;
  model: string;
  vin: string | null;
  odometer_miles: number;
  color: string;
  price: number | null;
  description: string | null;
  status: ProductStatusEnum;
  images: IImage[];
}

export interface IProductList {
  page: number;
  has_next_page: boolean;
  products: IProduct[];
}
