import json
import csv

# File paths
csv_file_path = 'students.csv'
json_file_path = 'result.json'
# List to store data
data_list = []
keys = []

# Write data to json file
def writeJson():
    with open(json_file_path, 'w') as file:
        json.dump(data_list, file, indent = 4, ensure_ascii=False)

# Main function
def main():

    # Keys of data
    keys = ['id','name','lastname','email','grade']

    # Read csv file    
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            data_list.append({
                    keys[0]: int(row[keys[0]]),
                    keys[1]: row[keys[1]],
                    keys[2]: row[keys[2]],
                    keys[3]: row[keys[3]],
                    keys[4]: int(row[keys[4]])
            })
    
    # While loop for user input
    while(True):

        # Get user input
        userinput = input('Enter command: ').lstrip().rstrip()

        # Remove extra spaces
        while('  ' in userinput):
            userinput = userinput.replace('  ',' ')
        
        # Parse user input
        parsed = userinput.split(' ')

        # Keys user wants to see if SELECT command
        user_keys = []
        if(parsed[0] == 'SELECT' and parsed[1] != 'ALL'):
            user_keys = parsed[1].split(',')
        elif(parsed[0] == 'SELECT' and parsed[1] == 'ALL'):
            user_keys = keys
        
        # SELECT COMMAND
        # EXAMPLE: SELECT ALL FROM STUDENTS WHERE CONDITION
        # EXAMPLE: SELECT {ALL|column_name} FROM STUDENTS WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR} ORDER BY{ASC|DSC}
        # EXAMPLE: SELECT name,lastname FROM STUDENTS WHERE grade !< 40 ORDER BY ASC
        # EXAMPLE: SELECT ALL FROM STUDENTS WHERE grade !< 40 AND grade !> 60 ORDER BY ASC
        if((len(parsed) == 11 or len(parsed) == 15) and parsed[0]=='SELECT' and all(var in keys for var in user_keys) 
           and parsed[2]=='FROM' and parsed[3]=='STUDENTS' and parsed[4]=='WHERE' 
           and (userinput.endswith('ORDER BY ASC') or userinput.endswith('ORDER BY DSC'))):

            # Selected data
            selected_data = [[],[]]

            # Condition
            condition = 0
            if(len(parsed) == 11):
                condition = 1
            if(len(parsed) == 15 and (parsed[8] == 'AND' or parsed[8] == 'OR')):
                condition = 2
            else:
                print('Your format is wrong!')
                print('SELECT {ALL|column_name} FROM STUDENTS WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR} ORDER BY{ASC|DSC}')
                continue

            # EXAMPLE: SELECT name,lastname FROM STUDENTS WHERE grade !< 40 ORDER BY ASC
            #           0      1             2      3        4    5    6  7  8     9  10  
            # EXAMPLE: SELECT ALL FROM STUDENTS WHERE grade !< 40 AND grade !> 60 ORDER BY ASC
            #           0      1    2      3     4       5   6  7  8   9    10 11  12   13  14
            # EXAMPLE: SELECT ALL FROM STUDENTS WHERE name = Sandy AND lastname = Schumm ORDER BY ASC
            for i in range(0, condition):
                
                # If cond is name or lastname
                if(parsed[5 + (i * 4)] == 'name' or parsed[5 + (i * 4)] == 'lastname' or parsed[5 + (i * 4)] == 'email'):
                    
                    if(parsed[6 + (i * 4)] == '='):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] == parsed[7 + (i * 4)]:
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '!='):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] != parsed[7 + (i * 4)]:
                                selected_data[i].append(row)
                    
                # operations = ['=','!=','<','>','<=','>=','!<','!>','AND','OR']
                # If cond is id or grade
                elif(parsed[5 + (i * 4)] == 'id' or parsed[5 + (i * 4)] == 'grade'):

                    if(parsed[6 + (i * 4)] == '='):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] == int(parsed[7 + (i * 4)]):
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '!='):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] != int(parsed[7 + (i * 4)]):
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '<'):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] < int(parsed[7 + (i * 4)]):
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '>'):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] > int(parsed[7 + (i * 4)]):
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '<=' or parsed[6 + (i * 4)] == '!>'):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] <= int(parsed[7 + (i * 4)]):
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '>=' or parsed[6 + (i * 4)] == '!<'):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] >= int(parsed[7 + (i * 4)]):
                                selected_data[i].append(row)
                
                else:
                    print('Your format is wrong!')
                    print('SELECT {ALL|column_name} FROM STUDENTS WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR} ORDER BY{ASC|DSC}')
                    continue

            merged_data = []

            if(parsed[8] == 'AND'):
                merged_data = [row for row in selected_data[0] if row in selected_data[1]]
            elif(parsed[8] == 'OR'):
                merged_data = selected_data[0] + selected_data[1]
                #my_list = [dict(t) for t in {tuple(sorted(d.items())) for d in my_list}]
                #merged_data = list(set(merged_data))
                merged_data = [dict(t) for t in {tuple(sorted(d.items())) for d in merged_data}]
            else:
                merged_data = selected_data[0]

            
            # Sort selected data
            if(userinput.endswith('ORDER BY ASC')):
                merged_data.sort(key=lambda x: x['id'])
            elif(userinput.endswith('ORDER BY DSC')):
                merged_data.sort(key=lambda x: x['id'], reverse=True)


            for row in merged_data:
                for key in user_keys:
                    print(row[key], end=' ')
                print()
                

        # INSERT COMMAND
        # Example: INSERT INTO STUDENTS VALUES id name surname email grade
        # Example: INSERT INTO STUDENTS VALUES 1 John Doe jhon.doe@gmail.com 20
        elif(userinput.startswith('INSERT INTO STUDENTS VALUES')):
            # Check if user input is correct
            if(len(parsed) == 9):

                try:
                    data_list.append({
                    keys[0]: int(parsed[4]),
                    keys[1]: parsed[5],
                    keys[2]: parsed[6],
                    keys[3]: parsed[7],
                    keys[4]: int(parsed[8])
                    })
                except:
                    print('Your values are wrong!')
                    print('Example: INSERT INTO STUDENTS VALUES id name surname email grade')

            # If user input is wrong
            else:
                print('Your values are wrong!')
                print('Example: INSERT INTO STUDENTS VALUES id name surname email grade')


        # DELETE COMMAND
        # Example: DELETE FROM STUDENTS WHERE CONDITION
        # Example: DELETE FROM STUDENT WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR }
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
            print("Wrong command!")

main()



