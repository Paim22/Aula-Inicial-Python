import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

conexao = sqlite3.connect('C:/Users/matheus.paim_onfly/Desktop/Faculdade/RAD/Banco_Python__RAD_BACKUP.db')
cursor = conexao.cursor()

def gestao_categoria():
    def carregar_dados():
        tabela.delete(*tabela.get_children())
        for row in cursor.execute("SELECT * FROM cadastro_categoria"):
            tabela.insert("", "end", values=(row[1], row[2]))

    def adicionar_tabela():
        tipo_categoria = entry_tipodecategoria.get()
        descricao_categoria = entry_descricaodecategoria.get()

        if tipo_categoria == "" or descricao_categoria == "":
            messagebox.showerror("Erro", "Nenhuma Informação inserida.")
        else:
            cursor.execute("INSERT INTO cadastro_categoria (Tipo_categoria, Descricao_categoria) VALUES (?, ?)",
                           (tipo_categoria, descricao_categoria))
            conexao.commit()
            tabela.insert("", "end", values=(tipo_categoria, descricao_categoria))
            entry_tipodecategoria.delete(0, 'end')
            entry_descricaodecategoria.delete(0, 'end')

    def excluir_categoria():
        """Excluir a categoria selecionada."""
        try:
            selecionado = tabela.selection()[0]
            valores = tabela.item(selecionado, "values")
            resposta = messagebox.askquestion("Confirmar", "Deseja excluir essa categoria?")
            if resposta == 'yes':
                cursor.execute("DELETE FROM cadastro_categoria WHERE Tipo_categoria=? AND Descricao_categoria=?",
                               (valores[0], valores[1]))
                conexao.commit()
                tabela.delete(selecionado)
                messagebox.showinfo("Exclusão", "Categoria excluída com sucesso!")
        except IndexError:
            messagebox.showerror("Erro", "Nenhuma Categoria Selecionada.")

    def editar_categoria():
        """Editar a categoria selecionada."""
        try:
            selecionado = tabela.selection()[0]
            valores = tabela.item(selecionado, "values")

            tipo_categoria_novo = entry_tipodecategoria.get()
            descricao_categoria_novo = entry_descricaodecategoria.get()

            if tipo_categoria_novo == "" or descricao_categoria_novo == "":
                messagebox.showerror("Erro", "Nenhuma Informação inserida.")
            else:
                cursor.execute("""
                UPDATE cadastro_categoria 
                SET Tipo_categoria=?, Descricao_categoria=? 
                WHERE Tipo_categoria=? AND Descricao_categoria=?""",
                               (tipo_categoria_novo, descricao_categoria_novo, valores[0], valores[1]))
                conexao.commit()
                tabela.item(selecionado, values=(tipo_categoria_novo, descricao_categoria_novo))
                messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
                entry_tipodecategoria.delete(0, 'end')
                entry_descricaodecategoria.delete(0, 'end')

        except IndexError:
            messagebox.showerror("Erro", "Nenhuma Categoria Selecionada.")

    janela_categoria = tk.Toplevel()
    janela_categoria.title("Gestão de Categoria")
    janela_categoria.geometry("800x600")

    titulo = tk.Label(janela_categoria, text="Gestão de Categoria", font=("Helvetica", 16, "bold"))
    titulo.place(relx=0.5, y=10, anchor="center")

    frame_campos = tk.Frame(janela_categoria)
    frame_campos.place(x=20, y=50)

    tk.Label(frame_campos, text="Tipo de Categoria:").grid(row=0, column=0, pady=5, sticky="w")
    entry_tipodecategoria = tk.Entry(frame_campos)
    entry_tipodecategoria.grid(row=0, column=1, pady=5)

    tk.Label(frame_campos, text="Descrição da Categoria:").grid(row=1, column=0, pady=5, sticky="w")
    entry_descricaodecategoria = tk.Entry(frame_campos)
    entry_descricaodecategoria.grid(row=1, column=1, pady=5)

    frame_botoes = tk.Frame(janela_categoria)
    frame_botoes.place(x=600, y=50)

    tk.Button(frame_botoes, text="Cadastrar Categoria", command=adicionar_tabela).pack(pady=5)
    tk.Button(frame_botoes, text="Excluir Categoria", command=excluir_categoria).pack(pady=5)
    tk.Button(frame_botoes, text="Editar Registro", command=editar_categoria).pack(pady=5)

    botao_menu_inicial = tk.Button(janela_categoria, text="Menu Inicial",
                                   command=lambda: [janela_categoria.destroy()])
    botao_menu_inicial.place(x=350, y=250)

    scrollbar_x = tk.Scrollbar(janela_categoria, orient="horizontal")
    scrollbar_x.place(x=50, y=500, width=700)

    colunas = ("Tipo de Categoria", "Descrição de Categoria")
    tabela = ttk.Treeview(janela_categoria, columns=colunas, show="headings", xscrollcommand=scrollbar_x.set)

    tabela.heading("Tipo de Categoria", text="Tipo de Categoria")
    tabela.heading("Descrição de Categoria", text="Descrição de Categoria")

    tabela.place(x=50, y=300, width=700, height=200)

    scrollbar_x.config(command=tabela.xview)

    carregar_dados()

    rodape_label = tk.Label(janela_categoria, text="© DEVELOPED BY CREATIVE TECH GROUP", font=("Arial", 8), anchor="e")
    rodape_label.pack(side="bottom", anchor="se", padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão")
    root.geometry("300x200")

    tk.Button(root, text="Gestão de Categoria", command=gestao_categoria).pack(pady=50)

    root.mainloop()
