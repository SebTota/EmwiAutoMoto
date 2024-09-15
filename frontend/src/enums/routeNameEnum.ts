import { ProductTypeEnum } from "@/enums/productTypeEnum";

export enum RouteNameEnum {
  HOME = "Home",
  LOGIN = "Login",
  CONTACT = "Contact",
  MOTORCYCLE_LIST = "Motorcycle List",
  MOWER_LIST = "Mower List",
  PART_LIST = "Parts List",
  MOTORCYCLE_DETAILS = "Motorcycle Details",
  MOWER_DETAILS = "Mower Details",
  PART_DETAILS = "Parts Details",
  NEW_MOTORCYCLE = "New Motorcycle",
  NEW_MOWER = "New Mower",
  NEW_PART = "New Parts",
  EDIT_MOTORCYCLE = "Edit Motorcycle",
  EDIT_MOWER = "Edit Mower",
  EDIT_PART = "Edit Part",
  MOTORCYCLE_DETAIL_SUGGESTIONS = "Motorcycle Detail Suggestion",
}

export function getProductDetailsRouteName(type: ProductTypeEnum) {
  switch (type) {
    case ProductTypeEnum.MOTORCYCLE:
      return RouteNameEnum.MOTORCYCLE_DETAILS;
    case ProductTypeEnum.MOWER:
      return RouteNameEnum.MOWER_DETAILS;
    case ProductTypeEnum.PART:
      return RouteNameEnum.PART_DETAILS;
  }
}

export function getProductEditRouteName(type: ProductTypeEnum) {
  switch (type) {
    case ProductTypeEnum.MOTORCYCLE:
      return RouteNameEnum.EDIT_MOTORCYCLE;
    case ProductTypeEnum.MOWER:
      return RouteNameEnum.EDIT_MOWER;
    case ProductTypeEnum.PART:
      return RouteNameEnum.EDIT_PART;
  }
}

export function getProductListRouteName(type: ProductTypeEnum) {
  switch (type) {
    case ProductTypeEnum.MOTORCYCLE:
      return RouteNameEnum.MOTORCYCLE_LIST;
    case ProductTypeEnum.MOWER:
      return RouteNameEnum.MOWER_LIST;
    case ProductTypeEnum.PART:
      return RouteNameEnum.PART_LIST;
  }
}
