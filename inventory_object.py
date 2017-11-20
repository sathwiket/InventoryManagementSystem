class UserRequest(object):
    def __init__(self):
        self._user_id = None
        self._user_name = None
        self._user_role_name = None
        self._email_id = None
        self._user_role_id = None
        self._product_id = None
        self._product_details = None
        self._status = None
        self._request_id = None
        self._request_type = None
        self._update_data = None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def user_role_name(self):
        return self._user_role_name

    @user_role_name.setter
    def user_role_name(self, value):
        self._user_role_name = value


    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, value):
        self._email_id = value


    @property
    def user_role_id(self):
        return self._user_role_id

    @user_role_id.setter
    def user_role_id(self, value):
        self._user_role_id = value


    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value


    @property
    def product_details(self):
        return self._product_details

    @product_details.setter
    def product_details(self, value):
        self._product_details = value


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


    @property
    def request_id(self):
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        self._request_id = value


    @property
    def request_type(self):
        return self._request_type

    @request_type.setter
    def request_type(self, value):
        self._request_type = value

    @property
    def update_data(self):
        return self._update_data

    @update_data.setter
    def update_data(self, value):
        self._update_data = value
