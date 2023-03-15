from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DBNAME = os.getenv('DATABASE')
USER = os.getenv('MY_SQL_USER')
PASSWORD = os.getenv('MY_SQL_PASSWORD')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{USER}:{PASSWORD}@financial_data_assigment_database:{PORT}/{DBNAME}".format(USER=USER, PASSWORD=PASSWORD, PORT=PORT, DBNAME=DBNAME)

db = SQLAlchemy()
db.init_app(app)

class Company_Financial_Data(db.Model): 
    __tablename__ = "company_financial_data"

    Entry_ID = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    entry_date = db.Column(db.Date)
    open_price = db.Column(db.Numeric(5,2))
    close_price = db.Column(db.Numeric(5,2))
    volume = db.Column(db.Integer)

    def __repr__(self):
        print(self.symbol, datetime.strftime(self.entry_date, '%Y-%m-%d'), sep=', ')

@app.route('/api/financial_data', methods=['GET'])
def financial_data():
    """API endpoint for requesting financial data from the financial_data database

        HTTP Args:
            start_date (optional): Formatted string (YYYY-MM-DD) for the starting date of data range
            end_date (optional): Formatted string (YYYY-MM-DD) for the ending date of data range
            symbol (optional): Ticker Symbol for company data to be returned 
            page (optional): Page of paginated data to be returned 
            limit (optional): Number of results per page

        Returns:
            JSON object example: 
                {
                    "data":[
                        {
                            "close_price":"129.30",
                            "date":"2023-02-28",
                            "open_price":"130.55",
                            "symbol":"IBM",
                            "volume":5143133
                        }
                    ],
                    "info":{"error":""},
                    "pagination":{
                        "count":1,
                        "limit":3,
                        "page":1,
                        "pages":1
                    }
                }
    """
    args = request.args
    start_date_arg = args.get('start_date', '2023-01-01', type=str)
    end_date_arg = args.get('end_date', '2023-01-14', type=str)
    symbol = args.get('symbol', 'IBM', type=str)
    page = args.get('page', 1, type=int)
    limit = args.get('limit', 5, type=int)
    errorString = ''
    start_date = None
    end_date = None

    try:
        start_date = datetime.strptime(start_date_arg, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_arg, '%Y-%m-%d')
    except ValueError:
        print(ValueError)
        errorString = 'start or end date incorrect format'
        start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2023-01-14', '%Y-%m-%d')
        
    # http://127.0.0.1:5000/api/financial_data?start_date=2023-02-28&end_date=2023-03-09&symbol=IBM&limit=3&page=1
    data = Company_Financial_Data.query.filter(db.and_(Company_Financial_Data.symbol==symbol, Company_Financial_Data.entry_date >= start_date, Company_Financial_Data.entry_date <= end_date)).paginate(page=page, per_page=limit)

    results = {
        'data': [{
            'symbol': symbol,
            'date': datetime.strftime(fd.entry_date, '%Y-%m-%d'),
            'open_price':fd.open_price,
            'close_price':fd.close_price,
            'volume':fd.volume
        } for fd in data],
        'pagination': {
            'count': data.total,
            'page': page,
            'limit': limit,
            "pages": data.pages,
        },
        'info':{'error': errorString}
    }

    return jsonify(results)

@app.route('/api/statistics', methods=['GET'])
def statistics():
    """API endpoint for requesting statistics about a company over a time period

        HTTP Args:
            start_date (required): Formatted string (YYYY-MM-DD) for the starting date of data range
            end_date (required): Formatted string (YYYY-MM-DD) for the ending date of data range
            symbol (required): Ticker Symbol for company data to be returned 

        Returns:
            JSON onject example: 
            {
                "data":{
                    "average_daily_close_price":"128.59",
                    "average_daily_open_price":"129.24",
                    "average_daily_volume":3734361,
                    "end_date":"2023-03-09",
                    "start_date":"2023-02-28",
                    "symbol":"IBM"
                },
                "info":{"error":""}
            }
    
    """
    args = request.args
    start_date = args.get('start_date')
    end_date = args.get('end_date')
    symbol = args.get('symbol')
    if None in (start_date, end_date, symbol):
        return "all parameters are required"

    data = Company_Financial_Data.query.filter(db.and_(Company_Financial_Data.symbol==symbol, Company_Financial_Data.entry_date >= datetime.strptime(start_date, '%Y-%m-%d'), Company_Financial_Data.entry_date <= datetime.strptime(end_date, '%Y-%m-%d'))).all()

    total_open_price = 0
    total_close_price = 0
    total_volume = 0
    num_records = len(data)

    if num_records == 0:
        return {'data': {}, 'info':{'error': 'No entries found for symbol: ' + symbol}}

    for fd in data:
        total_open_price += fd.open_price
        total_close_price += fd.close_price
        total_volume += fd.volume

    result = {
        'data': {
            'start_date': start_date,
            'end_date': end_date,
            'symbol': symbol,
            'average_daily_open_price': round(total_open_price / num_records, 2),
            'average_daily_close_price': round(total_close_price / num_records, 2),
            'average_daily_volume': round(total_volume / num_records)
        },
        'info': {'error': ''}
    }

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)