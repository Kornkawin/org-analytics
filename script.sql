-- drop all table
DROP TABLE IF EXISTS PROJECT;
DROP TABLE IF EXISTS EMPLOYEE;
DROP TABLE IF EXISTS ACTIVITY;
DROP TABLE IF EXISTS TASK;
DROP TABLE IF EXISTS TASK_REPORT;
DROP TABLE IF EXISTS TASK_PLAN;

-- master table
CREATE TABLE IF NOT EXISTS PROJECT
(
    Project_ID         INTEGER PRIMARY KEY AUTOINCREMENT,
    Project_Name       TEXT NOT NULL,
    Project_Manager    INT  NOT NULL REFERENCES EMPLOYEE (Employee_ID),
    Project_Start_Date DATE NOT NULL,
    Project_Deadline   DATE NOT NULL,
    Project_End_Date   DATE NOT NULL,
    Project_Status     TEXT NOT NULL
);
INSERT INTO PROJECT (Project_ID, Project_Name, Project_Manager, Project_Start_Date, Project_Deadline, Project_End_Date,
                     Project_Status)
VALUES (1, 'Project 1', 1, '2025-01-01', '2025-01-31', '', 'On Progress');

CREATE TABLE IF NOT EXISTS EMPLOYEE
(
    Employee_ID          INTEGER PRIMARY KEY AUTOINCREMENT,
    Employee_Name        TEXT    NOT NULL,
    Employee_Position    TEXT    NOT NULL,
    Skill_Level_Backend  INTEGER NOT NULL,
    Skill_Level_Frontend INTEGER NOT NULL,
    Skill_Level_Testing  INTEGER NOT NULL,
    Employee_Contact     TEXT    NOT NULL
);
INSERT INTO EMPLOYEE (Employee_ID, Employee_Name, Employee_Position, Skill_Level_Backend, Skill_Level_Frontend,
                      Skill_Level_Testing, Employee_Contact)
VALUES (1, 'John', 'Fullstack Developer', 3, 2, 0, '08123456789'),
       (2, 'Sara', 'Fullstack Developer', 2, 3, 0, '08123456789'),
       (3, 'Simon', 'Fullstack Developer', 1, 1, 0, '08123456789'),
       (4, 'Bobby', 'Tester', 0, 0, 5, '08123456789');


CREATE TABLE IF NOT EXISTS ACTIVITY
(
    Activity_ID          INTEGER PRIMARY KEY AUTOINCREMENT,
    Activity_Name        TEXT NOT NULL,
    Activity_Description TEXT NOT NULL
);
INSERT INTO ACTIVITY (Activity_ID, Activity_Name, Activity_Description)
VALUES (1, 'Frontend', 'To display the data'),
       (2, 'Backend-API', 'To manage the data'),
       (3, 'Gateway-API', 'To connect the third party services'),
       (4, 'Testing', 'To test the program before launched');

-- master table for scheduling
CREATE TABLE IF NOT EXISTS TASK
(
    Task_ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
    Task_Date_Launched      DATE    NOT NULL,
    Task_Size               TEXT    NOT NULL,
    Task_Language_Used      TEXT    NOT NULL,
    Task_Normal_Days        INTEGER NOT NULL,
    Task_Crash_Days         INTEGER NOT NULL,
    Task_Normal_Cost        REAL    NOT NULL,
    Task_Crash_Cost         REAL    NOT NULL,
    Task_Crash_Cost_Per_Day REAL    NOT NULL,
    Project_ID              INTEGER NOT NULL REFERENCES PROJECT (Project_ID),
    Activity_ID             INTEGER NOT NULL REFERENCES ACTIVITY (Activity_ID),
    Prev_Activity_ID_1      INTEGER NULL REFERENCES ACTIVITY (Activity_ID),
    Prev_Activity_ID_2      INTEGER NULL REFERENCES ACTIVITY (Activity_ID),
    Prev_Activity_ID_3      INTEGER NULL REFERENCES ACTIVITY (Activity_ID),
    Prev_Activity_ID_4      INTEGER NULL REFERENCES ACTIVITY (Activity_ID)
);
INSERT INTO TASK (Task_ID, Task_Date_Launched, Task_Size, Task_Language_Used, Task_Normal_Days, Task_Crash_Days,
                  Task_Normal_Cost, Task_Crash_Cost, Task_Crash_Cost_Per_Day, Project_ID, Activity_ID,
                  Prev_Activity_ID_1, Prev_Activity_ID_2, Prev_Activity_ID_3, Prev_Activity_ID_4)
VALUES (1, '2025-01-01', 'S', 'HTML/CSS/JS', 3, 2, 3000.0, 4500.0, (4500.0 - 3000.0) / (3 - 2), 1, 1, null, null, null, null),
       (2, '2025-01-01', 'M', 'JAVA', 5, 4, 5000.0, 6000.0, (6000.0 - 5000.0) / (5 - 4), 1, 2, null, null, null, null),
       (3, '2025-01-01', 'S', 'JAVA', 3, 1, 3000.0, 5000.0, (5000.0 - 3000.0) / (3 - 1), 1, 3, 2, null, null, null),
       (4, '2025-01-01', 'S', 'JS', 4, 2, 1000.0, 4000.0, (4000.0 - 1000.0) / (4 - 2), 1, 4, 1, 3, null, null);

-- to monitor the progress
CREATE TABLE IF NOT EXISTS TASK_REPORT
(
    Report_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
    Report_Date     DATE    NOT NULL,
    Report_By       TEXT    NOT NULL REFERENCES EMPLOYEE (Employee_ID),
    Report_Progress TEXT    NOT NULL,
    Task_ID         INTEGER NOT NULL REFERENCES TASK (Task_ID)
);
INSERT INTO TASK_REPORT (Report_ID, Report_Date, Report_By, Report_Progress, Task_ID)
VALUES (1, '2025-01-03', 'Employee 1', '75%', 1),
       (2, '2025-01-03', 'Employee 2', '20%', 2);

-- save the plan from model solution
CREATE TABLE IF NOT EXISTS TASK_PLAN
(
    Plan_ID                INTEGER NOT NULL,
    Plan_Task_Step         INTEGER NOT NULL,
    Plan_Date              DATE    NOT NULL,
    Plan_Task_Budget_Days  INTEGER NOT NULL,
    Plan_Task_Budget_Cost  REAL    NOT NULL,
    Plan_Early_Start_Days  INTEGER NOT NULL,
    Plan_Early_Finish_Days INTEGER NOT NULL,
    Plan_Late_Start_Days   INTEGER NOT NULL,
    Plan_Late_Finish_Days  INTEGER NOT NULL,
    Plan_Comment           TEXT    NOT NULL,
    Task_ID                INTEGER NOT NULL REFERENCES TASK (Task_ID),
    PRIMARY KEY (Plan_ID, Plan_Task_Step)
);

-- CREATE TABLE IF NOT EXISTS ASSIGNMENT (
--     Assignment_ID INT AUTOINCREMENT,
--     Assignment_Date_Assigned DATE NOT NULL,
--     Assignment_Date_Finished DATE NOT NULL,
--     Employee_ID INT NOT NULL,
--     Task_ID INT NOT NULL,
--     Activity_ID INT NOT NULL,
--     Project_ID INT NOT NULL,    
--     PRIMARY KEY (Assignment_ID),
--     FOREIGN KEY (Employee_ID) REFERENCES EMPLOYEE (Employee_ID),
--     FOREIGN KEY (Task_ID) REFERENCES TASK (Task_ID),
--     FOREIGN KEY (Activity_ID) REFERENCES ACTIVITY (Activity_ID),
--     FOREIGN KEY (Project_ID) REFERENCES PROJECT (Project_ID)
-- );
