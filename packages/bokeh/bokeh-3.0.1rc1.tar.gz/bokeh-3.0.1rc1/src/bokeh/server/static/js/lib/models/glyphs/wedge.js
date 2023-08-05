var _a;
import { XYGlyph, XYGlyphView } from "./xy_glyph";
import { generic_area_vector_legend } from "./utils";
import { LineVector, FillVector, HatchVector } from "../../core/property_mixins";
import { to_screen } from "../../core/types";
import { Direction } from "../../core/enums";
import * as p from "../../core/properties";
import { angle_between } from "../../core/util/math";
import { Selection } from "../selections/selection";
import { max } from "../../core/util/arrayable";
export class WedgeView extends XYGlyphView {
    _map_data() {
        if (this.model.properties.radius.units == "data")
            this.sradius = this.sdist(this.renderer.xscale, this._x, this.radius);
        else
            this.sradius = to_screen(this.radius);
        this.max_sradius = max(this.sradius);
    }
    _render(ctx, indices, data) {
        const { sx, sy, sradius, start_angle, end_angle } = data ?? this;
        const anticlock = this.model.direction == "anticlock";
        for (const i of indices) {
            const sx_i = sx[i];
            const sy_i = sy[i];
            const sradius_i = sradius[i];
            const start_angle_i = start_angle.get(i);
            const end_angle_i = end_angle.get(i);
            if (!isFinite(sx_i + sy_i + sradius_i + start_angle_i + end_angle_i))
                continue;
            ctx.beginPath();
            ctx.arc(sx_i, sy_i, sradius_i, start_angle_i, end_angle_i, anticlock);
            ctx.lineTo(sx_i, sy_i);
            ctx.closePath();
            this.visuals.fill.apply(ctx, i);
            this.visuals.hatch.apply(ctx, i);
            this.visuals.line.apply(ctx, i);
        }
    }
    _hit_point(geometry) {
        let dist, sx0, sx1, sy0, sy1;
        const { sx, sy } = geometry;
        const x = this.renderer.xscale.invert(sx);
        const y = this.renderer.yscale.invert(sy);
        // check diameter first
        sx0 = sx - this.max_sradius;
        sx1 = sx + this.max_sradius;
        const [x0, x1] = this.renderer.xscale.r_invert(sx0, sx1);
        sy0 = sy - this.max_sradius;
        sy1 = sy + this.max_sradius;
        const [y0, y1] = this.renderer.yscale.r_invert(sy0, sy1);
        const candidates = [];
        for (const i of this.index.indices({ x0, x1, y0, y1 })) {
            const r2 = this.sradius[i] ** 2;
            [sx0, sx1] = this.renderer.xscale.r_compute(x, this._x[i]);
            [sy0, sy1] = this.renderer.yscale.r_compute(y, this._y[i]);
            dist = (sx0 - sx1) ** 2 + (sy0 - sy1) ** 2;
            if (dist <= r2) {
                candidates.push(i);
            }
        }
        const anticlock = this.model.direction == "anticlock";
        const indices = [];
        for (const i of candidates) {
            // NOTE: minus the angle because JS uses non-mathy convention for angles
            const angle = Math.atan2(sy - this.sy[i], sx - this.sx[i]);
            const is_full_circle = Math.abs(this.start_angle.get(i) - this.end_angle.get(i)) >= 2 * Math.PI;
            if (is_full_circle || angle_between(-angle, -this.start_angle.get(i), -this.end_angle.get(i), anticlock)) {
                indices.push(i);
            }
        }
        return new Selection({ indices });
    }
    draw_legend_for_index(ctx, bbox, index) {
        generic_area_vector_legend(this.visuals, ctx, bbox, index);
    }
    scenterxy(i) {
        const r = this.sradius[i] / 2;
        const a = (this.start_angle.get(i) + this.end_angle.get(i)) / 2;
        const scx = this.sx[i] + r * Math.cos(a);
        const scy = this.sy[i] + r * Math.sin(a);
        return [scx, scy];
    }
}
WedgeView.__name__ = "WedgeView";
export class Wedge extends XYGlyph {
    constructor(attrs) {
        super(attrs);
    }
}
_a = Wedge;
Wedge.__name__ = "Wedge";
(() => {
    _a.prototype.default_view = WedgeView;
    _a.mixins([LineVector, FillVector, HatchVector]);
    _a.define(({}) => ({
        direction: [Direction, "anticlock"],
        radius: [p.DistanceSpec, { field: "radius" }],
        start_angle: [p.AngleSpec, { field: "start_angle" }],
        end_angle: [p.AngleSpec, { field: "end_angle" }],
    }));
})();
//# sourceMappingURL=wedge.js.map