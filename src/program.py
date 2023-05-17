import json
import csv

# File paths
csv_file_path = 'students.csv'
json_file_path = 'result.json'
# List to store data
data_list = []

# Write data to json file
def writeJson():
    with open(json_file_path, 'w') as file:
        json.dump(data_list, file, indent = 4, ensure_ascii=False)

# Main function
def main():

    
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            data_list.append(row)
        

    while(True):

        # Get user input
        userinput=input('Enter command: ')

        # Remove extra spaces
        while('  ' in userinput):
            userinput = userinput.replace('  ',' ')
        
        # Parse user input
        parsed = userinput.split(' ')
        
        # INSERT COMMAND
        # Example: INSERT INTO STUDENTS VALUES id name surname email grade
        # Example: INSERT INTO STUDENTS VALUES 1 John Doe jhon.doe@gmail.com 20
        if(userinput.startswith('INSERT INTO STUDENTS VALUES')):
            # Check if user input is correct
            if(len(parsed) == 9):
                keys = list(data_list[0].keys())
                data_list.append({
                    keys[0]: parsed[4],
                    keys[1]: parsed[5],
                    keys[2]: parsed[6],
                    keys[3]: parsed[7],
                    keys[4]: parsed[8]
                })

            # If user input is wrong
            else:
                print("Your values are wrong !")

        
        # DELETE COMMAND
        # Example: DELETE FROM STUDENTS WHERE CONDITION
        # Example: DELETE FROM STUDENTS WHERE id=1
        elif(userinput.startswith('DELETE FROM STUDENTS WHERE')):
            if len(parsed) == 5:  # just 1 condition
                column_name = parsed[4].split("=")[0]
                condition = parsed[4].split("=")[1]
                
                for row in data_list:
                    if row[column_name] == condition:
                        print(row)
                        data_list.remove(row)
                        writeJson()
            
        # EXIT COMMAND
        elif(userinput=="exit"):
            writeJson()
            exit()

        # WRONG COMMAND
        else:
            print("Wrong command !")

main()



