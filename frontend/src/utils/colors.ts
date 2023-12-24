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
    case MotorcycleColor.Green:
      return "bg-green-900";
    case MotorcycleColor.LightGreen:
      return "bg-green-300";
    case MotorcycleColor.Yellow:
      return "bg-yellow-600";
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
      return "Ciemnoczerwony";
    case MotorcycleColor.Violet:
      return "Fioletowy";
    case MotorcycleColor.Blue:
      return "Niebieski";
    case MotorcycleColor.LightBlue:
      return "Jasnoniebieski";
    case MotorcycleColor.Green:
      return "Zielony";
    case MotorcycleColor.LightGreen:
      return "Jasnozielony";
    case MotorcycleColor.Yellow:
      return "Żółty";
  }
}
