import { Model } from "../../model";
import { indexOf } from "../../core/util/arrayable";
import { contains, uniq } from "../../core/util/array";
import { Selection } from "../selections/selection";
export class GraphHitTestPolicy extends Model {
    constructor(attrs) {
        super(attrs);
    }
    _hit_test(geometry, graph_view, renderer_view) {
        if (!graph_view.model.visible)
            return null;
        const hit_test_result = renderer_view.glyph.hit_test(geometry);
        if (hit_test_result == null)
            return null;
        else
            return renderer_view.model.view.convert_selection_from_subset(hit_test_result);
    }
}
GraphHitTestPolicy.__name__ = "GraphHitTestPolicy";
export class EdgesOnly extends GraphHitTestPolicy {
    constructor(attrs) {
        super(attrs);
    }
    hit_test(geometry, graph_view) {
        return this._hit_test(geometry, graph_view, graph_view.edge_view);
    }
    do_selection(hit_test_result, graph, final, mode) {
        if (hit_test_result == null)
            return false;
        const edge_selection = graph.edge_renderer.data_source.selected;
        edge_selection.update(hit_test_result, final, mode);
        graph.edge_renderer.data_source._select.emit();
        return !edge_selection.is_empty();
    }
    do_inspection(hit_test_result, geometry, graph_view, final, mode) {
        if (hit_test_result == null)
            return false;
        const { edge_renderer } = graph_view.model;
        const edge_inspection = edge_renderer.get_selection_manager().get_or_create_inspector(graph_view.edge_view.model);
        edge_inspection.update(hit_test_result, final, mode);
        // silently set inspected attr to avoid triggering data_source.change event and rerender
        graph_view.edge_view.model.data_source.setv({ inspected: edge_inspection }, { silent: true });
        graph_view.edge_view.model.data_source.inspect.emit([graph_view.edge_view.model, { geometry }]);
        return !edge_inspection.is_empty();
    }
}
EdgesOnly.__name__ = "EdgesOnly";
export class NodesOnly extends GraphHitTestPolicy {
    constructor(attrs) {
        super(attrs);
    }
    hit_test(geometry, graph_view) {
        return this._hit_test(geometry, graph_view, graph_view.node_view);
    }
    do_selection(hit_test_result, graph, final, mode) {
        if (hit_test_result == null)
            return false;
        const node_selection = graph.node_renderer.data_source.selected;
        node_selection.update(hit_test_result, final, mode);
        graph.node_renderer.data_source._select.emit();
        return !node_selection.is_empty();
    }
    do_inspection(hit_test_result, geometry, graph_view, final, mode) {
        if (hit_test_result == null)
            return false;
        const { node_renderer } = graph_view.model;
        const node_inspection = node_renderer.get_selection_manager().get_or_create_inspector(graph_view.node_view.model);
        node_inspection.update(hit_test_result, final, mode);
        // silently set inspected attr to avoid triggering data_source.change event and rerender
        graph_view.node_view.model.data_source.setv({ inspected: node_inspection }, { silent: true });
        graph_view.node_view.model.data_source.inspect.emit([graph_view.node_view.model, { geometry }]);
        return !node_inspection.is_empty();
    }
}
NodesOnly.__name__ = "NodesOnly";
export class NodesAndLinkedEdges extends GraphHitTestPolicy {
    constructor(attrs) {
        super(attrs);
    }
    hit_test(geometry, graph_view) {
        return this._hit_test(geometry, graph_view, graph_view.node_view);
    }
    get_linked_edges(node_source, edge_source, mode) {
        let node_indices = [];
        if (mode == "selection") {
            node_indices = node_source.selected.indices.map((i) => node_source.data.index[i]);
        }
        else if (mode == "inspection") {
            node_indices = node_source.inspected.indices.map((i) => node_source.data.index[i]);
        }
        const edge_indices = [];
        for (let i = 0; i < edge_source.data.start.length; i++) {
            if (contains(node_indices, edge_source.data.start[i]) || contains(node_indices, edge_source.data.end[i]))
                edge_indices.push(i);
        }
        const linked_edges = new Selection();
        for (const i of edge_indices) {
            linked_edges.multiline_indices[i] = [0]; //currently only supports 2-element multilines, so this is all of it
        }
        linked_edges.indices = edge_indices;
        return linked_edges;
    }
    do_selection(hit_test_result, graph, final, mode) {
        if (hit_test_result == null)
            return false;
        const node_selection = graph.node_renderer.data_source.selected;
        node_selection.update(hit_test_result, final, mode);
        const edge_selection = graph.edge_renderer.data_source.selected;
        const linked_edges_selection = this.get_linked_edges(graph.node_renderer.data_source, graph.edge_renderer.data_source, "selection");
        edge_selection.update(linked_edges_selection, final, mode);
        graph.node_renderer.data_source._select.emit();
        return !node_selection.is_empty();
    }
    do_inspection(hit_test_result, geometry, graph_view, final, mode) {
        if (hit_test_result == null)
            return false;
        const node_inspection = graph_view.node_view.model.data_source.selection_manager.get_or_create_inspector(graph_view.node_view.model);
        node_inspection.update(hit_test_result, final, mode);
        graph_view.node_view.model.data_source.setv({ inspected: node_inspection }, { silent: true });
        const edge_inspection = graph_view.edge_view.model.data_source.selection_manager.get_or_create_inspector(graph_view.edge_view.model);
        const linked_edges = this.get_linked_edges(graph_view.node_view.model.data_source, graph_view.edge_view.model.data_source, "inspection");
        edge_inspection.update(linked_edges, final, mode);
        //silently set inspected attr to avoid triggering data_source.change event and rerender
        graph_view.edge_view.model.data_source.setv({ inspected: edge_inspection }, { silent: true });
        graph_view.node_view.model.data_source.inspect.emit([graph_view.node_view.model, { geometry }]);
        return !node_inspection.is_empty();
    }
}
NodesAndLinkedEdges.__name__ = "NodesAndLinkedEdges";
export class EdgesAndLinkedNodes extends GraphHitTestPolicy {
    constructor(attrs) {
        super(attrs);
    }
    hit_test(geometry, graph_view) {
        return this._hit_test(geometry, graph_view, graph_view.edge_view);
    }
    get_linked_nodes(node_source, edge_source, mode) {
        let edge_indices = [];
        if (mode == "selection")
            edge_indices = edge_source.selected.indices;
        else if (mode == "inspection")
            edge_indices = edge_source.inspected.indices;
        const nodes = [];
        for (const i of edge_indices) {
            nodes.push(edge_source.data.start[i]);
            nodes.push(edge_source.data.end[i]);
        }
        const node_indices = uniq(nodes).map((i) => indexOf(node_source.data.index, i));
        return new Selection({ indices: node_indices });
    }
    do_selection(hit_test_result, graph, final, mode) {
        if (hit_test_result == null)
            return false;
        const edge_selection = graph.edge_renderer.data_source.selected;
        edge_selection.update(hit_test_result, final, mode);
        const node_selection = graph.node_renderer.data_source.selected;
        const linked_nodes = this.get_linked_nodes(graph.node_renderer.data_source, graph.edge_renderer.data_source, "selection");
        node_selection.update(linked_nodes, final, mode);
        graph.edge_renderer.data_source._select.emit();
        return !edge_selection.is_empty();
    }
    do_inspection(hit_test_result, geometry, graph_view, final, mode) {
        if (hit_test_result == null)
            return false;
        const edge_inspection = graph_view.edge_view.model.data_source.selection_manager.get_or_create_inspector(graph_view.edge_view.model);
        edge_inspection.update(hit_test_result, final, mode);
        graph_view.edge_view.model.data_source.setv({ inspected: edge_inspection }, { silent: true });
        const node_inspection = graph_view.node_view.model.data_source.selection_manager.get_or_create_inspector(graph_view.node_view.model);
        const linked_nodes = this.get_linked_nodes(graph_view.node_view.model.data_source, graph_view.edge_view.model.data_source, "inspection");
        node_inspection.update(linked_nodes, final, mode);
        // silently set inspected attr to avoid triggering data_source.change event and rerender
        graph_view.node_view.model.data_source.setv({ inspected: node_inspection }, { silent: true });
        graph_view.edge_view.model.data_source.inspect.emit([graph_view.edge_view.model, { geometry }]);
        return !edge_inspection.is_empty();
    }
}
EdgesAndLinkedNodes.__name__ = "EdgesAndLinkedNodes";
export class NodesAndAdjacentNodes extends GraphHitTestPolicy {
    constructor(attrs) {
        super(attrs);
    }
    hit_test(geometry, graph_view) {
        return this._hit_test(geometry, graph_view, graph_view.node_view);
    }
    get_adjacent_nodes(node_source, edge_source, mode) {
        let selected_node_indices = [];
        if (mode == "selection") {
            selected_node_indices = node_source.selected.indices.map((i) => node_source.data.index[i]);
        }
        else if (mode == "inspection") {
            selected_node_indices = node_source.inspected.indices.map((i) => node_source.data.index[i]);
        }
        const adjacent_nodes = [];
        const selected_nodes = [];
        for (let i = 0; i < edge_source.data.start.length; i++) {
            if (contains(selected_node_indices, edge_source.data.start[i])) {
                adjacent_nodes.push(edge_source.data.end[i]);
                selected_nodes.push(edge_source.data.start[i]);
            }
            if (contains(selected_node_indices, edge_source.data.end[i])) {
                adjacent_nodes.push(edge_source.data.start[i]);
                selected_nodes.push(edge_source.data.end[i]);
            }
        }
        for (let i = 0; i < selected_nodes.length; i++)
            adjacent_nodes.push(selected_nodes[i]);
        const adjacent_node_indices = uniq(adjacent_nodes).map((i) => indexOf(node_source.data.index, i));
        return new Selection({ indices: adjacent_node_indices });
    }
    do_selection(hit_test_result, graph, final, mode) {
        if (hit_test_result == null)
            return false;
        const node_selection = graph.node_renderer.data_source.selected;
        node_selection.update(hit_test_result, final, mode);
        const adjacent_nodes_selection = this.get_adjacent_nodes(graph.node_renderer.data_source, graph.edge_renderer.data_source, "selection");
        if (!adjacent_nodes_selection.is_empty())
            node_selection.update(adjacent_nodes_selection, final, mode);
        graph.node_renderer.data_source._select.emit();
        return !node_selection.is_empty();
    }
    do_inspection(hit_test_result, geometry, graph_view, final, mode) {
        if (hit_test_result == null)
            return false;
        const node_inspection = graph_view.node_view.model.data_source.selection_manager.get_or_create_inspector(graph_view.node_view.model);
        node_inspection.update(hit_test_result, final, mode);
        graph_view.node_view.model.data_source.setv({ inspected: node_inspection }, { silent: true });
        const adjacent_nodes_inspection = this.get_adjacent_nodes(graph_view.node_view.model.data_source, graph_view.edge_view.model.data_source, "inspection");
        if (!adjacent_nodes_inspection.is_empty()) {
            node_inspection.update(adjacent_nodes_inspection, final, mode);
            graph_view.node_view.model.data_source.setv({ inspected: node_inspection }, { silent: true });
        }
        graph_view.node_view.model.data_source.inspect.emit([graph_view.node_view.model, { geometry }]);
        return !node_inspection.is_empty();
    }
}
NodesAndAdjacentNodes.__name__ = "NodesAndAdjacentNodes";
//# sourceMappingURL=graph_hit_test_policy.js.map