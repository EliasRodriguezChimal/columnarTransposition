from random import randint, uniform,random
import numpy as np

matrizAdy = [[0,1,1,0,0,0,0,0,0,0],
             [1,0,0,1,0,0,0,1,1,0],
             [1,0,0,1,0,0,1,0,0,1],
             [0,1,1,0,1,1,0,0,0,0],
             [0,0,0,1,0,0,0,0,0,0],
             [0,0,0,1,0,0,0,0,0,0],
             [0,0,1,0,0,0,0,0,0,1],
             [0,1,0,0,0,0,0,0,1,0],
             [0,1,0,0,0,0,0,1,0,0],
             [0,0,1,0,0,0,1,0,0,0]]

vectorRV = []
vectorCV = []

probabilidadMutacion = 30
probabilidadCruce = 99
umbralAptitud = 0
solucionCorrecta = False
cromosomaSolucion = []

# Cromosomas[((NodoA, NodoB),(colorA, colorB))]
listaCromosomas = []
listaAptitud = []
listaPrometedores = []
coloresNodos = []
listaCromosomasNueva = []
n = 12
m = 10
muestraPob = 80
nodo1Existe = False
nodo2Existe = False

for i in range(muestraPob):
    j=i
    vectorCV.append([i,j])

# Realizo la generación de la población de manera aleatoria, pero respetando las conexiones. 
# Hice pruebas con una población 40 cromosomas, pero la cantidad de veces que proporcionaba una 
# solución, era menor a la actual, donde estoy usando una población de 80 cromosomas.
for h in range(muestraPob):
    coloresNodos = []
    cromosoma = []
    for i in range(m):
        j=i
        while j<10:
            if matrizAdy[i][j] == 1:
                nodo1Existe=False
                nodo2Existe=False
                colorA = randint(1,3)
                colorB = randint(1,3)
                cromosoma.append([[i,j],[colorA,colorB]])
                for k in range(len(coloresNodos)):
                    if coloresNodos[k][0] == i:
                        nodo1Existe = True
                    if coloresNodos[k][0] == j:
                        nodo2Existe = True
                if nodo1Existe == False:
                    coloresNodos.append([i,colorA])
                if nodo2Existe == False:
                    coloresNodos.append([j,colorB])
            j=j+1
    vectorRV.append(coloresNodos)
    listaCromosomas.append(cromosoma)    

# Aquí es donde se realiza la regulación de los elementos de vectorSV (en este caso llamado 
# "listaCromosomas") en base a los elementos de vectorRV, tomando en cuenta las conexiones 
# ubicadas dentro de vectorCV
for i in range(len(vectorCV)):
    for h in range(m):
        for j in range(n):
            if listaCromosomas[vectorCV[i][0]][j][0][0] == vectorRV[vectorCV[i][1]][h][0]:
                listaCromosomas[vectorCV[i][0]][j][1][0] = vectorRV[vectorCV[i][1]][h][1]
            if listaCromosomas[vectorCV[i][0]][j][0][1] == vectorRV[vectorCV[i][1]][h][0]:
                listaCromosomas[vectorCV[i][0]][j][1][1] = vectorRV[vectorCV[i][1]][h][1]
# Definición de la función para evaluar la aptitud de cada cromosoma       
def fitnessFunc(posCromosoma):
    aptitudTotal = 0
    color1 = 0
    color2 = 0
    color3 = 0
    for h in range(m):
        
        for i in range(n):
            color1=0
            color2=0
            color3=0
            if listaCromosomas[posCromosoma][i][0][0] == h:
                if listaCromosomas[posCromosoma][i][1][0] == 1:
                    color1 = color1+1
                if listaCromosomas[posCromosoma][i][1][0] == 2:
                    color2 = color2+1
                if listaCromosomas[posCromosoma][i][1][0] == 3:
                    color3 = color3+1
            if listaCromosomas[posCromosoma][i][0][1] == h:
                if listaCromosomas[posCromosoma][i][1][1] == 1:
                    color1 = color1+1
                if listaCromosomas[posCromosoma][i][1][1] == 2:
                    color2 = color2+1
                if listaCromosomas[posCromosoma][i][1][1] == 3:
                    color3 = color3+1
        # La siguiente condición verifica si nuestro nodo tiene asignado más de un color en 
        # el mismo cromosoma, en caso de ser así, se le suma 1 a su aptitudTotal. Lo mismo 
        # sucede con la condición ubicada más abajo, donde si se repite un color en una conexión, 
        # también se le suma 1 a su aptitudTotal
        if (color1 and color2 > 0) or (color1 and color3 > 0) or (color2 and color3 > 0) or (color1 and color2 and color3 > 0):
            aptitudTotal = aptitudTotal+1
    repColor = 0
    aptitudResta = 0
    for i in range(n):
        if listaCromosomas[posCromosoma][i][1][0] == listaCromosomas[posCromosoma][i][1][1]:
            repColor = repColor + 1
    aptitudTotal = aptitudTotal + repColor
    # La generación de listaAptitud nos servirá en la función ubicada abajo (getPrometedores()) 
    # ya que nos permitirá establecer un límite de aptitud que podremos verificar más fácilmente 
    # a ésta misma lista y, así, obtener los cromosomas más útiles.
    listaAptitud.append([posCromosoma,aptitudTotal])
    return aptitudTotal
    
# Definición de la función para obtener los cromosomas que son más prometedores para 
# la creación de la siguiente generación
def getPrometedores():
    for i in range(len(listaAptitud)):
        # Para éste caso usé un máximo de aptitudTotal = 8, me dió buenos resultados, 
        # quizá considerando la forma en que se codificó la información, dicho límite 
        # podría ser disminuido (dando paso a mejores individuos pero quizá en cantidad
        # muy reducida).
        if listaAptitud[i][1] <= 8:
            listaPrometedores.append(listaCromosomas[listaAptitud[i][0]])
    
# Definición del operador mutación, el cuál actuará sobre el vector RV, realizando una 
# modificación aleatoria.
def mutacion(probMutacion):
    # Para la mutación, usé una probabilidad de 30%. Lo único que hago aquí tanto como 
    # en la función cruce(probCruce) es randomizar un número entre 0 y 100, en caso de 
    # que salga inferior a la probabilidad asignada previamente (para la mutación por 
    # ejemplo, menor a 30), se ejecuta el proceso.
    exitoMutacion = randint(0,100)
    if listaCromosomas:
        # En caso de que la mutación se realice, ésta funciona de la siguiente manera:
        # Elegimos una gen al azar de un cromosoma al azar y le asignamos un nuevo color 
        # al primer elemento de dicho gen (en este caso, siguiendo el formato de un gen en 
        # un cromosoma descrito previamente, que es el siguiente: 
        # ((nodoA,nodoB),(colorA,colorB)), el valor que modificaríamos sería colorA)
        
        # NOTA: para evitar confusiones y crasheos del programa, usamos siempre como 
        # rangos de ejecución para los ciclos el valor de longitud de la lista con la que 
        # estamos trabajando, ya que éstas estarán cambiando de longitud continuamente.
        rango = len(listaCromosomas)-1
        if exitoMutacion <= probMutacion:
            cromosomaMutado = randint(0,rango)
            genMutado = randint(0,11)
            valorSV = randint(1,3)
            nodoMutado = listaCromosomas[cromosomaMutado][genMutado][0][0]
            for i in range(n):
                # Hacemos la modificación del color para todos los nodos que hayan coincidido 
                # con el que ha sido mutado, para evitar nuevamente la asignación de dos colores 
                # distintos a un mismo nodo, aunque seguirá ocurriendo de misma manera en el cruce
                if listaCromosomas[cromosomaMutado][i][0][0] == nodoMutado:
                    listaCromosomas[cromosomaMutado][i][1][0] = valorSV
                if listaCromosomas[cromosomaMutado][i][0][1] == nodoMutado:
                    listaCromosomas[cromosomaMutado][i][1][1] = valorSV

# Definimos la función de cruce o Crossover
def cruce(probCruce):
    # Con 'global' le indicamos a la funcion que las listas existen previamente, ya 
    # que si no, marca error de que se les está intentando referenciar a pesar de que 
    # no han sido declaradas.
    global listaCromosomas
    global listaPrometedores
    listaCromosomasNueva = []
    
    #También usamos la misma verificación de probabilidad de cruce como se hizo con la mutación.
    exitoCruce = randint(0,100)
    if exitoCruce < probCruce:        
        p = 0
        h = 0
        
        # En caso de realizarse el cruce, éste funciona de la siguiente manera:
        # Al cromosomaAux1 se le asigna, como primer elemento, el primer gen del primer cromosoma 
        # progenitor, y a su vez, se le asigna el segundo gen del segundo nodo progenitor, y 
        # así consecutivamente hasta terminar con todos los genes existentes de dichos progenitores.
        # Para el cromosomaAux2, usamos los mismos progenitores pero los genes inversos. Es decir, 
        # como primer elemento, contendrá el primer gen del segundo progenitor, y el segundo gen del 
        # primer progenitor, y así consecutivamente hasta terminar con todos los genes.
        
        # Ambos hijos son agregados a la siguiente generación de cromosomas.
        while p<len(listaPrometedores):
            cromosomaAux1 = []
            cromosomaAux2 = []
            while h < n:
                if(p+1<len(listaPrometedores)):
                    cromosomaAux1.append(listaPrometedores[p][h])
                    cromosomaAux1.append(listaPrometedores[p+1][h+1])
                h=h+2
            h = 0
            while h < n:
                if(p+1<len(listaPrometedores)):
                    cromosomaAux2.append(listaPrometedores[p+1][h])
                    cromosomaAux2.append(listaPrometedores[p][h+1])
                h=h+2
                
            if cromosomaAux1 and cromosomaAux2:
                listaCromosomasNueva.append(cromosomaAux2)
                listaCromosomasNueva.append(cromosomaAux1)
            p = p+2
        listaCromosomas = []
        listaCromosomas = listaCromosomasNueva

# En éste punto, ya sólo es la ejecución de las funciones previamente descritas, además 
# de que a partir de éste punto se verán las corridas del programa. 
while solucionCorrecta!=True:
    listaAptitud = []
    listaPrometedores = []
    for i in range(len(listaCromosomas)):
        aptitudAux = fitnessFunc(i)
        # Aquí verificamos que, al evaluar la aptitud de los cromosomas, si alguno de ellos 
        # tiene 0 (lo cual significa que no se encontraron colores repetidos ni nodos con 
        # distintos colores asignados en un mismo cromosoma), se cataloga como la solución 
        # correcta, y por lo tanto, el programa termina. 
        
        # Esta verificación se hace 2 veces ya que la primera generación podría contener 
        # la solución al problema.
        if aptitudAux == 0:
                solucionCorrecta = True
                cromosomaSolucion = listaCromosomas[i]
                print("Solución Correcta: ", cromosomaSolucion)
                break
                
    getPrometedores()
    cruce(probabilidadCruce)
    mutacion(probabilidadMutacion)
    for i in range(len(listaCromosomas)):
        aptitudAux = fitnessFunc(i)
        if aptitudAux == 0:
                solucionCorrecta = True
                cromosomaSolucion = listaCromosomas[i]
                print("Solución Correcta: ", cromosomaSolucion)  