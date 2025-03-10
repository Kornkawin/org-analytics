"""
    Program to calculate the critical path of a project using the CPM method.
"""
def calculate_forward(_nodes, _edges):
    """Forward pass: calculate the earliest times (ET)"""
    for e in _edges:
        dest_node = e[1]
        # Find all edges leading to this destination and get max time
        candidates = [[_nodes[e[0]-1][1] + e[2], e[2]] for e in _edges if e[1] == dest_node]
        maximum = max(candidates, key=lambda x: x[0])
        # EF
        _nodes[dest_node-1][1] = maximum[0]
        # ES
        _nodes[dest_node-1][3] = _nodes[dest_node-1][1] - maximum[1]
    return _nodes[:-1]

def calculate_backward(_nodes, _edges):
    """Backward pass: calculate the latest times (LT)"""
    for e in reversed(_edges):
        src_node = e[0]
        # Find all edges starting from this node and get min time
        candidates = [_nodes[e[1]-1][2] - e[2] for e in _edges if e[0] == src_node]
        # LF
        _nodes[src_node-1][2] = min(candidates)
        # t = (EF-ES)
        t = _nodes[src_node-1][1] - _nodes[src_node-1][3]
        # LS = LF - t
        _nodes[src_node-1][4] = _nodes[src_node-1][2] - t
    for i in range(len(_nodes)-1): 
        # shift index
        _nodes[i][0] = _nodes[i][0] + 1
        _nodes[i][5] = _nodes[i+1][5]
        _nodes[i][6] = _nodes[i+1][6]
    return _nodes[:-1]

def find_critical_path(_nodes):
    """Find nodes where ET equals LT (critical path)"""
    return [node for node in _nodes if node[1] == node[2]]

def calculate_critical_time(_critical_path, _edges):
    _time = 0
    current_node = 0
    next_node = None
    for i in range(len(_critical_path)):
        for e in _edges:
            if e[0] == current_node and e[1] == _critical_path[i][0]:
                # move forward
                current_node = _critical_path[i][0]
                _time += e[2]
    return _time

def start(nodes, edges):
    # Calculate earliest times (ET)
    nodes = calculate_forward(nodes, edges)
    # Set latest time (LT) of last node equal to its earliest time
    nodes[-1][2] = nodes[-1][1]
    # Calculate latest times (LT)
    nodes = calculate_backward(nodes, edges)
    print("Data Node with ET and LT")
    print(nodes)
    # Find critical path
    critical_path = find_critical_path(nodes)
    print("Critical Path")
    print(critical_path)
    # Calculate critical time
    critical_time = calculate_critical_time(critical_path, edges)
    print("Critical Time")
    print(critical_time)
    return nodes, critical_path, critical_time


if __name__ == '__main__':
    # Graph Data structures (Nodes)
    # Index 0: Task ID - identifies each milestone or event in the project network
    # Index 1: Earliest Finish (EF) - initially set to 0, will be calculated during the forward pass algorithm
    # Index 2: Latest Finish (LF) - initially set to 0, will be calculated during the backward pass algorithm
    # Index 3: Earliest Start (ES)
    # Index 4: Latest Start (LS)
    # Index 5: Task Days
    # Index 6: Task Cost
    n = [
        [0, 0, 0, 0, 0, 0, 0],  #START
        [1, 0, 0, 0, 0, 0, 0],  #A
        [2, 0, 0, 0, 0, 0, 0],  #B
        [3, 0, 0, 0, 0, 0, 0],  #C
        [4, 0, 0, 0, 0, 0, 0],  #D
        [5, 0, 0, 0, 0, 0, 0],  #E
        [6, 0, 0, 0, 0, 0, 0],  #F
        [7, 0, 0, 0, 0, 0, 0],  #G
        [8, 0, 0, 0, 0, 0, 0],  #H
        [9, 0, 0, 0, 0, 0, 0],  #I
        [10, 0, 0, 0, 0, 0, 0], #J
        [11, 0, 0, 0, 0, 0, 0],  #END
    ]

    # Graph Data structures (Edges)
    # Index 0: Source node ID - the starting node of an activity
    # Index 1: Destination node ID - the ending node of an activity
    # Index 2: Actual Time - time required to complete the activity (in consistent units)
    e = [
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
    
    start(n, e)
