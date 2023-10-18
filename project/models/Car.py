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