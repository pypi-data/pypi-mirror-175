import { difference } from "./util/array";
import { assert } from "./util/assert";
async function _build_view(view_cls, model, options) {
    assert(view_cls != null, "model doesn't implement a view");
    const view = new view_cls({ ...options, model });
    view.initialize();
    await view.lazy_initialize();
    return view;
}
export async function build_view(model, options = { parent: null }, cls = (model) => model.default_view) {
    const view = await _build_view(cls(model), model, options);
    view.connect_signals();
    return view;
}
export async function build_views(view_storage, models, options = { parent: null }, cls = (model) => model.default_view) {
    const to_remove = difference([...view_storage.keys()], models);
    const removed_views = [];
    for (const model of to_remove) {
        const view = view_storage.get(model);
        if (view != null) {
            view_storage.delete(model);
            removed_views.push(view);
            view.remove();
        }
    }
    const created_views = [];
    const new_models = models.filter((model) => !view_storage.has(model));
    for (const model of new_models) {
        const view = await _build_view(cls(model), model, options);
        view_storage.set(model, view);
        created_views.push(view);
    }
    for (const view of created_views)
        view.connect_signals();
    return {
        created: created_views,
        removed: removed_views,
    };
}
export function remove_views(view_storage) {
    for (const [model, view] of view_storage) {
        view.remove();
        view_storage.delete(model);
    }
}
//# sourceMappingURL=build_views.js.map