## Task

1. Create DataClasses for the two tables `applog` and `uilog`. Consider the following points:
    - Assign the correct datatypes to the columns.
    - The `uilog` table can be joined to the `applog` table (n:1)
    - The join is dependend on two keys `uilog.appid -> applog.id` and `uilog.userid -> applog.userid`

2. Create an Endpoint `copyPasteAnalysis` that does the following:
    - Load the data from `uilog` and `applog` as needed into a `dask` dataframe
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

Additional Notes:
Feel free to modify the app.py and Dockerfile as needed. Feel free to use additional packages as needed. Create as many additional functions and classes as you feel is nescessary.
DO NOT modify the testdata.db!