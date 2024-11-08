import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

#conexão com o banco de dados
conn = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')
cursor = conn.cursor()

#configuração da tela principal
def gestao_funcionario():
    janela_funcionario = tk.Toplevel()
    janela_funcionario.title("Gestão de Funcionário")
    janela_funcionario.geometry("800x600")

    titulo = tk.Label(janela_funcionario, text="Gestão de Funcionário", font=("Helvetica", 16, "bold"))
    titulo.place(relx=0.5, y=10, anchor="center")

    frame_campos = tk.Frame(janela_funcionario)
    frame_campos.place(x=20, y=50)

    tk.Label(frame_campos, text="Nome:").grid(row=0, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame_campos)
    entry_nome.grid(row=0, column=1, pady=5)

    tk.Label(frame_campos, text="Idade:").grid(row=1, column=0, pady=5, sticky="w")
    entry_idade = tk.Entry(frame_campos)
    entry_idade.grid(row=1, column=1, pady=5)

    tk.Label(frame_campos, text="Formação:").grid(row=2, column=0, pady=5, sticky="w")
    entry_formacao = tk.Entry(frame_campos)
    entry_formacao.grid(row=2, column=1, pady=5)

    tk.Label(frame_campos, text="CPF:").grid(row=3, column=0, pady=5, sticky="w")
    entry_cpf = tk.Entry(frame_campos)
    entry_cpf.grid(row=3, column=1, pady=5)

    tk.Label(frame_campos, text="Data de Nascimento:").grid(row=4, column=0, pady=5, sticky="w")
    entry_nascimento = tk.Entry(frame_campos)
    entry_nascimento.grid(row=4, column=1, pady=5)

    tk.Label(frame_campos, text="Data de Entrada:").grid(row=5, column=0, pady=5, sticky="w")
    entry_entrada = tk.Entry(frame_campos)
    entry_entrada.grid(row=5, column=1, pady=5)


    tk.Label(frame_campos, text="Número de Celular:").grid(row=6, column=0, pady=5, sticky="w")
    entry_numero_celular = tk.Entry(frame_campos)
    entry_numero_celular.grid(row=6, column=1, pady=5)

    tk.Label(frame_campos, text="Salário:").grid(row=7, column=0, pady=5, sticky="w")
    salario_combobox = ttk.Combobox(frame_campos)
    salario_combobox.grid(row=7, column=1, pady=5)

    def obter_salarios():
        cursor.execute("SELECT Valor_Salario FROM cadastro_salario")
        salarios = [str(cadastro_salario[0]) for cadastro_salario in cursor.fetchall()]
        salario_combobox['values'] = salarios

    obter_salarios()

    #configuração da tabela do código
    def adicionar_tabela():
        cursor.execute("INSERT INTO cadastrofuncionario (nome, idade, formacao, cpf, datanascimento, dataentrada, numero_celular) VALUES ( ?, ?, ?, ?, ?, ?, ?)",
                       (entry_nome.get(), entry_idade.get(), entry_formacao.get(), entry_cpf.get(), entry_nascimento.get(), entry_entrada.get(), entry_numero_celular.get()))
        conn.commit()
        carregar_tabela()
        limpar_campos()

    def carregar_tabela():
        tabela.delete(*tabela.get_children())
        cursor.execute("SELECT * FROM cadastrofuncionario")
        for row in cursor.fetchall():
            tabela.insert("", "end", values=row[1:])  # Ignora o ID

    def limpar_campos():
        entry_nome.delete(0, 'end')
        entry_idade.delete(0, 'end')
        entry_formacao.delete(0, 'end')
        entry_cpf.delete(0, 'end')
        entry_nascimento.delete(0, 'end')
        entry_entrada.delete(0, 'end')
        entry_numero_celular.delete(0, 'end')
        salario_combobox.set('')

    #exclusão de funcionário
    def excluir_funcionario():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showwarning("Nenhum registro selecionado", "Por favor, selecione um registro para excluir.")
            return
        resposta = messagebox.askquestion("Confirmar", "Deseja mesmo excluir esse funcionário do sistema?")
        if resposta == 'yes':
            cursor.execute("DELETE FROM cadastrofuncionario WHERE nome=?", (tabela.item(selected_item)['values'][0],))  # Usa o nome para exclusão
            conn.commit()
            carregar_tabela()
            messagebox.showinfo("Exclusão", "Funcionário excluído com sucesso!")

    #edição de funcionário
    def editar_funcionario():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showwarning("Nenhum registro selecionado", "Por favor, selecione um registro para alterar.")
            return

        valores = tabela.item(selected_item)['values']
        entry_nome.insert(0, valores[0])
        entry_idade.insert(0, valores[1])
        entry_formacao.insert(0, valores[2])
        entry_cpf.insert(0, valores[3])
        entry_nascimento.insert(0, valores[4])
        entry_entrada.insert(0, valores[5])
        entry_numero_celular.insert(0, valores[6])
        salario_combobox.set(valores[7])

        def confirmar_edicao():
            cursor.execute("UPDATE cadastrofuncionario SET idade=?, formacao=?, cpf=?, nascimento=?, entrada=?, salario=?, numero_celular=? WHERE nome=?",
                           (entry_idade.get(), entry_formacao.get(), entry_cpf.get(), entry_nascimento.get(), entry_entrada.get(), salario_combobox.get(), entry_numero_celular.get(), valores[0]))  # Usa o nome original para localizar
            conn.commit()
            carregar_tabela()
            limpar_campos()
            edicao_janela.destroy()

        edicao_janela = tk.Toplevel(janela_funcionario)
        edicao_janela.title("Alterar Registro")
        tk.Label(edicao_janela, text="Confirmar Alteração").pack()
        tk.Button(edicao_janela, text="Confirmar", command=confirmar_edicao).pack()

    frame_botoes = tk.Frame(janela_funcionario)
    frame_botoes.place(x=600, y=50)

    tk.Button(frame_botoes, text="Cadastrar Funcionário", command=adicionar_tabela).pack(pady=20, padx=20, expand=True)
    tk.Button(frame_botoes, text="Excluir Usuário", command=excluir_funcionario).pack(pady=5)
    tk.Button(frame_botoes, text="Alterar Registro", command=editar_funcionario).pack(pady=5)

    botao_menu_inicial = tk.Button(janela_funcionario, text="Menu Inicial",
                                   command=lambda: [janela_funcionario.destroy()])
    botao_menu_inicial.place(x=(800 - 100) / 2, y=200)

    scrollbar_x = tk.Scrollbar(janela_funcionario, orient="horizontal")
    scrollbar_x.place(x=50, y=500, width=700)

    colunas = ("nome", "idade", "formacao", "cpf", "nascimento", "entrada", "salario", "numero_celular")
    tabela = ttk.Treeview(janela_funcionario, columns=colunas, show="headings", xscrollcommand=scrollbar_x.set)

    tabela.heading("nome", text="Nome")
    tabela.heading("idade", text="Idade")
    tabela.heading("formacao", text="Formação")
    tabela.heading("cpf", text="CPF")
    tabela.heading("nascimento", text="Data de Nascimento")
    tabela.heading("entrada", text="Data de Entrada")
    tabela.heading("salario", text="Salário")
    tabela.heading("numero_celular", text="Número de Celular")

    #configuração da barra horizontal da tabela
    tabela.place(x=50, y=300, width=700, height=200)
    scrollbar_x.config(command=tabela.xview)

    rodape_label = tk.Label(janela_funcionario, text="© DEVELOPED BY CREATIVE TECH GROUP", font=("Arial", 8), anchor="e")
    rodape_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    carregar_tabela()



