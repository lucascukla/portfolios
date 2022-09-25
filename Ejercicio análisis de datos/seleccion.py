# importo las librerias que voy a usar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importo la lista de jugadores con sus caracteristias
df_f22 = pd.read_csv("players_22.csv")

#inspecciono como es la lista
print("Head: \n", df_f22.head(3), "\n-----------------------\n")
print("Dimentions (rows, columns): \n", df_f22.shape, "\n-----------------------\n")
print("Nombres de columnas: \n")
columnas = df_f22.columns

for i in range(int((len(columnas))/3)):
    print(columnas[i], ",", columnas[i+1], ",", columnas[i+2], ",")#, columnas[i+3], "\t", columnas[i+4])
print("\n-----------------------\n")

# investigacion de que posiciones de jugadores tenemos en el fifa
posiciones = df_f22.player_positions
# print(posiciones.head())
pos = []
for i in posiciones:
    aux = ""
    for j in i:
        if(j != "," and j != " "):
            aux+=j
        else:
            if(aux not in pos and aux != ""):
                pos.append(aux)
            aux = ""
    if(aux not in pos and aux != ""):
        pos.append(aux)
print("Posiciones:\n", pos, "\n-----------------------\n")

# for i in pos:
#     print(i)

##############################################################################################
# sabiendo las posiciones, e investigando donde se posiciona cada una en la cancha en
# https://www.fifplay.com/fifa-22-position-modifier-cards/ , se definen los siguientes cupos:

# GK (arquero):                         2 jugadores
# CB (defensor central):                3 jugadores
# RB (defensor derecho):                2 jugadores
# LB (defensor izquierdo):              2 jugadores
# RWB (lateral derecho):                2 jugadores
# LWB (lateral izquierdo):              2 jugadores
# CDM (mediocampo defensivo central):   2 jugadores
# CM (mediocampo central):              2 jugadores
# RM (mediocampo derecho):              2 jugadores
# LM (mediocampo izquierdo):            2 jugadores
# CAM (mediocampo delantero central):   2 jugadores
# CF (delantero central):               2 jugadores
# RW (delantero derecho):               2 jugadores
# LW (delantero izquierdo):             2 jugadores
# ST (delantero pateador):              2 jugadores

##############################################################################################

# Analisis estadístico jugadores argentinos

# primero voy a filtrar solo los jugadores argentinos
players_f22_ar = df_f22[df_f22['nationality_name'] == "Argentina"]
print("jugadores argentinos (head)\n", players_f22_ar.short_name.head(), "\n") # veo que los jugadores sean realmente argentinos
print("Tamaño dataframe: \n",players_f22_ar.shape, "\n-----------------------\n")

# luego voy a eliminar las columnas que no estén incluidas en:
columnas_de_interes = ["short_name", "player_positions", "overall", "potential", "age", "height_cm", "weight_kg", "club_name", "preferred_foot", "weak_foot", "skill_moves", "international_reputation", "work_rate", "pace", "shooting", "passing", "dribbling", "defending", "physic", "attacking_crossing", "attacking_finishing", "attacking_heading_accuracy", "attacking_short_passing", "attacking_volleys", "skill_dribbling", "skill_curve", "skill_fk_accuracy", "skill_long_passing", "skill_ball_control", "movement_acceleration", "movement_sprint_speed", "movement_agility", "movement_reactions", "movement_balance", "power_shot_power", "power_jumping", "power_stamina", "power_strength", "power_long_shots", "mentality_aggression", "mentality_interceptions", "mentality_positioning", "mentality_vision", "mentality_penalties", "mentality_composure"]
print("FILTRADO: \n\nLuego de filtrado debería tener ", len(columnas_de_interes), "columnas\n\n")

players_AR = players_f22_ar.filter(items=columnas_de_interes)
print("El DataFrame filtrado tiene", players_AR.shape[0], "jugadores de nacionalidad argentina, y ", players_AR.shape[1],"caracteristicas de los  mismos\n\n")

# luego voy a graficar un grafico de campana de gauss de el overall
players_AR.overall.plot(kind = 'density', legend = 'overall', title = 'Puntaje promedio', )
plt.show()


# luego voy a hacer un grafico de barras que indique cuantos jugadores tenemos en cada posición

# en primera instancia pretendía utilizar one hot encoding, pero no funcionó, entonces lo hice
# de la siguiente manera:

dict_acu = {}               # creo un diccionario para acumular cuantos jugadores hay en cada posición
for i in pos:               # recorro las posiciones de los jugadores, que guardé anteriormente
    dict_acu["pos_"+i] = 0  # inicialmente tengo cero jugadores en cada posición


for i in range(int(players_AR.shape[0])):   # recorro la lista filtrada por columnas de interés
    aux = "pos_"                            # variable auxiliar usada para guardar la posición a contar
    # new_row_dict = dict_dummies                     # esta será la fila que se agregará al final del dataframe
    acu = 0                                         # acumula para contar las letras
    # print(players_AR.player_positions.iloc[i])
    for j in players_AR.player_positions.iloc[i]:   # recorro las posiciones de cada jugador, letra a letra
        acu += 1
        if(j != "," and j != " "):                  # aquí separo las palabras (posiciones) separadas por coma
            aux+=j                                  # construyo la palabra
            # print(aux)
            # print("len: ", len(players_AR.player_positions.iloc[i]), "\tacu: ", acu)

        if aux != "pos_" and (j == "," or j == " " or acu == len(players_AR.player_positions.iloc[i])):                         # si el caracter es una coma o un espacio, y se modifico la palabra original
            dict_acu[aux] += 1                      # acumulo un jugador en la posición
            # print(aux, ":", dict_acu[aux])
            aux = "pos_"                            # luego "reseteo" el valor de la variable auxiliar

# print(dict_acu)

pos_jugadores_ar = pd.Series(dict_acu)              # convierto mi diccionario en una serie

# intento de traducir los nombres de las posiciones de los jugadores
# posiciones_es = {'pos_GK':'Arquero', 'pos_CB':'Defensor central', 'pos_RB':'defensor derecho', 'pos_LB':'defensor izquierdo', 'pos_RWB':'lateral derecho', 'pos_LWB':'lateral izquierdo', 'pos_CDM':'mediocampo defensivo central', 'pos_CM':'mediocampo central', 'pos_RM':'mediocampo derecho', 'pos_LM':'mediocampo izquierdo', 'pos_CAM':'mediocampo delantero central', 'pos_CF':'delantero central', 'pos_RW':'delantero derecho', 'pos_LW':'delantero izquierdo', 'pos_ST':'Nueve'}
# pos_jugadores_ar_es = pos_jugadores_ar.rename(columns = {'pos_GK':'Arquero', 'pos_CB':'Defensor central', 'pos_RB':'defensor derecho', 'pos_LB':'defensor izquierdo', 'pos_RWB':'lateral derecho', 'pos_LWB':'lateral izquierdo', 'pos_CDM':'mediocampo defensivo central', 'pos_CM':'mediocampo central', 'pos_RM':'mediocampo derecho', 'pos_LM':'mediocampo izquierdo', 'pos_CAM':'mediocampo delantero central', 'pos_CF':'delantero central', 'pos_RW':'delantero derecho', 'pos_LW':'delantero izquierdo', 'pos_ST':'Nueve'})

pos_jugadores_ar = pos_jugadores_ar.sort_values(ascending=False)
pos_jugadores_ar.plot(kind='bar', legend='jugadores por posicion en Argentina')
plt.show()

# realizar un grafico de dispercion del puntage general en funcion de la edad
players_AR.plot.scatter('age', 'overall')
plt.show()  # mirando así no me dice mucho, pero en teoría debería ser como una parábola invertida

# realizar una matriz de correlacion
corr_players_AR = players_AR.corr()
# corr2 = round(corr_players_AR, 2)     # son tantas lineas que no se pueden ver
# print(corr2)

# plt.matshow(corr_players_AR)

sns.heatmap(corr_players_AR, annot=False)   # se observa gran correlacion entre las aptitudes físicas
plt.show()

correlations_players_AR = {}
for i in range(len(corr_players_AR.columns)-1):
    j = i+1
    while j < len(corr_players_AR.columns):
        correlations_players_AR[corr_players_AR.columns[i]+" vs "+corr_players_AR.columns[j]] = corr_players_AR[corr_players_AR.columns[i]][corr_players_AR.columns[j]]
        # print("i: ", i, ", j: ", j, " -> ", round(corr_players_AR[corr_players_AR.columns[i]][corr_players_AR.columns[j]], 3))
        j +=1

corr_players_AR_s = pd.Series(correlations_players_AR).sort_values(ascending=False)
corr_players_AR_s[0:25].plot(kind='bar', legend='correlaciones de mayor a menor')
plt.show()
# en el grafico no se entiende nada, pero se ve que muchas muchas variables estan correlacionadas,
# lo cual tiene sentido. El overall sería como una ponderación de todo. Se odrían deducir
# variables que engloben eso pero cumplirían una función similar al overall

# antes de hacer la selección hay que hacer un one hoy encoding, como vimos que no funcionó usando dummies,
# uso el método que usé para contar los jugadores por posición

# COMO NO FUNCIONO HARE MI PROPIO ONE HOT ENCODING  ###############################################
# pos_ohe = []                # defino las columnas que si deben estar

dict_dummies = dict_acu             # creo un diccionario para agregar nuevas columnas
pos_dummies = pd.DataFrame()        # creo un dataframe vacio, para el one hot encoding
for i in dict_dummies:              # llevo a cero todos los valores
    dict_dummies[i] = 0
    pos_dummies[i] = None


# print(pos_dummies.columns)

new_row_dict = dict_dummies 

for i in range(int(players_AR.shape[0])):           # recorro la lista filtrada por columnas de interés
    aux = "pos_"                    # esta será la fila que se agregará al final del dataframe
    
    for j in new_row_dict:          # por alguna razon tengo que setear todo a cero de esta forma para que no escriba mal en el dataframe
         new_row_dict[j] = 0
         
    new_row_dict['index'] = int(players_AR.index[i])# le agrego una columna indice para poder concatenar con el dataframe principal
    acu = 0 
    for j in players_AR.player_positions.iloc[i]:   # recorro las posiciones de cada jugador, letra a letra
        acu += 1
        if(j != "," and j != " "):                  # aquí separo las palabras (posiciones) separadas por coma
            aux+=j                                  # construyo la palabra
        
        if aux != "pos_"and (j == "," or j == " " or acu == len(players_AR.player_positions.iloc[i])):                         # si el caracter es una coma o un espacio, y se modifico la palabra original
            new_row_dict[aux] = 1                   # anota un 1 en ese lugar
            aux = "pos_"

    new_row = pd.Series(new_row_dict)               # al final agrego la fila al dataframe
    pos_dummies= pd.concat([pos_dummies, new_row.to_frame().T], ignore_index=True)
    
    
pos_dummies = pos_dummies.astype({'index':'int64'}) # hago un casting con el indice, ya que por defecto guarda float
pos_dummies.set_index(['index'], inplace = True)    # hago que la columna index sea el índice


# print(pos_dummies.head())

# concateno el one hot encoding
players_AR_dummies = pd.concat([players_AR, pos_dummies], axis=1)
# print(players_AR_dummies.columns)

# para hacer la selección uso el overall solamente, ya que entiendo que engloba todos los demás parámetros
# podría hacer una selección considerando cada parámetro específico por posición, pero a fines de demostrar
# que soy capaz de utilizar pandas, numpy, matplotlib y un poco de seaborn este código es suficiente
# ademas no se tanto de futbol como para realizar dicho análisis de manera correcta.

# primero ordeno de mayor a menor usando el overall
players_AR_dummies_sorted = players_AR_dummies.sort_values(by='overall', ascending=False)
# print(players_AR_dummies_sorted.head())

for i in dict_acu:      # voy a reutilizar este diccionario 
    dict_acu[i] = 0

# y creo un diccionario que tiene la cantidad de jugadores por posicion que tenemos como objetivo
dict_obj = {'pos_RW': 2, 'pos_ST': 2, 'pos_CF': 2, 'pos_LW': 2, 'pos_CAM': 2, 'pos_CM': 2, 'pos_GK': 2, 'pos_CDM': 2, 'pos_LM': 2, 'pos_CB': 3, 'pos_RB': 2, 'pos_RM': 2, 'pos_LB': 2, 'pos_RWB': 2, 'pos_LWB': 2}

# plantilla de fila del datafreame de la seleccion
dict_palyer_sel = {"short_name": 0, "player_positions": 0, "overall": 0, "potential": 0, "age": 0}


df_sel_AR = pd.DataFrame()  # creo el dataframe para la seleccion
cont = 0                    # contador de jugadores (van 26 al mundial)
for i in range(int(players_AR_dummies_sorted.shape[0])):
    new_player = dict_palyer_sel    # voy generando las nuevas filas del dataframe
    for j in dict_obj:
        if(players_AR_dummies_sorted.iloc[i][j] == 1 and dict_obj[j] > 0):  # me fijo en donde encaja el jugador y si hay posiciones disponibles para ese puesto
            # completo la fila
            new_player['short_name'] = players_AR_dummies_sorted.iloc[i]['short_name']
            new_player['player_positions'] = players_AR_dummies_sorted.iloc[i]['player_positions']
            new_player['overall'] = players_AR_dummies_sorted.iloc[i]['overall']
            new_player['potential'] = players_AR_dummies_sorted.iloc[i]['potential']
            new_player['age'] = players_AR_dummies_sorted.iloc[i]['age']
            
            new_row = pd.Series(new_player)               # al final agrego la fila al dataframe
            df_sel_AR = pd.concat([df_sel_AR, new_row.to_frame().T], ignore_index=True)
            # incremento el contador y descuento uno de la lista de vacantes
            dict_obj[j] -=1
            cont +=1
            break   # salto al siguiente jugador
        
    if(cont >= 26): # cuando llego a 26 jugadores, concluyo la seleccion (ver https://cnnespanol.cnn.com/2022/06/23/fifa-mundial-watar-2022-26-jugadores-orix/#:~:text=La%20FIFA%20aprueba%20el%20aumento%20de%20convocados%20al%20Mundial%20de,a%2026%20jugadores%20por%20selecci%C3%B3n&text=(CNN%20Espa%C3%B1ol)%20%2D%2D%20Las%20selecciones,cambios%20sobre%20el%20f%C3%BAtbol%20internacional.    )
        break

print("\n-----------------------\n", "Seleccion Argentina:\n\n")
print(df_sel_AR)        # se podría mejorar la seleccion, mas comparandola con la real
# pero a fines de análisis de datos pude demostrar que puedo realizar un análisis, filtrado
# y tratamiento de los mismos, aunque tengo mucho para mejorar.