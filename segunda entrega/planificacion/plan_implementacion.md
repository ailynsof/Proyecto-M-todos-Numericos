# Plan de implementacion y reproducibilidad - Segunda entrega
**Proyecto Integrador: Metodos Numericos**
**Universidad Externado de Colombia  Pregrado en Ciencia de Datos  2026-2**
**Articulo:** Jerezano, Chicharro y Garrido-Saez (2026)
**Equipo:** Ailyn Sofia Gomez Rodriguez, Julian Camilo Jimenez, Julian Steven Duarte
**Docente:** Edwin Fernando Munoz Chipatecua

## 1. Alcance y objetivos
La fase implementa en Python los metodos principales del articulo y los compara con referentes del curso. El producto central es un notebook ejecutable de principio a fin y un unico informe fuente LaTeX. Se reportan resultados calculados por el notebook; no se suponen convergencias ni cifras por anticipado.

La guia del proyecto pide implementacion propia en Python, comprension del articulo, problema computacional definido, justificacion de los datos o funciones, comparacion numerica y archivos suficientes para repetir el trabajo. Por ello, las funciones benchmark seran deterministas y se declararan en el notebook; no se requieren datos externos ni numeros aleatorios.

## 2. Metodos a implementar
Para una raiz de multiplicidad conocida m se implementan las dos variantes de la familia propuesta:
- w_k = x_k + beta*g(x_k)^2; D_k = (g(w_k)-g(x_k))/(w_k-x_k).
- y_k = x_k - m*g(x_k)/D_k; t_k = (g(y_k)/g(x_k))^(1/m).
- x_(k+1) = x_k - m*H(t_k)*g(x_k)/D_k.
- M1: H(t)=1+t+2*t^2. M2: H(t)=(1-t)/(1-2*t).

Como lineas base del curso se implementan Newton modificado (usa g') y Steffensen modificado (diferencia dividida con w=x+beta*g(x)). Se incluye tambien el competidor KK, comprometido en la primera entrega y reportado en el articulo: w=x+beta*g(x), y=x-m*g(x)/Dwx, t=(g(y)/g(x))^(1/m), x_nuevo=y-((m+2)*t/(1-2*t))*g(x)/(Dwx+2*Dwy), donde Dwx=g[w,x] y Dwy=g[w,y]. Se revisa que los nodos y denominadores no coincidan con cero.
Ademas, siguiendo el plan inicial, se comparan M1 y M2 con beta en {0.001,0.01,1.0}, y se incluye un experimento pedagogico de absorcion en float64. Para la medicion de tiempo se promedian 50 ejecuciones deterministas por combinacion del benchmark; las metricas de convergencia se calculan en la corrida base.

## 3. Problemas, semillas y procedencia
Se emplean los tres benchmarks deterministas descritos en el articulo:
1. Cubico con raiz doble objetivo 1.75 y raiz simple vecina 1.72; m=2.
2. Ecuacion de Planck elevada al cubo, g(x)=(exp(-x)-1+x/5)^3; la raiz objetivo es aproximadamente 4.96511423 y tiene multiplicidad 3. No confundirla con exp(-x)-1+x^3/5.
3. Polinomio de grado nueve del articulo, con raiz objetivo 3 de multiplicidad 4.

El notebook declara las expresiones, derivadas necesarias para Newton, las multiplicidades y dos semillas fijas por problema. La raiz de referencia solo se usa para medir error y no es entrada de los iteradores. Las semillas son reales, pero la potencia fraccionaria usa la rama principal compleja; las trayectorias pueden ser complejas y se documentan singularidades y estancamientos.

## 4. Reproducibilidad
- Entorno: Python 3.10 o superior con mpmath, pandas y matplotlib. El notebook incluye instrucciones de instalacion; numpy no es requisito del calculo.
- Precision inicial: 150 digitos decimales. Tolerancia: 1e-25. Maximo: 100 iteraciones. Beta base: 0.01; sensibilidad: 0.001, 0.01 y 1.0.
- Criterio de parada: tanto |x_(k+1)-x_k| como |g(x_(k+1))| deben ser menores o iguales a la tolerancia.
- Una corrida guarda estado (convergio, estancamiento, fallo de dominio, singularidad o limite de iteraciones), numero de iteraciones, iterados, pasos, residuos y tiempo transcurrido.
- Todas las constantes decimales se crean desde cadenas para evitar introducir redondeo binario innecesario. La precision se fija antes de construir los valores mpmath.
- Los tiempos son el promedio de 50 ejecuciones y aun varian entre equipos; las conclusiones no se basan solo en tiempo o iteraciones.

La alta precision ayuda a observar iteraciones cercanas a la raiz sin redondeo prematuro, pero no garantiza convergencia. No se afirma que la configuracion elegida replique las tolerancias extremas de todas las tablas del articulo; si se requiere una reproduccion con tolerancia 1e-200, se aumentaran precision y tolerancia juntas y se justificara el costo. Asi se evita usar 4000 digitos sin necesidad demostrada.

## 5. Metricas y analisis
Para cada funcion, semilla y metodo se exportan: estado, iteraciones, evaluaciones de g y g prima, error absoluto frente a la raiz de referencia, residuo final, ACOC y tiempo. ACOC se estima con tres pasos consecutivos:
ACOC = log(|x_(k+1)-x_k|/|x_k-x_(k-1)|) / log(|x_k-x_(k-1)|/|x_(k-1)-x_(k-2)|).
Solo es interpretable en el regimen asintotico y con diferencias no nulas. Se contrasta con el orden teorico (cuatro para M1/M2 y dos para las lineas base), sin convertir la expectativa en resultado.

Para interpretar costo se reportan por separado el numero de iteraciones, las evaluaciones funcionales que requiere cada formula y el tiempo orientativo. La eficiencia de Kung-Traub se menciona como cota teorica para metodos sin memoria bajo sus supuestos, no como medida universal que permita comparar directamente metodos con derivadas.

## 6. Flujo de trabajo
1. Definir funciones, derivadas, raices objetivo, multiplicidades y semillas.
2. Implementar diferencia dividida, potencia fraccionaria con rama principal compleja y solucionadores con manejo explicito de fallos.
3. Ejecutar la matriz completa de problemas, semillas y metodos.
4. Exportar tablas CSV, medir tiempos en 50 corridas, probar sensibilidad a beta y graficar residuos.
5. Interpretar convergencia, estabilidad ante semillas, ACOC y costo.
6. Redactar en el unico archivo LaTeX el problema, metodos, diseno, resultados generados y limites observados.
7. Ejecutar el notebook desde un kernel limpio antes de entregar. Las conclusiones se actualizan tras la ejecucion y se contrastan con las tablas del articulo.

## 7. Archivos de entrega
- `entregables/segunda_entrega.ipynb`: codigo comentado, explicaciones, experimentos, tabla, grafico e instrucciones para reproducir.
- `entregables/main.tex`: informe completo en un unico archivo fuente, con portada y lenguaje explicativo.
- `planificacion/plan_implementacion.md`: hoja de ruta metodologica.
- resultados/resultados_fase2.csv y resultados/sensibilidad_beta.csv: generados por el notebook; contienen la comparacion y el barrido de beta.

En la preparacion de esta segunda entrega se uso IA como apoyo para revisar el plan, organizar y documentar el notebook, y redactar el informe. El equipo debe verificar y comprender las formulas, la implementacion y los resultados antes de entregar y sustentar.
