from flask import Flask, request, render_template, g, redirect, Response, jsonify
import sys
from google.cloud import bigquery
import os
import json


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/Admin/Desktop/Big Data project/amazon phone-1728156202e2.json'
bigquery_client = bigquery.Client()


# @app.before_request
# def before_request():
#     pass
#     # con = sqlite3.Connection('newdb.sqlite')
#     # cur = con.cursor()
#     # cur.execute('CREATE TABLE "stuff" ("one" varchar(12), "two" varchar(12));')

@app.route('/')
def index():
    query = """
    SELECT
    distinct(brand)
    FROM
    `amazon-phone.amazonphone1.test1`

    """
    query_job = bigquery_client.query(query)
    brand_list = []
    # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        brand_list.append(row['brand'])

    context = {"brand_list": brand_list}
    return render_template("index.html", **context)

@app.route('/phone_recommend', methods=['POST'])
def recommend():
    query = """
    SELECT
    *
    FROM
    `amazon-phone.amazonphone1.F1_Data`
    WHERE
    brand=
    """  + "\"" +str(request.json) + "\"" + " ORDER BY ratingNum DESC " \
    + "LIMIT 10"
    query_job = bigquery_client.query(query)
    result_data = []
    # # print("The query data:")
    for row in query_job:
        result_data.append([row['asin'],row['ratingNum']])
        # result_data[row['asin']] = {}
        # for key, val in row.items():
        #     result_data[row['asin']][key] = val
    #     # Row values can be accessed by field name or index.
    #     result_data.append(row)
    #
    # # # context = {"result": result_data}
    # print(result_data)
    return jsonify(result=result_data)


@app.route('/search', methods=['POST'])
def search():
    input = request.form['query']
    query = """
        SELECT
          *
        FROM
          `amazon-phone.amazonphone1.items_table`
        where brand = 'ASUS'
        LIMIT 
    """ + input

    query_job = bigquery_client.query(query)
    print(query_job)
    # result_data = []
    # # print("The query data:")
    # for row in query_job:
    #     # Row values can be accessed by field name or index.
    #     result_data.append(row)

    # context = {"result": result_data}
    context = {}
    return render_template("index.html", **context)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8111, debug=True)