import argparse
import itertools

import cv2
import numpy as np


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SQRT2 = np.sqrt(2)

# 8-connected neighbor offsets and their Euclidean distances.
# Order: diagonals and cardinals alternated to prefer axis-aligned steps
# when accumulating arc length along the skeleton.
NEIGHBOR_OFFSETS = [
    ((-1, -1), SQRT2), ((-1, 0), 1.0), ((-1, 1), SQRT2),
    ((0,   1), 1.0),   ((1,  1), SQRT2), ((1,  0), 1.0),
    ((1,  -1), SQRT2), ((0, -1), 1.0),
]

# 3x3 kernel that counts the 8 neighbors of each pixel (center excluded).
NEIGHBOR_COUNT_KERNEL = np.array(
    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]],
    dtype=np.float32,
)

# 8-connected neighbor offsets used for label lookups (no distances needed).
OFFSETS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
             (1,   1),  (1, 0), (1,  -1), (0, -1)]


# ---------------------------------------------------------------------------
# Graph data structure
# ---------------------------------------------------------------------------

class Graph:
    """Minimal undirected graph storing node positions and edges."""

    __slots__ = ("node_positions", "edge_set")

    def __init__(self):
        self.node_positions = {}   # node_id -> (x_pixel, y_pixel)
        self.edge_set = set()      # set of (min_id, max_id) tuples

    def add_node(self, node_id, pos):
        self.node_positions[node_id] = pos

    def add_edge(self, node_a, node_b):
        if node_a != node_b:
            self.edge_set.add((min(node_a, node_b), max(node_a, node_b)))

    def number_of_nodes(self):
        return len(self.node_positions)

    def number_of_edges(self):
        return len(self.edge_set)

    def edges(self):
        return list(self.edge_set)


# ---------------------------------------------------------------------------
# Skeleton analysis
# ---------------------------------------------------------------------------

def _get_endpoints_and_junctions(skeleton):
    """
    Detect stroke endpoints and junction points in a skeleton image.

    Uses a neighbor-count convolution: a pixel with exactly 1 ink neighbor
    is an endpoint; a pixel with more than 2 ink neighbors is a junction.
    Adjacent junction candidates are deduplicated, keeping the one with the
    highest weighted neighbor count.

    Parameters
    ----------
    skeleton : np.ndarray
        Float32 array where 0.0 = skeleton pixel, 1.0 = background.

    Returns
    -------
    endpoints : list of (row, col)
    junctions : list of (row, col)  (deduplicated)
    possible_junctions : list of (row, col)  (raw, before dedup)
    """
    ink_mask = (1 - skeleton).astype(np.float32)
    neighbor_count = cv2.filter2D(
        ink_mask, ddepth=-1,
        kernel=NEIGHBOR_COUNT_KERNEL,
        borderType=cv2.BORDER_CONSTANT,
    )
    weighted_count = ink_mask * neighbor_count

    # np.nonzero is significantly faster than np.ndenumerate for sparse images.
    rows_j, cols_j = np.nonzero(weighted_count > 2)
    possible_junctions = list(zip(rows_j.tolist(), cols_j.tolist()))

    rows_e, cols_e = np.nonzero(weighted_count == 1)
    endpoints = list(zip(rows_e.tolist(), cols_e.tolist()))

    # Deduplicate adjacent junction candidates: keep the local maximum.
    junctions = []
    for point in possible_junctions:
        has_stronger_neighbor = False
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if not (dy or dx):
                    continue
                neighbor = (point[0] + dy, point[1] + dx)
                if neighbor in junctions:
                    if weighted_count[neighbor] <= weighted_count[point]:
                        junctions.remove(neighbor)
                    else:
                        has_stronger_neighbor = True
        if not has_stronger_neighbor:
            junctions.append(point)

    return endpoints, junctions, possible_junctions


def _find_path(skeleton_img, start_point, step_length):
    """
    Walk along the skeleton from start_point, sampling a keypoint every
    step_length pixels of accumulated arc length.

    Pixels are consumed (set to 1 = background) as they are visited,
    so each pixel is traversed at most once across all path-tracing calls.

    Parameters
    ----------
    skeleton_img : np.ndarray
        Mutable float32 skeleton (modified in place).
    start_point : (row, col)
    step_length : float
        Arc-length distance between successive keypoints.

    Returns
    -------
    keypoints : list of (row, col)
    skeleton_img : np.ndarray  (same array, consumed pixels set to 1)
    """
    keypoints = [start_point]
    accumulated_distance = 0.0
    current_point = start_point
    skeleton_img[current_point] = 1

    while True:
        next_point = None
        step_distance = 0.0
        for (dy, dx), dist in NEIGHBOR_OFFSETS:
            neighbor = (current_point[0] + dy, current_point[1] + dx)
            try:
                if skeleton_img[neighbor] == 0:
                    next_point = neighbor
                    step_distance = dist
                    break
            except IndexError:
                pass

        if next_point is None:
            break

        accumulated_distance += step_distance
        skeleton_img[next_point] = 1
        current_point = next_point

        if accumulated_distance >= step_length:
            keypoints.append(current_point)
            accumulated_distance = 0.0

    if current_point not in keypoints:
        keypoints.append(current_point)

    return keypoints, skeleton_img


# ---------------------------------------------------------------------------
# Path-list to graph
# ---------------------------------------------------------------------------

def skeleton_to_graph(skeleton, step_length):
    """
    Convert a skeleton image to a list of keypoint paths.

    Handles three topological cases:
      - Strokes with free endpoints (traced from each endpoint)
      - Stroke crossings / junctions (clustered and bridged)
      - Closed loops with no endpoints (circles / cursive joins)

    Parameters
    ----------
    skeleton : np.ndarray
        Float32 array where 0.0 = skeleton pixel, 1.0 = background.
    step_length : float
        Arc-length sampling interval for keypoints.

    Returns
    -------
    list of list of (row, col)
        Each inner list is an ordered sequence of keypoints for one stroke.
    """
    endpoints, junctions, possible_junctions = _get_endpoints_and_junctions(skeleton)

    # Remove junction pixels and build their label map in a single pass.
    skeleton_no_junctions = np.copy(skeleton)
    junction_pixel_map = np.zeros(skeleton.shape, dtype=np.uint8)
    for junction in possible_junctions:
        skeleton_no_junctions[junction] = 1
        junction_pixel_map[junction] = 1

    # Label each connected cluster of junction pixels.
    num_labels, junction_labels = cv2.connectedComponents(
        junction_pixel_map, connectivity=8,
    )
    num_junction_clusters = num_labels - 1

    # Compute the centroid of each junction cluster using np.nonzero.
    junction_groups = [[] for _ in range(num_junction_clusters)]
    rows_lbl, cols_lbl = np.nonzero(junction_labels)
    for row, col in zip(rows_lbl.tolist(), cols_lbl.tolist()):
        label_value = junction_labels[row, col]
        junction_groups[label_value - 1].append((row, col))

    junction_centroids = [
        tuple(int(round(sum(coords) / len(coords))) for coords in zip(*group))
        for group in junction_groups
    ]

    # For each arc endpoint, check which junction cluster it borders.
    endpoints_on_arc, _, _ = _get_endpoints_and_junctions(skeleton_no_junctions)

    nearest_junction = {}    # endpoint -> junction centroid
    ignore_endpoints = []    # endpoints between two junctions (bridge arcs)
    junction_bridge_paths = []
    endpoints_isolated = []  # endpoints not adjacent to any junction

    for point in endpoints_on_arc:
        neighbor_labels = []
        for dy, dx in OFFSETS_8:
            neighbor = (point[0] + dy, point[1] + dx)
            try:
                label_value = junction_labels[neighbor]
                if label_value:
                    neighbor_labels.append(label_value)
            except IndexError:
                pass

        if len(neighbor_labels) == 1:
            nearest_junction[point] = junction_centroids[neighbor_labels[0] - 1]
        elif len(neighbor_labels) == 2:
            ignore_endpoints.append(point)
            junction_bridge_paths.append([
                junction_centroids[neighbor_labels[0] - 1],
                junction_centroids[neighbor_labels[1] - 1],
            ])
        else:
            endpoints_isolated.append(point)

    # Sort so path tracing is deterministic (left-to-right, top-to-bottom).
    endpoints_near_junction = sorted(
        nearest_junction.keys(), key=lambda e: (e[1], e[0])
    )
    endpoints_isolated = sorted(endpoints_isolated, key=lambda e: (e[1], e[0]))

    # Use sets for O(1) membership tests in the tracing loop.
    ignore_endpoints_set = set(ignore_endpoints)
    endpoints_near_junction_set = set(endpoints_near_junction)

    working_skeleton = np.copy(skeleton_no_junctions)
    paths = []

    for endpoint in itertools.chain(endpoints_near_junction, endpoints_isolated):
        if endpoint not in ignore_endpoints_set:
            path, working_skeleton = _find_path(
                working_skeleton, endpoint, step_length
            )
            if path[0] in nearest_junction:
                path.insert(0, nearest_junction[path[0]])
            if path[-1] in nearest_junction:
                path.append(nearest_junction[path[-1]])
            paths.append(path)
        else:
            working_skeleton[endpoint] = 1

    paths.extend(junction_bridge_paths)

    # Trace any remaining ink as closed loops (e.g. letters o, e).
    num_labels, loop_labels = cv2.connectedComponents(
        np.uint8((1 - working_skeleton) > 0), connectivity=8,
    )
    # Find the leftmost (then topmost) pixel of each loop component.
    circle_start_points = [None] * (num_labels - 1)
    rows_loop, cols_loop = np.nonzero(loop_labels)
    for row, col in zip(rows_loop.tolist(), cols_loop.tolist()):
        label_value = loop_labels[row, col]
        idx = label_value - 1
        current = circle_start_points[idx]
        if current is None or col < current[1] or (col == current[1] and row < current[0]):
            circle_start_points[idx] = (row, col)

    for circle_start in circle_start_points:
        path, working_skeleton = _find_path(
            working_skeleton, circle_start, step_length
        )
        paths.append(path[:-1] + path[0:1])

    # Strip junction centroid placeholders from path interiors.
    return [
        [p for p in path if p not in endpoints_near_junction_set]
        for path in paths
    ]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def graph_to_dict(graph):
    """
    Convert a Graph to the standard dict format used by the model.

    Node coordinates are normalised to [0, 1] relative to the bounding box
    of the skeleton, with scale = max(x_span, y_span) so aspect ratio is
    preserved.  Two padding columns of zeros are appended so the node
    feature vector has shape (N, 4), matching the font-graph convention.

    Edges are stored bidirectionally: for every undirected edge (u, v) both
    (u -> v) and (v -> u) appear in edges[0] and edges[1] respectively.

    Returns
    -------
    dict with:
        'nodes' : np.ndarray, shape (N, 4), dtype float32
                  columns: [x_norm, y_norm, 0, 0]
        'edges' : np.ndarray, shape (2, 2*E), dtype int32
                  row 0 = source indices, row 1 = destination indices
    """
    num_nodes = graph.number_of_nodes()
    positions = list(graph.node_positions.values())

    x_pixels = np.array([p[0] for p in positions], dtype=np.float32)
    y_pixels = np.array([p[1] for p in positions], dtype=np.float32)

    scale = max(x_pixels.max() - x_pixels.min(), y_pixels.max() - y_pixels.min()) or 1.0
    x_norm = (x_pixels - x_pixels.min()) / scale
    y_norm = (y_pixels - y_pixels.min()) / scale

    nodes = np.stack(
        [x_norm, y_norm,
         np.zeros(num_nodes, dtype=np.float32),
         np.zeros(num_nodes, dtype=np.float32)],
        axis=1,
    )

    edge_list = graph.edges()
    if edge_list:
        edge_src = np.array([e[0] for e in edge_list], dtype=np.int32)
        edge_dst = np.array([e[1] for e in edge_list], dtype=np.int32)
        edges = np.stack(
            [np.concatenate([edge_src, edge_dst]),
             np.concatenate([edge_dst, edge_src])],
            axis=0,
        )
    else:
        edges = np.zeros((2, 0), dtype=np.int32)

    return {"nodes": nodes, "edges": edges}


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def show_results(original, binary, skeleton, graph):
    """
    Display original, binary, skeleton, and graph in four separate windows.
    Press any key to close.
    """
    height, width = original.shape
    node_positions = graph.node_positions

    graph_canvas = np.ones((height, width, 3), dtype=np.uint8) * 255
    for node_u, node_v in graph.edges():
        pt_u = (int(round(node_positions[node_u][0])),
                int(round(node_positions[node_u][1])))
        pt_v = (int(round(node_positions[node_v][0])),
                int(round(node_positions[node_v][1])))
        cv2.line(graph_canvas, pt_u, pt_v, color=(40, 40, 40), thickness=2)

    cv2.imshow("original", original)
    # cv2.imshow("binary",   binary)
    # cv2.imshow("skeleton", np.uint8(skeleton * 255))
    cv2.imshow("graph",    graph_canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="sample.png",
                        help="Path to a grayscale handwriting image")
    parser.add_argument("--step", type=float, default=5,
                        help="Keypoint spacing in pixels along the skeleton arc")
    args = parser.parse_args()

    # --- Load ---
    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found: '{args.image}'")

    # --- Sauvola binarization ---
    # Adaptively thresholds each pixel using the local mean and standard
    # deviation within a 31x31 window.  Produces 0 = ink, 255 = background.
    img_float = img.astype(np.float32)
    local_mean = cv2.boxFilter(src=img_float, ddepth=-1, ksize=(31, 31))
    mean_of_squares = cv2.boxFilter(src=img_float ** 2, ddepth=-1, ksize=(31, 31))
    local_stddev = np.sqrt(np.maximum(mean_of_squares - local_mean ** 2, 0.0))
    sauvola_threshold = local_mean * (1.0 + 0.1 * (local_stddev / 128.0 - 1.0))
    binary = np.uint8(np.where(img_float > sauvola_threshold, 255, 0))

    # --- Skeletonize ---
    # cv2.ximgproc.thinning expects 255 = ink; output is 255 = skeleton.
    # Convert to the internal convention: 0.0 = skeleton, 1.0 = background.
    ink_pixels = np.uint8((binary == 0) * 255)
    thinned = cv2.ximgproc.thinning(ink_pixels)
    skeleton = np.where(thinned == 255, 0.0, 1.0).astype(np.float32)

    # --- Extract graph ---
    paths = skeleton_to_graph(skeleton.copy(), step_length=args.step)

    # Assign a stable node ID to each unique skeleton point (col-major order).
    unique_points = sorted(
        {point for path in paths for point in path},
        key=lambda point: (point[1], point[0]),
    )
    node_id_of = {point: node_id for node_id, point in enumerate(unique_points)}

    graph = Graph()
    for node_id, (row, col) in enumerate(unique_points):
        graph.add_node(node_id, pos=(col, row))   # store as (x, y)
    for path in paths:
        for point_a, point_b in zip(path, path[1:]):
            graph.add_edge(node_id_of[point_a], node_id_of[point_b])

    print(f"  Nodes: {graph.number_of_nodes()},  Edges: {graph.number_of_edges()}")

    # --- Format output ---
    graph_dict = graph_to_dict(graph)
    print(f"  nodes array: {graph_dict['nodes'].shape}  {graph_dict['nodes'].dtype}")
    print(f"  edges array: {graph_dict['edges'].shape}  {graph_dict['edges'].dtype}")

    # --- Visualise ---
    show_results(img, binary, skeleton, graph)


if __name__ == "__main__":
    main()
