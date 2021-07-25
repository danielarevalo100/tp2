from os.path import isfile, join, isdir
from os import listdir
import os

def listar_directorio(ruta):
    print('Listado de carpetas en local: ')
    archivos = [a for a in listdir(ruta) if isfile(join(ruta, a))]
    
    print('\n')    
    return archivos

def listar_archivos() : 
    ruta = os.path.dirname(os.path.abspath(__file__))
    #listar_directorio(ruta)
    listado_archivos = listar_directorio(ruta)
    for i in range(len(listado_archivos)): 
        print(f"{i+1}) {listado_archivos[i]}")
