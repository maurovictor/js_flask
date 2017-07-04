def get_coordinates(MY_LIST):
    try:
        values = MY_LIST.replace('[','')
        values = values.replace(']','')
        values = values.split(',')
        x_values = [int(values[i]) for i in range(0,len(values),2)]
        y_values = [int(values[i]) for i in range(1,len(values),2)]

        return list(zip(x_values, y_values))
    except Exception as e:
        return e

def generate_commands(coordinates):
    '''
    try:
        columns = [pair[0] for pair in coordinates]
        commands = []
        for i in range(1,9):
            if i not in columns:
                commands.append('0b00000000')
            else:


    except Exception as e:
        return e
    '''
