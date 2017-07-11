## Mauro Victor Castro

import urllib.request
import urllib.parse
'''
    Module for helping functions, in order to organize the code in the main file
'''

def get_coordinates(REQUEST_STRING):
    if REQUEST_STRING == '[]': ## If the string data from request is empty return empty list
        print('EMPTY REQUEST COMMANDS')
        return []
    try:
            ## In other case treat the data in order to get the pair of coordinates.
            values = REQUEST_STRING.replace('[','')
            values = values.replace(']','')
            values = values.split(',')
            x_values = [int(values[i]) for i in range(0,len(values),2)]
            y_values = [int(values[i]) for i in range(1,len(values),2)]
            return list(zip(x_values, y_values))

    except Exception as e:
        print('')
        print('get_coordinates_error')
        print(e)
        return e

def generate_commands(coordinates):

    try:
        if coordinates == []:
            commands = [0 for i in range(8)]
            return commands
        else:
            columns = [pair[0] for pair in coordinates]
            commands = []
            for i in range(1,9):
                if i not in columns:
                    commands.append(0)
                else:
                    bits = [pair[1] for pair in coordinates if pair[0]==i]
                    byte = [pow(2, (j-1)) for j in bits]
                    byte = sum(byte)
                    commands.append(byte)
            commands.reverse()
            return commands

    except Exception as e:
        print('')
        print('generate_commands_error')
        print(e)
        return e

def generate_url(commands, ip):
    try:
        data = {}
        iterable_base = list(range(1,9))
        iterable_base.reverse()
        for idx,i in enumerate(iterable_base):
            data['byte_{0}'.format(i)] = commands[idx] ##add command values to dictionary

        data_url = urllib.parse.urlencode(data)
        url = 'http://192.168.0.26/' + '?' + data_url
        print(url)
        urllib.request.urlopen(url)
        return

    except Exception as e:
        print('########')
        print('generate_url_error')
        print(e)
        return ''
