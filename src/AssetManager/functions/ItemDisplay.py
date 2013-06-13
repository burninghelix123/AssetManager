'''Modual that populates asset information for Asset Manager'''

def itemDisplay(fileField, locationField, nameField,
                categoryField, tagsField, statusField,
                dateField, authorField, versionField,
                commentsField):
    text = 'File:   '
    text += fileField
    text += '\nLocation:   '
    text += locationField
    text += '\n'        
    if not (nameField == '' or nameField == ' '):
        text += 'Name:   '
        text += nameField
        exists = 1
    else:
        exists = 0
    if exists == 1:
        text += '        '
    if not (categoryField == '' or categoryField == ' '):
        text += 'Category:   '
        text += categoryField
        exists2 = 1
    else:
        exists2 = 0
    if exists == 1 or exists2 == 1:
        text += '\n'
    if not (tagsField == '' or tagsField == ' '):
        text += 'Tags:   '
        text += tagsField
        exists = 1
    else:
        exists = 0
    if exists == 1:
        text += '        '
    if not (statusField == '' or statusField == ' '):
        text += 'Status:   '
        text += statusField
        exists2 = 1
    else:                        
        exists2 = 0
    if exists == 1 or exists2 == 1:
        text += '\n'
    if not (dateField == '' or dateField == ' '):
        text += 'Date:   '
        text += dateField
        exists = 1
    else:
        exists = 0
    if exists == 1:
        text += '        '
    if not (authorField == '' or authorField == ' '):
        text += 'Author:   '
        text += authorField
        exists2 = 1
    else:
        exists2 = 0
    if exists2 == 1:
        text += '        '
    if not (versionField == '' or versionField == ' '):
        text += 'Version:   '
        text += versionField
        exists3 = 1
    else:
        exists3 = 0
    if exists == 1 or exists2 == 1 or exists3 == 1:
        text += '\n'
    if not (commentsField == '' or commentsField == ' '):
        text += 'Comments:   '
        text += commentsField
        exists = 1
    return(text)
