'''Used to setup text for items
Where info is a list of tuples consisting of a name and a value:
info =  [ ('Name: ', 'JohnDoe'), ('Age: ', '30') ]
'''

def textRow(info):
    textRow = ''
    for item, value in info:
        if value.strip():
            textRow += item + value
    return(textRow)  

def itemDisplay(info):
    text = ''
    lines = []
    for item, value in info:
        rowOfText = textRow([(item, value)])
        tempText = text
        text += rowOfText
        if len(text) > 100:
            text = tempText + '\n' + rowOfText + '\n'
            lines += text,
            text = ''
        elif len(text) > 40:
            text += '\n'
            lines += text,
            text = ''
        elif 0 < len(text) < 40:
            text += '      '
    lines += text
    text = ''
    for line in lines:
        text += line
    return(text)

