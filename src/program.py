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

# Check if str is in format
# Format = 1 -> "str"
# Format = 2 -> (str)
def isSTRinFormat(value, format):
    if(format == 1 and (len(value) < 2 or value[0] != '"' or value[-1] != '"')):
        return False
    elif(format == 2 and (len(value) < 2 or value[0] != "(" or value[-1] != ")")):
        return False
    return True

# Binary search for id in given list
def binarySearchID(list, id):
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = (low + high) // 2
        if list[mid]['id'] == id:
            return mid
        elif list[mid]['id'] > id:
            high = mid - 1
        else:
            low = mid + 1
    return -1

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
    
    # Sort data by id
    data_list.sort(key=lambda x: x['id'])

    # While loop for user input
    while(True):
        # Get user input
        userinput = input('Enter command: ').lstrip().rstrip()
        
        # Remove extra spaces
        while('  ' in userinput):
            userinput = userinput.replace('  ',' ')
        
        # Parse user input
        parsed = userinput.split(' ')

        # If command is select get user keys
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

            # If command is not correct
            flag = False

            # Condition
            condition = 0
            if(len(parsed) == 11):
                condition = 1
            elif(len(parsed) == 15 and (parsed[8] == 'AND' or parsed[8] == 'OR')):
                condition = 2
            else:
                print('Your format is wrong!')
                print('SELECT {ALL|column_name} FROM STUDENTS WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR} ORDER BY{ASC|DSC}')
                continue

            for i in range(0, condition):
                
                # If cond is name or lastname
                if(parsed[5 + (i * 4)] == 'name' or parsed[5 + (i * 4)] == 'lastname' or parsed[5 + (i * 4)] == 'email'):
                    
                    if(isSTRinFormat(parsed[7 + (i * 4)], 1)):
                        parsed[7 + (i * 4)] = parsed[7 + (i * 4)][1:-1]
                    else:
                        flag = True
                        break

                    if(parsed[6 + (i * 4)] == '='):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] == parsed[7 + (i * 4)]:
                                selected_data[i].append(row)
                    elif(parsed[6 + (i * 4)] == '!='):
                        for row in data_list:
                            if row[parsed[5 + (i * 4)]] != parsed[7 + (i * 4)]:
                                selected_data[i].append(row)
                    else:
                        flag = True
                        break
                    
                # If cond is id or grade
                # Operations = ['=','!=','<','>','<=','>=','!<','!>','AND','OR']
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
                        flag = True
                        break

            # If command is not correct  
            if(flag):
                print('Your format is wrong!')
                print('SELECT {ALL|column_name} FROM STUDENTS WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR} ORDER BY{ASC|DSC}')
                continue

            merged_data = []

            if(condition == 2 and parsed[8] == 'AND'):

                # Binary search can be used for faster search
                for row in selected_data[0]:
                    if (binarySearchID(selected_data[1], row['id']) != -1):
                        merged_data.append(row)

            elif(condition == 2 and parsed[8] == 'OR'):

                # Add two lists and remove duplicates from list (by using set, tuple)
                merged_data = selected_data[0]

                for row in selected_data[1]:
                    if (binarySearchID(merged_data, row['id']) == -1):
                        merged_data.append(row)
            elif(condition == 1):
                merged_data = selected_data[0]
       
            # Sort selected data
            if(userinput.endswith('ORDER BY ASC')):
                merged_data.sort(key=lambda x: x['id'])
            elif(userinput.endswith('ORDER BY DSC')):
                merged_data.sort(key=lambda x: x['id'], reverse=True)

            # Print selected data
            for row in merged_data:
                for key in user_keys:
                    print(row[key], end=' ')
                print()

            # Write selected data to json file if wanted
            # WriteJson(merged_data)

            # We did not want to change the original data_list so we did not write the selected data to json file
            # if we want to change the original data_list we can write the selected data to json file
            # data_list = merged_data
            # WriteJson()
            # data_list.sort(key=lambda x: x['id'])

        # INSERT COMMAND
        # Example: INSERT INTO STUDENTS VALUES(id name surname email grade)
        # Example: INSERT INTO STUDENTS VALUES(1,John,Doe,jhon.doe@gmail.com,20)
        elif(userinput.startswith('INSERT INTO STUDENTS VALUES') and len(parsed) == 4):

            # Check if user input is correct
            parsed[3] = parsed[3].replace('VALUES', '')
            keyValues = []
            flag = False

            if(isSTRinFormat(parsed[3], 2)):
                parsed[3] = parsed[3][1:-1]
                keyValues = parsed[3].split(',')

                if(len(keyValues) != 5):
                    flag = True
            else:
                flag = True

            # If user input is correct
            if(not flag):
           
                try:

                    # Check if id is already exist
                    if(binarySearchID(data_list, int(keyValues[0])) != -1):
                        print('This id is already exist!')
                        flag = True
                        continue

                    data_list.append({
                    keys[0]: int(keyValues[0]),
                    keys[1]: keyValues[1],
                    keys[2]: keyValues[2],
                    keys[3]: keyValues[3],
                    keys[4]: int(keyValues[4])
                    })
                except:
                    flag = True
            
            # If user command is wrong
            if(not flag):
                writeJson()
                data_list.sort(key=lambda x: x['id'])
            else:
                print('Your format is wrong!')
                print('INSERT INTO STUDENTS VALUES(id,name,surname,email,grade)')

        # DELETE COMMAND
        # Example: DELETE FROM STUDENT WHERE CONDITION
        # Example: DELETE FROM STUDENT WHERE {column_name|=,!=,<,>,<=,>=,!<,!>,AND,OR }     
        # Example: DELETE FROM STUDENT WHERE name = "Fatih"
        #           0       1   2       3      4  5    6                length = 7
        elif(userinput.startswith('DELETE FROM STUDENT WHERE')):
            firstcond_deleted_data = []
            deleted_data = [[],[]]

            delete_condition = 0
            if len(parsed) == 7:  # just 1 condition
                delete_condition=1
            elif len(parsed) == 11 and(parsed[7] == 'AND' or parsed[7] == 'OR'):  # 2 condition
                delete_condition=2
            else:
                print('Your format is wrong!')
                continue

            if len(parsed) == 7 and delete_condition==1:  # just 1 condition
                if(parsed[4] == 'name' or parsed[4] == 'lastname' or parsed[4] == 'email'):
                    parsed[6] = parsed[6].translate( { ord('"'): None } )
                    for row in data_list:
                        if row[parsed[4]] == parsed[6]:
                            firstcond_deleted_data.append(row)

                elif(parsed[4] == 'id' or parsed[4] == 'grade'):
                    if(parsed[5] == '='):
                        for row in data_list:
                            if row[parsed[4]] == int(parsed[6]):
                                firstcond_deleted_data.append(row)

                    elif(parsed[5] == '!='):
                        for row in data_list:
                            if row[parsed[4]] != int(parsed[6]):
                                firstcond_deleted_data.append(row)

                    elif(parsed[5] == '<'):
                        for row in data_list:
                            if row[parsed[4]] < int(parsed[6]):
                                firstcond_deleted_data.append(row)

                    elif(parsed[5] == '>'):
                        for row in data_list:
                            if row[parsed[4]] > int(parsed[6]):
                                firstcond_deleted_data.append(row)

                    elif(parsed[5] == '<='):
                        for row in data_list:
                            if row[parsed[4]] <= int(parsed[6]):
                                firstcond_deleted_data.append(row)
       
            # Example: DELETE FROM STUDENT WHERE name = "Fatih" AND grade = 20
            #           0       1   2       3      4  5    6    7    8    9 10 length = 11         
            elif(len(parsed)==11 and (parsed[7] == 'AND' or parsed[7] == 'OR')):
                
                for i in range(0, delete_condition):
                     # If condition is name or lastname or email
                    if(parsed[4 + (i * 4)] == 'name' or parsed[4 + (i * 4)] == 'lastname' or parsed[4 + (i * 4)] == 'email'):
                        parsed[6 + (i * 4)] = parsed[6 + (i * 4)].translate( { ord('"'): None } )
                        if(parsed[5+(i*4)]=='='):
                            for row in data_list:
                                if row[parsed[4+(i*4)]]==parsed[6+(i*4)]:
                                    deleted_data[i].append(row)
                                    
                    # If condition is id or grade
                    elif(parsed[4 + (i * 4)] == 'id' or parsed[4 + (i * 4)] == 'grade'):
                        if(parsed[5 + (i * 4)] == '='):
                            for row in data_list:
                                if row[parsed[4 + (i * 4)]] == int(parsed[6 + (i * 4)]):
                                    deleted_data[i].append(row)
                                    
                        elif(parsed[5 + (i * 4)] == '!='):
                            for row in data_list:
                                if row[parsed[4 + (i * 4)]] != int(parsed[6 + (i * 4)]):
                                    deleted_data[i].append(row)
                                    
                        elif(parsed[5 + (i * 4)] == '<'):
                            for row in data_list:
                                if row[parsed[4 + (i * 4)]] < int(parsed[6 + (i * 4)]):
                                    deleted_data[i].append(row)
                                    
                        elif(parsed[5 + (i * 4)] == '>'):
                            for row in data_list:
                                if row[parsed[4 + (i * 4)]] > int(parsed[6 + (i * 4)]):
                                    deleted_data[i].append(row)
                                    
                                    
                        elif(parsed[5 + (i * 4)] == '<=' or parsed[5 + (i * 4)] == '!>'):
                            for row in data_list:
                                if row[parsed[4 + (i * 4)]] <= int(parsed[6 + (i * 4)]):
                                    deleted_data[i].append(row)
                                    
                                    
                        elif(parsed[5 + (i * 4)] == '>=' or parsed[5 + (i * 4)] == '!<'):
                            for row in data_list:
                                if row[parsed[4 + (i * 4)]] >= int(parsed[6 + (i * 4)]):
                                    deleted_data[i].append(row)
                                    
                    else:
                        print("Wrong command! or Your format is wrong!")
                        continue

                merged_deleted_data =[]
                if(parsed[7]=='AND'):#merging deleted data
                    for row in deleted_data[0]:
                        if row in deleted_data[1]:
                            merged_deleted_data.append(row)
                elif(parsed[7]=='OR'):#adding the list of the data to be deleted
                    merged_deleted_data = deleted_data[0] + deleted_data[1]
                flag=False 
                for row in data_list:#removing merged deleted data from data_list
                    if row in merged_deleted_data:
                        print("Deleted data is:")
                        print(row)
                        data_list.remove(row)
                        flag=True
                        writeJson()
                    if flag==False:
                        print("There is no such a data")
                        break
            if(len(parsed)==7):
                for row in data_list:
                    if row in firstcond_deleted_data: 
                        print("Deleted data is:")
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



