import type { IProduct, IProductCreate, IProductList, IProductWithContent } from "@/interfaces/product";
import type { IMedia } from "@/interfaces/media";
import { useMainStore } from "@/stores/state";
import { ProductTypeEnum } from "@/enums/productTypeEnum";

export interface IPart extends IProduct {}

export interface IPartWithContent extends IProductWithContent {}

export interface IPartCreate extends IProductCreate {}

export interface IPartList extends IProductList {
  page: number;
  has_next_page: boolean;
  products: IPart[];
}

export async function createPart(product: any, media: IMedia[]): Promise<IProductWithContent> {
  const productCreate: IPartCreate = {
    title: product.title,
    subtitle: product.subtitle,
    price: product.price ? product.price : null,
    description: product.description,
    status: product.status,
    media: media,
  };
  return await useMainStore().createProduct(ProductTypeEnum.PART, productCreate);
}
