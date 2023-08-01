#include <stdio.h>
#include <math.h>

#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/projdefs.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "sdkconfig.h"
#include "xtensa/config/core-isa.h"
#include "esp_err.h"

// constantes
#define MPI 3.14159265358979323846  // numero pi
#define Fs  1000.0                 // frecuencia de muestreo de la señal a fitrar
#define N_periodos_test 150           // cantidad de periodos para el test unitario


struct filtro_IIR_2ord  // estructura que contiene los coeficientes deun filtro IIR de una etapa
{                       // para mas etapas se deben colocar en cascada
    // constantes del filtro
    float b_0;
    float b_1;
    float b_2;
    float a_1;
    float a_2;
    
    // constante de escala
    float k_f;
};

// funciones
void test_unitario_filtro(void);

extern void filtro_II_d_I(float* muestra_p, float* _x, float* _y, float* _SOS);    // algoritmo de filtro IIR 2° orden forma directa tipo 1
extern void casting_y_escala(int muestra_cuentas, float* muestra_p, float* k_veces_to_p);// recibe un entero, lo pasa a flotante mediante hardware y lo escala segun un factor de conversion
extern void producto_y_acumulacion(float *_y, float* out, float *_acu, float *_k);              // hace el producto por la constante de salida y acumula el cuadrado de la señal en un registro

// defino los parametros de mi filtro notch de frecuencia central a 50 Hz
// el filtro se diseñó utilizando la herramienta "Filter Builder" de Matlab(R)
// la freuencia de muestreo de la señal es 48 kHz
const struct filtro_IIR_2ord etapa_0 = {.b_0 = 0.3813687, .b_1 = -0.7254062, .b_2 =0.3813683, .a_1 = -1.9018863, .a_2 = 0.9987550, .k_f = 1};
const struct filtro_IIR_2ord etapa_1 = {.b_0 = 1.0514621, .b_1 = -2, .b_2 = 1.0514621, .a_1 = -1.8999511, .a_2 = 0.9987431, .k_f = 1};
const struct filtro_IIR_2ord etapa_2 = {.b_0 = 1.0514631, .b_1 = -2, .b_2 = 1.0514613, .a_1 = -1.8978416, .a_2 = 0.9955087, .k_f = 1};
const float k_salida = 2.363452434539795; // constante de salida del filtro (cuarto valor de escala de la matriz SOS)

void app_main(void)
{
    // printf("hola\n");
    test_unitario_filtro();
    while(1){
        printf("no hago nada en el loop\n");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void test_unitario_filtro(void){
    printf("\n\ntest unitario filtro\n");
    float frecuencias[] = {10.000000, 20.000000, 30.000000, 35.000000, 40.000000, 45.000000, 47.000000, 48.000000, 49.000000, 49.100000, 49.200000, 49.300000, 49.400000, 49.500000, 49.600000, 49.700000, 49.800000, 49.850000, 49.900000, 49.950000, 49.975000, 50.000000, 50.025000, 50.050000, 50.100000, 50.150000, 50.200000, 50.300000, 50.400000, 50.500000, 50.600000, 50.700000, 50.800000, 50.900000, 51.000000, 52.000000, 53.000000, 55.000000, 60.000000, 70.000000, 80.000000, 90.000000, 100.000000, 150.000000, 250.000000};//, 400.000000, 600.000000, 1000.000000};
    float dB_ideal[] = {-0.000001, -0.000017, -0.000074, -0.000162, -0.000428, -0.001940, -0.005520, -0.012123, -0.037803, -0.042660, -0.047249, -0.049892, -0.046435, -0.028385, 0.000109, -0.337419, -4.123855, -8.168420, -13.787466, -23.032032, -32.116837, -100.313210, -32.124646, -23.045462, -13.813988, -8.209435, -4.176333, -0.358491, -0.000334, -0.027297, -0.046025, -0.050124, -0.047899, -0.043560, -0.038842, -0.013077, -0.006218, -0.002379, -0.000652, -0.000186, -0.000091, -0.000056, -0.000038, -0.000011, -0.000002};
    
    float dB_test[sizeof(frecuencias)/sizeof(float)]; // para guardar la respuesta de nuestro filtro y compararlo con el ideal
    int tiempo_ciclos_filtro = 0;       // para medir el tiempo de aplicacion de cada filtro

    // punteros que contienen parametros del filtro
    struct filtro_IIR_2ord* punt_test = malloc(3*sizeof(struct filtro_IIR_2ord));
    *(punt_test+0) = etapa_0;
    *(punt_test+1) = etapa_1;
    *(punt_test+2) = etapa_2;

    float *x0, *x1, *x2, *y0, *y1, *y2, *k_out;
    x0 = malloc(3*sizeof(float));
    x1 = malloc(3*sizeof(float));
    x2 = malloc(3*sizeof(float));
    y0 = malloc(3*sizeof(float));
    y1 = malloc(3*sizeof(float));
    y2 = malloc(3*sizeof(float));
    k_out = malloc(sizeof(float));
    *k_out = k_salida;                  // constante de salida del filtro
    // inicializacion de buffers
    for(int i=0; i<3; i++){
        *(x0+i) = 0;
        *(x1+i) = 0;
        *(x2+i) = 0;
        *(y0+i) = 0;
        *(y1+i) = 0;
        *(y2+i) = 0;
    }

    // variables
    float omega;        // para sintetizar un seno a las frecuencias de prueba
    int seno_int;       // inicialmente el seno no tendrá decimales, para usar el casting
    float seno;         // donde se guardará el seno ya en formato flotante
    float k_p_m = (1.0/10000.0);// constante de conversion de veces a las unidades de nuesra señal fisica

    float acumulador_seno, acumulador_filtro;  // acumuladores de cuadrados, para calcular al final el valor rms

    float salida;       // aca podríamos ver la señal de salida del filtro

    for(int i=0; i<(sizeof(frecuencias)/sizeof(float)); i++){           // recorro el array de frecuencias
        omega = 2.0*MPI*frecuencias[i]/Fs;              // argumento del seno
        // inicializacion de acumuladores
        acumulador_filtro = 0;                                // estando la salida del filtro estabilizada
        acumulador_seno = 0;
        
        uint32_t N_muestras = (uint32_t)(N_periodos_test*Fs/frecuencias[i]);    // defino la cantidad de muestras para "N_periodos_test" periodos
        esp_rom_delay_us(20000);
        for(int j=0;j<N_muestras;j++){                                // recorro "N_periodos_test" periodos de la señal
            seno_int = (int)(10000.0*sin(omega*j));                   // calculo el seno (sin decimales)
            seno = sin(omega*j);

            ///////////////////////////////////////////////////////////////////////////////////////////////
            /////   aplicacion y testeo del filtro con sus perifericos  ///////////////////////////////////
            // tiempo_ciclos_filtro = esp_cpu_get_cycle_count(); // tomo los ciclos actuales del procesador
            // hago e casting mediante assembler y paso de unidades la señal
            // casting_y_escala(seno_int, &seno, &k_p_m);
            // filtros en cascada
            filtro_II_d_I(&seno, x0, y0, &(punt_test+0)->b_0);  // etapa 0
            filtro_II_d_I(y0, x1, y1, &(punt_test+1)->b_0);     // etapa 1
            filtro_II_d_I(y1, x2, y2, &(punt_test+2)->b_0);     // etapa 2
            // a la salida aplico la constante de salida y acumulo
            producto_y_acumulacion(y2, &salida, &acumulador_filtro, k_out);

            // calculo el tiempo que requiere esta operacion, para la ESP32 cada ciclo son 4 ns
            // int aux = esp_cpu_get_cycle_count();
            // tiempo_ciclos_filtro = 4*(aux - tiempo_ciclos_filtro); // NO CONSIDERO EL DESBORDE YA QUE EL TEST SE HACE UNA SOLA VEZ AL PRINCIPIO
            /////////////////////////////////////////////////////////////////////////////////////////////
            if(j >= ((N_periodos_test-1)*(N_muestras/N_periodos_test)-1)){                // solo en el ultimo periodo hago el rms
                acumulador_seno = acumulador_seno +  seno*seno;       // acumulo para calcular el rms en "N_periodos_test" periodos
                // acumulador_seno = 0;
                // printf("linea 133");
            }else{
                acumulador_filtro = 0;          // lo seteo a 0 si no acumulo aún
            }
            // vTaskDelay(1);
        }
        // acumulador_filtro =1;
        // printf("acu filtro = %f\tacu seno = %f\n", acumulador_filtro, acumulador_seno);
        dB_test[i] = 20.0*log10(sqrt((acumulador_filtro)/(acumulador_seno)));    // calculo la atenuación del filtro
        // printf("ACU %f\n", acumulador_filtro);
        // vTaskDelay(pdMS_TO_TICKS(10));                        // espero 20mS para la siguiente iteracion (pensado para RTOS)  
    }

    ////    presentación de resultados  ////
    // printf("tiempo de filtrado [ns] = %d\n", tiempo_ciclos_filtro);
    printf("f [Hz]\t\tdBA_filtro\tdBA_Ideal\n");
    for(int i=0; i<(sizeof(frecuencias)/sizeof(float)); i++){
        vTaskDelay(pdMS_TO_TICKS(20));
        printf("%f\t%f\t%f\n", frecuencias[i], dB_test[i], dB_ideal[i]);
    }

    // libero la memoria
    free(x0);
    free(x1);
    free(x2);
    free(y0);
    free(y1);
    free(y2);
    free(k_out);
    // free(punt_test);
}