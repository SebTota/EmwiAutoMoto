import { ProductColor } from "@/enums/productColor";

export function getCssClassFromColor(color: string): string {
  switch (color.toLowerCase().trim()) {
    case ProductColor.White:
      return "bg-neutral-50";
    case ProductColor.Silver:
      return "bg-zinc-400";
    case ProductColor.Black:
      return "bg-stone-900";
    case ProductColor.Red:
      return "bg-red-600";
    case ProductColor.DarkRed:
      return "bg-red-900";
    case ProductColor.Violet:
      return "bg-violet-900";
    case ProductColor.Blue:
      return "bg-blue-900";
    case ProductColor.LightBlue:
      return "bg-blue-400";
    case ProductColor.Green:
      return "bg-green-900";
    case ProductColor.LightGreen:
      return "bg-green-300";
    case ProductColor.Yellow:
      return "bg-yellow-600";
    default:
      return "";
  }
}
