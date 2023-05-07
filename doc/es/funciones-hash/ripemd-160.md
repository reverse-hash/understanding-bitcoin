# RIPEMD-160

{% hint style="info" %}
Puedes encontrar la implementación del algoritmo RIPEMD-160 en nuestro repositorio del proyecto. Si deseas revisar los detalles paso a paso, dirígete a la sección correspondiente haciendo clic en el siguiente enlace:

[Implementación de RIPEMD-160](../../../understandingbitcoin/hash/sha256.py)
{% endhint %}

RIPEMD-160 es un algoritmo de hash criptográfico desarrollado por Hans Dobbertin, Antoon Bosselaers y Bart Preneel en 1996. Fue diseñado como una alternativa al algoritmo de hash más antiguo y popular, MD5, y se utiliza para proporcionar integridad de datos y autenticación en aplicaciones criptográficas.

Bitcoin utiliza el algoritmo de hash SHA-256 en su proceso de minería para asegurar la integridad de la cadena de bloques y proteger la red contra la manipulación. Sin embargo, RIPEMD-160 se utiliza en Bitcoin en combinación con SHA-256 para generar las direcciones Bitcoin a partir de las claves públicas.

Se puede especular que Satoshi seleccionó RIPEMD-160 porque ofrecía un nivel adecuado de seguridad y eficiencia para la generación de direcciones Bitcoin en ese momento. Además, RIPEMD-160 ya había sido ampliamente utilizado y probado en otros protocolos criptográficos en ese momento, lo que lo convierte en una opción razonable para su uso en Bitcoin.&#x20;

Aunque RIPEMD-160 y SHA-256 comparten algunas similitudes en su estructura y diseño, existen diferencias significativas en la forma en que procesan los bloques de datos. En particular, RIPEMD-160 utiliza un proceso de compresión diferente al utilizado por SHA-256, lo que conduce a un cálculo de hash final distinto.

A continuación se describen las principales operaciones involucradas en el cálculo del hash:

1. **Preparación del mensaje**: El mensaje se divide en bloques de 512 bits, y se agrega relleno para que la longitud total del mensaje sea un múltiplo de 512 bits. Este proceso se lleva a cabo de manera similar al utilizado en SHA-256.
2. **Inicialización del estado**: Se inicializa un estado interno de 160 bits, que se utiliza para producir la salida final del hash.&#x20;
3. **Procesamiento de cada bloque**: Cada bloque de 512 bits se procesa de forma independiente, utilizando una serie de operaciones que incluyen combinaciones bit a bit, rotaciones y operaciones lógicas como AND, OR y XOR. Estas operaciones son diferentes a las utilizadas en SHA-256, ya que RIPEMD-160 utiliza una función de mezcla adicional para mejorar la seguridad del algoritmo.
4. **Actualización del estado**: Después de procesar cada bloque, se actualiza el estado interno del hash. Esta actualización implica combinar el estado anterior con el resultado del procesamiento del bloque actual. En RIPEMD-160, este proceso de actualización se realiza utilizando una función de compresión.
5. **Generación de salida**: Una vez que se han procesado todos los bloques del mensaje, se genera la salida final del hash. La salida es un valor de 160 bits que representa un resumen hash único del mensaje de entrada

## Preparación del mensaje

El proceso de padding en RIPEMD-160 y SHA-256 es esencialmente el mismo: se agregan bits de relleno para que la longitud total del mensaje sea un múltiplo de 512 bits. La principal diferencia entre los dos algoritmos radica en cómo se procesan los bloques de 512 bits. En RIPEMD-160, los bloques se procesan como secuencias de bytes little-endian, mientras que en SHA-256 se procesan como secuencias de bytes big-endian. Esto significa que los bytes que conforman cada bloque se leen en un orden diferente, lo que se refleja en la forma en que se realizan las operaciones de combinación, rotación y lógicas que conforman el proceso de hashing.

## Inicialización del estado

Los valores iniciales o valores de estado en RIPEMD-160 son una serie de cinco valores constantes denominados _H0_, _H1_, _H2_, _H3_ y _H4_, que se utilizan para inicializar los cinco registros de 32 bits utilizados en el proceso de hash. La secuencia difiere de la utilizada en SHA-256. La secuencia de números de 0 a f en hexadecimal, seguida por la secuencia de números de f a 0 en hexadecimal, se utiliza para formar una combinación que conforma una secuencia de 160 bits en el proceso de RIPEMD. Además, se añade una combinación de ambas secuencias para formar un total de tres combinaciones de 160 bits que se almacenan en little endian.

De la siguiente forma se pueden calcular y verificar las constantes:

```python
buffer: ByteBuffer = ByteBuffer(order=ByteOrder.LITTLE_ENDIAN)

buffer.put_word32(BitStream.from_hex('01234567'))  # 0 -> 7
buffer.put_word32(BitStream.from_hex('89abcdef'))  # 8 -> f

buffer.put_word32(BitStream.from_hex('fedcba98'))  # f -> 8
buffer.put_word32(BitStream.from_hex('76543210'))  # 7 -> 0

buffer.put_word32(BitStream.from_hex('f0e1d2c3'))  # f -> c mixed with 0 -> 3

print(buffer.hex())
```

Salida:

<pre><code><strong>67452301efcdab8998badcfe10325476c3d2e1f0 
</strong></code></pre>

Este sería el conjunto de 160 bits que se asignaría como estado inicial en los cinco registros de 32 bits del algoritmo.

## **Procesamiento de cada bloque**

El procesamiento de un bloque se lleva a cabo en dos fases:

### División del bloque

todo

### Compresión del bloque

| i    | 1 | 2 | 3  | 4 | 5  | 6 | 7  | 8 | 9  | 10 | 11 | 12 | 13 | 14 | 15 |
| ---- | - | - | -- | - | -- | - | -- | - | -- | -- | -- | -- | -- | -- | -- |
| p(i) | 7 | 4 | 13 | 1 | 10 | 6 | 15 | 3 | 12 | 0  | 9  |    |    |    |    |
|      |   |   |    |   |    |   |    |   |    |    |    |    |    |    |    |
|      |   |   |    |   |    |   |    |   |    |    |    |    |    |    |    |
