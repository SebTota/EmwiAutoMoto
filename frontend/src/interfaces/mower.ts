import type { IVehicle, IVehicleCreate, IVehicleList, IVehicleWithContent } from "@/interfaces/vehicle";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import type { IMedia } from "@/interfaces/media";
import type { IProductWithContent } from "@/interfaces/product";
import { useMainStore } from "@/stores/state";
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import { ProductColor } from "@/enums/productColor";

export interface IMower extends IVehicle {}

export interface IMowerWithContent extends IVehicleWithContent {}

export interface IMowerCreate extends IVehicleCreate {}

export interface IMowerList extends IVehicleList {
  page: number;
  has_next_page: boolean;
  products: IMower[];
}

export const MowerSchema = [
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
    title: "Cena (zł)",
    fieldType: "number",
    required: false,
  },
  {
    name: "description",
    title: "Opis",
    fieldType: "textarea",
    required: false,
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
    title: "Przebieg (Godzin)",
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

export async function createMower(product: any): Promise<IProductWithContent> {
  const productCreate: IMowerCreate = {
    title: `${product.year} ${product.make}`,
    subtitle: product.model,
    year: product.year,
    make: product.make,
    model: product.model,
    vin: product.vin,
    odometer: product.odometer,
    color: product.color,
    price: product.price,
    description: product.description ? product.description : "",
    status: product.status,
    media: product.media,
  };
  return await useMainStore().createProduct(ProductTypeEnum.MOWER, productCreate);
}

export async function updateMower(productId: string, product: any): Promise<IProductWithContent> {
  const productCreate: IMowerCreate = {
    title: `${product.year} ${product.make}`,
    subtitle: product.model,
    year: product.year,
    make: product.make,
    model: product.model,
    vin: product.vin,
    odometer: product.odometer,
    color: product.color,
    price: product.price,
    description: product.description ? product.description : "",
    status: product.status,
    media: product.media,
  };
  return await useMainStore().updateProduct(ProductTypeEnum.MOWER, productId, productCreate);
}
