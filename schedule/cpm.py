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
    return _nodes[:-1]

def calculate_latest_times(_nodes, _edges):
    """Backward pass: calculate the latest times (LT)"""
    for e in reversed(_edges):
        src_node = e[0]
        # Find all edges starting from this node and get min time
        candidates = [_nodes[e[1]-1][2] - e[2] for e in _edges if e[0] == src_node]
        _nodes[src_node-1][2] = min(candidates)
    # clean data
    for n in _nodes: n[0] = n[0] + 1
    return _nodes[:-1]

def find_critical_path(_nodes):
    """Find nodes where ET equals LT (critical path)"""
    return [node[0] for node in _nodes if node[1] == node[2]]

def calculate_critical_time(_critical_path):
    _time = 0
    current_node = 0
    next_node = None
    for i in range(len(critical_path)):
        for e in edges:
            if e[0] == current_node and e[1] == critical_path[i]:
                current_node = critical_path[i]
                _time += e[2]
    return _time

if __name__ == '__main__':
    # Data structures
    # Index 0: Task ID - identifies each milestone or event in the project network
    # Index 1: Earliest Finish (EF) - initially set to 0, will be calculated during the forward pass algorithm
    # Index 2: Latest Finish (LF) - initially set to 0, will be calculated during the backward pass algorithm
    nodes = [
        [0, 0, 0],  #START
        [1, 0, 0],  #A
        [2, 0, 0],  #B
        [3, 0, 0],  #C
        [4, 0, 0],  #D
        [5, 0, 0],  #E
        [6, 0, 0],  #F
        [7, 0, 0],  #G
        [8, 0, 0],  #H
        [9, 0, 0],  #I
        [10, 0, 0], #J
        [11, 0, 0]  #END
    ]

    # Index 0: Source node ID - the starting node of an activity
    # Index 1: Destination node ID - the ending node of an activity
    # Index 2: Actual Time - time required to complete the activity (in consistent units)
    edges = [
        [0, 1, 3],      # START->A
        [0, 2, 5],      # START->B
        [1, 4, 4],
        [2, 3, 3],
        [2, 9, 5],
        [3, 4, 4],
        [3, 6, 2],
        [4, 5, 8],
        [5, 10, 3],
        [6, 7, 4],
        [6, 8, 2],
        [7, 10, 3],
        [8, 10, 3],
        [9, 11, 0],     # I->END
        [10, 11, 0],    # J->END
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
    critical_time = calculate_critical_time(critical_path)
    print("\n\nCritical Time")
    print(critical_time)
