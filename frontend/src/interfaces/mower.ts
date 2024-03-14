import type { IVehicle, IVehicleCreate, IVehicleList, IVehicleWithContent } from "@/interfaces/vehicle";

export interface IMower extends IVehicle {}

export interface IMowerWithContent extends IVehicleWithContent {}

export interface IMowerCreate extends IVehicleCreate {}

export interface IMowerList extends IVehicleList {
  page: number;
  has_next_page: boolean;
  products: IMower[];
}
