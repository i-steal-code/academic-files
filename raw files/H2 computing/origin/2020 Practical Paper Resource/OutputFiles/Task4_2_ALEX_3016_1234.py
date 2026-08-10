class Person:

    def __init__(self,name,dob):
        self.full_name = name
        self.date_of_birth = dob

    def is_adult(self):
        import datetime
        this_year = datetime.datetime.today().year
        dob_year, dob_month, dob_day  = self.date_of_birth.split('-')
        if int(this_year) - int(dob_year) > 18:
            return True
        else:
            return False

    def screen_name(self):
        dob_year, dob_month, dob_day  = self.date_of_birth.split('-')
        full_name = ""
        for char in self.full_name:
            if char.isalpha():
                full_name += char        
        screenName = full_name + dob_month + dob_day
        return screenName

    def status(self):
        return "Person"

    def getFullName(self):
        return self.full_name

    def getDOB(self):
        return self.date_of_birth

    def setFullName(self,name):
        self.full_name = name
        self.date_of_birth = dob

class Staff(Person):

    def __init__(self,name,dob):
        super().__init__(name,dob)

    def screen_name(self):
        return self.getFullName() + "Staff"
    
    def is_adult(self):
        return True

    def status(self):
        return "Staff"

class Student(Person):

    def __init__(self,name,dob):
        super().__init__(name,dob)

    def is_adult(self):
        return False

    def status(self):
        return "Student"

file = open("people.txt",'r')
all_info = []
for line in file:
    name,dob,status = line.strip().split(',')
    if status == 'Person':
        all_info.append(Person(name, dob))
    elif status == 'Staff':
        all_info.append(Staff(name, dob))
    elif status == 'Student':
        all_info.append(Student(name, dob))
file.close()

input("Ready to insert all information from file into 'school.db'") #pause after print message, press enter
import sqlite3
db = sqlite3.connect("school.db")
for line in all_info:
    db.execute("INSERT INTO People(FullName,DateOfBirth,ScreenName,IsAdult) VALUES\
(?,?,?,?)",(line.getFullName(),line.getDOB(),line.screen_name(),line.is_adult()))
db.commit()
db.close()
