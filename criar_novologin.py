import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk

conn = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')
cursor = conn.cursor()

def cadastrar_usuario():
    login = entry_login.get()
    senha = entry_senha.get()

    if not login or not senha:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
        return

    try:
        cursor.execute("INSERT INTO login_user (login, senha) VALUES (?, ?)", (login, senha))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        retornar_menu_inicial()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Esse login já está em uso. Tente outro.")

def retornar_menu_inicial():
    janela_cadastro.destroy()
    abrir_menu_inicial()

def abrir_menu_inicial():
    menu_inicial = tk.Tk()
    menu_inicial.title("Menu Inicial")
    menu_inicial.geometry("400x400")

    label_bem_vindo = tk.Label(menu_inicial, text="Bem-vindo ao Menu Inicial")
    label_bem_vindo.pack(pady=20)

    menu_inicial.mainloop()

janela_cadastro = tk.Tk()
janela_cadastro.title("Cadastro de Usuário")
janela_cadastro.geometry("400x300")

titulo_label = tk.Label(janela_cadastro, text="Cadastro de Usuário", font=("Arial", 16, "bold"))
titulo_label.pack(pady=10)

label_login = tk.Label(janela_cadastro, text="Login:")
label_login.pack(pady=5)
entry_login = tk.Entry(janela_cadastro)
entry_login.pack(pady=5)

label_senha = tk.Label(janela_cadastro, text="Senha:")
label_senha.pack(pady=5)
entry_senha = tk.Entry(janela_cadastro, show="*")
entry_senha.pack(pady=5)

botao_cadastrar = tk.Button(janela_cadastro, text="Cadastrar Login", command=cadastrar_usuario)
botao_cadastrar.pack(pady=20)

janela_cadastro.mainloop()

conn.close()
