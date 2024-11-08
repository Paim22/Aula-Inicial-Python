import tkinter as tk
import sqlite3
import pandas as pd
import bcrypt
from tkinter import messagebox
from PIL import Image, ImageTk
from gestao_aluno import gestao_aluno
from gestao_categoria import gestao_categoria
from gestao_funcionario import gestao_funcionario
from gestao_salario import gestao_salario
from gestao_mensalidade import gestao_mensalidade

#conexão com o banco de dados
conn = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')

def abrir_tela_recuperacao():
    janela.withdraw()

    def atualizar_senha():
        login = entry_login_rec.get()
        nova_senha = entry_nova_senha.get()

        if login and nova_senha:
            cursor = conn.cursor()
            user = cursor.fetchone()

            if user:
                nova_senha_hashed = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE login_user SET senha = ? WHERE login = ?", (nova_senha_hashed, login))
                conn.commit()
                messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
                retornar_login()
            else:
                messagebox.showerror("Erro", "Login não encontrado.")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    def retornar_login():
        tela_recuperacao.destroy()
        janela.deiconify()

    tela_recuperacao = tk.Toplevel()
    tela_recuperacao.title("Recuperar Senha")
    tela_recuperacao.geometry("450x300")

    label_login_rec = tk.Label(tela_recuperacao, text="Login:")
    label_login_rec.pack(pady=5)
    entry_login_rec = tk.Entry(tela_recuperacao)
    entry_login_rec.pack(pady=5)

    label_nova_senha = tk.Label(tela_recuperacao, text="Nova Senha:")
    label_nova_senha.pack(pady=5)
    entry_nova_senha = tk.Entry(tela_recuperacao, show="*")
    entry_nova_senha.pack(pady=5)

    botao_atualizar_senha = tk.Button(tela_recuperacao, text="Atualizar Senha", command=atualizar_senha)
    botao_atualizar_senha.pack(pady=10)

    botao_retornar = tk.Button(tela_recuperacao, text="Retornar para Tela de Login", command=retornar_login)
    botao_retornar.pack(pady=10)

#função para realização de login no sistema
def fazer_login(event=None):
    usuario = entry_login.get()
    senha = entry_senha.get()

    if usuario and senha:
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM login_user WHERE login = ?", (usuario,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(senha.encode('utf-8'), user[0]):
                messagebox.showinfo("Login", "Login bem-sucedido!")
                abrir_menu_inicial()  # Abre o menu inicial
            else:
                messagebox.showerror("Erro", "Senha incorreta!")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado!")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")

def criar_novologin():
    janela.withdraw()

    tela_novologin = tk.Toplevel()
    tela_novologin.title("Criar Novo Login")
    tela_novologin.geometry("400x300")

    label_login = tk.Label(tela_novologin, text="Login:")
    label_login.pack(pady=5)
    entry_login_novo = tk.Entry(tela_novologin)
    entry_login_novo.pack(pady=5)

    label_senha = tk.Label(tela_novologin, text="Senha:")
    label_senha.pack(pady=5)
    entry_senha_nova = tk.Entry(tela_novologin, show="*")
    entry_senha_nova.pack(pady=5)

    def salvar_novologin():
        login = entry_login_novo.get()
        senha = entry_senha_nova.get()

        if login and senha:
            cursor = conn.cursor()
            # Verifica se o login já existe
            cursor.execute("SELECT login FROM login_user WHERE login = ?", (login,))
            user = cursor.fetchone()

            if user:
                messagebox.showerror("Erro", "Este login já está em uso. Por favor, escolha outro.")
            else:
                senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("INSERT INTO login_user (login, senha) VALUES (?, ?)", (login, senha_hashed))
                conn.commit()
                messagebox.showinfo("Sucesso", "Novo login criado com sucesso!")
                tela_novologin.destroy()
                janela.deiconify()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")

    botao_salvar_login = tk.Button(tela_novologin, text="Salvar", command=salvar_novologin)
    botao_salvar_login.pack(pady=10)

    botao_voltar = tk.Button(tela_novologin, text="Cancelar", command=lambda: [tela_novologin.destroy(), janela.deiconify()])
    botao_voltar.pack(pady=5)

#configuração de layout do menu incial
def abrir_menu_inicial():
    janela.withdraw()
    menu_inicial = tk.Toplevel()
    menu_inicial.title("Menu Inicial")
    menu_inicial.geometry("400x400")

    foto_original = Image.open("C:\\Users\\matheus.paim_onfly\\Downloads\\TechFute.png")
    foto_resized = foto_original.resize((80, 80))
    foto = ImageTk.PhotoImage(foto_resized)
    label_foto = tk.Label(menu_inicial, image=foto)
    label_foto.image = foto
    label_foto.place(x=280, y=5)

    label_bem_vindo = tk.Label(menu_inicial, text="SISTEMA DE GERENCIAMENTO TECHFUTE")
    label_bem_vindo.pack(pady=20)

    botoes = [
        ("Gestão de Aluno", gestao_aluno),
        ("Gestão de Funcionário", gestao_funcionario),
        ("Gestão de Salário", gestao_salario),
        ("Gestão de Mensalidade", gestao_mensalidade),
        ("Gestão de Categoria", gestao_categoria)
    ]

    for texto, comando in botoes:
        botao = tk.Button(menu_inicial, text=texto, width=30, command=comando)
        botao.pack(pady=5)

    botao_sair = tk.Button(menu_inicial, text="Retornar para Tela de Login", command=lambda: [menu_inicial.destroy(), janela.deiconify()])
    botao_sair.pack(pady=10)

    rodape_label = tk.Label(menu_inicial, text="© DEVELOPED BY CREATIVE TECH GROUP", font=("Arial", 8), anchor="e")
    rodape_label.pack(side="bottom", anchor="se", padx=10, pady=10)

janela = tk.Tk()
janela.title("Tela de Login")
janela.geometry("450x550")

titulo_label = tk.Label(janela, text="Sistema de Login TechFute", font=("Arial", 16, "bold"))
titulo_label.pack(pady=20)

label_login = tk.Label(janela, text="Login:")
label_login.pack(pady=5)
entry_login = tk.Entry(janela)
entry_login.pack(pady=5)

label_senha = tk.Label(janela, text="Senha:")
label_senha.pack(pady=5)
entry_senha = tk.Entry(janela, show="*")
entry_senha.pack(pady=5)

botao_login = tk.Button(janela, text="Fazer Login", command=fazer_login)
botao_login.pack(pady=10)

botao_novo_login = tk.Button(janela, text="Criar Novo Login", command=criar_novologin)
botao_novo_login.pack(pady=5)

botao_recuperar_senha = tk.Button(janela, text="Recuperar Senha", command=abrir_tela_recuperacao)
botao_recuperar_senha.pack(pady=5)

janela.bind('<Return>', fazer_login)

janela.mainloop()

conn.close()
