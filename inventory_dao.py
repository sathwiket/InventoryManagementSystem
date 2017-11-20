import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, Float, TEXT, DATE, ForeignKey, Enum, DATETIME

engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/inventoryDB', echo=False)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    email_id = Column(VARCHAR(100))
    created_datetime = Column(DATETIME)

    def __init__(self, user_name=None, password=None, email_id=None, created_datetime=None):
        self.user_name = user_name
        self.password = password
        self.email_id = email_id
        self.created_datetime = created_datetime

    def add_user(self):
        user_obj = User(user_name=self.user_name, password=self.password,
                        email_id=self.email_id, created_datetime=self.created_datetime)
        session.add(user_obj)
        session.commit()

    def remove_user(self, user_name):
        userObj = User().get_user_by_name(user_name)
        session.delete(userObj)
        session.commit()

    def get_all_users(self):
        user_obj_list = session.query(User).all()
        session.commit()
        return user_obj_list

    def get_user_details_by_id(self, user_id):
        user_obj = session.query(User).filter(User.user_id == user_id).all()
        session.commit()
        return user_obj

    def get_user_by_name(self, user_name):
        user_details = session.query(User).filter(User.user_name == user_name).first()
        session.commit()
        return user_details

    def user_login(self, user_name, password):
        user_obj = User().get_user_by_name(user_name)
        if user_obj.user_name is not None and user_obj.password is not None:
            if (user_obj.user_name == user_name and user_obj.password == password):
                print "Logged in"
            else:
                print "Please check credentials"


class UserRole(Base):
    __tablename__ = "user_role"
    user_role_id = Column(Integer, primary_key=True, autoincrement=True)
    user_role_name = Column(VARCHAR(100))
    created_datetime = Column(DATETIME)

    def __init__(self, user_role_name=None):
        self.user_role_name = user_role_name
        self.created_datetime = datetime.datetime.now()

    def add_role(self):
        user_role_obj = UserRole(user_role_name=self.user_role_name, created_datetime=self.created_datetime)
        session.add(user_role_obj)
        session.commit()

    def remove_role(self, user_role_name):
        user_role_obj = session.query(UserRole).filter(UserRole.user_role_name == user_role_name).first()
        session.delete(user_role_obj)
        session.commit()

    def get_all_roles(self):
        user_role_obj_list = session.query(UserRole).all()
        session.commit()
        return user_role_obj_list


class UserRoleMap(Base):
    __tablename__ = "user_role_map"
    user_role_map_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    user_role_id = Column(Integer, ForeignKey("UserRole.user_role_id"))
    created_datetime = Column(DATETIME)

    def __init__(self, user_id=None, user_role_id=None):
        self.user_id = user_id
        self.user_role_id = user_role_id
        self.created_datetime = datetime.datetime.now()

    def assign_role_to_user(self):
        user_role_map_obj = UserRoleMap(user_id=self.user_id,
                                        user_role_id=self.user_role_id, created_datetime=self.created_datetime)
        session.add(user_role_map_obj)
        session.commit()

    def remove_role_to_user(self, user_id):
        user_role_map_obj = session.query(UserRoleMap).filter(UserRoleMap.user_id == user_id).first()
        session.delete(user_role_map_obj)
        session.commit()

    def get_user_role(self, user_id):
        user_role_map_obj = session.query(UserRoleMap).filter(UserRoleMap.user_id == user_id).all()
        session.commit()
        return user_role_map_obj

    def get_all_assigned_roles(self):
        user_role_map_list = session.query(UserRoleMap).all()
        session.commit()
        return user_role_map_list


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(VARCHAR(100))
    quantity = Column(Integer)
    mrp = Column(Float)
    batch_num = Column(VARCHAR(100))
    batch_date = Column(VARCHAR(100))
    vendor_name = Column(VARCHAR(100))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    status = Column(VARCHAR(50), Enum("active", "inactive"))
    created_datetime = Column(DATETIME)

    def __init__(self, product_name=None, quantity=None, mrp=None, batch_num=None, batch_date=None,
                 vendor_name=None, user_id=None, status=None, created_datetime=None):
        self.product_name = product_name
        self.quantity = quantity
        self.batch_num = batch_num
        self.batch_date = batch_date
        self.mrp = mrp
        self.vendor_name = vendor_name
        self.status = status
        self.user_id = user_id
        self.created_datetime = datetime.datetime.now()

    def add_product_to_inventory(self):
        product_obj = Product(product_name=self.product_name, quantity=self.quantity,
                              mrp=self.mrp, batch_num=self.batch_num, batch_date=self.batch_date,
                              vendor_name=self.vendor_name, user_id=self.user_id, status=self.status,
                              created_datetime=self.created_datetime)
        session.add(product_obj)
        session.commit()
        return product_obj.product_id

    def update_product_in_inventory(self, product_id):
        session.query(Product).filter(Product.product_id == product_id).update({"product_name": self.product_name,
                                                                                   'quantity': self.quantity,
                                                                                   "mrp": self.mrp,
                                                                                   "batch_num": self.batch_num,
                                                                                   "batch_date": self.batch_date,
                                                                                   "vendor_name": self.vendor_name,
                                                                                   "status": "active"})
        session.commit()

    def remove_product_from_inventory(self, product_id):
        product_obj = session.query(Product).filter(Product.product_id == product_id).first()
        session.delete(product_obj)
        session.commit()

    def get_all_products(self):
        product_list = session.query(Product).all()
        session.commit()
        return product_list

    def get_all_products_by_user_id(self, user_id):
        product_list = session.query(Product).filter(Product.user_id == user_id).all()
        session.commit()
        return product_list

    def get_user_by_product_id(self, product_id):
        product_list = session.query(Product).filter(Product.product_id == product_id).first()
        user_list = session.query(UserRoleMap).filter(UserRoleMap.user_id == product_list.user_id).first()
        response = [product_list, user_list]
        session.commit()
        return response

    def get_active_products(self):
        acc_product_list = session.query(Product).filter(Product.status == "active").all()
        return acc_product_list

    def get_inactive_products(self):
        pen_product_obj = session.query(Product).filter(Product.status == "inactive").all()
        return pen_product_obj

    # def update_product_in_inventory(self, product_id):
    #     session.query(Product).filter_by(Product.product_id == product_id).update({"name": u"Bob Marley"})
    #     session.commit()


class UpdateRequest(Base):
    __tablename__ = "update_request"
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(VARCHAR(50), Enum("new_product", "update_product", "remove_product"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    status = Column(VARCHAR(50), Enum("approved", "pending"))
    update_data = Column(TEXT)
    created_datetime = Column(DATETIME)

    def __init__(self, request_id=None, request_type=None, user_id=None, status=None, update_data=None,
                 created_datetime=None):
        self.request_id = request_id
        self.request_type = request_type
        self.user_id = user_id
        self.status = status
        self.update_data = update_data
        self.created_datetime = datetime.datetime.today()

    def add_request(self):
        request_obj = UpdateRequest(request_type=self.request_type,
                                    user_id=self.user_id, status=self.status,
                                    update_data=self.update_data, created_datetime=self.created_datetime)
        session.add(request_obj)
        session.commit()
        return request_obj.request_id

    def update_request(self):
        request_obj = UpdateRequest(request_id=self.request_id, request_type=self.request_type,
                                    user_id=self.user_id, status=self.status,
                                    update_data=self.update_data, created_datetime=self.created_datetime)
        session.update(request_obj)
        session.commit()
        return request_obj.request_id

    def get_all_requests_by_status(self, request_status):
        product_requests = session.query(UpdateRequest).filter(UpdateRequest.status == request_status).all()
        session.commit()
        return product_requests

    def get_all_requests(self):
        product_requests = session.query(UpdateRequest, User).join(User).filter(
            UpdateRequest.user_id == User.user_id).all()
        session.commit()
        return product_requests

    def get_all_requests_by_user_id(self):
        req_list = session.query(UpdateRequest).filter(UpdateRequest.user_id == self.user_id).all()
        session.commit()
        return req_list

    def get_all_requests_by_req_id(self, request_data):
        req_list = session.query(UpdateRequest).filter(UpdateRequest.request_id == request_data['request_id']).all()
        session.query(UpdateRequest).filter(UpdateRequest.request_id == request_data['request_id']).update(
            {"status": request_data['status']})
        session.commit()
        return req_list[0]
