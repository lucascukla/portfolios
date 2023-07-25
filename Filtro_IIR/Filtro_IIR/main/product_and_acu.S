// Use defines to reference registers, los numeros mas bajos de a son las entradas
#define p_y a2
#define p_acu a3
#define p_k_filtro a4
#define y f1
#define acu f2
#define k_filtro f3


 
  .text                   # Code section
  .align                  # Align the byte boundaries - needed?
  .global producto_y_acumulacion         # Make the symbol available to C/C++ for call
  .type   producto_y_acumulacion,@function
producto_y_acumulacion:
  entry a1,    32           # Create a window for execution
  lsi y, p_y, 0                 # traigo la salida del filtro sin escalar
  lsi acu, p_acu, 0             # traigo el acumulador
  lsi k_filtro, p_k_filtro, 0   # traigo la constante de escala del filtro
  mul.s y, y, k_filtro          # escalo la salida del filtro
  madd.s acu, y, y              # acumulador += p^2
  ssi acu, p_acu, 0             # guardo el acumulador en memoria
  retw                      # Return from the windowed call