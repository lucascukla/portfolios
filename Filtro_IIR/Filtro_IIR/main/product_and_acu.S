// Use defines to reference registers, los numeros mas bajos de a son las entradas
#define p_y a2
#define p_out a3
#define p_acu a4
#define p_k_filtro a5
#define y f1
#define acu f2
#define k_filtro f3
#define out f4


 
  .text                   # Code section
  .align                  # Align the byte boundaries - needed?
  .global producto_y_acumulacion         # Make the symbol available to C/C++ for call
  .type   producto_y_acumulacion,@function
producto_y_acumulacion:
  entry a1,    32           # Create a window for execution
  lsi y, p_y, 0                 # traigo la salida del filtro sin escalar
  lsi out, p_out, 0             # esta seria la salida del filtro escalada
  lsi acu, p_acu, 0             # traigo el acumulador
  lsi k_filtro, p_k_filtro, 0   # traigo la constante de escala del filtro

  mul.s out, y, k_filtro        # escalo la salida del filtro
  madd.s acu, out, out          # acumulador += out^2
  ssi out, p_out, 0             # guardo la salida en memoria
  ssi acu, p_acu, 0             # guardo el acumulador en memoria
  retw                      # Return from the windowed call