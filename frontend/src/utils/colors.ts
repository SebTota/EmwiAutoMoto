import { MotorcycleColor } from "@/enums/motorcycleColor";

export function getCssClassFromColor(color: string): string {
  switch (color.toLowerCase().trim()) {
    case MotorcycleColor.White:
      return "bg-neutral-50";
    case MotorcycleColor.Silver:
      return "bg-zinc-400";
    case MotorcycleColor.Black:
      return "bg-stone-900";
    case MotorcycleColor.Red:
      return "bg-red-600";
    case MotorcycleColor.DarkRed:
      return "bg-red-900";
    case MotorcycleColor.Violet:
      return "bg-violet-900";
    case MotorcycleColor.Blue:
      return "bg-blue-900";
    case MotorcycleColor.LightBlue:
      return "bg-blue-400";
    default:
      return "";
  }
}

export function colorToPolish(color: string) {
  switch (color.toLowerCase().trim()) {
    case MotorcycleColor.White:
      return "Biały";
    case MotorcycleColor.Silver:
      return "Srebro";
    case MotorcycleColor.Black:
      return "Czarny";
    case MotorcycleColor.Red:
      return "Czerwony";
    case MotorcycleColor.DarkRed:
      return "Ciemno Czerwony";
    case MotorcycleColor.Violet:
      return "Fioletowy";
    case MotorcycleColor.Blue:
      return "Niebieski";
    case MotorcycleColor.LightBlue:
      return "Jasny Niebieski";
  }
}
