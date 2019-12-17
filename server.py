from flask import Flask, request, render_template, g, redirect, Response, jsonify
import sys
from google.cloud import bigquery
import os
import json


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/Admin/Desktop/Big Data project/bigData-4390f7f59d39.json'
bigquery_client = bigquery.Client()


# @app.before_request
# def before_request():
#     pass
#     # con = sqlite3.Connection('newdb.sqlite')
#     # cur = con.cursor()
#     # cur.execute('CREATE TABLE "stuff" ("one" varchar(12), "two" varchar(12));')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/product_recommendation')
def recommendation():
    query = """
    SELECT
    distinct(brand)
    FROM
    `rich-city-252820.amazonPhoneReview.F1`

    """
    query_job = bigquery_client.query(query)
    brand_list = []
    # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        brand_list.append(row['brand'])

    context = {"brand_list": brand_list}
    return render_template("product_recommendation.html", **context)

@app.route('/phone_recommend', methods=['POST'])
def recommend():
    if request.json['brand'] == "Default" and request.json['price'] == "Default":
        query = """
        SELECT
        *
        FROM
        `rich-city-252820.amazonPhoneReview.F1joinF3`
        where reviewNum>=10
        ORDER BY avg_sentimental_magnitude DESC
        LIMIT 5
        """

    elif request.json['brand'] != "Default" and request.json['price'] == "Default":
        query = """
        SELECT
        *
        FROM
        `rich-city-252820.amazonPhoneReview.F1joinF3`
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
            `rich-city-252820.amazonPhoneReview.F1joinF3`
            WHERE reviewNum>=10 and 
            """ + where_sentence + " ORDER BY avg_sentimental_magnitude DESC " \
            + "LIMIT 3"
        else:
            query = """
            SELECT
            *
            FROM
            `rich-city-252820.amazonPhoneReview.F1joinF3`
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
def initial_credential_page():
    query = """
    SELECT
    distinct(brand)
    FROM
    `rich-city-252820.amazonPhoneReview.F1joinF3`

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
    `rich-city-252820.amazonPhoneReview.F1joinF3`
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
    query = """
    select confidence
    from
    (select title1, round(1-fake_cnt/cnt,2) as confidence from
    (select title as title1, count(*) as cnt
    from `rich-city-252820.amazonPhoneReview.F1joinF3_2`
    group by title) t1
    Inner join
    (select title as title2, count(*) as fake_cnt
    from `rich-city-252820.amazonPhoneReview.F1joinF3_2`
    where rating=5 and sentimental_score<0.3
    group by title) t2
    on t1.title1 = t2.title2) t6
    where title1 =
    """ + "\"" +str(request.json['product']) + "\""
    print("^^^^^^^^^^^^^^", str(request.json['product']))
    query_job = bigquery_client.query(query)
    title_list = []
    # # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        title_list.append(row['confidence'])

    if not title_list:
        confidence = 1
    else:
        confidence = title_list[0]
    #
    context = {"confidence": confidence}
    return jsonify(result=context)

@app.route('/review_number', methods=['GET'])
def initial_review_number():
    query = """
    SELECT
    distinct(brand)
    FROM
    `rich-city-252820.amazonPhoneReview.F1joinF3`

    """
    query_job = bigquery_client.query(query)
    brand_list = []
    # print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        brand_list.append(row['brand'])

    context = {"brand_list": brand_list}
    return render_template("review_number.html", **context)

@app.route('/get_review_num', methods=['POST'])
def get_review_num_page():
    query = """
    select rating, count(*) as num
    from `rich-city-252820.amazonPhoneReview.F1joinF3_2`
    where title = 
    """ + "\"" +str(request.json['product']) + "\"" + \
    "group by rating"

    query_job = bigquery_client.query(query)
    rating_list = []
    rating_dict = {}
    for r in range(1, 6):
        rating_dict[r] = 0

    for row in query_job:
        # Row values can be accessed by field name or index.
        rating_dict[row['rating']] += row['num']

    for key, value in rating_dict.items():
        rating_list.append({"rating":key, "num":value})
    return jsonify(result=rating_list)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8111, debug=True)