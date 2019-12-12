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
    `amazon-phone.amazonphone1.F1_Data`

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
    if request.json['brand'] == "Default" and request.json['price'] == "Default":
        query = """
        SELECT
        *
        FROM
        `amazon-phone.amazonphone1.F1joinF3`
        where reviewNum>=10
        ORDER BY avg_sentimental_magnitude DESC
        LIMIT 3
        """

    elif request.json['brand'] != "Default" and request.json['price'] == "Default":
        query = """
        SELECT
        *
        FROM
        `amazon-phone.amazonphone1.F1joinF3`
        WHERE reviewNum>=10 and 
        brand=
        """  + "\"" +str(request.json['brand']) + "\"" + " ORDER BY avg_sentimental_magnitude DESC " \
        + "LIMIT 3"
    elif  request.json['price'] != "Default":

        if request.json['price'] == "<300":
            where_sentence = "priceNum<=300"
        elif request.json['price'] == "300-600":
            where_sentence = "priceNum BETWEEN 300 AND 600"
        elif request.json['price'] == "600-900":
            where_sentence = "priceNum BETWEEN 600 AND 900"
        elif request.json['price'] == ">900":
            where_sentence = "priceNum>=900"

        if request.json['brand'] == "Default":
            query = """
            SELECT
            *
            FROM
            `amazon-phone.amazonphone1.F1joinF3`
            WHERE reviewNum>=10 and 
            """ + where_sentence + " ORDER BY avg_sentimental_magnitude DESC " \
            + "LIMIT 3"
        else:
            query = """
            SELECT
            *
            FROM
            `amazon-phone.amazonphone1.F1joinF3`
            WHERE reviewNum>=10 and brand=
            """ + "\"" +str(request.json['brand']) + "\" AND " + where_sentence + " ORDER BY avg_sentimental_magnitude DESC " \
            + "LIMIT 3"

    query_job = bigquery_client.query(query)
    result_data = []
    # # print("The query data:")
    for row in query_job:
        print(row)
        result_data.append({"link":row['url'], "brand": row['brand'], "title": row['title'],"rating": row['ratingNum'], "image_url": row['image'], "price": row['priceNum']})
    return jsonify(result=result_data)


@app.route('/review_confidence', methods=['GET'])
def get_credential_for_reviews():
    query = """
    SELECT
    distinct(brand)
    FROM
    `amazon-phone.amazonphone1.F1joinF3`

    """
    query_job = bigquery_client.query(query)
    brand_list = []
    # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        brand_list.append(row['brand'])

    context = {"brand_list": brand_list}
    return render_template("review_confidence.html", **context)

@app.route('/get_products', methods=['POST'])
def get_products():
    query = """
    SELECT
    distinct(title)
    FROM
    `amazon-phone.amazonphone1.F1joinF3`
    where brand=

    """+ "\"" +str(request.json['brand']) + "\""
    query_job = bigquery_client.query(query)
    title_list = []
    # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        title_list.append(row['title'])

    context = {"product_list": title_list}
    return jsonify(result=context)

@app.route('/get_confidence', methods=['POST'])
def get_confidence():
    query = \
    "select round(1-fake_cnt/cnt,2) as confidence from" + \
    "(select title as title1, count(*) as cnt " + \
    "from `amazon-phone.amazonphone1.F1joinF3` " + \
    "group by title) t1" + \
    "Inner join" + \
    "(select title as title2, count(*) as fake_cnt" + \
    "from `amazon-phone.amazonphone1.F1joinF3`" + \
    "where rating=5 and sentimental_score<0.3" + \
    "group by title) t2" + \
    "on t1.title1 = t2.title2"\
    + "where title1= \"" +str(request.json['product']) + "\""
    query_job = bigquery_client.query(query)
    title_list = []
    # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        title_list.append(row['title'])

    context = {"product_list": title_list}
    return jsonify(result=context)




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8111, debug=True)