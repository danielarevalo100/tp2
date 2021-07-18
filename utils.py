from os import system, name

def clear():   
    if name == 'nt':   
        _ = system('cls')   
    else:   
        _ = system('clear') 


def printMenu( menu ) -> None:
    selectedItem = 0
    optionSelected = False

    
    while not optionSelected: 
        clear()
        for i in range(len(menu)):
            print( menu[i]  + '>>>' if selectedItem == i else menu[i])

        value = input('Usa w/s para subir o bajar, luego selecciona con enter')

        if value == 's' and selectedItem < len(menu) -1 :
            selectedItem += 1
        if value == 'w' and selectedItem != 0:
            selectedItem -= 1
        if value == '':
            optionSelected = True
    return selectedItem

def find(callback, arr) :
    for i in range(len(arr)):
        if callback(arr[i], i):
            return arr[i]
    return False

def requestNumber( text, errorText ):
    val = ''
    error = False;
    while not val.isnumeric():
        val = input(errorText if error else text)
        error = True
    return int(val)

def requestData( keys ) :
    # will recieve { title: text to show, field: field to return }
    result = {}
    for key in keys:
        if 'numeric' in key:
            result[key['field']] = requestNumber(f"ingrese {key['title']}", f"error ingrese {key['title']}")
        else:
            result[key['field']] = input(f"ingrese {key['title']}")

    return result   

