/*
 * The ASM test code to test
 * 
 * Called via a CALLX from C++/.ino
 * Input params are in a2-a7
 * 
 * Copies value in a2 to address in a3 via a10
 * Return is in a2
 */

// Use defines to reference registers, los numeros mas bajos de a son las entradas
#define m a2
#define x a3
#define y a4
#define SOS a5
#define x_0 f1
#define x_1 f2
#define x_2 f3
#define y_0 f4
#define y_1 f5
#define y_2 f6
#define b_0 f7
#define b_1 f8
#define b_2 f9
#define a_1 f10
#define a_2 f11


 
  .text                   # Code section
  .align                  # Align the byte boundaries - needed?
  .global filtro_II_d_I         # Make the symbol available to C/C++ for call
  .type   filtro_II_d_I,@function
filtro_II_d_I:
  entry a1,    32           # Create a window for execution
  lsi x_2, x, 4             # x[2] = x[1] o x[n-2] = x[n-1]
  lsi x_1, x, 0             # x[1] = x[0] o x[n-1] = x[n]
  lsi y_2, y, 4             # y[2] = y[1] o y[n-2] = y[n-1]
  lsi y_1, y, 0             # y[1] = y[0] o y[n-1] = y[n]

  lsi b_0, SOS, 0           # b_0 = SOS[0]
  lsi b_1, SOS, 4           # b_1 = SOS[1]
  lsi b_2, SOS, 8           # b_2 = SOS[2]
  lsi a_1, SOS, 12          # a_1 = SOS[3]
  lsi a_2, SOS, 16          # a_2 = SOS[4]

  lsi x_0, m, 0             # tomo la muestra ya en unidades de presion
  
  mul.s y_0, b_0, x_0      # y[n] = b_0*x[n]
  msub.s y_0, a_1, y_1      # y[n] = y[n] - a_1*y[n-1]
  madd.s y_0, b_1, x_1      # y[n] = y[n] + b_1*x[n-1]
  msub.s y_0, a_2, y_2      # y[n] = y[n] - a_2*y[n-2]
  madd.s y_0, b_2, x_2      # y[n] = y[n] + b_2*x[n-2]
  
  ssi x_0, x, 0             # guardo x[n] en memoria
  ssi x_1, x, 4             # guardo x[n-1] en memoria
  ssi x_2, x, 8             # guardo x[n-2] en memoria
  ssi y_0, y, 0             # guardo y[n] en memoria
  ssi y_1, y, 4             # guardo y[n-1] en memoria
  ssi y_2, y, 8             # guardo y[n-2] en memoria
  retw                    # Return from the windowed call