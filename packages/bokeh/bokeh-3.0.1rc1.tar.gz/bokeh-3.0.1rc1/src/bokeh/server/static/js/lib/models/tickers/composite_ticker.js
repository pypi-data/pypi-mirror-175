var _a;
import { ContinuousTicker } from "./continuous_ticker";
import { argmin, sorted_index, is_empty } from "../../core/util/array";
export class CompositeTicker extends ContinuousTicker {
    constructor(attrs) {
        super(attrs);
    }
    // The tickers should be in order of increasing interval size; specifically,
    // if S comes before T, then it should be the case that
    // S.get_max_interval() < T.get_min_interval().
    // FIXME Enforce this automatically.
    get min_intervals() {
        return this.tickers.map((ticker) => ticker.get_min_interval());
    }
    get max_intervals() {
        return this.tickers.map((ticker) => ticker.get_max_interval());
    }
    get_min_interval() {
        return this.min_intervals[0];
    }
    get_max_interval() {
        return this.max_intervals[0];
    }
    get_best_ticker(data_low, data_high, desired_n_ticks) {
        const data_range = data_high - data_low;
        const ideal_interval = this.get_ideal_interval(data_low, data_high, desired_n_ticks);
        const ticker_ndxs = [
            sorted_index(this.min_intervals, ideal_interval) - 1,
            sorted_index(this.max_intervals, ideal_interval),
        ];
        const intervals = [
            this.min_intervals[ticker_ndxs[0]],
            this.max_intervals[ticker_ndxs[1]],
        ];
        const errors = intervals.map((interval) => {
            return Math.abs(desired_n_ticks - (data_range / interval));
        });
        let best_ticker;
        if (is_empty(errors.filter((e) => !isNaN(e)))) {
            // this can happen if the data isn't loaded yet, we just default to the first scale
            best_ticker = this.tickers[0];
        }
        else {
            const best_index = argmin(errors);
            const best_ticker_ndx = ticker_ndxs[best_index];
            best_ticker = this.tickers[best_ticker_ndx];
        }
        return best_ticker;
    }
    get_interval(data_low, data_high, desired_n_ticks) {
        const best_ticker = this.get_best_ticker(data_low, data_high, desired_n_ticks);
        return best_ticker.get_interval(data_low, data_high, desired_n_ticks);
    }
    get_ticks_no_defaults(data_low, data_high, cross_loc, desired_n_ticks) {
        const best_ticker = this.get_best_ticker(data_low, data_high, desired_n_ticks);
        return best_ticker.get_ticks_no_defaults(data_low, data_high, cross_loc, desired_n_ticks);
    }
}
_a = CompositeTicker;
CompositeTicker.__name__ = "CompositeTicker";
(() => {
    _a.define(({ Array, Ref }) => ({
        tickers: [Array(Ref(ContinuousTicker)), []],
    }));
})();
//# sourceMappingURL=composite_ticker.js.map