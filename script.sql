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

CREATE TABLE IF NOT EXISTS EMPLOYEE
(
    Employee_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
    Employee_Name    TEXT NOT NULL,
    Employee_Contact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ACTIVITY
(
    Activity_ID          INTEGER PRIMARY KEY AUTOINCREMENT,
    Activity_Name        TEXT NOT NULL,
    Activity_Description TEXT NOT NULL
);

-- transaction table
CREATE TABLE IF NOT EXISTS TASK
(
    Task_ID               INTEGER PRIMARY KEY AUTOINCREMENT,
    Task_Date_Launched    DATE    NOT NULL,
    Task_Size             TEXT    NOT NULL,
    Task_Language_Used    TEXT    NOT NULL,
    Task_Actual_Days_Used REAL    NOT NULL,
    Task_Actual_Expense   REAL    NOT NULL,
    Task_Status           TEXT    NOT NULL,
    Project_ID            INTEGER NOT NULL REFERENCES PROJECT (Project_ID),
    Activity_ID           INTEGER NOT NULL REFERENCES ACTIVITY (Activity_ID),
    Prev_Activity_ID      INTEGER NOT NULL REFERENCES ACTIVITY (Activity_ID)
);

CREATE TABLE IF NOT EXISTS TASK_REPORT
(
    Report_ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
    Report_Date               DATE    NOT NULL,
    Report_By                 TEXT    NOT NULL REFERENCES EMPLOYEE (Employee_ID),
    Report_Progress         TEXT    NOT NULL,
    Task_ID                   INTEGER NOT NULL REFERENCES TASK (Task_ID)
);

CREATE TABLE IF NOT EXISTS TASK_PLAN
(
    Plan_ID                INTEGER NOT NULL,
    Plan_Version           INTEGER NOT NULL,
    Plan_Date              DATE    NOT NULL,
    Plan_Budget            REAL    NOT NULL,
    Plan_Early_Start_Date  DATE    NOT NULL,
    Plan_Early_Finish_Date DATE    NOT NULL,
    Plan_Late_Start_Date   DATE    NOT NULL,
    Plan_Late_Finish_Date  DATE    NOT NULL,
    Plan_Comment           TEXT    NOT NULL,
    Task_ID                INTEGER NOT NULL REFERENCES TASK (Task_ID),
    PRIMARY KEY (Plan_ID, Plan_Version)
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

-- insert master data
INSERT INTO PROJECT (Project_ID, Project_Name, Project_Manager, Project_Start_Date, Project_Deadline, Project_End_Date,
                     Project_Status)
VALUES (1, 'Project 1', 1, '2021-01-01', '2021-12-31', '', 'On Progress'),
       (2, 'Project 2', 2, '2021-01-01', '2021-12-31', '', 'On Progress'),
       (3, 'Project 3', 3, '2021-01-01', '2021-12-31', '', 'On Progress');

INSERT INTO EMPLOYEE (Employee_ID, Employee_Name, Employee_Contact)
VALUES (1, 'Employee 1', '08123456789'),
       (2, 'Employee 2', '08123456789'),
       (3, 'Employee 3', '08123456789');

INSERT INTO ACTIVITY (Activity_ID, Activity_Name, Activity_Description)
VALUES (1, 'Activity 1', 'Description 1'),
       (2, 'Activity 2', 'Description 2'),
       (3, 'Activity 3', 'Description 3');

-- insert transaction
-- activity 1,2,3 that belongs to project 1
INSERT INTO TASK (Task_ID, Task_Date_Launched, Task_Size, Task_Language_Used, Task_Actual_Days_Used,
                  Task_Actual_Expense, Task_Status, Project_ID, Activity_ID, Prev_Activity_ID)
VALUES (1, '2021-01-01', 'S', 'Python', '15', '1000', 'On Progress', 1, 1, 0),
       (2, '2021-01-01', 'M', 'Java', '10', '1000', 'On Progress', 1, 2, 1),
       (3, '2021-01-01', 'L', 'C++', '', '', 'On Progress', 1, 3, 2);
-- task progress for the task id
INSERT INTO TASK_REPORT (Report_ID, Report_Date, Report_By, Report_Progress, Task_ID)
VALUES (1, '2021-01-01', 'Employee 1', '100%', 1),
       (2, '2021-01-01', 'Employee 2', '10%', 2);
-- plan for task 1
INSERT INTO TASK_PLAN (Plan_ID, Plan_Version, Plan_Date, Plan_Budget, Plan_Early_Start_Date, Plan_Early_Finish_Date,
                           Plan_Late_Start_Date, Plan_Late_Finish_Date, Plan_Comment, Task_ID)
VALUES (1, 1, '2021-01-01', '100', '2021-01-01', '2021-01-15', '2021-02-01', '2021-02-15', 'Comment 1', 1),
       (1, 2, '2021-02-01', '110', '2021-02-01', '2021-02-15', '2021-03-01', '2021-03-15', 'Comment 2', 1),
       (1, 3, '2021-03-01', '120', '2021-03-01', '2021-03-15', '2021-04-01', '2021-04-15', 'Comment 3', 1);
       