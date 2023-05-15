import json
import csv

class Student:
    def __init__(self, id, name, surname, email, grade):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.grade = grade
    
    def get_info(self):
        return f"{self.id} {self.name} {self.surname} {self.email} {self.grade}"


csv_file_path = "students.csv"
json_file_path = "result.json"
students = []

def writeJson():
    with open(json_file_path, 'w') as file:
        json.dump(students, file, default=lambda o: o.__dict__, indent=4)

def main():

    


    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            #print(row)

            if(len(row) != 5):
                print("Error: Invalid CSV file format")
                #exit()
            else:
                students.append(Student(row[0], row[1], row[2], row[3], row[4]))

    while(True):
        userinput=input("Enter command: ")

        parsed=userinput.split(" ")
        # INSER INTO STUDENTS VALUES 31 MEHMET FATİH 31@GMAIL.COM 62

        if(parsed[0]=="INSERT" and parsed[1]=="INTO" and parsed[2]=="STUDENTS" and parsed[3]=="VALUES"):
            if(len(parsed) == 9):
                students.append(Student(parsed[4],parsed[5],parsed[6],parsed[7],parsed[8]))
                writeJson()

            else:
                print("Your values are wrong !")
        
        

        
        




        if(userinput=="exit"):
            writeJson()
            exit()







    








main()


