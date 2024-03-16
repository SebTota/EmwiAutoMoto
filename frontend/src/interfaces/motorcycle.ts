import type { IVehicle, IVehicleCreate, IVehicleList, IVehicleWithContent } from "@/interfaces/vehicle";
import type { IProductWithContent } from "@/interfaces/product";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import type { IMedia } from "@/interfaces/media";
import { useMainStore } from "@/stores/state";

export interface IMotorcycle extends IVehicle {}

export interface IMotorcycleWithContent extends IVehicleWithContent {}

export interface IMotorcycleCreate extends IVehicleCreate {}

export interface IMotorcycleList extends IVehicleList {
  page: number;
  has_next_page: boolean;
  products: IMotorcycle[];
}

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
