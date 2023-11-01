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

# ===== CREATE =====
@app.route('/save_customer', methods=["POST"])
def save_customer_info():
    record = request.form
    return save_customer(record['name'], record['age'], record['adress'], record['customer_id'])

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

