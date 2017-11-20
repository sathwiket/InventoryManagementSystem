import json
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from inventory_processor import ProductFetcher, ProductCreator, ProductUpdater, Login

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/login": {"origins": "http://localhost:5000"}})


def authenticate_request(auth_token):
    try:
        user_name = auth_token[auth_token.find("@") + 1: auth_token.find("+")]
        password = auth_token[auth_token.find("+") + 1: auth_token.find("$")]
        response = Login().check_login_credentials({'user_name': user_name, "password": password})
        return response
    except Exception as e:
        raise render_template("401.html", error=str("401"))


@app.route("/products", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_all_products():
    try:
        authenticate_request(request.headers['Authorization'])
        product_list = ProductFetcher().get_all_products()
        return json.dumps(product_list)
    except Exception as e:
        raise


@app.route("/product/requests", methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def get_all_products_requests():
    try:
        authenticate_request(request.headers['Authorization'])
        query_params = request.args
        product_list = ProductFetcher().get_all_product_requests(query_params)
        return json.dumps(product_list)
    except Exception as e:
        raise


@app.route("/products/user/<user_id>", methods=['GET'])
def get_all_products_by_user(user_id=None):
    try:
        authenticate_request(request.headers['auth_token'])
        product_list = ProductFetcher().get_all_products_by_user(user_id)
        return json.dumps(product_list)
    except Exception as e:
        raise


@app.route('/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def login():
    try:
        login_req_data = json.loads(request.data)
        response_data = Login().check_login_credentials(login_req_data)
        return json.dumps(response_data)
    except Exception as e:
        raise


@app.route("/product", methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def add_product_to_inventory():
    try:
        authenticate_request(request.headers['Authorization'])
        request_data = json.loads(request.data)
        response_data = ProductCreator().add_product_to_inventory(request_data)
        return json.dumps(response_data)
    except Exception as e:
        raise


@app.route("/product/<product_id>", methods=['PUT'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def update_product_in_inventory(product_id=None):
    try:
        authenticate_request(request.headers['Authorization'])
        request_data = json.loads(request.data)
        request_data['product_id'] = int(product_id)
        response_data = ProductUpdater().update_product_details(request_data)
        return json.dumps(response_data)
    except Exception as e:
        raise


@app.route("/product/request/<request_id>", methods=['PUT'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def update_product_request(request_id=None):
    try:
        authenticate_request(request.headers['Authorization'])
        request_data = json.loads(request.data)
        request_data['request_id'] = int(request_id)
        response_data = ProductUpdater().update_inventory_product(request_data)
        return json.dumps(response_data)
    except Exception as e:
        raise


if __name__ == "__main__":
    app.run()
