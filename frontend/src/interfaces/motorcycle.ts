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
    title: "Przebieg (Mil)",
    fieldType: "number",
    required: true,
  },
  {
    name: "color",
    title: "Kolor",
    fieldType: "text",
    required: true,
  },
];

export async function createMotorcycle(product: any): Promise<IProductWithContent> {
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
    description: product.description ? product.description : "",
    status: product.status,
    media: product.media,
  };
  return await useMainStore().createProduct(ProductTypeEnum.MOTORCYCLE, productCreate);
}

export async function updateMotorcycle(productId: string, product: any): Promise<IProductWithContent> {
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
    description: product.description ? product.description : "",
    status: product.status,
    media: product.media,
  };
  return await useMainStore().updateProduct(ProductTypeEnum.MOTORCYCLE, productId, productCreate);
}
