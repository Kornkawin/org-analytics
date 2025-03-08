"""
    Program to calculate the critical path of a project using the PERT method.
"""
def calculate_t(a, m, b):
    """Calculate expected time using PERT formula"""
    return (a + 4 * m + b) / 6

def calculate_variance(a, b):
    """Calculate variance using PERT formula"""
    return ((b - a) / 6) ** 2

def calculate_et(data_node, data_relation):
    """Forward pass: calculate earliest times"""
    for rel in data_relation:
        dest_node = rel[1]
        # Find all relations leading to this destination node and calculate candidates
        candidates = [data_node[r[0]-1][1] + r[5] for r in data_relation if r[1] == dest_node]
        data_node[dest_node-1][1] = max(candidates)
    return data_node

def calculate_el(data_node, data_relation):
    """Backward pass: calculate latest times"""
    for rel in reversed(data_relation):
        this_node = rel[0]
        # Find all relations starting from this node and calculate candidates
        candidates = [data_node[r[1]-1][2] - r[5] for r in data_relation if r[0] == this_node]
        data_node[this_node-1][2] = min(candidates)
    return data_node

def find_critical_path(data_node):
    """Find nodes where earliest time equals latest time (critical path)"""
    return [node[0] for node in data_node if node[1] == node[2]]


if __name__ == '__main__':
    # Constants for indexing
    # IDX_THIS_NODE: References the source node of an activity 
    # (index 0 in each relation)
    IDX_THIS_NODE = 0
    # References the destination node of an activity 
    # (index 1 in each relation)
    IDX_DEST_NODE = 1
    # References the expected time of an activity
    # (index 5 in each relation)
    IDX_TIME = 5
    # References the variance of an activity
    # (index 6 in each relation)
    IDX_VARIANCE = 6
    
    # Data
    # index 0: node ID
    # index 1: earliest time (ET), initially set 0 and updated during forward pass
    # index 2: latest time (LT), initially set 0 and updated during backward pass
    data_node = [
        [1, 0, 0],
        [2, 0, 0],
        [3, 0, 0],
        [4, 0, 0],
        [5, 0, 0],
    ]
    
    # Data relation
    # index 0: this node
    # index 1: destination node
    # index 2: optimistic time
    # index 3: most likely time
    # index 4: pessimistic time
    # index 5: expected time
    # index 6: variance
    data_relation = [
        [1, 2, 5, 8, 17, 0, 0],
        [1, 3, 7, 10, 13, 0, 0],
        [2, 3, 3, 5, 7, 0, 0],
        [2, 4, 1, 3, 5, 0, 0],
        [3, 4, 4, 6, 8, 0, 0],
        [3, 5, 3, 3, 3, 0, 0],
        [4, 5, 3, 4, 5, 0, 0],
    ]
    
    # Main execution
    # Calculate expected time and variance for each activity
    for rel in data_relation:
        rel[IDX_TIME] = calculate_t(rel[2], rel[3], rel[4])
        rel[IDX_VARIANCE] = calculate_variance(rel[2], rel[4])
    
    # Forward pass
    data_node = calculate_et(data_node, data_relation)
    
    # Set latest time of last node equal to its earliest time
    data_node[-1][2] = data_node[-1][1]
    
    # Backward pass
    data_node = calculate_el(data_node, data_relation)
    
    print("Data Node with ET and EL")
    print(data_node)
    
    # Find critical path
    critical_path = find_critical_path(data_node)
    print("\n\nCritical Path")
    print(critical_path)
    
    # Calculate critical time and total variance
    critical_time = 0
    sum_variance = 0
    
    # Find edges between consecutive critical path nodes
    for i in range(len(critical_path) - 1):
        current = critical_path[i]
        next_node = critical_path[i + 1]
        for rel in data_relation:
            if rel[IDX_THIS_NODE] == current and rel[IDX_DEST_NODE] == next_node:
                critical_time += rel[IDX_TIME]
                sum_variance += rel[IDX_VARIANCE]
                break
    
    print("\n\nCritical Time")
    print(critical_time)
    
    print("\n\nVariance")
    print(sum_variance)
