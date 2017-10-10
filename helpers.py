## Mauro Victor Castro
import urllib.request
import urllib.parse
import database_helper
from flask import redirect

'''
    Module for helping functions, in order to organize the code in the main file
'''

'''
Get the coordinates of the dot contacts on the contact matrix
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
    data = {}
    iterable_base = list(range(8))
    iterable_base.reverse()
    for idx,i in enumerate(iterable_base):
        data['byte_{0}'.format(i)] = commands[idx] ##add command values to dictionary

    data_url = urllib.parse.urlencode(data)
    try:
        wifi_connection = True
        url = 'http://'+ ip + '/?' + data_url
        print(url)
        urllib.request.urlopen(url)
        return True

    except Exception as e:
        wifi_connection = False
        print('########')
        print('generate_url_error')
        print(e)
        return False

def activate_phase_url(ip):
    try:
        url='http://' + ip + '/activate_phase'
        urllib.request.urlopen(url)
        return True
    except Exception as e:
        print('----------')
        print()
        print('Problem with /activate_phase request')
        print()
        print('----------')
        return False

def activate_protec_url(ip):
    try:
        url='http://' + ip + '/activate_protec'
        urllib.request.urlopen(url)
        return True
    except Exception as e:
        print('----------')
        print()
        print('Problem with /activate_protec request')
        print()
        print('----------')
        return False



def get_picture_path(deffect, board_name, size):
    if size == 'large':
        path = "static/pictures/editions/large_" + deffect + "_" + board_name + ".png"
        return path
    if size == 'small':
        path = "static/pictures/editions/small_" + deffect + "_" + board_name + ".png"
        return path
