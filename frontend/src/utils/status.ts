import { ProductStatusEnum } from "@/enums/productStatusEnum";

export function statusToPolish(status: ProductStatusEnum) {
  switch (status) {
    case ProductStatusEnum.DRAFT:
      return "Szkic";
    case ProductStatusEnum.FOR_SALE:
      return "Na sprzedaż";
    case ProductStatusEnum.SOLD:
      return "Sprzedany";
    case ProductStatusEnum.DELETED:
      return "Usunięty";
  }
}
