import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import DateEntry  # Biblioteca para entrada de data com máscara
import os
import csv
import time
from pontomais_api import consultar_pontomais  # Importa a função da API

def centralizar_janela(janela, largura, altura):
    # Obter a largura e altura da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcular a posição da janela para centralizá-la
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # Definir a geometria da janela para centralizá-la
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def mostrar_confirmacao(data_inicio, data_fim, codigo_unidade):
    # Criar uma nova janela de confirmação
    confirm_window = Toplevel(root)
    confirm_window.title("Confirme sua ação")
    
    # Definir o tamanho da janela
    largura, altura = 300, 200
    centralizar_janela(confirm_window, largura, altura)

    # Rótulos para mostrar os dados inseridos
    tk.Label(confirm_window, text="Confirme sua ação", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(confirm_window, text=f"Data Início: {data_inicio}", font=("Arial", 12)).pack(pady=5)
    tk.Label(confirm_window, text=f"Data Fim: {data_fim}", font=("Arial", 12)).pack(pady=5)
    tk.Label(confirm_window, text=f"Código Unidade: {codigo_unidade}", font=("Arial", 12)).pack(pady=5)

    # Função para cancelar o processamento
    def cancelar():
        confirm_window.destroy()

    # Função para continuar o processamento
    def continuar():
        confirm_window.destroy()
        iniciar_processamento(data_inicio, data_fim, codigo_unidade)

    # Botões "Cancelar" e "Continuar"
    btn_frame = tk.Frame(confirm_window)
    btn_frame.pack(pady=10)

    btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=cancelar, width=10)
    btn_cancelar.grid(row=0, column=0, padx=5)

    btn_continuar = tk.Button(btn_frame, text="Continuar", command=continuar, width=10)
    btn_continuar.grid(row=0, column=1, padx=5)

def iniciar_processamento(data_inicio, data_fim, codigo_unidade):
    label_status.config(text="Processando...", fg="black")
    label_status.pack(pady=10)  # Exibe o label
    root.update_idletasks()

    tempo_estimado = 5  # Simulação de tempo de processamento
    for i in range(tempo_estimado, 0, -1):
        time.sleep(1)
        root.update_idletasks()

    consultar_pontomais(data_inicio, data_fim, codigo_unidade)

    label_status.config(text="Processamento concluído!", fg="red")
    root.update_idletasks()

    root.after(60000, remover_mensagem)

def processar():
    data_inicio = entry_data_inicio.get_date().strftime('%Y-%m-%d')
    data_fim = entry_data_fim.get_date().strftime('%Y-%m-%d')
    codigo_unidade = entry_codigo_unidade.get()

    mostrar_confirmacao(data_inicio, data_fim, codigo_unidade)

def remover_mensagem():
    label_status.config(text="")
    label_status.pack_forget()
    root.update_idletasks()

root = tk.Tk()
root.title("WeCanShopee")  # Nome da janela ajustado
root.state('zoomed')  # Janela maximizada

# Configurar o layout da tela com dois frames
frame_top = tk.Frame(root, bg="lightgray", height=300)
frame_bottom = tk.Frame(root, bg="white")

frame_top.pack(fill=tk.BOTH, expand=False)
frame_bottom.pack(fill=tk.BOTH, expand=True)

frame_top.grid_columnconfigure(0, weight=1)
frame_top.grid_columnconfigure(1, weight=1)
frame_top.grid_columnconfigure(2, weight=1)

fields_frame = tk.Frame(frame_top)
fields_frame.pack(pady=10)

# Label e campo de Data Início com máscara
label_data_inicio = tk.Label(fields_frame, text="Data Início:", font=("Arial", 12))
label_data_inicio.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_data_inicio = DateEntry(fields_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_data_inicio.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Label e campo de Data Fim com máscara
label_data_fim = tk.Label(fields_frame, text="Data Fim:", font=("Arial", 12))
label_data_fim.grid(row=0, column=2, padx=10, pady=10, sticky="e")
entry_data_fim = DateEntry(fields_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_data_fim.grid(row=0, column=3, padx=10, pady=10, sticky="w")

# Label e campo de Código Unidade
label_codigo_unidade = tk.Label(fields_frame, text="Código Unidade:", font=("Arial", 12))
label_codigo_unidade.grid(row=0, column=4, padx=10, pady=10, sticky="e")
entry_codigo_unidade = tk.Entry(fields_frame)
entry_codigo_unidade.grid(row=0, column=5, padx=10, pady=10, sticky="w")

# Botão Processar abaixo dos campos, centralizado
button_processar = tk.Button(frame_top, text="Processar", command=processar)
button_processar.pack(pady=10)

label_status = tk.Label(frame_top, text="", font=("Arial", 12))  # O label começa invisível

separator = tk.Canvas(frame_top, height=2, bg="black")
separator.pack(fill=tk.X, side=tk.BOTTOM)

root.mainloop()
