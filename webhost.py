#!/usr/bin/env python

from bottle import route, run
import sqlite3
import json

SQLCONN = sqlite3.connect('/home/ryan/projects/gr8w8upd8m8/w8.db')
sqlcurs = SQLCONN.cursor()

sqlcurs.execute("SELECT CAST(strftime('%s', timestamp) AS INTEGER) * 1000 AS timestamp, weight FROM w8upd8 LIMIT 1000")
results = sqlcurs.fetchall()

sqlcurs.close()
SQLCONN.close()

@route('/')
@route('/index')
def index():
    return '''<!DOCTYPE html>
 <html>
    <head>
        <title>Weight Data</title>
        <script type="text/javascript" src="http://code.jquery.com/jquery-2.1.1.min.js"></script>
        <script type="text/javascript" src="http://code.highcharts.com/stock/highstock.js"></script>
        <script type="text/javascript" src="http://code.highcharts.com/stock/modules/exporting.js"></script>
        <script type="text/javascript">            
            function CreateChart(weightdata) {
                $("#chart").highcharts("StockChart", {
                    title: {
                        text : "Weight over time"
                    },
                    credits: {
                        href: "http://github.com/Ryan-Myers",
                        text: "Ryan Myers"
                    },
                    series: [{
                        name : "Weight in KG",
                        data : weightdata,
                        tooltip: {
                            valueDecimals: 2
                        }
                    }]
                });
            }
            
            $(function() {
                $.getJSON("/get_data", function(weightdata) {
                    CreateChart(weightdata);
                });
            });
        </script>
    </head>
    <body>
        <div id="chart">TEST</div>
    </body>
</html>
'''

@route('/get_data')
def get_data():
    return json.dumps(results)

run(host='192.168.1.98', port=8080)