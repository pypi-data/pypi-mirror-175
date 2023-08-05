var _a;
import { Annotation, AnnotationView } from "./annotation";
import { Title } from "./title";
import { CartesianFrame } from "../canvas/cartesian_frame";
import { LinearAxis } from "../axes";
import { Ticker } from "../tickers/ticker";
import { BasicTicker } from "../tickers";
import { TickFormatter } from "../formatters/tick_formatter";
import { BasicTickFormatter } from "../formatters";
import { LabelingPolicy, NoOverlap } from "../policies/labeling";
import { LinearScale } from "../scales";
import { Range1d } from "../ranges";
import { BaseText } from "../text/base_text";
import { Anchor, Orientation } from "../../core/enums";
import * as mixins from "../../core/property_mixins";
import { Grid } from "../../core/layout";
import { HStack, VStack, NodeLayout } from "../../core/layout/alignments";
import { BorderLayout } from "../../core/layout/border";
import { Panel } from "../../core/layout/side_panel";
import { build_view } from "../../core/build_views";
import { BBox } from "../../core/util/bbox";
import { isString, isPlainObject } from "../../core/util/types";
import { Dict } from "../../core/util/object";
const MINOR_DIM = 25;
const MAJOR_DIM_MIN_SCALAR = 0.3;
const MAJOR_DIM_MAX_SCALAR = 0.8;
export class BaseColorBarView extends AnnotationView {
    get orientation() {
        return this._orientation;
    }
    *children() {
        yield* super.children();
        yield this._axis_view;
        yield this._title_view;
    }
    initialize() {
        super.initialize();
        const { ticker, formatter } = this.model;
        this._ticker = ticker != "auto" ? ticker : this._create_ticker();
        this._formatter = formatter != "auto" ? formatter : this._create_formatter();
        this._major_range = this._create_major_range();
        this._major_scale = this._create_major_scale();
        this._minor_range = new Range1d({ start: 0, end: 1 });
        this._minor_scale = new LinearScale();
        // configure some frame, update when the layout is know
        this._frame = new CartesianFrame(this._major_scale, this._minor_scale, this._major_range, this._minor_range);
        this._axis = this._create_axis();
        this._apply_axis_properties();
        this._title = new Title();
        this._apply_title_properties();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        const self = this;
        const parent = {
            get parent() {
                return self.parent;
            },
            get root() {
                return self.root;
            },
            get frame() {
                return self._frame;
            },
            get canvas_view() {
                return self.parent.canvas_view;
            },
            request_layout() {
                self.parent.request_layout();
            },
            request_paint() {
                self.parent.request_paint(self);
            },
            request_render() {
                self.request_paint();
            },
        };
        this._axis_view = await build_view(this._axis, { parent });
        this._title_view = await build_view(this._title, { parent });
    }
    remove() {
        this._title_view.remove();
        this._axis_view.remove();
        super.remove();
    }
    _apply_axis_properties() {
        const attrs = {
            ticker: this._ticker,
            formatter: this._formatter,
            major_label_standoff: this.model.label_standoff,
            axis_line_color: null,
            major_tick_in: this.model.major_tick_in,
            major_tick_out: this.model.major_tick_out,
            minor_tick_in: this.model.minor_tick_in,
            minor_tick_out: this.model.minor_tick_out,
            major_label_overrides: this.model.major_label_overrides,
            major_label_policy: this.model.major_label_policy,
            // TODO: this needs strict typing
            ...mixins.attrs_of(this.model, "major_label_", mixins.Text, true),
            ...mixins.attrs_of(this.model, "major_tick_", mixins.Line, true),
            ...mixins.attrs_of(this.model, "minor_tick_", mixins.Line, true),
        };
        this._axis.setv(attrs);
    }
    _apply_title_properties() {
        const attrs = {
            text: this.model.title ?? "",
            standoff: this.model.title_standoff,
            // TODO: this needs strict typing
            ...mixins.attrs_of(this.model, "title_", mixins.Text, false),
        };
        this._title.setv(attrs);
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.change, () => {
            this._apply_title_properties();
            this._apply_axis_properties();
            // TODO?: this.plot_view.invalidate_layout()
        });
        this.connect(this._ticker.change, () => this.request_render());
        this.connect(this._formatter.change, () => this.request_render());
    }
    _update_frame() {
        const [x_scale, y_scale, x_range, y_range] = (() => {
            if (this.orientation == "horizontal")
                return [this._major_scale, this._minor_scale, this._major_range, this._minor_range];
            else
                return [this._minor_scale, this._major_scale, this._minor_range, this._major_range];
        })();
        this._frame.in_x_scale = x_scale;
        this._frame.in_y_scale = y_scale;
        this._frame.x_range = x_range;
        this._frame.y_range = y_range;
        this._frame.configure_scales();
    }
    update_layout() {
        const { location, width: w, height: h, padding, margin } = this.model;
        const [valign, halign] = (() => {
            if (isString(location)) {
                switch (location) {
                    case "top_left":
                        return ["start", "start"];
                    case "top":
                    case "top_center":
                        return ["start", "center"];
                    case "top_right":
                        return ["start", "end"];
                    case "bottom_left":
                        return ["end", "start"];
                    case "bottom":
                    case "bottom_center":
                        return ["end", "center"];
                    case "bottom_right":
                        return ["end", "end"];
                    case "left":
                    case "center_left":
                        return ["center", "start"];
                    case "center":
                    case "center_center":
                        return ["center", "center"];
                    case "right":
                    case "center_right":
                        return ["center", "end"];
                }
            }
            else
                return ["end", "start"]; // "bottom_left"
        })();
        const orientation = this._orientation = (() => {
            const { orientation } = this.model;
            if (orientation == "auto") {
                if (this.panel != null)
                    return this.panel.is_horizontal ? "horizontal" : "vertical";
                else {
                    if (halign == "start" || halign == "end" || ( /*halign == "center" &&*/valign == "center"))
                        return "vertical";
                    else
                        return "horizontal";
                }
            }
            else
                return orientation;
        })();
        this._update_frame();
        const center_panel = new NodeLayout();
        const top_panel = new VStack();
        const bottom_panel = new VStack();
        const left_panel = new HStack();
        const right_panel = new HStack();
        center_panel.absolute = true;
        top_panel.absolute = true;
        bottom_panel.absolute = true;
        left_panel.absolute = true;
        right_panel.absolute = true;
        center_panel.on_resize((bbox) => this._frame.set_geometry(bbox));
        const layout = new BorderLayout();
        this._inner_layout = layout;
        layout.absolute = true;
        layout.center_panel = center_panel;
        layout.top_panel = top_panel;
        layout.bottom_panel = bottom_panel;
        layout.left_panel = left_panel;
        layout.right_panel = right_panel;
        const padding_box = { left: padding, right: padding, top: padding, bottom: padding };
        const margin_box = (() => {
            if (this.panel == null) {
                if (isString(location))
                    return { left: margin, right: margin, top: margin, bottom: margin };
                else {
                    const [left, bottom] = location;
                    return { left, right: margin, top: margin, bottom };
                }
            }
            else {
                /**
                 * XXX: alignment is broken in Grid, which is used to govern positioning of a ColorBar
                 * in side panels. Earlier attempts at fixing this failed and resulted in a multitude
                 * or regressions in various places in the layout. So instead of this, let's assume that
                 * the positioning is always at "start" regardless of configuration, and fix this here
                 * by manually computing "center" and "end" alignment.
                 */
                if (isString(location)) {
                    layout.fixup_geometry = (outer, inner) => {
                        const origin = outer;
                        if (orientation == "horizontal") {
                            const { top, width, height } = outer;
                            if (halign == "end") {
                                const { right } = this.layout.bbox;
                                outer = new BBox({ right, top, width, height });
                            }
                            else if (halign == "center") {
                                const { hcenter } = this.layout.bbox;
                                outer = new BBox({ hcenter: Math.round(hcenter), top, width, height });
                            }
                        }
                        else {
                            const { left, width, height } = outer;
                            if (valign == "end") {
                                const { bottom } = this.layout.bbox;
                                outer = new BBox({ left, bottom, width, height });
                            }
                            else if (valign == "center") {
                                const { vcenter } = this.layout.bbox;
                                outer = new BBox({ left, vcenter: Math.round(vcenter), width, height });
                            }
                        }
                        if (inner != null) {
                            const dh = outer.left - origin.left;
                            const dv = outer.top - origin.top;
                            const { left, top, width, height } = inner;
                            inner = new BBox({ left: left + dh, top: top + dv, width, height });
                        }
                        return [outer, inner];
                    };
                    return undefined;
                }
                else {
                    const [left, bottom] = location;
                    layout.fixup_geometry = (outer, inner) => {
                        const origin = outer;
                        const grid = this.layout.bbox;
                        const { width, height } = outer;
                        outer = new BBox({ left: grid.left + left, bottom: grid.bottom - bottom, width, height });
                        if (inner != null) {
                            const dh = outer.left - origin.left;
                            const dv = outer.top - origin.top;
                            const { left, top, width, height } = inner;
                            inner = new BBox({ left: left + dh, top: top + dv, width, height });
                        }
                        return [outer, inner];
                    };
                    return { left, right: 0, top: 0, bottom };
                }
            }
        })();
        layout.padding = padding_box;
        let major_policy;
        let major_size;
        let min_major_size;
        let max_major_size;
        if (this.panel != null) {
            major_policy = "max";
            major_size = undefined;
            min_major_size = undefined;
            max_major_size = undefined;
        }
        else {
            if ((orientation == "horizontal" ? w : h) == "auto") {
                major_policy = "fixed";
                const major_size_factor = this._get_major_size_factor();
                if (major_size_factor != null)
                    major_size = major_size_factor * MINOR_DIM;
                min_major_size = { percent: MAJOR_DIM_MIN_SCALAR };
                max_major_size = { percent: MAJOR_DIM_MAX_SCALAR };
            }
            else {
                major_policy = "fit";
                major_size = undefined;
            }
        }
        if (orientation == "horizontal") {
            const width = w == "auto" ? undefined : w;
            const height = h == "auto" ? MINOR_DIM : h;
            layout.set_sizing({
                width_policy: major_policy, height_policy: "min",
                width: major_size, min_width: min_major_size, max_width: max_major_size,
                halign, valign, margin: margin_box,
            });
            layout.center_panel.set_sizing({ width_policy: w == "auto" ? "fit" : "fixed", height_policy: "fixed", width, height });
        }
        else {
            const width = w == "auto" ? MINOR_DIM : w;
            const height = h == "auto" ? undefined : h;
            layout.set_sizing({
                width_policy: "min", height_policy: major_policy,
                height: major_size, min_height: min_major_size, max_height: max_major_size,
                halign, valign, margin: margin_box,
            });
            layout.center_panel.set_sizing({ width_policy: "fixed", height_policy: h == "auto" ? "fit" : "fixed", width, height });
        }
        top_panel.set_sizing({ width_policy: "fit", height_policy: "min" });
        bottom_panel.set_sizing({ width_policy: "fit", height_policy: "min" });
        left_panel.set_sizing({ width_policy: "min", height_policy: "fit" });
        right_panel.set_sizing({ width_policy: "min", height_policy: "fit" });
        const { _title_view } = this;
        if (orientation == "horizontal") {
            _title_view.panel = new Panel("above");
            _title_view.update_layout();
            top_panel.children.push(_title_view.layout);
        }
        else {
            _title_view.panel = new Panel("left");
            _title_view.update_layout();
            left_panel.children.push(_title_view.layout);
        }
        const { panel } = this;
        const side = (() => {
            if (panel != null && orientation == panel.orientation)
                return panel.side;
            else
                return orientation == "horizontal" ? "below" : "right";
        })();
        const stack = (() => {
            switch (side) {
                case "above":
                    return top_panel;
                case "below":
                    return bottom_panel;
                case "left":
                    return left_panel;
                case "right":
                    return right_panel;
            }
        })();
        const { _axis_view } = this;
        _axis_view.panel = new Panel(side);
        _axis_view.update_layout();
        stack.children.push(_axis_view.layout);
        if (this.panel != null) {
            const outer = new Grid([{ layout, row: 0, col: 0 }]);
            outer.absolute = true;
            if (orientation == "horizontal") {
                outer.set_sizing({ width_policy: "max", height_policy: "min" });
            }
            else {
                outer.set_sizing({ width_policy: "min", height_policy: "max" });
            }
            this.layout = outer;
        }
        else {
            this.layout = this._inner_layout;
        }
        const { visible } = this.model;
        this.layout.sizing.visible = visible;
    }
    _create_axis() {
        return new LinearAxis();
    }
    _create_formatter() {
        return new BasicTickFormatter();
    }
    _create_major_range() {
        return new Range1d({ start: 0, end: 1 });
    }
    _create_major_scale() {
        return new LinearScale();
    }
    _create_ticker() {
        return new BasicTicker();
    }
    _get_major_size_factor() {
        return null;
    }
    _render() {
        const { ctx } = this.layer;
        ctx.save();
        this._paint_bbox(ctx, this._inner_layout.bbox);
        this._paint_colors(ctx, this._inner_layout.center_panel.bbox);
        this._title_view.render();
        this._axis_view.render();
        ctx.restore();
    }
    _paint_bbox(ctx, bbox) {
        const { x, y } = bbox;
        let { width, height } = bbox;
        // XXX: shrink outline region by 1px to make right and bottom lines visible
        // if they are on the edge of the canvas.
        if (x + width >= this.parent.canvas_view.bbox.width) {
            width -= 1;
        }
        if (y + height >= this.parent.canvas_view.bbox.height) {
            height -= 1;
        }
        ctx.save();
        if (this.visuals.background_fill.doit) {
            this.visuals.background_fill.set_value(ctx);
            ctx.fillRect(x, y, width, height);
        }
        if (this.visuals.border_line.doit) {
            this.visuals.border_line.set_value(ctx);
            ctx.strokeRect(x, y, width, height);
        }
        ctx.restore();
    }
    serializable_state() {
        const { children = [], ...state } = super.serializable_state();
        children.push(this._title_view.serializable_state());
        children.push(this._axis_view.serializable_state());
        return { ...state, children };
    }
}
BaseColorBarView.__name__ = "BaseColorBarView";
export class BaseColorBar extends Annotation {
    constructor(attrs) {
        super(attrs);
    }
}
_a = BaseColorBar;
BaseColorBar.__name__ = "BaseColorBar";
(() => {
    _a.mixins([
        ["major_label_", mixins.Text],
        ["title_", mixins.Text],
        ["major_tick_", mixins.Line],
        ["minor_tick_", mixins.Line],
        ["border_", mixins.Line],
        ["bar_", mixins.Line],
        ["background_", mixins.Fill],
    ]);
    _a.define(({ Alpha, Number, String, Tuple, Map, Or, Ref, Auto, Nullable }) => ({
        location: [Or(Anchor, Tuple(Number, Number)), "top_right"],
        orientation: [Or(Orientation, Auto), "auto"],
        title: [Nullable(String), null],
        title_standoff: [Number, 2],
        width: [Or(Number, Auto), "auto"],
        height: [Or(Number, Auto), "auto"],
        scale_alpha: [Alpha, 1.0],
        ticker: [Or(Ref(Ticker), Auto), "auto"],
        formatter: [Or(Ref(TickFormatter), Auto), "auto"],
        major_label_overrides: [Map(Or(String, Number), Or(String, Ref(BaseText))), new globalThis.Map(), {
                convert(v) {
                    return isPlainObject(v) ? new Dict(v) : v;
                },
            }],
        major_label_policy: [Ref(LabelingPolicy), () => new NoOverlap()],
        label_standoff: [Number, 5],
        margin: [Number, 30],
        padding: [Number, 10],
        major_tick_in: [Number, 5],
        major_tick_out: [Number, 0],
        minor_tick_in: [Number, 0],
        minor_tick_out: [Number, 0],
    }));
    _a.override({
        background_fill_color: "#ffffff",
        background_fill_alpha: 0.95,
        bar_line_color: null,
        border_line_color: null,
        major_label_text_font_size: "11px",
        major_tick_line_color: "#ffffff",
        minor_tick_line_color: null,
        title_text_font_size: "13px",
        title_text_font_style: "italic",
    });
})();
//# sourceMappingURL=base_color_bar.js.map