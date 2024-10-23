import requests
import os

def consultar_pontomais(data_inicio, data_fim, codigo_unidade):
    url = 'https://api.pontomais.com.br/external_api/v1/reports/work_days'
    headers = {
        'access-token': '$2a$12$VAv45Kh7Swe1kScfVdgl2ef20SAfEw4JWPVdnyFtPWNY0Oe35l9Re',
        # 'Content-Type': 'application/json'
    }
    
    payload = {
        "report": {
            "start_date": data_inicio,
            "end_date": data_fim,
            "group_by": "employee",
            "row_filters": "with_inactives,has_time_cards",
            "columns": "registration_number,employee_name,date,team_name,shift_time,total_time,time_cards,extra_time,summary,overnight_time,time_balance,motive",
            "format": "csv",
            "business_unit_id": codigo_unidade
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        salvar_csv(response.text, data_inicio, data_fim)
        print("Relatório gerado e salvo com sucesso.")
    else:
        print(f"Erro ao gerar o relatório: {response.status_code} - {response.text}")

def salvar_csv(dados_csv, data_inicio, data_fim):
    # Novo cabeçalho alinhado aos campos do payload
    cabecalho_desejado = "Data,Matricula,Adicional noturno,Motivo/Observação,Saldo de B.H.,Totais da jornada,Total de H. extras,Nome"

    linhas = dados_csv.splitlines()
    linhas_formatadas = []
    cabecalho_incluido = False
    nome_colaborador = ""

    for linha in linhas:
        # Ignorar as três linhas iniciais indesejadas
        if "Relatório de Jornada" in linha or "Por " in linha or "De " in linha:
            continue

        # Capturar o nome do colaborador na linha "Colaborador, (Nome da pessoa)"
        if linha.startswith("Colaborador,"):
            nome_colaborador = linha.split(",")[1]
            continue

        # Adicionar o cabeçalho apenas uma vez
        if not cabecalho_incluido:
            linhas_formatadas.append(cabecalho_desejado)
            cabecalho_incluido = True

        # Ignorar linhas "TOTAIS"
        if linha.startswith("TOTAIS,"):
            continue

        # Adicionar o nome do colaborador na linha de dados
        if linha.startswith('"Ter') or linha.startswith('"Qua') or linha.startswith('"Sex') or linha.startswith('"Dom'):
            partes_linha = linha.split(",")
            # Remover o texto do dia da semana da data e as aspas duplas
            data_numerica = partes_linha[0].strip('"')[4:]
            partes_linha[0] = data_numerica

            # Adicionar o nome do colaborador ao final da linha
            partes_linha.append(nome_colaborador)

            # Remover aspas de todos os elementos e substituir vírgulas por espaços
            partes_linha = [parte.strip('"').replace(',', '') for parte in partes_linha]
            
            # Juntar os elementos com vírgulas, removendo qualquer espaço no início
            linha_formatada = ",".join(partes_linha).lstrip()

            # Remover vírgula e espaço no início da linha, se presentes
            if linha_formatada.startswith(", "):
                linha_formatada = linha_formatada[2:]

            linhas_formatadas.append(linha_formatada)

    if not linhas_formatadas:
        print("Nenhum dado válido encontrado após a formatação.")
        return

    # Formatando as datas para o nome do arquivo
    data_inicio_formatada = '-'.join(reversed(data_inicio.split('-')))
    data_fim_formatada = '-'.join(reversed(data_fim.split('-')))

    nome_arquivo = f"RelatorioJornada_{data_inicio_formatada}_{data_fim_formatada}.csv"
    result_dir = os.path.join(os.getcwd(), 'result')

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    csv_file = os.path.join(result_dir, nome_arquivo)

    # Criar o arquivo CSV formatado
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        for linha in linhas_formatadas:
            file.write(linha + "\n")

    print(f"Arquivo salvo em: {csv_file}")

# Teste de exemplo
# consultar_pontomais("2024-08-01", "2024-08-02", "1064073")