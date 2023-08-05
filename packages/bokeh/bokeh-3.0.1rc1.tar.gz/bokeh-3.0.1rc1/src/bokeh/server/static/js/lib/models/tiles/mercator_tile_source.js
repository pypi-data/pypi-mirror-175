var _a;
import { TileSource } from "./tile_source";
import { range } from "../../core/util/array";
import { meters_extent_to_geographic } from "./tile_utils";
export class MercatorTileSource extends TileSource {
    constructor(attrs) {
        super(attrs);
    }
    initialize() {
        super.initialize();
        this._resolutions = range(this.min_zoom, this.max_zoom + 1).map((z) => this.get_resolution(z));
    }
    _computed_initial_resolution() {
        if (this.initial_resolution != null)
            return this.initial_resolution;
        else {
            // TODO testing 2015-11-17, if this codepath is used it seems
            // to use 100% cpu and wedge Chrome
            return (2 * Math.PI * 6378137) / this.tile_size;
        }
    }
    is_valid_tile(x, y, z) {
        if (!this.wrap_around) {
            if (x < 0 || x >= 2 ** z)
                return false;
        }
        if (y < 0 || y >= 2 ** z)
            return false;
        return true;
    }
    parent_by_tile_xyz(x, y, z) {
        const quadkey = this.tile_xyz_to_quadkey(x, y, z);
        const parent_quadkey = quadkey.substring(0, quadkey.length - 1);
        return this.quadkey_to_tile_xyz(parent_quadkey);
    }
    get_resolution(level) {
        return this._computed_initial_resolution() / 2 ** level;
    }
    get_resolution_by_extent(extent, height, width) {
        const x_rs = (extent[2] - extent[0]) / width;
        const y_rs = (extent[3] - extent[1]) / height;
        return [x_rs, y_rs];
    }
    get_level_by_extent(extent, height, width) {
        const x_rs = (extent[2] - extent[0]) / width;
        const y_rs = (extent[3] - extent[1]) / height;
        const resolution = Math.max(x_rs, y_rs);
        let i = 0;
        for (const r of this._resolutions) {
            if (resolution > r) {
                if (i == 0)
                    return 0;
                if (i > 0)
                    return i - 1;
            }
            i += 1;
        }
        // otherwise return the highest available resolution
        return (i - 1);
    }
    get_closest_level_by_extent(extent, height, width) {
        const x_rs = (extent[2] - extent[0]) / width;
        const y_rs = (extent[3] - extent[1]) / height;
        const resolution = Math.max(x_rs, y_rs);
        const closest = this._resolutions.reduce(function (previous, current) {
            if (Math.abs(current - resolution) < Math.abs(previous - resolution))
                return current;
            else
                return previous;
        });
        return this._resolutions.indexOf(closest);
    }
    snap_to_zoom_level(extent, height, width, level) {
        const [xmin, ymin, xmax, ymax] = extent;
        const desired_res = this._resolutions[level];
        let desired_x_delta = width * desired_res;
        let desired_y_delta = height * desired_res;
        if (!this.snap_to_zoom) {
            const xscale = (xmax - xmin) / desired_x_delta;
            const yscale = (ymax - ymin) / desired_y_delta;
            if (xscale > yscale) {
                desired_x_delta = (xmax - xmin);
                desired_y_delta = desired_y_delta * xscale;
            }
            else {
                desired_x_delta = desired_x_delta * yscale;
                desired_y_delta = (ymax - ymin);
            }
        }
        const x_adjust = (desired_x_delta - (xmax - xmin)) / 2;
        const y_adjust = (desired_y_delta - (ymax - ymin)) / 2;
        return [xmin - x_adjust, ymin - y_adjust, xmax + x_adjust, ymax + y_adjust];
    }
    tms_to_wmts(x, y, z) {
        // Note this works both ways
        return [x, 2 ** z - 1 - y, z];
    }
    wmts_to_tms(x, y, z) {
        // Note this works both ways
        return [x, 2 ** z - 1 - y, z];
    }
    pixels_to_meters(px, py, level) {
        const res = this.get_resolution(level);
        const mx = (px * res) - this.x_origin_offset;
        const my = (py * res) - this.y_origin_offset;
        return [mx, my];
    }
    meters_to_pixels(mx, my, level) {
        const res = this.get_resolution(level);
        const px = (mx + this.x_origin_offset) / res;
        const py = (my + this.y_origin_offset) / res;
        return [px, py];
    }
    pixels_to_tile(px, py) {
        let tx = Math.ceil(px / this.tile_size);
        tx = tx === 0 ? tx : tx - 1;
        const ty = Math.max(Math.ceil(py / this.tile_size) - 1, 0);
        return [tx, ty];
    }
    pixels_to_raster(px, py, level) {
        const mapSize = this.tile_size << level;
        return [px, mapSize - py];
    }
    meters_to_tile(mx, my, level) {
        const [px, py] = this.meters_to_pixels(mx, my, level);
        return this.pixels_to_tile(px, py);
    }
    get_tile_meter_bounds(tx, ty, level) {
        // expects tms styles coordinates (bottom-left origin)
        const [xmin, ymin] = this.pixels_to_meters(tx * this.tile_size, ty * this.tile_size, level);
        const [xmax, ymax] = this.pixels_to_meters((tx + 1) * this.tile_size, (ty + 1) * this.tile_size, level);
        return [xmin, ymin, xmax, ymax];
    }
    get_tile_geographic_bounds(tx, ty, level) {
        const bounds = this.get_tile_meter_bounds(tx, ty, level);
        const [minLon, minLat, maxLon, maxLat] = meters_extent_to_geographic(bounds);
        return [minLon, minLat, maxLon, maxLat];
    }
    get_tiles_by_extent(extent, level, tile_border = 1) {
        // unpack extent and convert to tile coordinates
        const [xmin, ymin, xmax, ymax] = extent;
        let [txmin, tymin] = this.meters_to_tile(xmin, ymin, level);
        let [txmax, tymax] = this.meters_to_tile(xmax, ymax, level);
        // add tiles which border
        txmin -= tile_border;
        tymin -= tile_border;
        txmax += tile_border;
        tymax += tile_border;
        const tiles = [];
        for (let ty = tymax; ty >= tymin; ty--) {
            for (let tx = txmin; tx <= txmax; tx++) {
                if (this.is_valid_tile(tx, ty, level))
                    tiles.push([tx, ty, level, this.get_tile_meter_bounds(tx, ty, level)]);
            }
        }
        this.sort_tiles_from_center(tiles, [txmin, tymin, txmax, tymax]);
        return tiles;
    }
    quadkey_to_tile_xyz(quadKey) {
        /**
         * Computes tile x, y and z values based on quadKey.
         */
        let tileX = 0;
        let tileY = 0;
        const tileZ = quadKey.length;
        for (let i = tileZ; i > 0; i--) {
            const value = quadKey.charAt(tileZ - i);
            const mask = 1 << (i - 1);
            switch (value) {
                case "0":
                    continue;
                case "1":
                    tileX |= mask;
                    break;
                case "2":
                    tileY |= mask;
                    break;
                case "3":
                    tileX |= mask;
                    tileY |= mask;
                    break;
                default:
                    throw new TypeError(`Invalid Quadkey: ${quadKey}`);
            }
        }
        return [tileX, tileY, tileZ];
    }
    tile_xyz_to_quadkey(x, y, z) {
        /*
         * Computes quadkey value based on tile x, y and z values.
         */
        let quadkey = "";
        for (let i = z; i > 0; i--) {
            const mask = 1 << (i - 1);
            let digit = 0;
            if ((x & mask) !== 0) {
                digit += 1;
            }
            if ((y & mask) !== 0) {
                digit += 2;
            }
            quadkey += digit.toString();
        }
        return quadkey;
    }
    children_by_tile_xyz(x, y, z) {
        const quadkey = this.tile_xyz_to_quadkey(x, y, z);
        const child_tile_xyz = [];
        for (let i = 0; i <= 3; i++) {
            const [x, y, z] = this.quadkey_to_tile_xyz(quadkey + i.toString());
            const b = this.get_tile_meter_bounds(x, y, z);
            child_tile_xyz.push([x, y, z, b]);
        }
        return child_tile_xyz;
    }
    get_closest_parent_by_tile_xyz(x, y, z) {
        const world_x = this.calculate_world_x_by_tile_xyz(x, y, z);
        [x, y, z] = this.normalize_xyz(x, y, z);
        let quadkey = this.tile_xyz_to_quadkey(x, y, z);
        while (quadkey.length > 0) {
            quadkey = quadkey.substring(0, quadkey.length - 1);
            [x, y, z] = this.quadkey_to_tile_xyz(quadkey);
            [x, y, z] = this.denormalize_xyz(x, y, z, world_x);
            if (this.tiles.has(this.tile_xyz_to_key(x, y, z)))
                return [x, y, z];
        }
        return [0, 0, 0];
    }
    normalize_xyz(x, y, z) {
        if (this.wrap_around) {
            const tile_count = 2 ** z;
            return [((x % tile_count) + tile_count) % tile_count, y, z];
        }
        else {
            return [x, y, z];
        }
    }
    denormalize_xyz(x, y, z, world_x) {
        return [x + (world_x * 2 ** z), y, z];
    }
    denormalize_meters(meters_x, meters_y, _level, world_x) {
        return [meters_x + (world_x * 2 * Math.PI * 6378137), meters_y];
    }
    calculate_world_x_by_tile_xyz(x, _y, z) {
        return Math.floor(x / 2 ** z);
    }
}
_a = MercatorTileSource;
MercatorTileSource.__name__ = "MercatorTileSource";
(() => {
    _a.define(({ Boolean }) => ({
        snap_to_zoom: [Boolean, false],
        wrap_around: [Boolean, true],
    }));
    _a.override({
        x_origin_offset: 20037508.34,
        y_origin_offset: 20037508.34,
        initial_resolution: 156543.03392804097,
    });
})();
//# sourceMappingURL=mercator_tile_source.js.map