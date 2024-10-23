import requests
import json
import pandas as pd
from tkinter import messagebox
import os

def consultar_pontomais(data_inicio, data_fim, codigo_unidade):
    payload = {
        "report": {
            "start_date": data_inicio,
            "end_date": data_fim,
            "group_by": "employee",
            "row_filters": "with_inactives,has_time_cards",
            "columns": "registration_number,employee_name,date,team_name,shift_time,total_time,time_cards,extra_time,summary,overnight_time,time_balance,motive",
            "format": "json",  # Alterado para JSON
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

            # Normaliza e converte o JSON para DataFrame
            if isinstance(data, dict):
                df = pd.json_normalize(data, errors='ignore')
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                messagebox.showerror("Erro", "Formato inesperado de resposta JSON.")
                return None

            # Reordenar o DataFrame de acordo com os campos desejados
            columns_order = [
                "registration_number", "employee_name", "date", "team_name",
                "shift_time", "total_time", "time_cards", "extra_time",
                "summary", "overnight_time", "time_balance", "motive"
            ]
            df = df[columns_order]

            # Criar a pasta 'result' se não existir
            if not os.path.exists('result'):
                os.makedirs('result')

            # Salvar o DataFrame em um arquivo CSV na pasta 'result'
            output_path = os.path.join('result', 'relatorio_trabalho.csv')
            df.to_csv(output_path, index=False, encoding='utf-8')

            print(f"Relatório salvo em: {output_path}")
            messagebox.showinfo("Sucesso", f"Relatório salvo em: {output_path}")
            return df

        else:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
            messagebox.showerror("Erro", f"Erro na requisição: {response.status_code}")
            return None

    except Exception as e:
        print(f"Erro ao realizar a requisição: {e}")
        messagebox.showerror("Erro", f"Erro ao realizar a requisição: {e}")
        return None
