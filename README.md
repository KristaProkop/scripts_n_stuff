# A collection of useful scripts


## Setup
1) set up your venv, `pip install -r requirements.txt`
2) Add a `config.py` with something like this:

```python
DATABASES = {
    "stage_db" : {
        "connection": {
            "user": "username",
            "passwd": "password",
            "host": "host.url.com",
            "port": 3306,
            "db": "dbname",
            "charset": "utf8"
    },
        "params": {
        }
    },
    "prod_db" : {
        "connection": {
            "user": "username",
            "passwd": "password",
            "host": "host.url.com",
            "port": 3306,
            "db": "dbname",
            "charset": "utf8"
    },
        "params": {
        }
    }
}
```

## Usage


### Batch inserting in a mysql database
With a local csv file, use [db-batch-update.py](./db-batch-update.py) to execute queries in batches.
This is useful after you brought your entire application down when you tried to run a lot of inserts all at once.  
Just add your table configuration to the `jobs` object in `get_table_config()`.  
For example, to update the `employee` table in batches of 100:
```
jobs = {
    # name of the table
    "employee": {
        # the query to run on the table. The string variables should match the structure of your csv file
        'query': "INSERT employee (first_name, last_name, annual_salary) VALUES (%s, %s, %s)",
        # csv values are strings by default. Each column type will be converted as needed:
        'col_types': [str, str, float]
    }
```
Invoke the script with `python3 db-batch-update.py -t employee -b 100 -f "Users/me/path_to_file.csv"`  
The number of records successfully processed will be displayed in your terminal. Use the `-s` arg to start 
processing where you left off:  
 `python3 db-batch-update.py -t employee -b 100 -f "Users/me/path_to_file.csv" -s 252`


