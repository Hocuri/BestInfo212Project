from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

URI = "neo4j+s://8b2aea2e.databases.neo4j.io"
AUTH = ("neo4j", "kkj4obvCz4EyhJG6XVHP2oMORQWy-vBDfon6LfPViLc")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        # nodes_json = [node_to_json(record["a"]) for record in cars]
        # print(nodes_json)
        return 'Ok'

def findCarByReg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
        # print(cars)
        # nodes_json = [node_to_json(record["a"]) for record in cars]
        # print(nodes_json)
        return 'Ok'

def save_car(make, model, reg, year, capacity):
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg, \
            year: $year, capacity:$capacity}) RETURN a;",
            make = make, model = model, reg = reg, year = year, capacity = capacity)
    
    print(cars.records)
    # nodes_json = [node_to_json(record["a"]) for record in cars]
    # print(nodes_json)
    # return nodes_json
    return 'Ok'

def update_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, \
                a.capacity = $capacity RETURN a;",
                reg=reg, make=make, model=model, year=year, capacity=capacity)
        # print(cars)
        # nodes_json = [node_to_json(record["a"]) for record in cars]
        # print(nodes_json)

        return 'Ok'

def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg = reg)

class Car:
    def __init__(self, model, year, location, status): #constructer method, calles når du lager en ny instans av car
        #self er en referanse til instansen av klassen som blir opprettet
        self.model = model
        self.year = year
        self.location = location
        self.status = status

#get metode, hent ut modellen
#retrieve the value of the model attribute
    def get_Model(self):
        return self.model

#set metode, sett modellen
#allows you to set or update the model attribute 
    def set_Model(self, value):
        self.model = value

    def get_Year(self):
        return self.year
    
    def set_Year(self, value):
        self.year = value

    def get_Location(self):
        return self.location
    
    def set_Location(self, value):
        self.location = value

    def get_Status(self):
        return self.status
    
    def set_Status(self, value):
        self.status = value



#Customer

class Customer:
    def __init__(self, name, age, adress): #constructer method, calles når du lager en ny instans av car
        #self er en referanse til instansen av klassen som blir opprettet
        self.name = name
        self.age = age
        self.adress = adress

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

def order_car(customer_id, reg):
    with _get_connection().session() as session:
        if session.run("MATCH (u:Customer {customer_id: $customer_id})-[:BOOKED]->();", customer_id=customer_id) > 0:
            print("This customer has already booked a car")
            return
        if session.run("MATCH ()-[:BOOKED]->(c:Car {reg: $reg});", reg=reg) > 0:
            print("This car is already booked")
            return

        cars = session.run("MATCH (a:Car{reg:$reg}), c:Customer{customer_id} CREATE(c)-[:BOOKED]->(c);",
                reg=reg, make=make, model=model, year=year, capacity=capacity)

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

    
    
