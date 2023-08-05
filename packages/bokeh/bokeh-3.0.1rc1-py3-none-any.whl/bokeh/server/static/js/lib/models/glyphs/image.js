var _a;
import { ImageBase, ImageBaseView } from "./image_base";
import { ColorMapper } from "../mappers/color_mapper";
import { LinearColorMapper } from "../mappers/linear_color_mapper";
export class ImageView extends ImageBaseView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.color_mapper.change, () => this._update_image());
    }
    _update_image() {
        // Only reset image_data if already initialized
        if (this.image_data != null) {
            this._set_data(null);
            this.renderer.request_render();
        }
    }
    _flat_img_to_buf8(img) {
        const cmap = this.model.color_mapper.rgba_mapper;
        return cmap.v_compute(img);
    }
}
ImageView.__name__ = "ImageView";
// NOTE: this needs to be redefined here, because palettes are located in bokeh-api.js bundle
const Greys9 = () => ["#000000", "#252525", "#525252", "#737373", "#969696", "#bdbdbd", "#d9d9d9", "#f0f0f0", "#ffffff"];
export class Image extends ImageBase {
    constructor(attrs) {
        super(attrs);
    }
}
_a = Image;
Image.__name__ = "Image";
(() => {
    _a.prototype.default_view = ImageView;
    _a.define(({ Ref }) => ({
        color_mapper: [Ref(ColorMapper), () => new LinearColorMapper({ palette: Greys9() })],
    }));
})();
//# sourceMappingURL=image.js.map