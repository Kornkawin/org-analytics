""""
    main program
"""
import sqlite3
from schedule import cpm


def get_nodes_from_db(db_path, task_ids):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Query to get data from the Task table
    cursor.execute("SELECT Task_ID, Task_Normal_Days, Task_Normal_Cost FROM Task WHERE Task_ID IN " + str(tuple(task_ids)))
    tasks = cursor.fetchall()
    # Formulate the nodes structure
    result = [[0, 0, 0, 0, 0, 0, 0]]
    for task in tasks:
        result.append([task[0], 0, 0, 0, 0, task[1], task[2]])
    result.append([len(tasks)+1, 0, 0, 0, 0, 0, 0])
    # Close the connection
    conn.close()
    return result

def get_edges_from_db(db_path, task_ids, start_task_ids, terminal_task_ids):
    # create edges from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Task_ID, Activity_ID, Task_Normal_Days, Task_Normal_Cost, Prev_Activity_ID_1, Prev_Activity_ID_2, Prev_Activity_ID_3, Prev_Activity_ID_4 FROM Task WHERE Task_ID IN " + str(tuple(task_ids)))
    tasks = cursor.fetchall()
    result = []
    start_node = 0
    terminal_node = len(tasks) + 1
    for task in terminal_task_ids:
        result.append([task, terminal_node, 0])
    for task in tasks:
        if task[4] == 0:
            # start edge
            result.append([start_node, task[0], task[2]])
        else:
            # normal edge
            result.append([task[4], task[0], task[2]])
            if task[5] != 0:
                result.append([task[5], task[0], task[2]])
            if task[6] != 0:
                result.append([task[6], task[0], task[2]])
            if task[7] != 0:
                result.append([task[7], task[0], task[2]])
    conn.close()
    # sort by index 0 and 1
    result = sorted(result, key=lambda x: (x[0], x[1]))
    return result

def save_task_plan(db_path, _nodes):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the latest Plan_ID from TASK_PLAN table
    cursor.execute("SELECT MAX(Plan_ID) FROM TASK_PLAN")
    max_plan_id = cursor.fetchone()[0]
    if max_plan_id is None:
        max_plan_id = 1
    else:
        max_plan_id += 1

    # Insert data into TASK_PLAN table
    for node in _nodes:
        cursor.execute("""
            INSERT INTO TASK_PLAN (
                Plan_ID, Plan_Task_Step, Plan_Date, Plan_Task_Budget_Days, Plan_Task_Budget_Cost,
                Plan_Early_Start_Days, Plan_Early_Finish_Days, Plan_Late_Start_Days, Plan_Late_Finish_Days,
                Plan_Comment, Task_ID
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            max_plan_id, node[0], '2025-01-01', node[5], node[6],
            node[3], node[1], node[4], node[2], '', node[0]
        ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Run Scheduler")
    print("Read data from the database")
    nodes = get_nodes_from_db("project.db", [1, 2, 3, 4])
    print("NODES: ", nodes)
    edges = get_edges_from_db("project.db", [1, 2, 3, 4], [1, 2], [4])
    print("EDGES: ", edges)
    print("\nCalculate By the CPM model")
    nodes, critical_path, critical_time = cpm.start(nodes, edges)
    print("End Scheduler")
    save_task_plan("project.db", nodes)
    