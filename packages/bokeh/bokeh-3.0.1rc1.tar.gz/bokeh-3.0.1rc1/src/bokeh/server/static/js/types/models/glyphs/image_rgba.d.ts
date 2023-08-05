import { ImageBase, ImageBaseView, ImageDataBase } from "./image_base";
import { Arrayable } from "../../core/types";
import * as p from "../../core/properties";
export declare type ImageRGBAData = ImageDataBase;
export interface ImageRGBAView extends ImageRGBAData {
}
export declare class ImageRGBAView extends ImageBaseView {
    model: ImageRGBA;
    visuals: ImageRGBA.Visuals;
    protected _flat_img_to_buf8(img: Arrayable<number>): Uint8ClampedArray;
}
export declare namespace ImageRGBA {
    type Attrs = p.AttrsOf<Props>;
    type Props = ImageBase.Props;
    type Visuals = ImageBase.Visuals;
}
export interface ImageRGBA extends ImageRGBA.Attrs {
}
export declare class ImageRGBA extends ImageBase {
    properties: ImageRGBA.Props;
    __view_type__: ImageRGBAView;
    constructor(attrs?: Partial<ImageRGBA.Attrs>);
}
//# sourceMappingURL=image_rgba.d.ts.map