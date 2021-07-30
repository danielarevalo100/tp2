from os.path import isfile, join, isdir
from os import listdir, path
import os


def listar_archivos(basedir, profundidad = 0) : 
    espacios = ''
    for i in range(profundidad):
        espacios += '   '
    for elemento in listdir(basedir):
        if isdir(path.join(basedir, elemento)) and elemento != '.git':
            print(espacios, 'carpeta', elemento)
            listar_archivos(path.join(basedir, elemento), profundidad +1)
            print('')
        else:
            print(espacios,elemento)
