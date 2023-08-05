var _a;
import { LayoutDOM, LayoutDOMView } from "./layout_dom";
import { GridAlignmentLayout } from "./alignments";
import { px } from "../../core/dom";
import { Container } from "../../core/layout/grid";
import { Enum } from "../../core/kinds";
import { enumerate } from "../../core/util/iterator";
import { isNumber, isString, isArray } from "../../core/util/types";
import * as k from "../../core/kinds";
const { max } = Math;
export const TrackAlign = Enum("start", "center", "end", "auto");
export const TrackSize = k.String;
export const TrackSizing = k.Struct({ size: k.Opt(TrackSize), align: k.Opt(TrackAlign) });
export const TrackSizingLike = k.Or(TrackSize, TrackSizing);
export const TracksSizing = k.Or(TrackSizingLike, k.Array(TrackSizingLike), k.Map(k.Int, TrackSizingLike));
export class CSSGridBoxView extends LayoutDOMView {
    connect_signals() {
        super.connect_signals();
        const { spacing } = this.model.properties;
        this.on_change(spacing, () => this.invalidate_layout());
    }
    get child_models() {
        return this._children.map(([child]) => child);
    }
    _intrinsic_display() {
        return { inner: this.model.flow_mode, outer: "grid" };
    }
    _update_layout() {
        super._update_layout();
        const styles = {};
        const [row_gap, column_gap] = (() => {
            const { spacing } = this.model;
            return isNumber(spacing) ? [spacing, spacing] : spacing;
        })();
        styles.row_gap = px(row_gap);
        styles.column_gap = px(column_gap);
        let nrows = 0;
        let ncols = 0;
        const layoutable = new Container();
        for (const [[, row, col, row_span = 1, col_span = 1], i] of enumerate(this._children)) {
            const view = this.child_views[i];
            nrows = max(nrows, row + row_span);
            ncols = max(ncols, col + col_span);
            // CSS grid is 1-based, but layout is 0-based
            const styles = {};
            styles.grid_row_start = `${row + 1}`;
            styles.grid_row_end = `span ${row_span}`;
            styles.grid_column_start = `${col + 1}`;
            styles.grid_column_end = `span ${col_span}`;
            view.style.append(":host", styles);
            if (view instanceof LayoutDOMView && view.layout != null) {
                const r0 = row;
                const c0 = col;
                const r1 = row + row_span - 1;
                const c1 = col + col_span - 1;
                layoutable.add({ r0, c0, r1, c1 }, view);
            }
        }
        const { _rows: rows, _cols: cols } = this;
        if (rows instanceof Map)
            nrows = max(nrows, ...rows.keys());
        else if (isArray(rows))
            nrows = max(nrows, rows.length);
        if (cols instanceof Map)
            ncols = max(ncols, ...cols.keys());
        else if (isArray(cols))
            ncols = max(ncols, cols.length);
        function parse_sizing(tracks, template) {
            if (tracks instanceof Map) {
                for (const [i, spec] of tracks.entries()) {
                    if (isString(spec))
                        template[i].size = spec;
                    else
                        template[i] = spec;
                }
            }
            else if (isArray(tracks)) {
                for (const [spec, i] of enumerate(tracks)) {
                    if (isString(spec))
                        template[i].size = spec;
                    else
                        template[i] = spec;
                }
            }
            else if (tracks != null) {
                for (const row of template) {
                    if (isString(tracks))
                        row.size = tracks;
                    else {
                        row.size = tracks.size;
                        row.align = tracks.align;
                    }
                }
            }
        }
        const rows_template = Array(nrows).fill(null).map(() => ({}));
        const cols_template = Array(ncols).fill(null).map(() => ({}));
        parse_sizing(rows, rows_template);
        parse_sizing(cols, cols_template);
        for (const [[, row, col], i] of enumerate(this._children)) {
            const child = this.child_views[i];
            const { halign, valign } = child.box_sizing();
            child.style.append(":host", {
                justify_self: halign ?? cols_template[col].align,
                align_self: valign ?? rows_template[row].align,
            });
        }
        const default_size = "1fr";
        styles.grid_template_rows = rows_template.map(({ size }) => size ?? default_size).join(" ");
        styles.grid_template_columns = cols_template.map(({ size }) => size ?? default_size).join(" ");
        this.style.append(":host", styles);
        if (layoutable.size != 0) {
            this.layout = new GridAlignmentLayout(layoutable);
            this.layout.set_sizing();
        }
        else {
            delete this.layout;
        }
    }
}
CSSGridBoxView.__name__ = "CSSGridBoxView";
export class CSSGridBox extends LayoutDOM {
    constructor(attrs) {
        super(attrs);
    }
}
_a = CSSGridBox;
CSSGridBox.__name__ = "CSSGridBox";
(() => {
    _a.define(({ Number, Tuple, Or }) => ({
        spacing: [Or(Number, Tuple(Number, Number)), 0],
    }));
})();
//# sourceMappingURL=css_grid_box.js.map