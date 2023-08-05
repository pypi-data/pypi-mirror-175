var _a;
import { SelectTool, SelectToolView } from "./select_tool";
import { BoxAnnotation } from "../../annotations/box_annotation";
import { Dimensions, BoxOrigin } from "../../../core/enums";
import * as icons from "../../../styles/icons.css";
export class BoxSelectToolView extends SelectToolView {
    get overlays() {
        return [...super.overlays, this.model.overlay];
    }
    _compute_limits(curpoint) {
        const frame = this.plot_view.frame;
        const dims = this.model.dimensions;
        let base_point = this._base_point;
        if (this.model.origin == "center") {
            const [cx, cy] = base_point;
            const [dx, dy] = curpoint;
            base_point = [cx - (dx - cx), cy - (dy - cy)];
        }
        return this.model._get_dim_limits(base_point, curpoint, frame, dims);
    }
    _pan_start(ev) {
        const { sx, sy } = ev;
        if (this.plot_view.frame.bbox.contains(sx, sy))
            this._base_point = [sx, sy];
    }
    _pan(ev) {
        if (this._base_point == null)
            return;
        const { sx, sy } = ev;
        const [sxlim, sylim] = this._compute_limits([sx, sy]);
        const [[left, right], [top, bottom]] = [sxlim, sylim];
        this.model.overlay.update({ left, right, top, bottom });
        if (this.model.select_every_mousemove) {
            this._do_select(sxlim, sylim, false, this._select_mode(ev));
        }
    }
    _pan_end(ev) {
        if (this._base_point == null)
            return;
        const { sx, sy } = ev;
        const [sxlim, sylim] = this._compute_limits([sx, sy]);
        this._do_select(sxlim, sylim, true, this._select_mode(ev));
        this.model.overlay.clear();
        this._base_point = null;
        this.plot_view.state.push("box_select", { selection: this.plot_view.get_selection() });
    }
    _do_select([sx0, sx1], [sy0, sy1], final, mode = "replace") {
        const geometry = { type: "rect", sx0, sx1, sy0, sy1 };
        this._select(geometry, final, mode);
    }
}
BoxSelectToolView.__name__ = "BoxSelectToolView";
const DEFAULT_BOX_OVERLAY = () => {
    return new BoxAnnotation({
        level: "overlay",
        visible: false,
        top_units: "canvas",
        left_units: "canvas",
        bottom_units: "canvas",
        right_units: "canvas",
        fill_color: "lightgrey",
        fill_alpha: 0.5,
        line_color: "black",
        line_alpha: 1.0,
        line_width: 2,
        line_dash: [4, 4],
    });
};
export class BoxSelectTool extends SelectTool {
    constructor(attrs) {
        super(attrs);
        this.tool_name = "Box Select";
        this.event_type = "pan";
        this.default_order = 30;
    }
    get computed_icon() {
        const icon = super.computed_icon;
        if (icon != null)
            return icon;
        else {
            switch (this.dimensions) {
                case "both": return `.${icons.tool_icon_box_select}`;
                case "width": return `.${icons.tool_icon_x_box_select}`;
                case "height": return `.${icons.tool_icon_y_box_select}`;
            }
        }
    }
    get tooltip() {
        return this._get_dim_tooltip(this.dimensions);
    }
}
_a = BoxSelectTool;
BoxSelectTool.__name__ = "BoxSelectTool";
(() => {
    _a.prototype.default_view = BoxSelectToolView;
    _a.define(({ Boolean, Ref }) => ({
        dimensions: [Dimensions, "both"],
        select_every_mousemove: [Boolean, false],
        overlay: [Ref(BoxAnnotation), DEFAULT_BOX_OVERLAY],
        origin: [BoxOrigin, "corner"],
    }));
    _a.register_alias("box_select", () => new BoxSelectTool());
    _a.register_alias("xbox_select", () => new BoxSelectTool({ dimensions: "width" }));
    _a.register_alias("ybox_select", () => new BoxSelectTool({ dimensions: "height" }));
})();
//# sourceMappingURL=box_select_tool.js.map