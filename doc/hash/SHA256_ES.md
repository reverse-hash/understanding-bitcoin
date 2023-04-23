# SHA-256

SHA-256 es una función criptográfica de hash que fue desarrollada por la Agencia de Seguridad Nacional de los Estados Unidos (NSA) y publicada por primera vez en 2001. Se utiliza ampliamente en varios protocolos y aplicaciones de seguridad, incluyendo Bitcoin. En la red de Bitcoin, SHA-256 se utiliza para asegurar la cadena de bloques y validar las transacciones. Es un componente crítico del protocolo Bitcoin, ya que garantiza la integridad y la seguridad de la red, lo que la hace extremadamente difícil de hackear o manipular.

Las principales operaciones realizadas en el cálculo del hash SHA-256 se describen a continuación:

1. **Preparación del mensaje**: El mensaje se divide en bloques de 512 bits, y se agrega relleno (también conocido como padding en inglés) para que la longitud total del mensaje sea un múltiplo de 512 bits.
2. **Inicialización del estado**: Se inicializa un estado interno de 256 bits, que se utiliza para producir la salida final del hash.
3. **Procesamiento de cada bloque**: Cada bloque de 512 bits se procesa de forma independiente. Para procesar un bloque, se realizan una serie de operaciones que involucran combinaciones bit a bit, rotaciones y operaciones lógicas como AND, OR y XOR.
4. **Actualización del estado**: Después de procesar cada bloque, se actualiza el estado interno del hash. Esta actualización implica combinar el estado anterior con el resultado del procesamiento del bloque actual.
5. **Generación de salida**: Una vez que se han procesado todos los bloques del mensaje, se genera la salida final del hash. La salida es un valor de 256 bits que representa un resumen hash único del mensaje de entrada (también conocido como digest en inglés).

## Preparación del mensaje

En criptografía, el padding es un proceso que se aplica a los mensajes para que tengan una longitud que sea múltiplo de un tamaño de bloque determinado. Se realiza para garantizar que la longitud del mensaje sea un múltiplo de 512 bits, que es el tamaño del bloque que se procesa en el algoritmo. 

El proceso de padding en SHA-256 consta de los siguientes pasos:

1. Agregar un bit $\large 1$ al final del mensaje original. Esto se debe a que la adición del bit $\large 1$ marca el final del mensaje y da inicio al proceso de padding necesario para alcanzar un tamaño de bloque múltiplo de 512 bits. Técnicamente, se podría haber elegido usar un $\large 0$ en lugar de un $\large 1$ para marcar el final del mensaje en el proceso de padding. Sin embargo, el uso del bit $\large 1$ al final del mensaje es una práctica ampliamente aceptada y utilizada en los algoritmos criptográficos. Además, incluso si el mensaje original ya termina en un $\large 1$, agregar otro $\large 1$ al final no cambiará el significado del mensaje y no afectará el resultado del hash.
2. Agregar multiples bit $\large 0$ al final del mensaje original para que la longitud del mensaje sea congruente con 448 módulo 512. En otras palabras, agregar ceros hasta que la longitud del mensaje original más el bit $\large 1$ y los bits de relleno sea un múltiplo de 512 bits menos 64 bits (para el bloque final de longitud).
3. Agregar un bloque final de 64 bits que contiene la longitud del mensaje original en bits (como un número de 64 bits).

El algoritmo tiene un tamaño máximo de mensaje que puede procesar. El tamaño máximo es $\large 2^{64}-1$ bits, lo que equivale a $\large 2^{64}-1$ bytes. Este límite es muy grande y prácticamente no hay mensajes en el mundo real que alcancen esta cantidad de bits. Estamos hablando de un poco más de 2.3 trillones de gigabytes.

## Inicialización del estado

Los valores iniciales o valores de estado son una serie de ocho valores hexadecimales que se utilizan para inicializar los ocho registros de 32 bits utilizados en el proceso de hash. Estos valores se denominan $\large H_{0}$, $\large H_{1}$, $\large H_{2}$, $\large H_{3}$, $\large H_{4}$, $\large H_{5}$, $\large H_{6}$ y $\large H_{7}$, y se han elegido de manera cuidadosa para garantizar que no tengan propiedades especiales que puedan debilitar la seguridad del algoritmo.

En el caso de SHA-256, las constantes $\large H_i$ son los primeros 32 bits de la parte fraccionaria de las raíces cuadradas de los primeros ocho números primos. Se eligieron números primos porque su raíz cuadrada siempre es irracional, lo que da lugar a un número que parece aleatorio. El uso de números primos también asegura que las constantes sean relativamente independientes entre sí y no puedan expresarse fácilmente en términos de otras constantes. Esto evita que los atacantes encuentren debilidades en el algoritmo a través del análisis de las relaciones entre las constantes.

Además, el hecho de que las constantes $\large H_i$ sean públicas y verificables por cualquiera garantiza que no haya puertas traseras ocultas en el algoritmo. El uso de números primos garantiza que las constantes se eligieron de manera aleatoria y sin ninguna intención maliciosa por parte de los diseñadores del algoritmo.

Las constantes pueden ser calculadas y verificadas de la siguiente forma:

```python
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19]

for n in prime_numbers:
    square_root = pow(n, (1 / 2))
    fractional_part = square_root % 1
    first_32bits = int(fractional_part * (1 << 32))
    print(hex(first_32bits))
```

Salida:
```
0x6a09e667 0xbb67ae85 0x3c6ef372 0xa54ff53a 0x510e527f 0x9b05688c 0x1f83d9ab 0x5be0cd19
```

## Procesamiento de cada bloque

El procesamiento de un bloque se lleva a cabo en dos fases:

### Expansión del bloque

En primer lugar, el bloque de 512 bits se divide en 16 palabras de 32 bits numeradas del 0 al 15. Luego, se genera una expansión del bloque que incluye 48 palabras adicionales de 32 bits cada una. Para hacer esto, se aplican una serie de cálculos y operaciones aritmético-lógicas a las 16 palabras de entrada, generando así las palabras adicionales. En resumen, un bloque se expande a un total de 64 palabras de 32 bits, lo que equivale a 2048 bits en total.

Para iniciar el proceso de expansión, las 16 palabras de entrada se colocan en las primeras 16 posiciones de la matriz de palabras y aplicamos la siguiente fórmula para calcular el resto, numeradas del 16 al 63.

```math
\large W_i = W_{i-16} + σ0(W_{i-15}) + W_{i-7} + σ1(W_{i-2})
```

Donde $\large \sigma _{0}$ y $\large \sigma _{1}$ son dos funciones no lineales definidas en el estándar SHA-256, que veremos a continuación e $\large i$ es el índice de la palabra actual que se está calculando.

La generación de palabras adicionales tiene como objetivo aumentar la complejidad del algoritmo y, por ende, mejorar su seguridad. La expansión de palabras dificulta que un atacante encuentre colisiones o encuentre una entrada que produzca un hash específico, lo que aumenta la seguridad del algoritmo. Cuantas más palabras adicionales se generen, más difícil será para un atacante predecir el valor hash de una entrada específica.

#### $\large \sigma _{0}$ (sigma 0)

Esta función toma una palabra de entrada de 32 bits y realiza una serie de operaciones no lineales para generar una palabra de salida de 32 bits.

La función se define de la siguiente manera:

```math
\large \sigma_{0}(X) = RotR(X,7) \oplus RotR(X,18) \oplus ShR(X,3)
```

Donde $\large RotR$ es una función de rotación hacia la derecha, $\large ShR$ es una función de desplazamiento hacia la derecha, $\large \oplus$ es una operación de exclusión lógica (también conocida como OR exclusiva o XOR) y los números dentro de los paréntesis indican la cantidad de bits a rotar o desplazar.

En la función $\large \sigma _{0}$, la palabra de entrada $\large X$ se rota 7 bits hacia la derecha, luego se rota 18 bits hacia la derecha y, por último, se desplaza 3 bits hacia la derecha. Luego, se realiza una operación XOR entre los resultados de las rotaciones y el desplazamiento. El resultado final es una palabra de 32 bits que es utilizada como variable temporal en el procesamiento del bloque.

La combinación de rotaciones, desplazamientos y operaciones lógicas de exclusión (XOR) se utilizan en el algoritmo por varias razones:

- Resistencia a ataques de criptoanálisis: Las operaciones de rotación y desplazamiento ayudan a dispersar los bits de la entrada, lo que hace que sea más difícil para un atacante deducir la entrada original a partir de la salida. Las operaciones de exclusión lógica (XOR) introducen no-linealidad en el proceso, lo que dificulta la posibilidad de encontrar dos entradas diferentes que produzcan la misma salida (colisión).

- Eficiencia en la implementación: Las operaciones de rotación y desplazamiento son muy eficientes en términos de tiempo y espacio de la computación, lo que las hace ideales para la implementación en algoritmos criptográficos. Las operaciones de exclusión lógica también son muy rápidas en términos de tiempo de procesamiento y, por lo tanto, son muy adecuadas para la implementación de algoritmos criptográficos.

- Dificultad en la inversión: Las operaciones de desplazamiento son operaciones unidireccionales, lo que significa que es difícil obtener la entrada original a partir de la salida. Como resultado, estas operaciones hacen que el proceso de hash sea resistente a la inversión, lo que es una característica deseable para un algoritmo de hash criptográfico.

La elección de la rotación de 7 bits y 18 bits y el desplazamiento de 3 bits no está basada en una elección arbitraria, sino que es el resultado de un análisis cuidadoso de la seguridad y la eficiencia del algoritmo. Rotar 7 bits y 18 bits dispersa los bits de entrada de manera efectiva y mejora la resistencia a los ataques de criptoanálisis, al tiempo que se puede implementar fácilmente en la mayoría de los procesadores modernos. Mientras que el desplazamiento de 3 bits es una forma eficiente de mezclar los bits de entrada y proporcionar no linealidad en el proceso de hash.

#### $\large \sigma _{1}$  (sigma 1)

La función $\large \sigma _{1}$ es similar a $\large \sigma _{0}$ en términos de operaciones, pero utiliza diferentes valores de entrada y operaciones de rotación. La razón por la que las funciones utilizan valores diferentes es para aumentar la complejidad y la seguridad de la función hash SHA-256.

Cada función utiliza diferentes constantes y operaciones de rotación, lo que significa que tienen diferentes efectos en los bits de entrada. Al combinar diferentes constantes y operaciones en diferentes rondas de la función hash, se generan diferentes transformaciones no lineales en los datos de entrada, lo que aumenta la resistencia de la función hash a los ataques criptográficos.

La función se establece de acuerdo con lo siguiente:

```math
\large \sigma _{1} (X) = RotR(X,17) \oplus RotR(X,19) \oplus ShR(X,10)
```

### Compresión del bloque

La compresión de un bloque es una operación fundamental que consiste en procesar el bloque expandido $\large W_i$ de 64 palabras de 32 bits (2048 bits) para producir una salida de 8 palabras de 32 bits (256 bits) que utilizaremos para actualizar los ocho registros de estado.

Al iniciar el procesamiento de bloque, se define un índice de bloque $\large t$ para cada bloque derivado del mensaje extendido, donde $\large t$ se toma de un rango de valores de $\large 1$ a $\large n$, siendo $\large n$ el número total de bloques en que se divide el mensaje.

Durante el procesamiento de cada bloque de datos, se utilizan variables intermedias $\large a$, $\large b$, $\large c$, $\large d$, $\large e$, $\large f$, $\large g$ y $\large h$ en cada ronda, y estos valores se calculan a partir de los valores de la ronda anterior y los datos del bloque actual.

```math
\large (a,b,c,d,e,f,g,h) = ({H}_{1}^{(t- 1)},{H}_{2}^{(t- 1)},{H}_{3}^{(t- 1)},{H}_{4}^{(t- 1)},{H}_{5}^{(t- 1)},{H}_{6}^{(t- 1)},{H}_{7}^{(t- 1)},{H}_{8}^{(t- 1)})
```

Para $\large t = 1$ tomaremos como los valores conocidos como valores iniciales o valores de estado que vimos en apartados de inicialización de estado:

```math
\large
\displaylines{
H_0^{(0)} = 0x6a09e667, H_1^{(0)} = 0xbb67ae85, H_2^{(0)} = 0x3c6ef372, H_3^{(0)} = 0xa54ff53a \\
H_4^{(0)} = 0x510e527f, H_5^{(0)} = 0x9b05688c, H_6^{(0)} = 0x1f83d9ab, H_7^{(0)} = 0x5be0cd19
}
```

A continuación, la compresión se lleva a cabo mediante una serie de pasos que se ejecutan en un ciclo repetido 64 veces. En cada ciclo, se aplican dos funciones de mezcla $\large \Sigma_{0}$ y $\large \Sigma_{1}$, que combinan bits del bloque de entrada con constantes específicas de la función hash. Luego, se aplican operaciones de rotación y XOR para producir una salida de 256 bits. El proceso de compresión también utiliza otras dos funciones de mezcla adicionales que combinan diferentes partes del bloque de entrada. Estas funciones se denominan $\large Ch$ y $\large Maj$.

Es decir, por cada bloque extendido $\large W_i$, repetiremos las siguientes operaciones 64 veces:

```math
\large
\begin{flalign}
 T_1 & = h + \Sigma_1(e) + Ch(e,f,g) + K_i + W_i \\
 T_2 &  = \Sigma_0(a) + Maj(a,b,c) \\
h & = g \\
g & = f \\
f & = e \\
e & = d + T_1 \\
d & = c \\
c & = b \\
b & = a \\
a & = T_1 + T_2 \\
\end{flalign}
```

#### $\large K_i$ (constantes)

Las constantes $\large K_i$ son un conjunto predefinido de valores de 32 bits que se utilizan en en las operaciones de mezcla durante la compresión de bloques. Se calculan utilizando los primeros 32 bits de las fracciones decimales de la raíz cuadrada de los primeros 64 números primos. Es importante destacar que estos valores son elegidos para asegurar que sean irracionales y que parezcan aleatorios.

Las constantes pueden ser calculadas y verificadas de la siguiente forma:
```python
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
                 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
                 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
                 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269,
                 271, 277, 281, 283, 293, 307, 311]

for number in prime_numbers:
    cube_root = pow(number, (1 / 3))
    fractional_part = cube_root % 1
    first_32bits = int(fractional_part * (1 << 32))
    print(hex(first_32bits))
```

Salida:
```
0x428a2f98 0x71374491 0xb5c0fbcf 0xe9b5dba5 0x3956c25b 0x59f111f1 0x923f82a4 0xab1c5ed5 0xd807aa98 0x12835b01 0x243185be 
0x550c7dc3 0x72be5d74 0x80deb1fe 0x9bdc06a7 0xc19bf174 0xe49b69c1 0xefbe4786 0x0fc19dc6 0x240ca1cc 0x2de92c6f 0x4a7484aa 
0x5cb0a9dc 0x76f988da 0x983e5152 0xa831c66d 0xb00327c8 0xbf597fc7 0xc6e00bf3 0xd5a79147 0x06ca6351 0x14292967 0x27b70a85 
0x2e1b2138 0x4d2c6dfc 0x53380d13 0x650a7354 0x766a0abb 0x81c2c92e 0x92722c85 0xa2bfe8a1 0xa81a664b 0xc24b8b70 0xc76c51a3 
0xd192e819 0xd6990624 0xf40e3585 0x106aa070 0x19a4c116 0x1e376c08 0x2748774c 0x34b0bcb5 0x391c0cb3 0x4ed8aa4a 0x5b9cca4f 
0x682e6ff3 0x748f82ee 0x78a5636f 0x84c87814 0x8cc70208 0x90befffa 0xa4506ceb 0xbef9a3f7 0xc67178f2
```

#### $\large \Sigma _{0}$  (Sigma 0)

La función $\large \Sigma _{0}$ se utiliza como una de las operaciones de mezcla en la compresión de bloques en SHA-256. Para ello toma una palabra de entrada de 32 bits $\large X$, se realiza una rotación circular a la derecha de 2 bits en $\large X$, se realiza otra rotación circular a la derecha de 13 bits en $\large X$, y finalmente se realiza una rotación circular a la derecha de 22 bits en $\large X$. Luego, se realiza una operación XOR entre los resultados de las rotaciones, generando así una nueva palabra de 32 bits.

La función se define de la siguiente manera:

```math
\large \Sigma _{0} (X) = RotR(X,2) \oplus RotR(X,13) \oplus RotR(X,22)
```

Donde $\large RotR$ es una función de rotación circular a la derecha, y $\large \oplus$ es una operación de exclusión lógica (también conocida como OR exclusiva o XOR).

Es posible que hayas notado que en el proceso de compresión se utilizan exclusivamente rotaciones circulares y no desplazamientos a diferencia de otras funciones como $\large \sigma _{0}$ y $\large \sigma _{1}$. Las rotaciones de bits permiten una mayor difusión de los bitsal moverse de un extremo al otro e interactuando con los bits existentes en la palabra de entrada. En la fase de expansión, se utilizan desplazamientos porque el objetivo es simplemente expandir los datos de entrada a un conjunto más grande de datos que serán procesados en la fase de compresión. La complejidad no es un factor crítico en la fase de expansión, a diferencia de la fase de compresión.

#### $\large \Sigma _{1}$ (Sigma 1)

La función $\large \Sigma _{1}$ es otra de las funciones de mezcla utilizadas en la compresión de bloques. Esta función es muy similar a la función $\large \Sigma _{0}$, pero utiliza valores de rotación diferentes para realizar las operaciones de mezcla. Al igual que el resto de funciones que hemos visto, tiene como objetivo generar mezclas de bits más complejas para aumentar la seguridad del algoritmo y evitar posibles vulnerabilidades criptográficas.

La función se define como:

```math
\large \Sigma _{1} (X) = RotR(X,6) \oplus RotR(X,11) \oplus RotR(X,25)
```

#### $\large Ch$ (choice)

La función $\large Ch$ se utiliza para seleccionar entre dos palabras de 32 bits, La función $\large Ch$ recibe tres parámetros de entrada $\large X$, $\large Y$ y $\large Z$ y produce una salida que combina sus valores de manera no lineal.

```math
\large Ch(X,Y,Z) = (X \wedge Y) \oplus ({X}' \wedge Z)
```

Donde $\large \wedge$ es una función AND, $\large {X}'$ es la operación NOT que invierte los bits de $\large X$ y \oplus$ es una operación de exclusión lógica XOR.

#### $\large Maj$ (majority)

La función $\large Maj$ es otra de las funciones no lineales utilizadas en el algoritmo. Su nombre es una abreviatura de "majority" y es una función que opera sobre tres palabras de entrada de 32 bits $\large X$, $\large Y$ y $\large Z$ y produce una salida que depende de la mayoría de los bits individuales de las palabras de entrada.

Por ejemplo, si los tres primeros bits más a la derecha de $\large X$, $\large Y$ y $\large Z$ son $\large 0$, $\large 1$ y $\large 1$, la mayoría de los bits individuales es $\large 1$, por lo que la salida de la función $\large Maj$ será $\large 1$. En cambio, si los tres bits de entrada son $\large 0$, $\large 0$ y $\large 1$, la mayoría de los bits individuales son $\large 0$, por lo que la salida de la función $\large Maj$ será $\large 0$.

Matemáticamente, se define como:

```math
\large Maj(X,Y,Z) = (X \wedge Y) \oplus (X \wedge Z) \oplus (Y \wedge Z)
```

### Actualización del estado

Una vez que el bloque ha sido comprimido, se utiliza una fórmula que toma en cuenta la salida de la compresión $\large a$, $\large b$, $\large c$, $\large d$, $\large e$, $\large f$, $\large g$ y $\large h$, y el valor del estado anterior $\large H_i^{(t-1)}$ para actualizar el valor de estado $\large H_i^{(t)}$.

Esta fórmula se aplica a cada una de las ocho variables $\large H_i$ en el algoritmo, lo que permite actualizar el estado del hash y prepararse para procesar el siguiente bloque de datos:

```math
\large
\begin{flalign}
H_0^{(t)} & = H_0^{(t-1)} + a \\
H_1^{(t)} & = H_1^{(t-1)} + b \\
H_2^{(t)} & = H_2^{(t-1)} + c \\
H_3^{(t)} & = H_3^{(t-1)} + d \\
H_4^{(t)} & = H_4^{(t-1)} + e \\
H_5^{(t)} & = H_5^{(t-1)} + f \\
H_6^{(t)} & = H_6^{(t-1)} + g \\
H_7^{(t)} & = H_7^{(t-1)} + h \\
\end{flalign}
```

### Generación de salida

Una vez procesados todos los bloques de datos, la salida del algoritmo de hash se genera concatenando los valores de las ocho variables $\large H_i$ (en orden de $\large H_0$ a $\large H_7$). Cada variable $\large H_i$ es de 32 bits, por lo que la salida del algoritmo tendrá una longitud total de 256 bits (32 bytes).

```math
\large H = H_0^{(n)} || H_1^{(n)} || H_2^{(n)} || H_3^{(n)} || H_4^{(n)} || H_5^{(n)} || H_6^{(n)} || H_7^{(n)}
```
