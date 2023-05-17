import json
import csv




csv_file_path = "students.csv"
json_file_path = "result.json"
csv_dict = []

def writeJson():
        with open(json_file_path, 'w') as file:
             json.dump(csv_dict, file, indent = 4, ensure_ascii=False)

def main():

    


    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)

        
        for row in reader:
            csv_dict.append(row)
        

    while(True):
        userinput=input("Enter command: ")

        parsed=userinput.split(" ")
        # INSER INTO STUDENTS VALUES 31 MEHMET FATİH 31@GMAIL.COM 62

        if(userinput.startswith("INSERT INTO STUDENTS VALUES")):
            if(len(parsed) == 9):
                students.append(Student(parsed[4],parsed[5],parsed[6],parsed[7],parsed[8]))
                writeJson()

            else:
                print("Your values are wrong !")

        
        #"DELETE FROM STUDENTS WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR }"
        elif(userinput.startswith('DELETE FROM STUDENTS WHERE')):
            if len(parsed) == 5:  # just 1 condition
                column_name = parsed[4].split("=")[0]
                condition = parsed[4].split("=")[1]
                
                for row in csv_dict:
                    if row[column_name] == condition:
                        print(row)
                        csv_dict.remove(row)
                        writeJson()
            
        #  elif(len(parsed)==7):

            
            

        
        

        
        




        if(userinput=="exit"):
            writeJson()
            exit()



main()



