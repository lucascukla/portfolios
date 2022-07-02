# from numpy import average
from cmath import nan
from random import randint, random
from statistics import mean, median
from time import time_ns

class quicksort:
    pivote = ""         # pivote de mi algoritmo
    array = []          # array a ordenar
    flag_pivote = False # indica que no se coloco el pivote manualmente
    indice = 0          # indice donde se encuentra el pivote
    flag_ok = False     # indica cuando algo salio mal
    
    ##  constructores   ##
    def __init__(self, *args):                  # puede recibir varios argumentos
        if len(args) == 0 or len(args) > 2:     # si recibe menos de 1 o mas de 2 argumentos
            self.flag_ok = False                # rechaza la lista
            print("Faltan o sobran argumentos")
            return
        elif len(args) == 2:
            self.array = args[0]                # el primer argumento es la lista
            self.pivote = args[1]               # el segundo argumento, si existe, es el pivote
            if type(self.pivote) != type(0) and type(self.pivote) != type(0.0):
                print("Error en el tipo de dato del pivote")
                self.flag_ok = False
                return
        else:
            self.array = args[0]
        
        if len(self.array) > 1:     # si la longitud del array es muy corta no es necesario ordenar
            
            indice = 0                          # aca me fijo si hay datos que no son numericos y los elimino
            while self.flag_ok == False:
                largo_lista = len(self.array)
                if largo_lista == 0:
                    print("ningun elemento de la lista es un numero")
                    return
                
                if type(self.array[indice]) != type(0) and type(self.array[indice]) != type(0.0):     # recorro la lista para asegurarme que todos sean numeros
                    print("Error en datos del array, se eliminará el elemento numero", indice, " -> ", self.array[indice])
                    self.array.remove(self.array[indice])   # si un elemento no es un numero lo elimino
                else:
                    indice += 1                             # si el elemento era un numero incremento el índice
                
                if indice >= len(self.array):               # cuando el indice es igual a la longitud de la lista esta ok
                    self.flag_ok = True
                
            if len(self.array) == 0:    # si borró todos los datos
                print("array no tiene ningun valor numérico")
                self.flag_ok = False
                return
              
            if len(args) == 1:  # si solo tengo un argumento tengo que calcular mi pivote
                self.pivote = mean(self.array)  # el pivote tiene que estar al medio de los datos
                
            # print("pivote: ", self.pivote)
            if self.pivote != "":
                # self.indice = self.array.index(self.pivote) # obtengo el indice donde esta el pivote
                self.flag_ok = True
            else:
                self.flag_ok = False
        elif len(self.array) == 1:
            self.flag_ok = True
            return self.array
        else:
            print("Su array es muy corto")
            # self.flag_ok = True
            return self.array

    def mayor_a_menor(self):
        if self.flag_ok == True:
            if len(self.array) > 1:
                _low = []
                _high = []
                distr_equals = False
                for i in self.array:
                    if i > self.pivote:
                        # print(i, " va para High")
                        _high.append(i)
                    elif i < self.pivote:
                        _low.append(i)
                        # print(i, " va para Low")
                    else:
                        if distr_equals == True:
                            # print(i, " va para High")
                            _high.append(i)
                            distr_equals = False
                        else:
                            _low.append(i)
                            # print(i, " va para Low")
                            distr_equals = True
                
                if len(_high) > 1:
                    _high = quicksort(_high).mayor_a_menor()
                if len(_low) > 1:
                    _low = quicksort(_low).mayor_a_menor()
                
                # print("High -> ", _high)
                # print("Low -> ", _low)
                
                _high.extend(_low)      #concateno los 2 arrays
                self.array = _high
            return self.array
        else:
            # print("No se puede ordenar")
            return self.array
            
    
    def menor_a_mayor(self):
        if self.flag_ok == True:
            if len(self.array) > 1:
                _low = []
                _high = []
                distr_equals = False
                for i in self.array:
                    if i < self.pivote:
                        # print(i, " va para High")
                        _high.append(i)
                    elif i > self.pivote:
                        _low.append(i)
                        # print(i, " va para Low")
                    else:
                        if distr_equals == True:
                            # print(i, " va para High")
                            _high.append(i)
                            distr_equals = False
                        else:
                            _low.append(i)
                            # print(i, " va para Low")
                            distr_equals = True
                
                if len(_high) > 1:
                    _high = quicksort(_high).menor_a_mayor()
                if len(_low) > 1:
                    _low = quicksort(_low).menor_a_mayor()
                
                # print("High -> ", _high)
                # print("Low -> ", _low)
                
                _high.extend(_low)      #concateno los 2 arrays
                self.array = _high
            return self.array
        else:
            # print("No se puede ordenar")
            return self.array





arreglo = []
aux = []
for i in range(5000):
    arreglo.append(randint(-100, 100))
    aux.append((random()-0.5)*200)
arreglo.extend(aux)
# arreglo = [10, 20, 15, 12.5, "coquito", 33, 1.1, -55, 101]
# arreglo = [-6513, "coco", "pepe", 10, "toto", "lola", "lalo", 10, 10.1]

_test = quicksort(arreglo)
# print(_test.array)

# _test = quicksort(arreglo).mayor_a_menor()
start = time_ns()
_test.mayor_a_menor()
stop = time_ns()
print("duracion [ms] -> ",(stop - start)/1000000)
print("pivote ->", _test.pivote)
print("media ->", mean(_test.array))
print("mediana ->", median(_test.array))
# print("array: ")
# print(_test.array)

if _test.flag_ok:
    print("anda")
else:
    print("no anda")