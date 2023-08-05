var _a;
import { Filter } from "./filter";
import { Indices } from "../../core/types";
import { logger } from "../../core/logging";
export class GroupFilter extends Filter {
    constructor(attrs) {
        super(attrs);
    }
    compute_indices(source) {
        const column = source.get_column(this.column_name);
        const size = source.get_length() ?? 1;
        if (column == null) {
            logger.warn(`${this}: groupby column '${this.column_name}' not found in the data source`);
            return Indices.all_set(size);
        }
        else {
            const indices = new Indices(size, 0);
            for (let i = 0; i < indices.size; i++) {
                if (column[i] === this.group)
                    indices.set(i);
            }
            return indices;
        }
    }
}
_a = GroupFilter;
GroupFilter.__name__ = "GroupFilter";
(() => {
    _a.define(({ String }) => ({
        column_name: [String],
        group: [String],
    }));
})();
//# sourceMappingURL=group_filter.js.map