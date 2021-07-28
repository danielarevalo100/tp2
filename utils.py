from os import system, name

def clear():   
    if name == 'nt':   
        _ = system('cls')   
    else:   
        _ = system('clear') 


def ingresar_opcion(menu):
    print('\n')
    for i in range(len(menu)):
        print(menu[i])
    opcion = input('Que opcion desea elegir?: ')
    while not opcion.isnumeric() or int(opcion)<1 or int(opcion)>len(menu):
        opcion = input('Eliga una opcion correcta: ')
    opcion = int(opcion)
    return opcion

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

