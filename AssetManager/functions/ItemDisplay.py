'''
Used to setup info for a file
Where info is a list of tuples consisting of a name and a value:
info =  [ ('Name: ', 'JohnDoe'), ('Age: ', '30') ]
'''

def textRow(info):
    '''Adds row of text'''
    textRow = ''
    for item, value in info:
        if value.strip():
            textRow += item + value
    return(textRow)  

def itemDisplay(info):
    '''Builds description'''
    text = ''
    lines = []
    for item, value in info:
        rowOfText = textRow([(item, value)])
        tempText = text
        text += rowOfText
        if len(text) > 100: #If very long line of text, break before and after
            text = tempText + '\n' + rowOfText + '\n'
            lines += text,
            text = ''
        elif len(text) > 40: #If Long line, break before
            text += '\n'
            lines += text,
            text = ''
        elif 0 < len(text) < 40: #If short line add tab
            text += '      '
    lines += text
    text = ''
    for line in lines:
        text += line
    return(text)