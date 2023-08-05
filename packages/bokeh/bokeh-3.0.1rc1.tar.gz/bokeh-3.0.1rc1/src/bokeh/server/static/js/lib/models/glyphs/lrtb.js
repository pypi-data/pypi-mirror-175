var _a;
import { LineVector, FillVector, HatchVector } from "../../core/property_mixins";
import { Glyph, GlyphView } from "./glyph";
import { generic_area_vector_legend } from "./utils";
import { Selection } from "../selections/selection";
export class LRTBView extends GlyphView {
    get_anchor_point(anchor, i, _spt) {
        const left = Math.min(this.sleft[i], this.sright[i]);
        const right = Math.max(this.sright[i], this.sleft[i]);
        const top = Math.min(this.stop[i], this.sbottom[i]); // screen coordinates !!!
        const bottom = Math.max(this.sbottom[i], this.stop[i]); //
        switch (anchor) {
            case "top_left": return { x: left, y: top };
            case "top":
            case "top_center": return { x: (left + right) / 2, y: top };
            case "top_right": return { x: right, y: top };
            case "bottom_left": return { x: left, y: bottom };
            case "bottom":
            case "bottom_center": return { x: (left + right) / 2, y: bottom };
            case "bottom_right": return { x: right, y: bottom };
            case "left":
            case "center_left": return { x: left, y: (top + bottom) / 2 };
            case "center":
            case "center_center": return { x: (left + right) / 2, y: (top + bottom) / 2 };
            case "right":
            case "center_right": return { x: right, y: (top + bottom) / 2 };
        }
    }
    _index_data(index) {
        const { min, max } = Math;
        const { data_size } = this;
        for (let i = 0; i < data_size; i++) {
            const [l, r, t, b] = this._lrtb(i);
            index.add_rect(min(l, r), min(t, b), max(r, l), max(t, b));
        }
    }
    _render(ctx, indices, data) {
        const { sleft, sright, stop, sbottom } = data ?? this;
        for (const i of indices) {
            const sleft_i = sleft[i];
            const stop_i = stop[i];
            const sright_i = sright[i];
            const sbottom_i = sbottom[i];
            if (!isFinite(sleft_i + stop_i + sright_i + sbottom_i))
                continue;
            ctx.beginPath();
            ctx.rect(sleft_i, stop_i, sright_i - sleft_i, sbottom_i - stop_i);
            this.visuals.fill.apply(ctx, i);
            this.visuals.hatch.apply(ctx, i);
            this.visuals.line.apply(ctx, i);
        }
    }
    // We need to clamp the endpoints inside the viewport, because various browser canvas
    // implementations have issues drawing rects with enpoints far outside the viewport
    _clamp_viewport() {
        const hr = this.renderer.plot_view.frame.bbox.h_range;
        const vr = this.renderer.plot_view.frame.bbox.v_range;
        const n = this.stop.length;
        for (let i = 0; i < n; i++) {
            this.stop[i] = Math.max(this.stop[i], vr.start);
            this.sbottom[i] = Math.min(this.sbottom[i], vr.end);
            this.sleft[i] = Math.max(this.sleft[i], hr.start);
            this.sright[i] = Math.min(this.sright[i], hr.end);
        }
    }
    _hit_rect(geometry) {
        return this._hit_rect_against_index(geometry);
    }
    _hit_point(geometry) {
        const { sx, sy } = geometry;
        const x = this.renderer.xscale.invert(sx);
        const y = this.renderer.yscale.invert(sy);
        const indices = [...this.index.indices({ x0: x, y0: y, x1: x, y1: y })];
        return new Selection({ indices });
    }
    _hit_span(geometry) {
        const { sx, sy } = geometry;
        let indices;
        if (geometry.direction == "v") {
            const y = this.renderer.yscale.invert(sy);
            const hr = this.renderer.plot_view.frame.bbox.h_range;
            const [x0, x1] = this.renderer.xscale.r_invert(hr.start, hr.end);
            indices = [...this.index.indices({ x0, y0: y, x1, y1: y })];
        }
        else {
            const x = this.renderer.xscale.invert(sx);
            const vr = this.renderer.plot_view.frame.bbox.v_range;
            const [y0, y1] = this.renderer.yscale.r_invert(vr.start, vr.end);
            indices = [...this.index.indices({ x0: x, y0, x1: x, y1 })];
        }
        return new Selection({ indices });
    }
    draw_legend_for_index(ctx, bbox, index) {
        generic_area_vector_legend(this.visuals, ctx, bbox, index);
    }
}
LRTBView.__name__ = "LRTBView";
export class LRTB extends Glyph {
    constructor(attrs) {
        super(attrs);
    }
}
_a = LRTB;
LRTB.__name__ = "LRTB";
(() => {
    _a.mixins([LineVector, FillVector, HatchVector]);
})();
//# sourceMappingURL=lrtb.js.map