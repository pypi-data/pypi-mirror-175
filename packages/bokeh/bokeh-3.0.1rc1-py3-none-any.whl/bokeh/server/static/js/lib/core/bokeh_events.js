var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { serialize } from "./serialization";
import { equals } from "./util/eq";
function event(event_name) {
    return (cls) => {
        cls.prototype.event_name = event_name;
    };
}
export class BokehEvent {
    [serialize](serializer) {
        const { event_name: name, event_values } = this;
        const values = serializer.encode(event_values);
        return { type: "event", name, values };
    }
    [equals](that, cmp) {
        return this.event_name == that.event_name && cmp.eq(this.event_values, that.event_values);
    }
}
BokehEvent.__name__ = "BokehEvent";
export class ModelEvent extends BokehEvent {
    constructor() {
        super(...arguments);
        this.origin = null;
    }
    get event_values() {
        return { model: this.origin };
    }
}
ModelEvent.__name__ = "ModelEvent";
let DocumentReady = class DocumentReady extends BokehEvent {
    get event_values() {
        return {};
    }
};
DocumentReady.__name__ = "DocumentReady";
DocumentReady = __decorate([
    event("document_ready")
], DocumentReady);
export { DocumentReady };
let ButtonClick = class ButtonClick extends ModelEvent {
};
ButtonClick.__name__ = "ButtonClick";
ButtonClick = __decorate([
    event("button_click")
], ButtonClick);
export { ButtonClick };
let MenuItemClick = class MenuItemClick extends ModelEvent {
    constructor(item) {
        super();
        this.item = item;
    }
    get event_values() {
        const { item } = this;
        return { ...super.event_values, item };
    }
};
MenuItemClick.__name__ = "MenuItemClick";
MenuItemClick = __decorate([
    event("menu_item_click")
], MenuItemClick);
export { MenuItemClick };
// A UIEvent is an event originating on a canvas this includes.
// DOM events such as keystrokes as well as hammer, LOD, and range events.
export class UIEvent extends ModelEvent {
}
UIEvent.__name__ = "UIEvent";
let LODStart = class LODStart extends UIEvent {
};
LODStart.__name__ = "LODStart";
LODStart = __decorate([
    event("lodstart")
], LODStart);
export { LODStart };
let LODEnd = class LODEnd extends UIEvent {
};
LODEnd.__name__ = "LODEnd";
LODEnd = __decorate([
    event("lodend")
], LODEnd);
export { LODEnd };
let RangesUpdate = class RangesUpdate extends UIEvent {
    constructor(x0, x1, y0, y1) {
        super();
        this.x0 = x0;
        this.x1 = x1;
        this.y0 = y0;
        this.y1 = y1;
    }
    get event_values() {
        const { x0, x1, y0, y1 } = this;
        return { ...super.event_values, x0, x1, y0, y1 };
    }
};
RangesUpdate.__name__ = "RangesUpdate";
RangesUpdate = __decorate([
    event("rangesupdate")
], RangesUpdate);
export { RangesUpdate };
let SelectionGeometry = class SelectionGeometry extends UIEvent {
    constructor(geometry, final) {
        super();
        this.geometry = geometry;
        this.final = final;
    }
    get event_values() {
        const { geometry, final } = this;
        return { ...super.event_values, geometry, final };
    }
};
SelectionGeometry.__name__ = "SelectionGeometry";
SelectionGeometry = __decorate([
    event("selectiongeometry")
], SelectionGeometry);
export { SelectionGeometry };
let Reset = class Reset extends UIEvent {
};
Reset.__name__ = "Reset";
Reset = __decorate([
    event("reset")
], Reset);
export { Reset };
export class PointEvent extends UIEvent {
    constructor(sx, sy, x, y) {
        super();
        this.sx = sx;
        this.sy = sy;
        this.x = x;
        this.y = y;
    }
    get event_values() {
        const { sx, sy, x, y } = this;
        return { ...super.event_values, sx, sy, x, y };
    }
}
PointEvent.__name__ = "PointEvent";
let Pan = class Pan extends PointEvent {
    /* TODO: direction: -1 | 1 */
    constructor(sx, sy, x, y, delta_x, delta_y) {
        super(sx, sy, x, y);
        this.delta_x = delta_x;
        this.delta_y = delta_y;
    }
    get event_values() {
        const { delta_x, delta_y /*, direction*/ } = this;
        return { ...super.event_values, delta_x, delta_y /*, direction*/ };
    }
};
Pan.__name__ = "Pan";
Pan = __decorate([
    event("pan")
], Pan);
export { Pan };
let Pinch = class Pinch extends PointEvent {
    constructor(sx, sy, x, y, scale) {
        super(sx, sy, x, y);
        this.scale = scale;
    }
    get event_values() {
        const { scale } = this;
        return { ...super.event_values, scale };
    }
};
Pinch.__name__ = "Pinch";
Pinch = __decorate([
    event("pinch")
], Pinch);
export { Pinch };
let Rotate = class Rotate extends PointEvent {
    constructor(sx, sy, x, y, rotation) {
        super(sx, sy, x, y);
        this.rotation = rotation;
    }
    get event_values() {
        const { rotation } = this;
        return { ...super.event_values, rotation };
    }
};
Rotate.__name__ = "Rotate";
Rotate = __decorate([
    event("rotate")
], Rotate);
export { Rotate };
let MouseWheel = class MouseWheel extends PointEvent {
    constructor(sx, sy, x, y, delta) {
        super(sx, sy, x, y);
        this.delta = delta;
    }
    get event_values() {
        const { delta } = this;
        return { ...super.event_values, delta };
    }
};
MouseWheel.__name__ = "MouseWheel";
MouseWheel = __decorate([
    event("wheel")
], MouseWheel);
export { MouseWheel };
let MouseMove = class MouseMove extends PointEvent {
};
MouseMove.__name__ = "MouseMove";
MouseMove = __decorate([
    event("mousemove")
], MouseMove);
export { MouseMove };
let MouseEnter = class MouseEnter extends PointEvent {
};
MouseEnter.__name__ = "MouseEnter";
MouseEnter = __decorate([
    event("mouseenter")
], MouseEnter);
export { MouseEnter };
let MouseLeave = class MouseLeave extends PointEvent {
};
MouseLeave.__name__ = "MouseLeave";
MouseLeave = __decorate([
    event("mouseleave")
], MouseLeave);
export { MouseLeave };
let Tap = class Tap extends PointEvent {
};
Tap.__name__ = "Tap";
Tap = __decorate([
    event("tap")
], Tap);
export { Tap };
let DoubleTap = class DoubleTap extends PointEvent {
};
DoubleTap.__name__ = "DoubleTap";
DoubleTap = __decorate([
    event("doubletap")
], DoubleTap);
export { DoubleTap };
let Press = class Press extends PointEvent {
};
Press.__name__ = "Press";
Press = __decorate([
    event("press")
], Press);
export { Press };
let PressUp = class PressUp extends PointEvent {
};
PressUp.__name__ = "PressUp";
PressUp = __decorate([
    event("pressup")
], PressUp);
export { PressUp };
let PanStart = class PanStart extends PointEvent {
};
PanStart.__name__ = "PanStart";
PanStart = __decorate([
    event("panstart")
], PanStart);
export { PanStart };
let PanEnd = class PanEnd extends PointEvent {
};
PanEnd.__name__ = "PanEnd";
PanEnd = __decorate([
    event("panend")
], PanEnd);
export { PanEnd };
let PinchStart = class PinchStart extends PointEvent {
};
PinchStart.__name__ = "PinchStart";
PinchStart = __decorate([
    event("pinchstart")
], PinchStart);
export { PinchStart };
let PinchEnd = class PinchEnd extends PointEvent {
};
PinchEnd.__name__ = "PinchEnd";
PinchEnd = __decorate([
    event("pinchend")
], PinchEnd);
export { PinchEnd };
let RotateStart = class RotateStart extends PointEvent {
};
RotateStart.__name__ = "RotateStart";
RotateStart = __decorate([
    event("rotatestart")
], RotateStart);
export { RotateStart };
let RotateEnd = class RotateEnd extends PointEvent {
};
RotateEnd.__name__ = "RotateEnd";
RotateEnd = __decorate([
    event("rotateend")
], RotateEnd);
export { RotateEnd };
//# sourceMappingURL=bokeh_events.js.map