import requests
import json
import os
import pandas as pd
from tkinter import messagebox

def consultar_pontomais(data_inicio, data_fim, codigo_unidade):
    payload = {
        "report": {
            "start_date": data_inicio,
            "end_date": data_fim,
            "group_by": "employee",
            "row_filters": "with_inactives,has_time_cards",
            "columns": "registration_number,employee_name,date,team_name,shift_time,total_time,time_cards,extra_time,summary,overnight_time,time_balance,motive",
            "format": "json",
            "business_unit_id": codigo_unidade
        }
    }

    url = 'https://api.pontomais.com.br/external_api/v1/reports/work_days'
    headers = {
        'Access-Token': '$2a$12$VAv45Kh7Swe1kScfVdgl2ef20SAfEw4JWPVdnyFtPWNY0Oe35l9Re',
        'Content-Type': 'application/json'
    }

    try:
        # Fazendo a requisição POST
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()

            # Criar a pasta 'result' se não existir
            if not os.path.exists('result'):
                os.makedirs('result')

            # Salvar o JSON em um arquivo
            output_path = os.path.join('result', 'relatorio_trabalho.json')
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Relatório salvo em: {output_path}")
            messagebox.showinfo("Sucesso", f"Relatório salvo em: {output_path}")

            # Processar o JSON e criar um DataFrame
            df = extrair_dados_empregados(data)

            # Exportar o DataFrame para CSV na pasta 'result'
            csv_output_path = os.path.join('result', 'relatorio_trabalho.csv')
            df.to_csv(csv_output_path, index=False, encoding='utf-8')
            print(f"Relatório CSV salvo em: {csv_output_path}")
            messagebox.showinfo("Sucesso", f"Relatório CSV salvo em: {csv_output_path}")

            return df

        else:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
            messagebox.showerror("Erro", f"Erro na requisição: {response.status_code}")
            return None

    except Exception as e:
        print(f"Erro ao realizar a requisição: {e}")
        messagebox.showerror("Erro", f"Erro ao realizar a requisição: {e}")
        return None

def extrair_dados_empregados(json_data):
    # Inicializando uma lista para armazenar as linhas de dados
    linhas = []

    # Percorrendo a chave 'data' no JSON
    for grupo in json_data.get("data", []):
        for empregado in grupo:
            for registro in empregado.get("data", []):
                # Extraindo os campos relevantes para o DataFrame
                linha = {
                    "date": registro.get("date"),
                    "employee_name": registro.get("employee_name"),
                    "team_name": registro.get("team_name"),
                    "total_time": registro.get("total_time"),
                    "shift_time": registro.get("shift_time"),
                    "overnight_time": registro.get("overnight_time"),
                    "registration_number": registro.get("registration_number"),
                    "motive": registro.get("motive")
                }

                # Extraindo os dados de 'summary' e 'extra_time'
                summary = registro.get("summary", [])
                linha.update({
                    "summary_credit": summary[0] if len(summary) > 0 else None,
                    "summary_debit": summary[1] if len(summary) > 1 else None,
                    "summary_interval": summary[2] if len(summary) > 2 else None,
                    "summary_normal_hours": summary[3] if len(summary) > 3 else None
                })

                extra_time = registro.get("extra_time", [])
                linha.update({
                    "extra_time_50": extra_time[0]["value"] if len(extra_time) > 0 else None,
                    "extra_time_100": extra_time[1]["value"] if len(extra_time) > 1 else None
                })

                # Adicionando a linha à lista
                linhas.append(linha)

    # Criando o DataFrame a partir das linhas extraídas
    df = pd.DataFrame(linhas)

    return df
