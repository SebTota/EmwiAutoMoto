import type { IMedia } from "@/interfaces/media";
import { ProductStatusEnum } from "@/enums/productStatusEnum";

export interface IProduct {
  id: string;
  date_created: Date;
  date_last_updated: Date;
  title: string;
  subtitle: string;
  price: number | null;
  description: string;
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

export const ProductSchema = [
  {
    name: "title",
    title: "Tytuł",
    fieldType: "text",
    required: true,
  },
  {
    name: "subtitle",
    title: "Podtytuł",
    fieldType: "text",
    required: true,
  },
  {
    name: "price",
    title: "Cena (zł)",
    fieldType: "number",
    required: false,
  },
  {
    name: "description",
    title: "Opis",
    fieldType: "textarea",
    required: true,
  },
  {
    name: "status",
    title: "Status",
    fieldType: "select",
    required: true,
    options: [
      { value: ProductStatusEnum.FOR_SALE, label: ProductStatusEnum.FOR_SALE },
      { value: ProductStatusEnum.RESERVED, label: ProductStatusEnum.RESERVED },
      { value: ProductStatusEnum.SOLD, label: ProductStatusEnum.SOLD },
      { value: ProductStatusEnum.DRAFT, label: ProductStatusEnum.DRAFT },
      { value: ProductStatusEnum.DELETED, label: ProductStatusEnum.DELETED },
    ],
  },
];
