'''Reads and writes ini files'''
'''Uses \n to separate keys and values'''
''' 
    data = '#Example:'
    section = ['Colors', 'Flavors']
    key = ['Dark', 'Light', '\n', 'Sweet', 'Salty'] 
    value = ['Black', 'Blue', '\n', 'White, 'Yellow', '\n', 'Candy', 'Soda', '\n', 'Peanuts', 'Chips'] 
    data = build(data, section, key, value)
    write(data, location)
'''

import ConfigParser    

def addSection(data, section):
    '''Adds Section to log file'''
    data += "\n\n[" + section + "]"
    return(data)

def addKey(data, key, value):
    '''Adds Key and values to log file'''
    if type(value) == list:
        data += '\n' + key + ' = ' 
        for item in value:
            data += item + '\n\t'
    else:    
        data += "\n" + key + "=" + value
    return(data)

def build(data, section, key, value):
    '''Builds log file'''
    for onesection in section:
        data = addSection(data, onesection)
        for number, onekey in enumerate(key):
            if onekey == '\n':
                del key[0:number + 1]
                break
            values = []
            for number, onevalue in enumerate(value):
                if onevalue == '\n':
                    del value[0:number +1]
                    break
                else:
                    values += onevalue,
            data = addKey(data, onekey, values)
    return(data)

def write(data, location):
    '''Writes log file'''
    file = open(location, 'w+')
    file.write(data)
    file.close
    
def read(location):
    '''Reads log file'''
    dict = {}
    config = ConfigParser.ConfigParser()
    config.read(location)
    sections = config.sections()
    for onesection in sections:
        keys = config.options(onesection)
        for onekey in keys:
            dict[onekey] = config.get(onesection, onekey)
    return(dict)