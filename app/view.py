from flask import Blueprint, request, jsonify, render_template
from app.controller.password_auth import PasswordAuth
import json

api = Blueprint('api', __name__)


@api.route('/api/signup', methods=['POST'])
def sign_up():
    data = json.loads(request.get_data().decode('utf-8'))
    for auth in [PasswordAuth()]:
        # check input
        val_status, val_result = auth.check_input(data)
        if not val_status:
            return jsonify(status=val_result), 400
        # process input
        processed_input = auth.process_input(val_result)

        # signup
        signup_res, signup_val = auth.signup_user(processed_input)
        if not signup_res:
            return jsonify(status=signup_val), 400

    return jsonify(status="User signed in"), 201


@api.route('/api/login', methods=['POST'])
def login():
    data = json.loads(request.get_data().decode('utf-8'))
    type_of_auth = data.get('type', None)
    if not type_of_auth:
        return jsonify(status="No type provided"), 400
    
    # Modular part
    if type_of_auth == 'captcha':
        return jsonify(status="Incorrect type"), 400
        # auth = CaptchaAuth()
    elif type_of_auth == 'password':
        auth = PasswordAuth()
    else:
        return jsonify(status="Incorrect type"), 400
    
    # Check input
    val_status, val_result = auth.check_input(data)
    if not val_status:
        return jsonify(status=val_result), 400

    # Process Input
    processed_input = auth.process_input(val_result)

    # login user
    login_res, login_val = auth.login_user(processed_input)
    if not login_res:
        return jsonify(status=login_val), 403

    return jsonify(status="Login Successful"), 200



# @api.route('/', defaults={'path': ''})
# @api.route('/<path:path>')
# def index(path):
#     return "Welcome"
    # return render_template("index.html")
