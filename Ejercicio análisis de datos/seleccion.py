# importo las librerias que voy a usar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# GK (arquero):                         3 jugadores
# CB (defensor central):                3 jugadores
# RB (defensor derecho):                2 jugadores
# LB (defensor izquierdo):              2 jugadores
# RWB (lateral derecho):                2 jugadores
# LWB (lateral izquierdo):              2 jugadores
# CDM (mediocampo defensivo central):   2 jugadores
# CM (mediocampo central):               2 jugadores
# RM (mediocampo derecho):               2 jugadores
# LM (mediocampo izquierdo):             2 jugadores
# CAM (mediocampo delantero central):    2 jugadores
# CF (delantero central):                2 jugadores
# RW (delantero derecho):                2 jugadores
# LW (delantero izquierdo):              2 jugadores
# ST (delantero pateador):               2 jugadores

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
    print(players_AR.player_positions.iloc[i])
    for j in players_AR.player_positions.iloc[i]:   # recorro las posiciones de cada jugador, letra a letra
        acu += 1
        if(j != "," and j != " "):                  # aquí separo las palabras (posiciones) separadas por coma
            aux+=j                                  # construyo la palabra
            print(aux)
            # print("len: ", len(players_AR.player_positions.iloc[i]), "\tacu: ", acu)
            
        if aux != "pos_" and (j == "," or j == " " or acu == len(players_AR.player_positions.iloc[i])):                         # si el caracter es una coma o un espacio, y se modifico la palabra original
            dict_acu[aux] += 1                      # acumulo un jugador en la posición
            print(aux, ":", dict_acu[aux])
            aux = "pos_"                            # luego "reseteo" el valor de la variable auxiliar
    
print(dict_acu)

pos_jugadores_ar = pd.Series(dict_acu)              # convierto mi diccionario en una serie

# intento de traducir los nombres de las posiciones de los jugadores
# posiciones_es = {'pos_GK':'Arquero', 'pos_CB':'Defensor central', 'pos_RB':'defensor derecho', 'pos_LB':'defensor izquierdo', 'pos_RWB':'lateral derecho', 'pos_LWB':'lateral izquierdo', 'pos_CDM':'mediocampo defensivo central', 'pos_CM':'mediocampo central', 'pos_RM':'mediocampo derecho', 'pos_LM':'mediocampo izquierdo', 'pos_CAM':'mediocampo delantero central', 'pos_CF':'delantero central', 'pos_RW':'delantero derecho', 'pos_LW':'delantero izquierdo', 'pos_ST':'Nueve'}
# pos_jugadores_ar_es = pos_jugadores_ar.rename(columns = {'pos_GK':'Arquero', 'pos_CB':'Defensor central', 'pos_RB':'defensor derecho', 'pos_LB':'defensor izquierdo', 'pos_RWB':'lateral derecho', 'pos_LWB':'lateral izquierdo', 'pos_CDM':'mediocampo defensivo central', 'pos_CM':'mediocampo central', 'pos_RM':'mediocampo derecho', 'pos_LM':'mediocampo izquierdo', 'pos_CAM':'mediocampo delantero central', 'pos_CF':'delantero central', 'pos_RW':'delantero derecho', 'pos_LW':'delantero izquierdo', 'pos_ST':'Nueve'})

pos_jugadores_ar = pos_jugadores_ar.sort_values(ascending=False)
pos_jugadores_ar.plot(kind='bar', legend='jugadores por posicion en Argentina')
plt.show()
