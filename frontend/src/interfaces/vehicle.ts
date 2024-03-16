import type { IMedia } from "@/interfaces/media";
import type { IProduct, IProductCreate, IProductList } from "@/interfaces/product";
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import { ProductColor } from '@/enums/productColor'

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

export const VehicleSchema = [
  {
    name: "make",
    title: "Marka",
    fieldType: "text",
    required: true,
  },
  {
    name: "model",
    title: "Model",
    fieldType: "text",
    required: true,
  },
  {
    name: "year",
    title: "Rok",
    fieldType: "number",
    required: true,
  },
  {
    name: "price",
    title: "Cena",
    fieldType: "number",
    required: true,
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
  {
    name: "vin",
    title: "VIN",
    fieldType: "text",
    required: false,
  },
  {
    name: "odometer",
    title: "Przebieg",
    fieldType: "number",
    required: true,
  },
  {
    name: "color",
    title: "Kolor",
    fieldType: "select",
    required: true,
    options: [
      { value: ProductColor.White, label: ProductColor.White },
      { value: ProductColor.Silver, label: ProductColor.Silver },
      { value: ProductColor.Black, label: ProductColor.Black },
      { value: ProductColor.Red, label: ProductColor.Red },
      { value: ProductColor.DarkRed, label: ProductColor.DarkRed },
      { value: ProductColor.Violet, label: ProductColor.Violet },
      { value: ProductColor.Blue, label: ProductColor.Blue },
      { value: ProductColor.LightBlue, label: ProductColor.LightBlue },
      { value: ProductColor.Green, label: ProductColor.Green },
      { value: ProductColor.LightGreen, label: ProductColor.LightGreen },
      { value: ProductColor.Yellow, label: ProductColor.Yellow },
    ],
  },
];
