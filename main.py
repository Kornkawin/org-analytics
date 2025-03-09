""""
    main program
"""
import sqlite3
from schedule import cpm
from assignment import algorithm


def get_nodes_from_db(db_path, task_ids):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Query to get data from the Task table
    cursor.execute("SELECT Task_ID, Task_Days, Task_Cost "
                   "    FROM TASK "
                   "    WHERE Task_ID IN " + str(tuple(task_ids)))
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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Task_ID, Activity_ID, Task_Days, Task_Cost, Prev_Activity_ID_1, "
                   "    Prev_Activity_ID_2, Prev_Activity_ID_3, Prev_Activity_ID_4 "
                   "    FROM TASK "
                   "    WHERE Task_ID IN " + str(tuple(task_ids)))
    tasks = cursor.fetchall()
    result = []
    start_node = 0
    terminal_node = len(tasks) + 1
    for task in terminal_task_ids:
        result.append([task, terminal_node, 0])
    for task in tasks:
        if task[4] is None:
            # start edge
            result.append([start_node, task[0], task[2]])
        else:
            # normal edge
            result.append([task[4], task[0], task[2]])
            if task[5] is not None:
                result.append([task[5], task[0], task[2]])
            if task[6] is not None:
                result.append([task[6], task[0], task[2]])
            if task[7] is not None:
                result.append([task[7], task[0], task[2]])
    conn.close()
    # sort by index 0 and 1
    result = sorted(result, key=lambda x: (x[0], x[1]))
    return result


def save_task_plan(db_path, _nodes):
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
                Plan_ID, Plan_Task_Step, Plan_Date_Launched, Plan_Task_Days, Plan_Task_Cost,
                Plan_Early_Start_Days, Plan_Early_Finish_Days, Plan_Late_Start_Days, Plan_Late_Finish_Days,
                Plan_Comment, Task_ID
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            max_plan_id, node[0], '2025-01-01', node[5], node[6],
            node[3], node[1], node[4], node[2], '', node[0]
        ))

    conn.commit()
    conn.close()
    
    
def get_tasks_from_db(db_path, task_ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Task_ID, Task_Size, Task_Language_Used, Task_Days "
                   "    FROM TASK "
                   "    WHERE Task_ID IN " + str(tuple(task_ids)))
    result = cursor.fetchall()
    conn.close()
    return result


def get_employee_skill_lvl_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Employee_ID, Skill_Java, Skill_Html_Css_Js, Skill_Test FROM EMPLOYEE")
    result = cursor.fetchall()
    conn.close()
    return result


def get_employee_cost_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Employee_ID, Wage_Per_Day FROM EMPLOYEE")
    result = cursor.fetchall()
    conn.close()
    return result


def get_day_parameters_from_db(db_path, _tasks, _employees):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT Task_Size, Task_Language_Used, Skill_Level, Expected_Days FROM ASSIGN_PARAMETER")
    result = cursor.fetchall()
    conn.close()
    
    # Formulate the parameters structure
    params = dict()
    for r in result:
        params[(r[0], r[1], r[2])] = r[3]
    result = dict()
    for task in _tasks:
        task_size: str = task[1]
        task_lang: str = task[2]
        dev_levels = dict()
        for employee in _employees:
            if task_lang.lower() == 'java':
                dev_levels[employee[0]] = employee[1]
            elif task_lang.lower() == 'html/css/js':
                dev_levels[employee[0]] = employee[2]
            elif task_lang.lower() == 'test':
                dev_levels[employee[0]] = employee[3]
            else:
                raise "Language not supported"
        dev_days = dict()
        for dev in dev_levels:
            if (task_size, task_lang, dev_levels[dev]) in params:
                dev_days[f"ID{dev}"] = params[(task_size, task_lang, dev_levels[dev])]
            else:
                dev_days[f"ID{dev}"] = float('inf')
        result[f"#{task[0]}"] = dev_days    
    return result


def save_assignment(db_path, assignment_result):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Insert data into ASSIGNMENT table
    for assignment in assignment_result:
        task_id = int(assignment[0][0][1:])
        employee_id = int(assignment[0][1][2:])
        # remove old assignment
        cursor.execute("""
            DELETE FROM ASSIGNMENT
            WHERE Task_ID = ?
        """, (task_id,))
        cursor.execute("""
            INSERT INTO ASSIGNMENT (Assignment_Date, Assignment_Days_Used, Employee_ID, Task_ID)
            VALUES (?, ?, ?, ?)
        """, ('2025-01-01', assignment[1], employee_id, task_id))
    conn.commit()
    conn.close()
    update_task(db_path, assignment_result)
    
    
def update_task(db_path, assignment_result):
    cost = get_employee_cost_from_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update data in TASK table
    for assignment in assignment_result:
        task_id = int(assignment[0][0][1:])
        employee_id = int(assignment[0][1][2:])
        cursor.execute("""
            UPDATE TASK
            SET Task_Days = ?
            WHERE Task_ID = ?
        """, (assignment[1], task_id))
        cursor.execute("""
            UPDATE TASK
            SET Task_Cost = ?
            WHERE Task_ID = ?
        """, (assignment[1] * cost[employee_id-1][1], task_id))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print("Run Assignment Algorithm")
    print("Read data from the database")
    tasks = get_tasks_from_db("project.db", [1, 2, 3, 4])
    print("Tasks: ", tasks)
    employees = get_employee_skill_lvl_from_db("project.db")
    print("Employees Skill: ", employees)
    parameters = get_day_parameters_from_db("project.db", tasks, employees)
    print("Parameters: ", parameters)
    print("\nCalculate By the Assignment Algorithm")
    solution = algorithm.find_matching(parameters, matching_type = 'min', return_type = 'list' )
    solution.sort(key=lambda x: x[0][0])
    print("Assignment Solution: ", solution)
    print("saving assignment ...")
    save_assignment("project.db", solution)

    print("Run Scheduler")
    print("Read data from the database")
    nodes = get_nodes_from_db("project.db", [1, 2, 3, 4])
    print("NODES: ", nodes)
    edges = get_edges_from_db("project.db", [1, 2, 3, 4], [1, 2], [4])
    print("EDGES: ", edges)
    print("\nCalculate By the CPM model")
    nodes, critical_path, critical_time = cpm.start(nodes, edges)
    print("saving task plan ...")
    save_task_plan("project.db", nodes)
    print("\nDONE")
