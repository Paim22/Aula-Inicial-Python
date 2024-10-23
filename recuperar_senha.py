import tkinter as tk
import sqlite3
from tkinter import messagebox

def retornar_login():
    janela_recuperacao.destroy()
    menu_inicial.deiconify()


def atualizar_senha():
    login = entry_login.get()
    nova_senha = entry_nova_senha.get()

    if login and nova_senha:
        conn = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE login_user SET senha = ? WHERE login = ?", (nova_senha, login))

        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
            retornar_login()  # Retorna para a tela de login
        else:
            messagebox.showerror("Erro", "Login não encontrado.")

        conn.close()
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")

janela_recuperacao = tk.Tk()
janela_recuperacao.title("Recuperação de Senha")
janela_recuperacao.geometry("450x300")

titulo_label = tk.Label(janela_recuperacao, text="Recuperar Senha", font=("Arial", 16, "bold"))
titulo_label.pack(pady=20)

label_login = tk.Label(janela_recuperacao, text="Login:")
label_login.pack(pady=5)
entry_login = tk.Entry(janela_recuperacao)
entry_login.pack(pady=5)

label_nova_senha = tk.Label(janela_recuperacao, text="Nova Senha:")
label_nova_senha.pack(pady=5)
entry_nova_senha = tk.Entry(janela_recuperacao, show="*")
entry_nova_senha.pack(pady=5)

botao_atualizar = tk.Button(janela_recuperacao, text="Atualizar Senha", command=atualizar_senha)
botao_atualizar.pack(pady=10)

botao_retornar = tk.Button(janela_recuperacao, text="Retornar para Tela de Login", command=retornar_login)
botao_retornar.pack(pady=10)

janela_recuperacao.mainloop()
