import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import DateEntry  # Biblioteca para entrada de data com máscara
import time
from pontomais_api import consultar_pontomais  # Importa a função da API

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def mostrar_confirmacao(data_inicio, data_fim, codigo_unidade):
    confirm_window = Toplevel(root)
    confirm_window.title("Confirme sua ação")
    largura, altura = 300, 200
    centralizar_janela(confirm_window, largura, altura)

    tk.Label(confirm_window, text="Confirme sua ação", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(confirm_window, text=f"Data Início: {data_inicio}", font=("Arial", 12)).pack(pady=5)
    tk.Label(confirm_window, text=f"Data Fim: {data_fim}", font=("Arial", 12)).pack(pady=5)
    tk.Label(confirm_window, text=f"Código Unidade: {codigo_unidade}", font=("Arial", 12)).pack(pady=5)

    def cancelar():
        confirm_window.destroy()

    def continuar():
        confirm_window.destroy()
        iniciar_processamento(data_inicio, data_fim, codigo_unidade)

    btn_frame = tk.Frame(confirm_window)
    btn_frame.pack(pady=10)

    btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=cancelar, width=10)
    btn_cancelar.grid(row=0, column=0, padx=5)

    btn_continuar = tk.Button(btn_frame, text="Continuar", command=continuar, width=10)
    btn_continuar.grid(row=0, column=1, padx=5)

def iniciar_processamento(data_inicio, data_fim, codigo_unidade):
    label_status.config(text="Processando...", fg="black")
    label_status.pack(pady=10)
    root.update_idletasks()

    df = consultar_pontomais(data_inicio, data_fim, codigo_unidade)

    if df is not None:
        print(df.head())  # Exibe as primeiras linhas do DataFrame no console
        label_status.config(text="Processamento concluído e dados carregados!", fg="green")
    else:
        label_status.config(text="Erro ao carregar os dados.", fg="red")

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
root.title("WeCanShopee")
root.state('zoomed')

frame_top = tk.Frame(root, bg="lightgray", height=300)
frame_bottom = tk.Frame(root, bg="white")
frame_top.pack(fill=tk.BOTH, expand=False)
frame_bottom.pack(fill=tk.BOTH, expand=True)

fields_frame = tk.Frame(frame_top)
fields_frame.pack(pady=10)

label_data_inicio = tk.Label(fields_frame, text="Data Início:", font=("Arial", 12))
label_data_inicio.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_data_inicio = DateEntry(fields_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_data_inicio.grid(row=0, column=1, padx=10, pady=10, sticky="w")

label_data_fim = tk.Label(fields_frame, text="Data Fim:", font=("Arial", 12))
label_data_fim.grid(row=0, column=2, padx=10, pady=10, sticky="e")
entry_data_fim = DateEntry(fields_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
entry_data_fim.grid(row=0, column=3, padx=10, pady=10, sticky="w")

label_codigo_unidade = tk.Label(fields_frame, text="Código Unidade:", font=("Arial", 12))
label_codigo_unidade.grid(row=0, column=4, padx=10, pady=10, sticky="e")
entry_codigo_unidade = tk.Entry(fields_frame)
entry_codigo_unidade.grid(row=0, column=5, padx=10, pady=10, sticky="w")

button_processar = tk.Button(frame_top, text="Processar", command=processar)
button_processar.pack(pady=10)

label_status = tk.Label(frame_top, text="", font=("Arial", 12))
separator = tk.Canvas(frame_top, height=2, bg="black")
separator.pack(fill=tk.X, side=tk.BOTTOM)

root.mainloop()
