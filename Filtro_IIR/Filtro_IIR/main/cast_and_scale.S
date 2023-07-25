// Use defines to reference registers, los numeros mas bajos de a son las entradas
#define m a2
#define m_p a3
#define p_k_veces_to_p a4
#define k_veces_to_p f1
#define muestra_p f2


 
  .text                   # Code section
  .align                  # Align the byte boundaries - needed?
  .global casting_y_escala         # Make the symbol available to C/C++ for call
  .type   casting_y_escala,@function
casting_y_escala:
  entry a1,    32           # Create a window for execution
  lsi k_veces_to_p, p_k_veces_to_p, 0       # guardo la constante de conversion
  float.s muestra_p, m, 0                   # casting de muestra en veces
  mul.s muestra_p, muestra_p, k_veces_to_p  # conversion a presion
  ssi muestra_p, m_p, 0                     # guardo la muestra en unidades de presion
  retw                      # Return from the windowed call