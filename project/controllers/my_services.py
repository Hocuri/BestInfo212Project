from project import app
from flask import render_template, request, redirect, url_for
from project.models.my_dao import *
import json

# ===========================================================
# CAR ENDPOINTS
# ===========================================================

# ===== READ =====
@app.route('/get_cars', methods=['GET'])
def query_records():
    return findAllCars()

@app.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    record = request.form
    return findCarByReg(record['reg'])

# ===== CREATE =====
@app.route('/save_car', methods=["POST"])
def save_car_info():
    record = request.form
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# ===== UPDATE =====
@app.route('/update_car', methods=['PUT'])
def update_car_info():
    record = request.form
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

# ===== DELETE =====
@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = request.form
    print(record)
    delete_car(record['reg'])
    return findAllCars()

# ===========================================================
# CUSTOMER ENDPOINTS
# ===========================================================

# ===== READ =====
@app.route('/get_customers', methods=["GET"])
def get_customers():
    return findAllCustomers()

@app.route('/get_customers_by_id', methods=["GET"])
def get_customer():
    record = request.form
    return findCustomerById(record['customer_id'])

# ===== CREATE =====
@app.route('/save_customer', methods=["POST"])
def save_customer_info():
    record = request.form
    return save_customer(record['name'], record['age'], record['adress'], record['customer_id'])

# ===== UPDATE =====
@app.route('/save_customer', methods=["PUT"])
def update_customer_info():
    record = request.form
    return update_customer(record['name'], record['age'], record['adress'], record['customer_id'])

# ===== DELETE =====
@app.route('/save_customer', methods=["DELETE"])
def delete_customer_info():
    record = request.form
    return delete_customer(record['customer_id'])


# ===========================================================
# ORDER ENDPOINTS
# ===========================================================

@app.route('/order_car', methods=['PUT'])
def make_order():
    record = request.form
    return order_car(record['customer_id'], record['reg'])

@app.route('/cancel_order_car', methods=['POST'])
def cancel_order():
    record = request.form
    return cancel_order_car(record['customer_id'], record['reg'])

@app.route('/rent_car', methods=['POST'])
def rent():
    record = request.form
    return rent_car(record['customer_id'], record['reg'])

@app.route('/return_car', methods=['POST'])
def return_rented_car():
    record = request.form
    return return_car(record['customer_id'], record['reg'], record['car_status'])

