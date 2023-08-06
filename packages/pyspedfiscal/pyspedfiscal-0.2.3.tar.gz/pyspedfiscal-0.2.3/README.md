# PySpedFiscal

Lê e serializa um arquivo do tipo Sped Fiscal

### Exemplo

Utilização básica:

```python
# Importe a classe SpedFiscal
from pyspedfiscal import SpedFiscal

# Utilize o metodo da classe `importar` para carregar um arquivo sped
sped_fiscal = SpedFiscal.importar('caminho_arquivo')

# Utilize a hierarquia do arquivo para percorrer os registros
registros_0200 = sped_fiscal.bloco_0.resgistro_0001.registros_0200

for registro in registros_0200:
  ...

```

### Registros Implementados

| Bloco 0 | Bloco B | Bloco C | Bloco D | Bloco E | Bloco G | Bloco H | Bloco G | Bloco K | Bloco 1 | Bloco 9 |
| ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| 0000    | C001    |         |         | E001    |         |         |         |         |         | 9001    |
| 0001    | C100    |         |         | E100    |         |         |         |         |         | 9999    |
| 0200    | C101    |         |         | E110    |         |         |         |         |         |         |
| 0460    | C105    |         |         | E115    |         |         |         |         |         |         |
|         | C110    |         |         |         |         |         |         |         |         |         |
|         | C111    |         |         |         |         |         |         |         |         |         |
|         | C112    |         |         |         |         |         |         |         |         |         |
|         | C113    |         |         |         |         |         |         |         |         |         |
|         | C114    |         |         |         |         |         |         |         |         |         |
|         | C115    |         |         |         |         |         |         |         |         |         |
|         | C116    |         |         |         |         |         |         |         |         |         |
|         | C120    |         |         |         |         |         |         |         |         |         |
|         | C130    |         |         |         |         |         |         |         |         |         |
|         | C140    |         |         |         |         |         |         |         |         |         |
|         | C160    |         |         |         |         |         |         |         |         |         |
|         | C170    |         |         |         |         |         |         |         |         |         |
|         | C180    |         |         |         |         |         |         |         |         |         |
|         | C190    |         |         |         |         |         |         |         |         |         |
|         | C195    |         |         |         |         |         |         |         |         |         |
|         | C197    |         |         |         |         |         |         |         |         |         |

### Instalação

- `pip install pyspedfiscal`

### Dependencias

- Pydantic
