import type { IProduct, IProductCreate, IProductList, IProductWithContent } from "@/interfaces/product";
import type { IMedia } from "@/interfaces/media";
import { useMainStore } from "@/stores/state";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import { ProductStatusEnum } from '@/enums/productStatusEnum'

export interface IPart extends IProduct {}

export interface IPartWithContent extends IProductWithContent {}

export interface IPartCreate extends IProductCreate {}

export interface IPartList extends IProductList {
  page: number;
  has_next_page: boolean;
  products: IPart[];
}

export const PartSchema = [
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
    required: false,
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
];

export async function createPart(product: any): Promise<IProductWithContent> {
  const productCreate: IPartCreate = {
    title: product.title,
    subtitle: product.subtitle ? product.subtitle : "",
    price: product.price ? product.price : null,
    description: product.description ? product.subtitle : "",
    status: product.status,
    media: product.media,
  };
  return await useMainStore().createProduct(ProductTypeEnum.PART, productCreate);
}

export async function updatePart(productId: string, product: any): Promise<IProductWithContent> {
  const productCreate: IPartCreate = {
    title: product.title,
    subtitle: product.subtitle ? product.subtitle : "",
    price: product.price ? product.price : null,
    description: product.description ? product.subtitle : "",
    status: product.status,
    media: product.media,
  };
  return await useMainStore().updateProduct(ProductTypeEnum.PART, productId, productCreate);
}