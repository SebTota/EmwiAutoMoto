import type { IMedia } from "@/interfaces/media";
import type { ProductStatusEnum } from "@/enums/productStatusEnum";
import type { ProductTypeEnum } from "@/enums/productTypeEnum";
import type { OdometerTypeEnum } from "@/enums/odometerTypeEnum";

export interface IProduct {
  id: string;
  date_created: Date;
  date_last_updated: Date;
  type: ProductTypeEnum;
  year: number;
  make: string;
  model: string;
  vin: string | null;
  odometer: number;
  odometer_type: OdometerTypeEnum;
  color: string;
  price: number | null;
  description: string | null;
  status: ProductStatusEnum;
  thumbnail_url: string;
  medium_thumbnail_url: string;
}

export interface IProductWithContent extends IProduct {
  media: IMedia[];
}

export interface IProductCreate {
  type: ProductTypeEnum;
  year: number;
  make: string;
  model: string;
  vin: string | null;
  odometer: number;
  odometer_type: OdometerTypeEnum;
  color: string;
  price: number | null;
  description: string | null;
  status: ProductStatusEnum;
  media: IMedia[];
}

export interface IProductList {
  page: number;
  has_next_page: boolean;
  products: IProduct[];
}
