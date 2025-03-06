from rich.console import Console
from rich.table import Table
from typer import Argument, Context, Exit, Option, Typer
from typing_extensions import Annotated

from crawler_datajud import __version__
from atributos import ATRIBUTOS
from endpoints import (
    ENDPOINTS_EST,
    ENDPOINTS_TRE,
    ENDPOINTS_TJM,
    ENDPOINTS_TRF,
    ENDPOINTS_TRT,
    ENDPOINTS_TSU
)
from main import CrawlerDataJud

console = Console()
app = Typer()


def version_func(flag):
    if flag:
        print(__version__)
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=version_func, is_flag=True)
):
    message = '''Forma de uso: [b]crawlers-datajud [SUBCOMANDO] [ARGUMENTOS][/]'''

    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def pesquisa(
    arquivo_saida: str = Argument('', help='Nome do arquivo em que as informações serão armazenadas. Arquivo xlsx ou json'),
    sigla: str = Argument('', help='Sigla do endpoint desejado'),
    **parametros: Annotated[list[str], Argument(help='Uma lista de parâmetros da seguinte forma: classe.codigo=1126 orgaoJulgador.codigo=13597 ...')]
):
    parametros_dict = {}
    for parametro in parametros['parametros']:
        if '=' not in parametro:
            print('Formatação errada. Acesse o menu de ajuda.')
            return
        
        k, v = parametro.split('=')
        parametros_dict[k] = v

    crawler = CrawlerDataJud(sigla, parametros_dict, arquivo_saida)
    crawler.pesquisa_dados()
    crawler.salva_dados()


@app.command()
def endpoints(
    tipo: str = Argument('estadual', help='Lista endpoints: estadual, tre, tjm, trf, trt, tsu')
):
    table = Table()
    table.add_column('Sigla')
    table.add_column('Endpoint')

    if tipo == 'estadual':
        for k, v in ENDPOINTS_EST.items():
            table.add_row(*[k, v])
    elif tipo == 'tre':
        for k, v in ENDPOINTS_TRE.items():
            table.add_row(*[k, v])
    elif tipo == 'tjm':
        for k, v in ENDPOINTS_TJM.items():
            table.add_row(*[k, v])
    elif tipo == 'trf':
        for k, v in ENDPOINTS_TRF.items():
            table.add_row(*[k, v])
    elif tipo == 'trt':
        for k, v in ENDPOINTS_TRT.items():
            table.add_row(*[k, v])
    elif tipo == 'tsu':
        for k, v in ENDPOINTS_TSU.items():
            table.add_row(*[k, v])
    
    console.print(table)


@app.command()
def atributos(
    atributo: str = Argument('', help='Lista os atributos de pesquisa disponíveis')
):
    table = Table()
    table.add_column('Atributo')
    table.add_column('Descrição')

    if not atributo:
        for k, v in ATRIBUTOS.items():
            table.add_row(*[k, v])
    else:
        if ATRIBUTOS.get(atributo, None):
            table.add_row(*[atributo, ATRIBUTOS[atributo]])
        else:
            for k, v in ATRIBUTOS.items():
                table.add_row(*[k, v])

    console.print(table)


if __name__ == '__main__':
    app()