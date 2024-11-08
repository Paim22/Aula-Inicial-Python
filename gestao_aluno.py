import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import subprocess

#conexão com o banco de dados
conn = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')
cursor = conn.cursor()

#definição de categoria por idade
def obter_categorias_por_idade(idade):
    if idade >= 4 and idade <= 5:
        return ['Sub 5']
    elif idade >= 6 and idade <= 7:
        return ['Sub 7']
    elif idade >= 8 and idade <= 9:
        return ['Sub 9']
    elif idade >= 10 and idade <= 11:
        return ['Sub 11']
    elif idade >= 12 and idade <= 13:
        return ['Sub 13']
    else:
        return []

#configuração de conexão com outros códigos do sistema
def obter_categorias():
    cursor.execute("SELECT Tipo_categoria FROM cadastro_categoria")
    return [categoria[0] for categoria in cursor.fetchall()]

def obter_mensalidades_por_cpf(cpf):
    cursor.execute("SELECT Valor_mensalidade FROM cadastro_mensalidade WHERE cpfaluno_mensalidade = ?", (cpf,))
    mensalidades = cursor.fetchall()
    return [str(mensalidade[0]) for mensalidade in mensalidades]

def abrir_menu_inicial(janela_aluno):
    # Executa o arquivo menu_inicial.py
    subprocess.Popen(['python', 'C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/menu_inicial.py'])
    janela_aluno.destroy()  # Fecha a janela atual

def gestao_aluno():
    janela_aluno = tk.Toplevel()
    janela_aluno.title("Gestão de Aluno")
    janela_aluno.geometry("800x600")

    titulo = tk.Label(janela_aluno, text="Gestão de Aluno", font=("Helvetica", 16, "bold"))
    titulo.place(relx=0.5, y=10, anchor="center")

    frame_campos = tk.Frame(janela_aluno)
    frame_campos.place(x=20, y=50)

    tk.Label(frame_campos, text="Nome do Aluno:").grid(row=0, column=0, pady=5, sticky="w")
    entry_nome = tk.Entry(frame_campos)
    entry_nome.grid(row=0, column=1, pady=5)

    tk.Label(frame_campos, text="Idade:").grid(row=0, column=2, pady=5, sticky="w")
    entry_idade = tk.Entry(frame_campos)
    entry_idade.grid(row=0, column=3, pady=5)

    tk.Label(frame_campos, text="Data de Nascimento:").grid(row=1, column=0, pady=5, sticky="w")
    entry_nascimento = tk.Entry(frame_campos)
    entry_nascimento.grid(row=1, column=1, pady=5)

    tk.Label(frame_campos, text="CPF:").grid(row=1, column=2, pady=5, sticky="w")
    entry_cpf = tk.Entry(frame_campos)
    entry_cpf.grid(row=1, column=3, pady=5)

    tk.Label(frame_campos, text="Número de Matrícula:").grid(row=2, column=0, pady=5, sticky="w")
    entry_matricula = tk.Entry(frame_campos)
    entry_matricula.grid(row=2, column=1, pady=5)

    tk.Label(frame_campos, text="Nome do Responsável:").grid(row=2, column=2, pady=5, sticky="w")
    entry_nome_responsavel = tk.Entry(frame_campos)
    entry_nome_responsavel.grid(row=2, column=3, pady=5)

    tk.Label(frame_campos, text="Parentesco do Responsável:").grid(row=3, column=0, pady=5, sticky="w")
    entry_parentesco_responsavel = tk.Entry(frame_campos)
    entry_parentesco_responsavel.grid(row=3, column=1, pady=5)

    tk.Label(frame_campos, text="Telefone do Responsável:").grid(row=3, column=2, pady=5, sticky="w")
    entry_telefone_responsavel = tk.Entry(frame_campos)
    entry_telefone_responsavel.grid(row=3, column=3, pady=5)

    tk.Label(frame_campos, text="Categoria do Aluno:").grid(row=4, column=0, pady=5, sticky="w")
    categoria_combobox = ttk.Combobox(frame_campos, state="disabled")
    categoria_combobox.grid(row=4, column=1, pady=5)

    tk.Label(frame_campos, text="Valor de Mensalidade:").grid(row=4, column=2, pady=5, sticky="w")
    mensalidade_combobox = ttk.Combobox(frame_campos)  # Sem valores inicialmente
    mensalidade_combobox.grid(row=4, column=3, pady=5)
    mensalidade_combobox['state'] = 'disabled'

    #configuração da tabela presente no código
    columns = (
    "Nome", "Idade", "Matrícula", "Data de Nascimento", "Nome do Responsável", "Telefone", "Categoria", "Mensalidade")
    tabela = ttk.Treeview(janela_aluno, columns=columns, show='headings')
    tabela.place(x=10, y=300, width=750, height=250)

    scrollbar_x = tk.Scrollbar(janela_aluno, orient="horizontal")
    scrollbar_x.place(x=50, y=500, width=700)

    for col in columns:
        tabela.heading(col, text=col)
        tabela.column(col, width=100)

        def validar_cpf(event):
            cpf = entry_cpf.get()
            if cpf:
                mensalidades = obter_mensalidades_por_cpf(cpf)

                if mensalidades:
                    mensalidade_combobox['state'] = 'readonly'
                    mensalidade_combobox['values'] = mensalidades
                else:
                    mensalidade_combobox['state'] = 'disabled'
                    mensalidade_combobox.set('')
                    messagebox.showwarning("CPF não encontrado", "O CPF informado não tem mensalidades cadastradas.")

        entry_cpf.bind("<FocusOut>", validar_cpf)

    #função para puxar categoria de acordo com idade
    def idade_preenchida(event):
        try:
            idade = int(entry_idade.get())
            categorias = obter_categorias_por_idade(idade)
            if categorias:
                categoria_combobox['values'] = categorias
                categoria_combobox['state'] = 'readonly'
            else:
                messagebox.showwarning("Idade Inválida", "Não há categorias disponíveis para essa idade.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para a idade.")

    entry_idade.bind("<FocusOut>", idade_preenchida)

    #função para adicionar aluno no sistema
    def adicionar_aluno():
        nome = entry_nome.get()
        idade = entry_idade.get()
        nascimento = entry_nascimento.get()
        cpf = entry_cpf.get()
        matricula = entry_matricula.get()
        nome_responsavel = entry_nome_responsavel.get()
        parentesco_responsavel = entry_parentesco_responsavel.get()
        telefone_responsavel = entry_telefone_responsavel.get()
        categoria = categoria_combobox.get()
        mensalidade = mensalidade_combobox.get()

        cursor.execute("SELECT matricula_numero FROM alunos WHERE matricula_numero = ?", (matricula,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Matrícula já cadastrada!")
        else:
            try:
                cursor.execute('''INSERT INTO alunos (nome, idade, data_nascimento, cpf, matricula_numero, 
                                nome_responsavel, parentesco_responsavel, telefone_responsavel, categoria, mensalidade)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (nome, idade, nascimento, cpf, matricula, nome_responsavel, parentesco_responsavel, telefone_responsavel, categoria, mensalidade))
                conn.commit()
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                adicionar_tabela()

            except sqlite3.Error as e:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao inserir dados: {e}")

    #edição de aluno
    def alterar_aluno():
        try:
            selected_item = tabela.selection()[0]
            valores = tabela.item(selected_item, "values")

            entry_nome.delete(0, 'end')
            entry_nome.insert(0, valores[0])
            entry_idade.delete(0, 'end')
            entry_idade.insert(0, valores[1])
            entry_matricula.delete(0, 'end')
            entry_matricula.insert(0, valores[2])
            entry_nascimento.delete(0, 'end')
            entry_nascimento.insert(0, valores[3])
            entry_nome_responsavel.delete(0, 'end')
            entry_nome_responsavel.insert(0, valores[4])
            entry_telefone_responsavel.delete(0, 'end')
            entry_telefone_responsavel.insert(0, valores[5])
            categoria_combobox.set(valores[6])
            mensalidade_combobox.set(valores[7])

            def salvar_alteracoes():
                nome = entry_nome.get()
                idade = entry_idade.get()
                matricula = entry_matricula.get()
                nascimento = entry_nascimento.get()
                nome_responsavel = entry_nome_responsavel.get()
                telefone_responsavel = entry_telefone_responsavel.get()
                categoria = categoria_combobox.get()
                mensalidade = mensalidade_combobox.get()

                cursor.execute('''UPDATE alunos 
                                  SET nome = ?, idade = ?, data_nascimento = ?, nome_responsavel = ?, telefone_responsavel = ?, categoria = ?, mensalidade = ? 
                                  WHERE matricula_numero = ?''',
                               (nome, idade, nascimento, nome_responsavel, telefone_responsavel, categoria, mensalidade,
                                matricula))
                conn.commit()

                tabela.item(selected_item, values=(nome, idade, matricula, nascimento, nome_responsavel, telefone_responsavel, categoria, mensalidade))

                messagebox.showinfo("Sucesso", "Registro alterado com sucesso!")
                janela_alterar.destroy()

            janela_alterar = tk.Toplevel()
            janela_alterar.title("Salvar Alterações")
            tk.Label(janela_alterar, text="Deseja salvar as alterações?").pack(pady=10)
            tk.Button(janela_alterar, text="Sim", command=salvar_alteracoes).pack(pady=5)
            tk.Button(janela_alterar, text="Não", command=janela_alterar.destroy).pack(pady=5)

        except IndexError:
            messagebox.showerror("Erro", "Selecione um aluno na tabela para alterar!")

    #exclusão de aluno
    def excluir_aluno():
        try:
            selected_item = tabela.selection()[0]  # Seleciona o item atual
            matricula = tabela.item(selected_item, "values")[2]  # Pega a matrícula do aluno

            cursor.execute("SELECT cpf FROM alunos WHERE matricula_numero = ?", (matricula,))
            resultado = cursor.fetchone()

            if resultado:
                cpf_aluno = resultado[0]

                # Verifica se existe uma mensalidade cadastrada para esse CPF na tabela 'mensalidades'
                cursor.execute("SELECT * FROM mensalidades WHERE cpf = ?", (cpf_aluno,))
                mensalidade = cursor.fetchone()

                if mensalidade:
                    messagebox.showwarning("Aviso",
                                           "CPF do aluno com mensalidade cadastrada, apague a mensalidade e tente novamente.")
                else:
                    resposta = messagebox.askyesno("Confirmação", "Deseja confirmar a exclusão do aluno?")
                    if resposta:
                        # Exclui o aluno da tabela 'alunos'
                        cursor.execute("DELETE FROM alunos WHERE matricula_numero = ?", (matricula,))
                        conn.commit()
                        messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                        tabela.delete(selected_item)
            else:
                messagebox.showerror("Erro", "Aluno não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


        except IndexError:
            messagebox.showerror("Erro", "Selecione um aluno na tabela para excluir!")

    def adicionar_tabela():
        cursor.execute("SELECT * FROM alunos")
        tabela.delete(*tabela.get_children())
        for row in cursor.fetchall():
            tabela.insert('', 'end', values=row)

    btn_cadastrar = tk.Button(janela_aluno, text="Cadastrar Aluno", command=adicionar_aluno)
    btn_cadastrar.place(relx=0.5, y=240, anchor="center")

    button_alterar = tk.Button(janela_aluno, text="Alterar Registro do Aluno", command=alterar_aluno)
    button_alterar.place(x=650, y=50)

    button_excluir = tk.Button(janela_aluno, text="Excluir Aluno", command=excluir_aluno)
    button_excluir.place(x=650, y=100)

    button_menu_inicial = tk.Button(janela_aluno, text="Menu Inicial", command=lambda: abrir_menu_inicial(janela_aluno))
    button_menu_inicial.place(x=400, y=270, anchor="center")

    tabela.place(x=50, y=300, width=700, height=200)
    scrollbar_x.config(command=tabela.xview)

    rodape_label = tk.Label(janela_aluno, text="© DEVELOPED BY CREATIVE TECH GROUP", font=("Arial", 8), anchor="e")
    rodape_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    adicionar_tabela()

