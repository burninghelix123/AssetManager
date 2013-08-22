import ConfigParser

def addSection(data, section):
    "Add a section delimiter to the INI file"
    data += "\n\n[" + section + "]"
    return(data)

def addKey(data, key, value):
    "Writes a string to the INI file"
    if type(value) == list:
        data += '\n' + key + ' = ' 
        for item in value:
            data += item + '\n\t'
    else:    
        data += "\n" + key + "=" + value
    return(data)

def build(data, section, key, value):
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
    file = open(location, 'w+')
    file.write(data)
    file.close
    
def read(location):    
    dict = {}
    config = ConfigParser.ConfigParser()
    config.read(location)
    sections = config.sections()
    for onesection in sections:
        keys = config.options(onesection)
        for onekey in keys:
            dict[onekey] = config.get(onesection, onekey)
    return(dict)

if __name__ == '__main__':
    
    data = '#Header Information'
    section = ['cake', 'shapes', 'colors'] 
    key = ['chocolate', 'vanilla', 'strawberry', '\n', 'circle', 'square', 'triangle', '\n', 'red', 'black', 'yellow', 'blue']
    value = ['1234','2234','3234','\n','\n','\n','1','\n','1','2','3','\n','1','2','3','\n','1','2','3','\n','1','2','3','\n','1','2','3','\n','1','2','3','\n',] 
    data = build(data, section, key, value)
    
    location = 'C:/users/helix/test.txt'
    write(data, location)
    data = read(location)
