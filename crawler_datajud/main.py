import json
import os

import httpx
import pandas as pd

from dotenv import load_dotenv

from atributos import ATRIBUTOS
from endpoints import (
    ENDPOINTS_EST,
    ENDPOINTS_TRE,
    ENDPOINTS_TJM,
    ENDPOINTS_TRF,
    ENDPOINTS_TRT,
    ENDPOINTS_TSU
)

load_dotenv('.env.api_key')

API_KEY = os.getenv('API_KEY', None)

if API_KEY is None:
    os._exit()


class CrawlerDataJud:
    BASE_URL = 'https://api-publica.datajud.cnj.jus.br'
    OUTPUT_DIR = 'outputs/'

    def __init__(self, sigla, parametros, output_filename):
        self.api_key = API_KEY
        self.sigla = sigla
        self.parametros = parametros
        self.output_filename = output_filename
        self.contador = 1

    def monta_payload(self, search_after=[]):
        fields = []
        for k, v in self.parametros.items():
            if k not in ATRIBUTOS.keys():
                print(f'Atributo inválido: {k}')
                return None
            
            fields.append({'match': {k: v}})
        
        if len(fields) == 1:
            query = {
                'size': 100,
                'query': fields[0],
                'sort': [
                    {
                        '@timestamp': {
                            'order': 'asc'
                        }
                    }
                ]
            }
        else:
            query = {
                'size': 100,
                'query': {
                    'bool': {
                        'must': fields
                    }
                },
                'sort': [
                    {
                        '@timestamp': {
                            'order': 'asc'
                        }
                    }
                ]
            }
        
        if search_after:
            query['search_after'] = search_after

        return json.dumps(query)

    def obtem_endpoint(self):
        endpoints = [
            ENDPOINTS_EST,
            ENDPOINTS_TRE,
            ENDPOINTS_TJM,
            ENDPOINTS_TRF,
            ENDPOINTS_TRT,
            ENDPOINTS_TSU
        ]

        for lista in endpoints:
            if lista.get(self.sigla.upper(), None) is not None:
                return lista[self.sigla.upper()]
        
        return None

    def requisita_api(self, endpoint, payload):
        headers = {
            'Authorization': f'APIKey {self.api_key}',
            'Content-Type': 'application/json'
        }

        response = httpx.post(
            self.BASE_URL+endpoint,
            headers=headers,
            data=payload
        )

        return response.json()

    def pesquisa_dados(self):
        payload = self.monta_payload()

        if payload is None:
            return

        endpoint = self.obtem_endpoint()
        if endpoint is None:
            print(f'Endpoint não encontrado: {self.sigla}')
            return
        
        response = self.requisita_api(endpoint, payload)

        self.response_final = response

        while response['hits']['hits'] != []:
            search_after = response['hits']['hits'][-1]['sort']
            payload = self.monta_payload(search_after)
            response = self.requisita_api(endpoint, payload)

            if len(self.response_final['hits']['hits']) > 100:
                self.salva_dados()
                self.response_final['hits']['hits'] = []
            
            self.response_final['hits']['hits'].extend(response['hits']['hits'])

    def salva_dados(self):
        if not os.path.exists('outputs/'):
            os.mkdir('outputs/')

        if self.output_filename.endswith('.xlsx'):
            lista = self.response_final['hits'].get('hits', [])
            if len(lista) == 0:
                print('Sem resultados')
                return
            
            df = pd.DataFrame()
            for item in lista:
                dados = item.get('_source', {})
                if dados == {}:
                    continue

                resultado = {
                    'numeroProcesso': dados.get('numeroProcesso', None),
                    'classe': dados.get('classe', {}).get('nome', None),
                    'formato': dados.get('formato', {}).get('nome', None),
                    'tribunal': dados.get('tribunal', None),
                    'movimentos': dados.get('movimentos', []),
                    'id': dados.get('id', None),
                    'nivelSigilo': dados.get('nivelSigilo', None),
                    'orgaoJulgador': dados.get('orgaoJulgador', {}).get('nome', None),
                    'assuntos': dados.get('assuntos', [])
                }
                df_aux = pd.DataFrame([resultado])
                df = pd.concat([df, df_aux])
            
            output_final = self.output_filename.replace(
                '.xlsx', f' - {self.contador}.xlsx'
            )
            df.to_excel(f'outputs/{output_final}', index=False)
            
            self.contador += 1
        elif self.output_filename.endswith('.json'):
            output_final = self.output_filename.replace(
                '.json', f' - {self.contador}.json'
            )
            with open(f'outputs/{output_final}', 'w', encoding='utf-8') as fp:
                json.dump(self.response_final, fp)
            
            self.contador += 1
        else:
            print('O formato final do arquivo deve ser .xlsx ou .json')
            return
