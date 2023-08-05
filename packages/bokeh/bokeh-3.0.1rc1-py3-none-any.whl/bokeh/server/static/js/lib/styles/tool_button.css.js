export const tool_icon = "bk-tool-icon"
export const disabled = "bk-disabled"
export const tool_chevron = "bk-tool-chevron"
export const above = "bk-above"
export const below = "bk-below"
export const left = "bk-left"
export const right = "bk-right"
export const active = "bk-active"
export default `:host{--button-width:30px;--button-height:30px;--button-color:lightgray;--button-border:2px;--active-tool-highlight:#26aae1;--active-tool-border:var(--button-border) solid transparent;}:host{position:relative;width:var(--button-width);height:var(--button-height);cursor:pointer;user-select:none;-webkit-user-select:none;}.bk-tool-icon{position:relative;top:calc(var(--button-border)/2);width:calc(var(--button-width) - var(--button-border));height:calc(var(--button-height) - var(--button-border));mask-size:60% 60%;mask-position:center center;mask-repeat:no-repeat;-webkit-mask-size:60% 60%;-webkit-mask-position:center center;-webkit-mask-repeat:no-repeat;background-size:60% 60%;background-origin:border-box;background-position:center center;background-repeat:no-repeat;}:host(.bk-disabled) .bk-tool-icon{background-color:var(--bokeh-icon-color-disabled);cursor:not-allowed;}.bk-tool-chevron{position:absolute;visibility:hidden;width:8px;height:8px;mask-size:100% 100%;mask-position:center center;mask-repeat:no-repeat;-webkit-mask-size:100% 100%;-webkit-mask-position:center center;-webkit-mask-repeat:no-repeat;}:host(:hover) .bk-tool-chevron{visibility:visible;}:host(.bk-above) .bk-tool-chevron{right:0;bottom:0;background-color:var(--bokeh-icon-color);mask-image:var(--bokeh-icon-chevron-down);-webkit-mask-image:var(--bokeh-icon-chevron-down);}:host(.bk-below) .bk-tool-chevron{right:0;top:0;background-color:var(--bokeh-icon-color);mask-image:var(--bokeh-icon-chevron-up);-webkit-mask-image:var(--bokeh-icon-chevron-up);}:host(.bk-left) .bk-tool-chevron{right:0;bottom:0;background-color:var(--bokeh-icon-color);mask-image:var(--bokeh-icon-chevron-right);-webkit-mask-image:var(--bokeh-icon-chevron-right);}:host(.bk-right) .bk-tool-chevron{left:0;bottom:0;background-color:var(--bokeh-icon-color);mask-image:var(--bokeh-icon-chevron-left);-webkit-mask-image:var(--bokeh-icon-chevron-left);}:host(:hover){background-color:rgba(192, 192, 192, 0.15);}:host(:focus),:host(:focus-visible){outline:1px dotted var(--active-tool-highlight);outline-offset:-1px;}:host::-moz-focus-inner{border:0;}:host(.bk-above){border-bottom:var(--active-tool-border);}:host(.bk-above.bk-active){border-bottom-color:var(--active-tool-highlight);}:host(.bk-below){border-top:var(--active-tool-border);}:host(.bk-below.bk-active){border-top-color:var(--active-tool-highlight);}:host(.bk-right){border-left:var(--active-tool-border);}:host(.bk-right.bk-active){border-left-color:var(--active-tool-highlight);}:host(.bk-left){border-right:var(--active-tool-border);}:host(.bk-left.bk-active){border-right-color:var(--active-tool-highlight);}`
