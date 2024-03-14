import type { IMedia } from "@/interfaces/media";
import type { ProductStatusEnum } from "@/enums/productStatusEnum";

export interface IProduct {
  id: string;
  date_created: Date;
  date_last_updated: Date;
  title: string;
  subtitle: string;
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
  title: string;
  subtitle: string;
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
