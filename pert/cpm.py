"""
    Program to calculate the critical path of a project using the CPM method.
"""
def calculate_earliest_times(_nodes, _edges):
    """Forward pass: calculate the earliest times (ET)"""
    for e in _edges:
        dest_node = e[1]
        # Find all edges leading to this destination and get max time
        candidates = [_nodes[e[0]-1][1] + e[2] for e in _edges if e[1] == dest_node]
        _nodes[dest_node-1][1] = max(candidates)
    return _nodes

def calculate_latest_times(_nodes, _edges):
    """Backward pass: calculate the latest times (LT)"""
    for e in reversed(_edges):
        src_node = e[0]
        # Find all edges starting from this node and get min time
        candidates = [_nodes[e[1]-1][2] - e[2] for e in _edges if e[0] == src_node]
        _nodes[src_node-1][2] = min(candidates)
    return _nodes

def find_critical_path(_nodes):
    """Find nodes where ET equals LT (critical path)"""
    return [node[0] for node in _nodes if node[1] == node[2]]

if __name__ == '__main__':
    # Data structures
    # Index 0: Node ID (from 1 to 8) - identifies each milestone or event in the project network
    # Index 1: Earliest Time (ET) - initially set to 0, will be calculated during the forward pass algorithm
    # Index 2: Latest Time (LT) - initially set to 0, will be calculated during the backward pass algorithm
    nodes = [
        [1, 0, 0],
        [2, 0, 0],
        [3, 0, 0],
        [4, 0, 0],
        [5, 0, 0],
        [6, 0, 0],
        [7, 0, 0],
        [8, 0, 0],
    ]

    # Index 0: Source node ID - the starting node of an activity
    # Index 1: Destination node ID - the ending node of an activity
    # Index 2: Duration - time required to complete the activity (in consistent units)
    edges = [
        [1, 2, 12],
        [2, 3, 8],
        [2, 4, 4],
        [2, 5, 3],
        [3, 6, 12],
        [4, 6, 18],
        [4, 5, 5],
        [5, 7, 8],
        [6, 7, 4],
        [7, 8, 6],
    ]
    
    # Calculate earliest times (ET)
    nodes = calculate_earliest_times(nodes, edges)
    
    # Set latest time (LT) of last node equal to its earliest time
    nodes[-1][2] = nodes[-1][1]
    
    # Calculate latest times (LT)
    nodes = calculate_latest_times(nodes, edges)
    
    print("Data Node with ET and LT")
    print(nodes)
    
    # Find critical path
    critical_path = find_critical_path(nodes)
    print("\n\nCritical Path")
    print(critical_path)
    
    # Calculate critical time
    critical_time = 0
    for i in range(len(critical_path) - 1):
        current, next_node = critical_path[i], critical_path[i + 1]
        for edge in edges:
            if edge[0] == current and edge[1] == next_node:
                critical_time += edge[2]
                break
    
    print("\n\nCritical Time")
    print(critical_time)
