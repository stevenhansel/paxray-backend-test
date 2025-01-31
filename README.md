## Task

1. Create DataClasses for the two tables `applog` and `uilog`. Consider the following points:
    - Assign the correct datatypes to the columns.
    - The `uilog` table can be joined to the `applog` table (n:1)
    - The join is dependend on two keys `uilog.appid -> applog.id` and `uilog.userid -> applog.userid`

2. Create an Endpoint `copyPasteAnalysis` that does the following:
    - Load the data from `uilog` and `applog` as needed into a `pandas` dataframe
    - Identify Events where Data was copied (this can be either, if the shortcuts `CTRL + C` or `CTRL + X` where pressed (`eventtype`), or when an element was clicked (`eventtype = Left-Down`) with the `accellereatorkey` property `STRG+C`)
    - Similarly Identify Eventw where data was pasted.
    - Create a copy paste analysis that shows how often data was copied from one application to another. Consider that copying data without pasting it does not count as a copy-paste event.
    - Return the data as a JSON object with the following structure:
    ```
        [
            {'from':'applicationA', 'to':'applicationB', 'count':42},
            {'from':'applicationB', 'to':'applicationC', 'count':3},
            ...
        ]
    ```
    - NOTE 1: It is possible that one copy event corresponds to multple paste events. Ignore these cases. Only count pairs of copy-paste events.
    - NOTE 2: Consider that the tables can become very large. Make sure, that you do not use loops to process the data. Try only using pandas aggregation and apply functions.

Additional Notes:
Feel free to modify the app.py and Dockerfile as needed. Feel free to use additional packages as needed. Create as many additional functions and classes as you feel is nescessary.
DO NOT modify the testdata.db!


3. Make the Database scalable:
    
    - There is a third table in the database "processlog". This table has the following columns:
        - activity: The activity that was performed
        - timestamp: The timestamp of the activity
        - caseid: The caseid of the activity (multiple activities can belong to the same case, consider a case as one instance of a process)
        - process: the name of the process that the case belongs to (multiple cases (i.e. instances of a process) can belong to the same cluster (i.e. process))

    - There are some issues with this table. If we want to assign cases to a different process, we have to update a lot of rows in this table, similar issues occur when we simply want to rename a process
    - Provide a solution to this problem. You can alter the database however you want. Provide all queries that alter the database and updates information.
    
