import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def conectar_banco():
    return sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')

def gestao_salario():
    conn = conectar_banco()

    def adicionar_tabela():
        if not (entry_anodevigencia.get() and entry_descricaodepagamento.get() and entry_valordosalario.get()):
            messagebox.showerror("Erro", "Nenhum registro inserido.")
            return

        cursor = conn.cursor()
        cursor.execute("INSERT INTO cadastro_salario (Ano_vigencia, Descricao_pagamento, Valor_Salario) VALUES (?, ?, ?)",
                       (entry_anodevigencia.get(), entry_descricaodepagamento.get(), entry_valordosalario.get()))
        conn.commit()

        tabela.insert("", "end", values=(
            entry_anodevigencia.get(),
            entry_descricaodepagamento.get(),
            entry_valordosalario.get()
        ))

        entry_anodevigencia.delete(0, 'end')
        entry_descricaodepagamento.delete(0, 'end')
        entry_valordosalario.delete(0, 'end')

    def excluir_salario():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum registro selecionado.")
            return

        resposta = messagebox.askquestion("Confirmar", "Deseja mesmo excluir esse salário do sistema?")
        if resposta == 'yes':
            item = tabela.item(selecionado)
            ano_vigencia = item['values'][0]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cadastro_salario WHERE Ano_vigencia = ?", (ano_vigencia,))
            conn.commit()

            for i in selecionado:
                tabela.delete(i)

            messagebox.showinfo("Exclusão", "Salário excluído com sucesso!")
        else:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.")

    def editar_salario():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum registro selecionado.")
            return

        item = tabela.item(selecionado)
        ano_vigencia = item['values'][0]

        if not (entry_anodevigencia.get() and entry_descricaodepagamento.get() and entry_valordosalario.get()):
            messagebox.showerror("Erro", "Nenhum registro inserido.")
            return

        cursor = conn.cursor()
        cursor.execute('''UPDATE cadastro_salario
                          SET Ano_vigencia = ?, Descricao_pagamento = ?, Valor_Salario = ?
                          WHERE Ano_vigencia = ?''',
                       (entry_anodevigencia.get(), entry_descricaodepagamento.get(), entry_valordosalario.get(), ano_vigencia))
        conn.commit()

        for i in selecionado:
            tabela.item(i, values=(entry_anodevigencia.get(), entry_descricaodepagamento.get(), entry_valordosalario.get()))

        messagebox.showinfo("Editar", "Edição de registro realizada com sucesso!")

    # Janela principal de gestão de salário
    janela_salario = tk.Toplevel()
    janela_salario.title("Gestão de Salário")
    janela_salario.geometry("800x600")

    titulo = tk.Label(janela_salario, text="Gestão de Salário", font=("Helvetica", 16, "bold"))
    titulo.place(relx=0.5, y=10, anchor="center")

    frame_campos = tk.Frame(janela_salario)
    frame_campos.place(x=20, y=50)

    tk.Label(frame_campos, text="Ano de Vigência:").grid(row=0, column=0, pady=5, sticky="w")
    entry_anodevigencia = tk.Entry(frame_campos)
    entry_anodevigencia.grid(row=0, column=1, pady=5)

    tk.Label(frame_campos, text="Descrição do Pagamento:").grid(row=1, column=0, pady=5, sticky="w")
    entry_descricaodepagamento = tk.Entry(frame_campos)
    entry_descricaodepagamento.grid(row=1, column=1, pady=5)

    tk.Label(frame_campos, text="Valor do Salário:").grid(row=2, column=0, pady=5, sticky="w")
    entry_valordosalario = tk.Entry(frame_campos)
    entry_valordosalario.grid(row=2, column=1, pady=5)

    frame_botoes = tk.Frame(janela_salario)
    frame_botoes.place(x=600, y=50)

    tk.Button(frame_botoes, text="Cadastrar Salário", command=adicionar_tabela).pack(pady=5)
    tk.Button(frame_botoes, text="Excluir Salário", command=excluir_salario).pack(pady=5)
    tk.Button(frame_botoes, text="Editar Registro", command=editar_salario).pack(pady=5)

    botao_menu_inicial = tk.Button(janela_salario, text="Menu Inicial",
                                   command=lambda: [janela_salario.destroy()])
    botao_menu_inicial.place(x=350, y=250)

    scrollbar_x = tk.Scrollbar(janela_salario, orient="horizontal")
    scrollbar_x.place(x=50, y=500, width=700)

    colunas = ("Ano de Vigência", "Descrição de Pagamento", "Valor do Salário")
    tabela = ttk.Treeview(janela_salario, columns=colunas, show="headings", xscrollcommand=scrollbar_x.set)

    tabela.heading("Ano de Vigência", text="Ano de Vigência")
    tabela.heading("Descrição de Pagamento", text="Descrição de Pagamento")
    tabela.heading("Valor do Salário", text="Valor do Salário")

    tabela.place(x=50, y=300, width=700, height=200)

    scrollbar_x.config(command=tabela.xview)

    rodape_label = tk.Label(janela_salario, text="© DEVELOPED BY CREATIVE TECH GROUP", font=("Arial", 8), anchor="e")
    rodape_label.pack(side="bottom", anchor="se", padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão")
    root.geometry("300x200")
    tk.Button(root, text="Gestão de Salário", command=gestao_salario).pack(pady=50)
    root.mainloop()
