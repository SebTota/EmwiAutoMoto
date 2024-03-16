import type { IVehicle, IVehicleCreate, IVehicleList, IVehicleWithContent } from "@/interfaces/vehicle";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import type { IMedia } from "@/interfaces/media";
import type { IProductWithContent } from "@/interfaces/product";
import { useMainStore } from "@/stores/state";

export interface IMower extends IVehicle {}

export interface IMowerWithContent extends IVehicleWithContent {}

export interface IMowerCreate extends IVehicleCreate {}

export interface IMowerList extends IVehicleList {
  page: number;
  has_next_page: boolean;
  products: IMower[];
}

export async function createMower(product: any, media: IMedia[]): Promise<IProductWithContent> {
  const productCreate: IMowerCreate = {
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
  return await useMainStore().createProduct(ProductTypeEnum.MOWER, productCreate);
}
