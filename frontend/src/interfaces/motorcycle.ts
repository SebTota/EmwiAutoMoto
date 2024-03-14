import type { IVehicle, IVehicleCreate, IVehicleList, IVehicleWithContent } from "@/interfaces/vehicle";

export interface IMotorcycle extends IVehicle {}

export interface IMotorcycleWithContent extends IVehicleWithContent {}

export interface IMotorcycleCreate extends IVehicleCreate {}

export interface IMotorcycleList extends IVehicleList {
  page: number;
  has_next_page: boolean;
  products: IMotorcycle[];
}
