# Python Assingment for CTW by Ryan Yu

This project contains two parts:

1. get_raw_data.py: 
    This script will get daily stock data from the [AlphaVantage](https://www.alphavantage.co/documentation/) API for the two stocks: IBM, APPL
    and store the data retreived in a MySQL database. The data stored will be data from the last 14 days from when the script is run. 
    
2. Flask API:
    This API serves data to two routes:
    
    ```/api/financial_data```,
    ```/api/statistics```
    
    The API is set to port 5002
    
    [Example Queries](#Examples)
    
# Technologies Used

<details>
    <summary>Flask</summary>
    <p>Python library for creating simple REST APIs.</p>
</details>
<details>
    <summary>SQLAlchemy</summary>
    <p>This python library is an ORM for interfacing with SQL databases using python classes as a model.
    For this project the SQLAlchemy paginate function was used to implement the pagination feature of the API.</p>
</details>
<details>    
    <summary>mysql-connector</summary>
    <p>This python library is a simple library for connecting to a SQL database. This was used by the get_raw_data.py 
    script to connect to the MySQL database and insert new data. Since only insertion of new data was required by 
        get_raw_data.py, mysql-connector was prefered for its simplicity. </p>
</details>
<details>
    <summary>dotenv</summary>
    <p>Python library is used for reading the .env file.</p>
</details>

# Requirements

First create an .env in the root of your directory. This .env will contain environment variables that are used by both the database, api, and get_raw_data.py. 
    By using an .env file to pass environment variables to our programs, we can keep secrets like our API keys, and passwords from ending up in public places
    by adding the .env file to .gitignore and .dockerignore files. For local development, this .env file can stay on the local machine, 
    and in a production environment, these environment variables can be passed as commandline arguments when running ```docker-compose up```. 
    
The .env should contain the following variables:
    
```
# MySQL
DATABASE=<Database Name>
ROOT_USER=<Your Root User>
ROOT_PASSWORD=<Your Root User password>
MY_SQL_USER=<Your User>
MY_SQL_PASSWORD=<Your User Password>
PORT=3306

# API_KEY for get_raw_data.py
API_KEY=<Your API Key>
```

- - - -

To run get_raw_data.py first install requirements:
```
pip3 install requests mysql-connector-python python-dotenv
```
Then run:
```
python3 get_raw_data.py
```

- - - -

To start the database and API services:
```
docker-compose up
```
    
# Examples<a name="Examples"></a>

```
Query: http://localhost:5002/api/statistics?start_date=2023-02-28&end_date=2023-03-09&symbol=IBM 
Response: 
{
    "data":[
        {
            "close_price":"129.30",
            "date":"2023-02-28",
            "open_price":"130.55",
            "symbol":"IBM",
            "volume":5143133
        },
        {
            "close_price":"128.19",
            "date":"2023-03-01",
            "open_price":"128.90",
            "symbol":"IBM",
            "volume":3760678
        },
        {
            "close_price":"128.93",
            "date":"2023-03-02",
            "open_price":"128.39",
            "symbol":"IBM",
            "volume":3340254
        }
    ],
    "info":{
        "error":""
    },
    "pagination":{
        "count":10,
        "limit":3,
        "page":1,
        "pages":4
    }
}

Query: http://localhost:5002/api/financial_data?start_date=2023-02-28&end_date=2023-03-13&symbol=IBM&limit=3&page=1
Response: 
{
    "data":{
        "average_daily_close_price":"128.59",
        "average_daily_open_price":"129.24",
        "average_daily_volume":3734361,
        "end_date":"2023-03-09",
        "start_date":"2023-02-28",
        "symbol":"IBM"
    },
    "info":{
        "error":""
    }
}
```