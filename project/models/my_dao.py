from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
from flask import jsonify

URI = "neo4j+s://8b2aea2e.databases.neo4j.io"
AUTH = ("neo4j", "kkj4obvCz4EyhJG6XVHP2oMORQWy-vBDfon6LfPViLc")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

# Returns list of all cars
def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

# Returns car by reg
def findCarByReg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

# Saves car, returns 201 status
def save_car(make, model, reg, year, capacity):
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg, \
            year: $year, capacity:$capacity}) RETURN a;",
            make = make, model = model, reg = reg, year = year, capacity = capacity)
    return jsonify('Car created'), 201 

# Updates and returns car
def update_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, \
                a.capacity = $capacity RETURN a;",
                reg=reg, make=make, model=model, year=year, capacity=capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        return nodes_json

# Deletes car
def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg = reg)
    return jsonify('Car deleted'), 200


#Customer
# Saves customer, returns 201 status
def save_customer(name, age, adress, customer_id):
    customer = _get_connection().execute_query("MERGE (a:Customer{name: $name, age: $age, adress: $adress, \
            customer_id: $customer_id}) RETURN a;",
            name = name, age = age, adress = adress, customer_id = customer_id)
    return jsonify('Customer created'), 201


def update_customer(name, age, adress, customer_id):
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer{customer_id:$customer_id}) set a.name=$name, a.age=$age, a.adress = $adress, \
                RETURN a;",
                name=name, age=age, adress=adress, customer_id=customer_id)
        nodes_json = [node_to_json(record["a"]) for record in customers]
        return nodes_json
    

def delete_customer(customer_id):
    _get_connection().execute_query("MATCH (a:Customer{customer_id: $customer_id}) delete a;", customer_id = customer_id)
    return jsonify("Customer deleted"), 200

def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json

# Returns car by reg
def findCustomerById(customer_id):
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) where a.customer_id=$customer_id RETURN a;", customer_id=customer_id)
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json

class Customer:
    def __init__(self, name, age, adress, customer_id): #constructer method, calles når du lager en ny instans av car
        #self er en referanse til instansen av klassen som blir opprettet
        self.name = name
        self.age = age
        self.adress = adress
        self.customer_id = customer_id

    def get_Name(self):
        return self.name

    def set_Name(self, value):
        self.name = value

    def get_Age(self):
        return self.age
    
    def set_Age(self, value):
        self.age = value

    def get_Adress(self):
        return self.adress
    
    def set_Adress(self, value):
        self.adress = value

    def get_Customer_id(self):
        return self.customer_id
    
    def set_Customer_id(self, value):
        self.customer_id = value

def order_car(customer_id, reg):
    with _get_connection().session() as session:
        if session.run("MATCH (u:Customer {customer_id: $customer_id})-[b:BOOKED]->() RETURN COUNT(b)", customer_id=customer_id).single()[0] > 0:
            return jsonify("This customer has already booked a car"), 400
        if session.run("MATCH ()-[b:BOOKED]->(c:Car {reg: $reg}) RETURN COUNT(b)", reg=reg).single()[0] > 0:
            return jsonify("This car is already booked"), 400

        session.run("MATCH (c:Car {reg: $reg}), (u:Customer {customer_id: $customer_id}) CREATE (u)-[:BOOKED]->(c);",
                customer_id=customer_id, reg=reg)
        session.run("MATCH (c:Car{reg:$reg}) set c.status=$status", reg=reg, status="booked")
        return jsonify('ok'), 200


def cancel_order_car(customer_id, reg):
    with _get_connection().session() as session:
        if session.run("MATCH (u:Customer {customer_id: $customer_id})-[b:BOOKED]->(c:Car {reg: $reg}) RETURN COUNT(b)",
                        customer_id=customer_id, reg=reg).single()[0] > 0:
            session.run("MATCH (u:Customer {customer_id: $customer_id})-[b:BOOKED]->(c:Car {reg: $reg})\
                        set c.status=$status\
                        DELETE b",
                        customer_id=customer_id, reg=reg, status="available")
            return jsonify('Order cancelled'), 200
        else:
            return jsonify("This customer hasn't booked this car, so it can't be cancelled."), 400

def rent_car(customer_id, reg):
    with _get_connection().session() as session:
        if session.run("MATCH (u:Customer {customer_id: $customer_id})-[b:BOOKED]->(c:Car {reg: $reg}) RETURN COUNT(b)",
                        customer_id=customer_id, reg=reg).single()[0] > 0:
            session.run("MATCH (u:Customer {customer_id: $customer_id})-[b:BOOKED]->(c:Car {reg: $reg})\
                        set c.status=$status\
                        CREATE(u)-[:RENTED]->(c)\
                        DELETE b",
                        customer_id=customer_id, reg=reg, status="rented")
            return jsonify("Ok"), 200

        else:
            return jsonify("This customer hasn't booked this car, so it can't be rented."), 400

def return_car(customer_id, reg, car_status):
    with _get_connection().session() as session:
        if session.run("MATCH (u:Customer {customer_id: $customer_id})-[r:RENTED]->(c:Car {reg: $reg}) RETURN COUNT(r)",
                        customer_id=customer_id, reg=reg).single()[0] > 0:

            new_status = "available" if car_status == "ok" else "damaged"
            session.run("MATCH (u:Customer {customer_id: $customer_id})-[r:RENTED]->(c:Car {reg: $reg}) \
                        set c.status=$status \
                        DELETE r",
                        customer_id=customer_id, reg=reg, status=new_status)
            return jsonify("Ok"), 200

        else:
            return jsonify("This customer hasn't rented this car, so it can't be returned."), 400
            

#Employee

class Employee:
    def __init__(self, name, adress, branch): #constructer method, calles når du lager en ny instans av car
        #self er en referanse til instansen av klassen som blir opprettet
        self.name = name
        self.adress = adress
        self.branch = branch

    def get_Name(self):
        return self.name

    def set_Name(self, value):
        self.name = value

    def get_Adress(self):
        return self.adress
    
    def set_Adress(self, value):
        self.adress = value

    def get_Branch(self):
        return self.branch
    
    def set_Branch(self, value):
        self.branch = value


def save_employee(name, adress, branch):
    employee = _get_connection().execute_query("MERGE (a:Employee{name: $name, adress: $adress, \
            branch: $branch}) RETURN a;",
            name = name, adress = adress, branch = branch)
    return jsonify('Employee created'), 201


def update_employee(name, adress, branch):
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee{name:$name}) set a.adress = $adress, a.branch = $branch \
                RETURN a;",
                name=name, adress=adress, branch=branch)
        nodes_json = [node_to_json(record["a"]) for record in employees]
        return nodes_json
    

def delete_employee(name):
    _get_connection().execute_query("MATCH (a:Employee{name: $name}) delete a;", name = name)

def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employees]
        print(nodes_json)
        return nodes_json

# Returns employee by name
def findEmployeesByName(name):
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) where a.name=$name RETURN a;", name=name)
        nodes_json = [node_to_json(record["a"]) for record in employees]
        print(nodes_json)
        return nodes_json

    
    
