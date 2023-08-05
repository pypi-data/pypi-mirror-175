import { Document } from "../document";
import { logger } from "../core/logging";
import { unescape, uuid4 } from "../core/util/string";
import { entries } from "../core/util/object";
import { isString } from "../core/util/types";
import { defer } from "../core/util/defer";
import { add_document_standalone } from "./standalone";
import { add_document_from_session, _get_ws_url } from "./server";
import { _resolve_element, _resolve_root_elements } from "./dom";
export { add_document_standalone, index } from "./standalone";
export { add_document_from_session } from "./server";
export { embed_items_notebook, kernels } from "./notebook";
export async function embed_item(item, target) {
    const docs_json = {};
    const doc_id = uuid4();
    docs_json[doc_id] = item.doc;
    if (target == null)
        target = item.target_id;
    const roots = { [item.root_id]: target };
    const render_item = { roots, root_ids: [item.root_id], docid: doc_id };
    await defer();
    const [views] = await _embed_items(docs_json, [render_item]);
    return views;
}
// TODO (bev) this is currently clunky. Standalone embeds only provide
// the first two args, whereas server provide the app_app, and *may* prove and
// absolute_url as well if non-relative links are needed for resources. This function
// should probably be split in to two pieces to reflect the different usage patterns
export async function embed_items(docs_json, render_items, app_path, absolute_url) {
    await defer();
    return _embed_items(docs_json, render_items, app_path, absolute_url);
}
async function _embed_items(docs_json, render_items, app_path, absolute_url) {
    if (isString(docs_json))
        docs_json = JSON.parse(unescape(docs_json));
    const docs = {};
    for (const [docid, doc_json] of entries(docs_json)) {
        docs[docid] = Document.from_json(doc_json);
    }
    const views = [];
    for (const item of render_items) {
        const element = _resolve_element(item);
        const roots = _resolve_root_elements(item);
        if (item.docid != null) {
            views.push(await add_document_standalone(docs[item.docid], element, roots, item.use_for_title));
        }
        else if (item.token != null) {
            const websocket_url = _get_ws_url(app_path, absolute_url);
            logger.debug(`embed: computed ws url: ${websocket_url}`);
            try {
                views.push(await add_document_from_session(websocket_url, item.token, element, roots, item.use_for_title));
                console.log("Bokeh items were rendered successfully");
            }
            catch (error) {
                console.log("Error rendering Bokeh items:", error);
            }
        }
        else
            throw new Error("Error rendering Bokeh items: either 'docid' or 'token' was expected.");
    }
    return views;
}
//# sourceMappingURL=index.js.map