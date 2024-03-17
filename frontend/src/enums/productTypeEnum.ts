export enum ProductTypeEnum {
  MOTORCYCLE = "Motocykle",
  MOWER = "Traktory Ogrodowe",
  PART = "Części i Akcesoria",
}

export function productNameToSingular(type: ProductTypeEnum) {
  switch (type) {
    case ProductTypeEnum.MOTORCYCLE:
      return "Motocykl";
    case ProductTypeEnum.MOWER:
      return "Traktor Ogrodowy";
    case ProductTypeEnum.PART:
      return "Część lub Akcesorium";
  }
}
