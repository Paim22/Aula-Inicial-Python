import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

conn = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')
cursor = conn.cursor()

def gestao_mensalidade():
    janela_mensalidade = tk.Toplevel()
    janela_mensalidade.title("Gestão de Mensalidade")
    janela_mensalidade.geometry("800x600")

    titulo = tk.Label(janela_mensalidade, text="Gestão de Mensalidade", font=("Helvetica", 16, "bold"))
    titulo.place(relx=0.5, y=10, anchor="center")

    frame_campos = tk.Frame(janela_mensalidade)
    frame_campos.place(x=20, y=50)

    tk.Label(frame_campos, text="Ano de Vigência:").grid(row=0, column=0, pady=5, sticky="w")
    entry_anodevigencia = tk.Entry(frame_campos)
    entry_anodevigencia.grid(row=0, column=1, pady=5)

    tk.Label(frame_campos, text="Descrição da Mensalidade:").grid(row=1, column=0, pady=5, sticky="w")
    entry_descricaodemensalidade = tk.Entry(frame_campos)
    entry_descricaodemensalidade.grid(row=1, column=1, pady=5)

    tk.Label(frame_campos, text="Valor da Mensalidade:").grid(row=2, column=0, pady=5, sticky="w")
    entry_valordemensalidade = tk.Entry(frame_campos)
    entry_valordemensalidade.grid(row=2, column=1, pady=5)

    tk.Label(frame_campos, text="CPF do Aluno:").grid(row=3, column=0, pady=5, sticky="w")
    entry_cpfdoaluno = tk.Entry(frame_campos)
    entry_cpfdoaluno.grid(row=3, column=1, pady=5)

    def adicionar_tabela():
        try:
            ano_vigencia = int(entry_anodevigencia.get())
            descricao_mensalidade = entry_descricaodemensalidade.get()
            valor_mensalidade = float(entry_valordemensalidade.get())
            cpfdoaluno = entry_cpfdoaluno.get()

            if not ano_vigencia or not descricao_mensalidade or not valor_mensalidade or not cpfdoaluno:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            else:
                cursor.execute('''
                    INSERT INTO cadastro_mensalidade (Ano_vigencia, Descricao_mensalidade, Valor_mensalidade, cpfaluno_mensalidade)
                    VALUES (?, ?, ?, ?)
                ''', (ano_vigencia, descricao_mensalidade, valor_mensalidade, cpfdoaluno))
                conn.commit()
                messagebox.showinfo("Sucesso", "Mensalidade cadastrada com sucesso!")
                carregar_tabela()  # Recarregar a tabela após adicionar a nova mensalidade
                limpar_campos()

        except ValueError:
            messagebox.showerror("Erro",
                                 "Por favor, insira valores válidos para Ano de Vigência e Valor da Mensalidade.")

    def limpar_campos():
        """Limpa os campos de entrada."""
        entry_anodevigencia.delete(0, 'end')
        entry_descricaodemensalidade.delete(0, 'end')
        entry_valordemensalidade.delete(0, 'end')
        entry_cpfdoaluno.delete(0, 'end')

    def carregar_tabela():
        """Carrega as mensalidades cadastradas no banco de dados e insere na tabela."""
        tabela.delete(*tabela.get_children())  # Limpa a tabela
        cursor.execute('SELECT * FROM cadastro_mensalidade')  # Seleciona todas as mensalidades
        mensalidades = cursor.fetchall()
        for mensalidade in mensalidades:
            tabela.insert("", "end", values=(mensalidade[0], mensalidade[1], mensalidade[2], mensalidade[3]))

    def excluir_mensalidade():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum registro selecionado")
        else:
            resposta = messagebox.askquestion("Confirmar", "Deseja mesmo excluir essa mensalidade do sistema?")
            if resposta == 'yes':
                item = tabela.item(selected_item)
                ano_vigencia = item['values'][0]
                cursor.execute('DELETE FROM cadastro_mensalidade WHERE Ano_vigencia = ?', (ano_vigencia,))
                conn.commit()
                carregar_tabela()  # Atualiza a tabela após a exclusão
                messagebox.showinfo("Exclusão", "Mensalidade excluída com sucesso!")

    def editar_mensalidade():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum registro selecionado")
        else:
            item = tabela.item(selected_item)
            ano_vigencia = item['values'][0]

            nova_descricao = entry_descricaodemensalidade.get()
            novo_valor = entry_valordemensalidade.get()

            if not nova_descricao or not novo_valor:
                messagebox.showerror("Erro", "Nenhum registro selecionado")
            else:
                cursor.execute('''
                    UPDATE cadastro_mensalidade
                    SET Descricao_mensalidade = ?, Valor_mensalidade = ?
                    WHERE Ano_vigencia = ?
                ''', (nova_descricao, novo_valor, ano_vigencia))
                conn.commit()
                carregar_tabela()  # Atualiza a tabela após a edição
                messagebox.showinfo("Editar", "Edição de registro realizada com sucesso!")

    frame_botoes = tk.Frame(janela_mensalidade)
    frame_botoes.place(x=600, y=50)

    tk.Button(frame_botoes, text="Cadastrar Mensalidade", command=adicionar_tabela).pack(pady=5)
    tk.Button(frame_botoes, text="Excluir Mensalidade", command=excluir_mensalidade).pack(pady=5)
    tk.Button(frame_botoes, text="Editar Registro", command=editar_mensalidade).pack(pady=5)

    botao_menu_inicial = tk.Button(janela_mensalidade, text="Menu Inicial",
                                   command=lambda: [janela_mensalidade.destroy()])
    botao_menu_inicial.place(x=350, y=250)

    scrollbar_x = tk.Scrollbar(janela_mensalidade, orient="horizontal")
    scrollbar_x.place(x=50, y=500, width=700)

    colunas = ("Ano de Vigência", "Descrição da Mensalidade", "Valor da Mensalidade", "CPF do Aluno")
    tabela = ttk.Treeview(janela_mensalidade, columns=colunas, show="headings", xscrollcommand=scrollbar_x.set)

    tabela.heading("Ano de Vigência", text="Ano de Vigência")
    tabela.heading("Descrição da Mensalidade", text="Descrição da Mensalidade")
    tabela.heading("Valor da Mensalidade", text="Valor da Mensalidade")
    tabela.heading("CPF do Aluno", text="CPF do Aluno")

    tabela.place(x=50, y=300, width=700, height=200)

    scrollbar_x.config(command=tabela.xview)

    rodape_label = tk.Label(janela_mensalidade, text="© DEVELOPED BY CREATIVE TECH GROUP", font=("Arial", 8), anchor="e")
    rodape_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    carregar_tabela()  # Carrega as mensalidades ao abrir a janela

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão")
    root.geometry("300x200")

    tk.Button(root, text="Gestão de Mensalidade", command=gestao_mensalidade).pack(pady=50)

    root.mainloop()

