from inventory_dao import User, UserRoleMap, Product, UpdateRequest
import json

user_roles = {1: "Store Manager", 2: "Department Manager"}


class Login:
    def __init__(self):
        pass

    def generate_auth_token(self, auth_data):
        auth_token = "@" + auth_data.user_name + "+" + auth_data.password + "$"
        return auth_token

    def check_login_credentials(self, login_req_data):
        try:
            login_data = User().get_user_by_name(login_req_data['user_name'])
            user_obj = UserRoleMap().get_user_role(login_data.user_id)
            user_role_obj = []
            for user in user_obj:
                user_dict = {'id': user.user_role_id, 'name': user_roles[user.user_role_id]}
                user_role_obj.append(user_dict)
            if login_req_data['user_name'] is None or login_req_data['password'] is None:
                raise
            elif login_data.user_name == login_req_data['user_name'] and login_data.password == login_req_data[
                'password']:
                auth_token = self.generate_auth_token(login_data)
                user_obj = {'name': login_data.user_name,
                            "id": login_data.user_id,
                            "email": login_data.email_id,
                            "auth_token": auth_token,
                            "roles": user_role_obj}
                return user_obj
            else:
                raise
        except Exception, e:
            raise


class ProductFetcher:
    def __init__(self):
        pass

    def construct_product_response(self, product_obj):
        try:
            product_list = []
            for product in product_obj:
                product_dict = {"product_id": product.product_id, "product_name": product.product_name,
                                "quantity": product.quantity, "batch_num": product.batch_num,
                                "batch_date": product.batch_date, "mrp": product.mrp,
                                "vendor_name": product.vendor_name, "status": product.status,
                                "created_datetime": str(product.created_datetime)}
                product_list.append(product_dict)
            return product_list
        except Exception:
            raise

    def get_all_products(self):
        try:
            product_obj = Product().get_all_products()
            product_details = self.construct_product_response(product_obj)
            return product_details
        except Exception:
            raise

    def get_all_products_by_user(self, user_id):
        try:
            product_obj = Product().get_all_products_by_user_id(user_id)
            product_details = self.construct_product_response(product_obj)
            return product_details
        except Exception:
            raise

    def get_all_product_requests(self, request_data):
        try:
            update_request_obj = UpdateRequest()
            if request_data is None:
                product_obj = update_request_obj.get_all_requests()
            else:
                product_obj = update_request_obj.get_all_requests_by_status(request_data['status'])
            product_list = []
            if product_obj:
                for product in product_obj:
                    product_data = json.loads(product.update_data)
                    if not product_data.has_key('product_id'):
                        product_data['product_id'] = None
                    product_dict = {"request_id": product.request_id,
                                    "request_type": product.request_type,
                                    "created_datetime": str(product.created_datetime),
                                    "user_name": product.user_id, "status": product.status,
                                    "product_details": {
                                        "product_id": product_data['product_id'],
                                        "product_name": product_data['product_name'],
                                        "quantity": product_data['quantity'],
                                        "batch_num": product_data['batch_num'],
                                        "batch_date": product_data['batch_date'], "mrp": product_data['mrp'],
                                        "vendor_name": product_data['vendor_name']}}
                    product_list.append(product_dict)
            return product_list
        except Exception:
            raise


class ProductCreator:
    def __init__(self):
        pass

    def check_user_role(self, user_id):
        try:
            user_role_obj = UserRoleMap().get_user_role(user_id)
            for user_obj in user_role_obj:
                if user_obj.user_role_id == 1:
                    return 1
            return 2
        except Exception:
            raise

    def add_product_to_inventory(self, product_dict):
        try:
            if not product_dict['user_id']:
                user_obj = User().get_user_by_name(product_dict.user_name)
                user_id = user_obj.user_id
            else:
                user_id = product_dict['user_id']
            user_role_id = self.check_user_role(user_id)
            product_data = product_dict['product_details']
            if user_role_id == 1:
                product_id = Product(product_name=product_data["product_name"], quantity=product_data["quantity"],
                                     mrp=product_data["mrp"],
                                     batch_num=product_data["batch_num"], batch_date=product_data["batch_date"],
                                     vendor_name=product_data["vendor_name"], user_id=user_id,
                                     status="active").add_product_to_inventory()
                return {'product_id': product_id}
            elif user_role_id == 2:
                request_id = UpdateRequest(request_type="new_product", user_id=user_id, status="pending",
                                           update_data=json.dumps(product_data)).add_request()
                return {'request_id': request_id}
        except Exception:
            raise


class ProductUpdater:
    def __init__(self):
        pass

    def update_product_details(self, request_data):
        try:
            user_obj = Product().get_user_by_product_id(request_data['product_id'])
            if user_obj[1].user_role_id == 2:
                product_data = {"product_name": request_data['product_name'],
                                "quantity": request_data['quantity'],
                                "mrp": request_data['mrp'],
                                "batch_num": request_data['batch_num'],
                                "batch_date": request_data['batch_date'],
                                "vendor_name": request_data['vendor_name'],
                                "product_id": request_data['product_id']
                                }
                UpdateRequest(request_type="update_product",
                              user_id=user_obj[0].user_id, status="pending",
                              update_data=str(product_data)).add_request()
            elif user_obj[1].user_role_id == 1:
                product_id = Product(product_name=request_data["product_name"], quantity=request_data["quantity"],
                                     mrp=request_data["mrp"],
                                     batch_num=request_data["batch_num"], batch_date=request_data["batch_date"],
                                     vendor_name=request_data["vendor_name"], user_id=user_obj[0].user_id,
                                     status="active").update_product_in_inventory(request_data['product_id'])
                return {'product_id': product_id}
        except Exception:
            raise

    def update_inventory_product(self, request_data):
        try:
            request_obj = UpdateRequest().get_all_requests_by_req_id(request_data)
            product_data = json.loads(request_obj.update_data)
            product_dict = {'user_id': request_obj.user_id, "product_details": {
                "product_name": product_data['product_name'],
                "quantity": product_data['quantity'],
                "batch_num": product_data['batch_num'],
                "batch_date": product_data['batch_num'], "mrp": product_data['mrp'],
                "vendor_name": product_data['vendor_name']}}
            if request_data['status'] == "approve":
                product_id = ProductCreator().add_product_to_inventory(product_dict)
                return product_id
        except Exception:
            raise
