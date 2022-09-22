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
#CM (mediocampo central):               2 jugadores
#RM (mediocampo derecho):               2 jugadores
#LM (mediocampo izquierdo):             2 jugadores
#CAM (mediocampo delantero central):    2 jugadores
#CF (delantero central):                2 jugadores
#RW (delantero derecho):                2 jugadores
#LW (delantero izquierdo):              2 jugadores
#ST (delantero pateador):               2 jugadores

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

# print(players_AR.groupby(['player_positions']).mean().head())



# luego voy a hacer un grafico de barras de las posiciones de jugadores
# para hacer esto debo hacer one hot encoding
pos_dummies = pd.get_dummies(players_AR.player_positions, prefix='pos')
# print(pos_dummies.head())   # veo que no funciona, ya que agrupa los que tienen un array como array

# pos_ohe = pos_dummies.filter(regex = ".*,.*")       # estas son las columnas que no deben estar

# COMO NO FUNCIONO HARE MI PROPIO ONE HOT ENCODING  ###############################################
pos_ohe = []                # defino las columnas que si deben estar
dict_dummies = {}           # creo un diccionario para agregar nuevas columnas
for i in pos:
    pos_ohe.append("pos_"+i)
    dict_dummies["pos_"+i] = 0

pos_dummies_final = pd.DataFrame()  # creo un dataframe vacio, para el one hot encoding
dict_dummies_acu = dict_dummies     # tendra el acumulado de cada posicion
print(dict_dummies_acu)
for i in pos_ohe:       # agrego columna por columna para hacer el one hot encoding
    pos_dummies_final[i] = None

for i in range(int(players_AR.shape[0])):   # recorro la lista filtrada por columnas de interés
    aux = "pos_"
    new_row_dict = dict_dummies                     # esta será la fila que se agregará al final del dataframe
    for j in players_AR.player_positions.iloc[i]:   # recorro las posiciones de cada jugador, letra a letra
        if(j != "," and j != " "):                  # aquí separo las palabras (posiciones) separadas por coma
            aux+=j                                  # construyo la palabra
        elif aux != "pos_":                         # si el caracter es una coma o un espacio, y se modifico la palabra original
            if aux in pos_dummies_final.columns:    # y si la palabra está incluida en las columnas del dataframe
                new_row_dict[aux] = 1               # anota un 1 en ese lugar
                # dict_dummies_acu[aux] += 1
                # setattr(dict_dummies_acu, aux, getattr(dict_dummies_acu, aux)+1)
            else:
                print(aux, " no está")              # de lo contrario tira un mensaje indicando que no esta en el dataframe
            aux = "pos_"
    
    new_row = pd.Series(new_row_dict)               # al final agrego la fila al dataframe
    pos_dummies_final = pd.concat([pos_dummies_final, new_row.to_frame().T], ignore_index=True)
    
    
# print(pos_dummies_final.head())
print(dict_dummies_acu)

# print(players_AR.player_positions.ninuque())

# ahora debo juntar los 2 dataframes

    
    
    
    
    
    
    
    
    # if(aux not in pos and aux != ""):
    #     pos.append(aux)
        
    # aux = "pos_"
    # aux2 = i.player_positions
    # for j in aux2:
        


# luego voy a hacer un grafico de dispercion de la puntuacion general en
# funcion de las edades de los jugadores

#luego tengo que hacer la seleccion de los 26 jugadores en funcion de lo definido anteriormente