# Crawler da API do Datajud

### Requisitos
- Python 3.12

### Instalação
- Clone o repositório: ```git clone https://github.com/Direito-e-Tech-Insper/crawler-datajud```
- Acesse o repositório: ```cd crawler-datajud/```
- Crie um ambiente virtual Python: ```python -m venv crawlerdatajud-venv```
- Ative o ambiente virtual: ```.\crawlerdatajud-venv\Scripts\activate```
- Instale o repositório: ```pip install .```


### Instruções de uso
Feita a instalação descrita acima e com o ambiente virtual ativado, você pode executar o código da seguinte forma:
```powershell
crawler-datajud --help
```

Para listar os endpoints:
```powershell
crawler-datajud endpoints [tipo]
```

É possível listar os endpoints dos seguintes tipos: estadual, tre, tjm, trf, trt, tsu. Exemplo:
```powershell
crawler-datajud endpoints tre
```

Para listar os atributos utilizados para fazer as consultas:
```powershell
crawler-datajud atributos
```

Para realizar as consultas:
```powershell
crawler-datajud pesquisa [arquivo de saida (xlsx ou json)] [sigla do endpoint] [atributos separados por espaço]
```

Exemplos de consultas
1. No Tribunal de Justiça do Distrito Federal e dos Territórios (TJDFT) pesquisa pela classe que tem o código 1116 e pelo órgão julgador que tem o código 13597:
    ```powershell
    crawler-datajud pesquisa arquivo_final-df.xlsx df classe.codigo=1116 orgaoJulgador.codigo=13597
    ```
2. Pesquisa pelo número de processo no Tribunal Regional Eleitoral de Goiás (TRE-GO):
    ```powershell
    crawler-datajud pesquisa consulta_processo_tre-go.xlsx tre-go numeroProcesso=06000087020246090019
    ```