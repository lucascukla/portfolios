| Microcontroladores soportados | ESP32 | ESP32-C2 | ESP32-C3 | ESP32-S2 | ESP32-S3 |
| ----------------------------- | ----- | -------- | -------- | -------- | -------- |

# Filtro IIR
***
En el presente repositorio se tiene un algoritmo de un filtro IIR de grado 2 según la estructura directa tipo 1, como se muestra en la figura, estando la ecuación a diferencias del mismo debajo de la misma.

![Forma directa tipo 1](https://github.com/lucascukla/portfolios/blob/desarrollo_filtro/Filtro_IIR/Filtro_IIR/Imagenes/diagrama_filtro.png?raw=true)

$$y[n] = b_0 \cdot k \cdot x[n] + b_1 \cdot k \cdot x[n-1] + b_2 \cdot k \cdot x[n-2] - a_1 \cdot y[n-1] - a_2 \cdot y[n-2]$$

El filtro se encuentra en el archivo llamado *filtro.S*, el cual está programado en assembler. Se complementa con una función de casting por hardware en caso de que la señal a filtrar tenga una interfáz de tipo entera o entera sin signo, el mismo está en el archivo denominado *cast_and_scale.S*.

También se tiene una función denominada `producto_y_acumulacion`
en el caso de que el filtro tenga una constante proporcional de salida, generalmente incluida en las estructuras de filtros proporcionadas por las herramientas de MATLAB®; esta función está incluida en el archivo denominado *product_and_acu.S*

### Descripción del ejemplo
En el código implementado se encuentra la definición de un filtro de tipo *notch* de grado 6, expresado como 3 filtros de grado 2 en cascada (esto se usa generalmente para minimizar el error por truncamiento en el procesamiento de señales digitales). Los filtros notch se aplican para eliminar *ruido* presente a una frecuencia específica (en este caso el ruido generado por la red eléctrica a 50 Hz).

En la función `test_unitario_filtro()` se encuentra el testeo del filtro antes nombrado, haciendo un barrido en frecuencia en el mismo para luego contrastar la respuesta del filtro implementado con la respuesta teórica arrojada por un script de MATLAB®. 


### Uso de los archivos hechos en Assembler
#### Cast_and_scale.S
Se encarga de recibir la muestra de la señal en veces (numero entero sin signo generalmente) y pasarlo a las unidades que correspondan. Para utilizarlo se lo encluye en el script.c, globalmente de la siguiente forma:
```c
extern void casting_y_escala(int muestra_cuentas, float* muestra_f, float* k_veces_to_f);
```
donde:
- *muestra_cuentas*: es la muestra de la señal en veces
- *muestra_f*: puntero que apunta a la dirección de memoria donde se guardará la muestra en unidades físicas.
- *k_veces_to_f*: puntero que apunta a la dirección de memoria donde está la constante de conversión de unidades.

#### filtro.S
Contiene un algoritmo correspondiente a un filtro IIR de grado 2 según la forma directa tipo I. Para utilizarlo se lo encluye en el script.c, globalmente de la siguiente forma:
```c
extern void filtro_II_d_I(float* muestra_f, float* _x, float* _y, float* _SOS);
```
donde:
- *muestra_f*: puntero que apunta a la dirección de memoria donde se guardará la muestra ya en las unidades físicas que corresponda.
- *_x*: apunta al primer elemento de un stack de 3 elementos correspondientes a x[n], x[n-1] y x[n-2], dicho stack es una pila FIFO.
- *_y*: apunta al primer elemento de un stack de 3 elementos correspondientes a y[n], y[n-1] y y[n-2], dicho stack es una pila FIFO.
- *_SOS*: apunta al primer elemento de array que contiene los parámetros del filtro a implementar. La disposición de los parámetros es la siguiente:
    - *(_sos + 0) = b0
    - *(_sos + 1) = b1
    - *(_sos + 2) = b2
    - *(_sos + 3) = a1
    - *(_sos + 4) = a2
    - *(_sos + 5) = k
    
Si se pretende aplicar un filtro de grado mayor a 2 se debe implementar como una cascada de filtros de grado 2 según forma directa tipo I.

#### product_and_acu.S
Se encarga de realizar una escala a la salida de la etapa de filtrado y de realizar el acumulado del cuadrado de la señal, para eventualmente calcular el valor rms de la misma. Para utilizarlo se lo encluye en el script.c, globalmente de la siguiente forma:
```c
extern void producto_y_acumulacion(float *_y, float* out, float *_acu, float *_k);  
```
donde:
- *_y*: apunta a la salida de la etapa de filtrado.
- *out*: apunta a la salida del filtro ya escalada.
- *_acu*: apunta a la direccion de memoria donde se guardará el acumulado de los cuadrados de la salida del filtro para calcular luego el Leq.
- *_k*: apunta a la constante de salida del filtro.
