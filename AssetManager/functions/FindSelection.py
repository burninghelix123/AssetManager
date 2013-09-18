def findSelection(listVar):
    '''Find selected item/asset'''
    items = listVar.count()
    fileToOpen = ''
    selectedItems=[]
    rangedList =range(items)
    for i in rangedList:
        if listVar.isItemSelected(listVar.item(i))==True:
            fileToOpen = listVar.item(i).statusTip()
    return(fileToOpen)
