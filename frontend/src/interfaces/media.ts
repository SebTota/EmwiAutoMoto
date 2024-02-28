import type { MediaTypeEnum } from "@/enums/mediaTypeEnum";

export interface IMedia {
  type: MediaTypeEnum;
  url: string;
  thumbnail_url: string;
  medium_thumbnail_url: string;
}
