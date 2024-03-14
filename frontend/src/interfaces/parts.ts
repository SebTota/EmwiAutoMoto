import type { IProduct, IProductCreate, IProductList, IProductWithContent } from "@/interfaces/product";

export interface IPart extends IProduct {}

export interface IPartWithContent extends IProductWithContent {}

export interface IPartCreate extends IProductCreate {}

export interface IPartList extends IProductList {
  page: number;
  has_next_page: boolean;
  products: IPart[];
}
