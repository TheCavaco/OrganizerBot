import os


def checkNum(num:str):
    try:
        int(num)
    except ValueError:
        return False
    return True

def create_file(filename:str):
    try:
        if not os.path.exists(filename):
            # If it doesn't exist, create and write to the file
            with open(filename, 'w') as file:
                file.write("This is a new file.")
        else:
            print("file already exists")
    except IOError as e:
        print(f"An error occurred: {e}")


def handle_response(message:str, token, filename: str):
    # message type -> 92475;Henrique Cavaco;4
    # RESPONSES : CREATE, ADD, NOTHING
    p_spl = message.split(sep=token)
    if token == " ":
        if (len(p_spl) <= 3) or  not checkNum(p_spl[0]) or not checkNum(p_spl[len(p_spl) - 1]) or len(p_spl[0]) < 4 or len(p_spl[len(p_spl) - 1]) > 2:
            print("Wrong format message 1: " + message)
            return "NOTHING", None
    elif (len(p_spl) != 3) or  not checkNum(p_spl[0]) or not checkNum(p_spl[2]) or len(p_spl[0]) < 4 or len(p_spl[2]) > 2:
        print("Wrong format message 2: " + message)
        return "NOTHING", None
    
    name = ""
    number = p_spl[0]
    if token == " ":
        name = p_spl[1]
        for i in range(2, len(p_spl) - 1):
            name += " " + p_spl[i]
    else: 
        name = p_spl[1]

    if token == " ":  
        group = p_spl[len(p_spl) - 1]
    else:
        group = p_spl[2]


    if len(group) == 1:
        group = "0"+group


    # CHECK IF GROUP EXISTS
    # RETURN
    create_file(filename)
    current = "CREATE"
    data = number + ";" + group + ";" + '\n'

    with open(filename, 'r') as file:
        lines = file.readlines()
        print(str(lines))
        for line_number, line in enumerate(lines, start=0):
            sp = line.split(";")
            if sp[0] == number:
                return "NOTHING", None
            elif sp[1] == group:
                current = "ADD"

    
    with open(filename, 'a') as file:
        print("Writing: " + data)
        file.write(data)



    l = [number, name, group]
    

    return current, l



