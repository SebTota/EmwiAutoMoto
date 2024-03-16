import type { IVehicle, IVehicleCreate, IVehicleList, IVehicleWithContent } from "@/interfaces/vehicle";
import type { IProductWithContent } from "@/interfaces/product";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import type { IMedia } from "@/interfaces/media";
import { useMainStore } from "@/stores/state";
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import { ProductColor } from "@/enums/productColor";

export interface IMotorcycle extends IVehicle {}

export interface IMotorcycleWithContent extends IVehicleWithContent {}

export interface IMotorcycleCreate extends IVehicleCreate {}

export interface IMotorcycleList extends IVehicleList {
  page: number;
  has_next_page: boolean;
  products: IMotorcycle[];
}

export const MotorcycleSchema = [
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
  {
    name: "vin",
    title: "VIN",
    fieldType: "text",
    required: false,
  },
  {
    name: "odometer",
    title: "Przebieg (Mil)",
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

export async function createMotorcycle(product: any, media: IMedia[]): Promise<IProductWithContent> {
  const productCreate: IMotorcycleCreate = {
    title: `${product.year} ${product.make}`,
    subtitle: product.model,
    year: product.year,
    make: product.make,
    model: product.model,
    vin: product.vin,
    odometer: product.odometer,
    color: product.color,
    price: product.price ? product.price : null,
    description: product.description,
    status: product.status,
    media: media,
  };
  return await useMainStore().createProduct(ProductTypeEnum.MOTORCYCLE, productCreate);
}
