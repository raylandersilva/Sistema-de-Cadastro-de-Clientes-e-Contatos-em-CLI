#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Cadastro de Clientes e Contatos - Interface Gráfica
Este módulo implementa a interface gráfica do sistema usando Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_config import get_db_connection
from mysql.connector import Error

class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro de Clientes")
        self.root.geometry("800x600")
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Criação das abas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba de Clientes
        self.clientes_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.clientes_frame, text="Clientes")
        
        # Aba de Contatos
        self.contatos_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.contatos_frame, text="Contatos")
        
        # Configurar as abas
        self.setup_clientes_tab()
        self.setup_contatos_tab()
        
        # Carregar dados iniciais
        self.carregar_clientes()
    
    def setup_clientes_tab(self):
        # Frame para formulário de cliente
        form_frame = ttk.LabelFrame(self.clientes_frame, text="Cadastro de Cliente", padding="10")
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Campos do formulário
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        self.nome_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nome_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=40).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=0, sticky=tk.W)
        self.telefone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.telefone_var, width=40).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Endereço:").grid(row=3, column=0, sticky=tk.W)
        self.endereco_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.endereco_var, width=40).grid(row=3, column=1, padx=5, pady=2)
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_cliente).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_form_cliente).grid(row=0, column=1, padx=5)
        
        # Tabela de clientes
        table_frame = ttk.LabelFrame(self.clientes_frame, text="Lista de Clientes", padding="10")
        table_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Criar Treeview
        self.tree_clientes = ttk.Treeview(table_frame, columns=("ID", "Nome", "Email", "Telefone", "Endereço"), 
                                        show="headings", height=10)
        
        # Configurar colunas
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nome", text="Nome")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.heading("Telefone", text="Telefone")
        self.tree_clientes.heading("Endereço", text="Endereço")
        
        self.tree_clientes.column("ID", width=50)
        self.tree_clientes.column("Nome", width=150)
        self.tree_clientes.column("Email", width=200)
        self.tree_clientes.column("Telefone", width=100)
        self.tree_clientes.column("Endereço", width=200)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botões de ação para a tabela
        btn_frame_table = ttk.Frame(table_frame)
        btn_frame_table.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame_table, text="Editar", command=self.editar_cliente).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame_table, text="Excluir", command=self.excluir_cliente).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame_table, text="Atualizar", command=self.carregar_clientes).grid(row=0, column=2, padx=5)
    
    def setup_contatos_tab(self):
        # Frame para seleção de cliente
        select_frame = ttk.LabelFrame(self.contatos_frame, text="Selecionar Cliente", padding="10")
        select_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(select_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W)
        self.cliente_combo = ttk.Combobox(select_frame, width=40)
        self.cliente_combo.grid(row=0, column=1, padx=5)
        self.cliente_combo.bind('<<ComboboxSelected>>', self.carregar_contatos_cliente)
        
        # Frame para formulário de contato
        form_frame = ttk.LabelFrame(self.contatos_frame, text="Cadastro de Contato", padding="10")
        form_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        self.contato_nome_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.contato_nome_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Telefone:").grid(row=1, column=0, sticky=tk.W)
        self.contato_telefone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.contato_telefone_var, width=40).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W)
        self.contato_email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.contato_email_var, width=40).grid(row=2, column=1, padx=5, pady=2)
        
        # Botões do formulário de contato
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_contato).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_form_contato).grid(row=0, column=1, padx=5)
        
        # Tabela de contatos
        table_frame = ttk.LabelFrame(self.contatos_frame, text="Lista de Contatos", padding="10")
        table_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Criar Treeview para contatos
        self.tree_contatos = ttk.Treeview(table_frame, 
                                        columns=("ID", "Nome", "Telefone", "Email"),
                                        show="headings", height=10)
        
        # Configurar colunas
        self.tree_contatos.heading("ID", text="ID")
        self.tree_contatos.heading("Nome", text="Nome")
        self.tree_contatos.heading("Telefone", text="Telefone")
        self.tree_contatos.heading("Email", text="Email")
        
        self.tree_contatos.column("ID", width=50)
        self.tree_contatos.column("Nome", width=200)
        self.tree_contatos.column("Telefone", width=150)
        self.tree_contatos.column("Email", width=200)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_contatos.yview)
        self.tree_contatos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_contatos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botões de ação para a tabela de contatos
        btn_frame_table = ttk.Frame(table_frame)
        btn_frame_table.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame_table, text="Excluir", command=self.excluir_contato).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame_table, text="Atualizar", command=lambda: self.carregar_contatos_cliente(None)).grid(row=0, column=1, padx=5)
    
    def cadastrar_cliente(self):
        nome = self.nome_var.get().strip()
        email = self.email_var.get().strip()
        telefone = self.telefone_var.get().strip()
        endereco = self.endereco_var.get().strip()
        
        if not nome or not email:
            messagebox.showerror("Erro", "Nome e email são obrigatórios!")
            return
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO cliente (nome, email, telefone, endereco) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (nome, email, telefone, endereco))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_form_cliente()
            self.carregar_clientes()
            
        except Error as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Erro", "Este email já está cadastrado!")
            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def carregar_clientes(self):
        # Limpar tabela atual
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cliente ORDER BY nome")
            clientes = cursor.fetchall()
            
            # Atualizar tabela
            for cliente in clientes:
                self.tree_clientes.insert("", "end", values=(
                    cliente['id_cliente'],
                    cliente['nome'],
                    cliente['email'],
                    cliente['telefone'],
                    cliente['endereco']
                ))
            
            # Atualizar combobox de clientes
            self.atualizar_combo_clientes(clientes)
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def atualizar_combo_clientes(self, clientes):
        # Limpar combobox
        self.cliente_combo['values'] = []
        
        # Criar lista de clientes para o combobox
        cliente_list = [f"{c['id_cliente']} - {c['nome']}" for c in clientes]
        self.cliente_combo['values'] = cliente_list
        
        if cliente_list:
            self.cliente_combo.set(cliente_list[0])
    
    def editar_cliente(self):
        selected_item = self.tree_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        # Obter dados do cliente selecionado
        cliente_data = self.tree_clientes.item(selected_item[0])['values']
        
        # Criar janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Cliente")
        edit_window.geometry("400x300")
        
        # Variáveis para os campos
        nome_var = tk.StringVar(value=cliente_data[1])
        email_var = tk.StringVar(value=cliente_data[2])
        telefone_var = tk.StringVar(value=cliente_data[3])
        endereco_var = tk.StringVar(value=cliente_data[4])
        
        # Criar formulário
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=nome_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=email_var, width=40).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=telefone_var, width=40).grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Endereço:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=endereco_var, width=40).grid(row=3, column=1, padx=5, pady=2)
        
        def salvar_edicao():
            conn = get_db_connection()
            if not conn:
                return
            
            try:
                cursor = conn.cursor()
                sql = """UPDATE cliente 
                         SET nome = %s, email = %s, telefone = %s, endereco = %s 
                         WHERE id_cliente = %s"""
                cursor.execute(sql, (
                    nome_var.get(),
                    email_var.get(),
                    telefone_var.get(),
                    endereco_var.get(),
                    cliente_data[0]
                ))
                conn.commit()
                
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                edit_window.destroy()
                self.carregar_clientes()
                
            except Error as e:
                if "Duplicate entry" in str(e):
                    messagebox.showerror("Erro", "Este email já está cadastrado para outro cliente!")
                else:
                    messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")
            finally:
                cursor.close()
                conn.close()
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=salvar_edicao).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=edit_window.destroy).grid(row=0, column=1, padx=5)
    
    def excluir_cliente(self):
        selected_item = self.tree_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return
        
        cliente_data = self.tree_clientes.item(selected_item[0])['values']
        
        if not messagebox.askyesno("Confirmar Exclusão", 
                                 f"Deseja realmente excluir o cliente {cliente_data[1]}?\n" +
                                 "Todos os contatos associados também serão excluídos."):
            return
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Excluir contatos primeiro (devido à chave estrangeira)
            cursor.execute("DELETE FROM contato WHERE id_cliente = %s", (cliente_data[0],))
            
            # Excluir o cliente
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (cliente_data[0],))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Cliente e seus contatos foram excluídos com sucesso!")
            self.carregar_clientes()
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def cadastrar_contato(self):
        if not self.cliente_combo.get():
            messagebox.showwarning("Aviso", "Selecione um cliente primeiro!")
            return
        
        nome = self.contato_nome_var.get().strip()
        telefone = self.contato_telefone_var.get().strip()
        email = self.contato_email_var.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome do contato é obrigatório!")
            return
        
        # Obter ID do cliente selecionado
        id_cliente = int(self.cliente_combo.get().split(" - ")[0])
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO contato (id_cliente, nome, telefone, email) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (id_cliente, nome, telefone, email))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Contato cadastrado com sucesso!")
            self.limpar_form_contato()
            self.carregar_contatos_cliente(None)
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar contato: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def carregar_contatos_cliente(self, event):
        if not self.cliente_combo.get():
            return
        
        # Limpar tabela atual
        for item in self.tree_contatos.get_children():
            self.tree_contatos.delete(item)
        
        # Obter ID do cliente selecionado
        id_cliente = int(self.cliente_combo.get().split(" - ")[0])
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_contato, nome, telefone, email 
                FROM contato 
                WHERE id_cliente = %s 
                ORDER BY nome
            """, (id_cliente,))
            contatos = cursor.fetchall()
            
            # Atualizar tabela
            for contato in contatos:
                self.tree_contatos.insert("", "end", values=(
                    contato['id_contato'],
                    contato['nome'],
                    contato['telefone'],
                    contato['email']
                ))
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar contatos: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def excluir_contato(self):
        selected_item = self.tree_contatos.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um contato para excluir!")
            return
        
        contato_data = self.tree_contatos.item(selected_item[0])['values']
        
        if not messagebox.askyesno("Confirmar Exclusão", 
                                 f"Deseja realmente excluir o contato {contato_data[1]}?"):
            return
        
        conn = get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contato WHERE id_contato = %s", (contato_data[0],))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")
            self.carregar_contatos_cliente(None)
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir contato: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def limpar_form_cliente(self):
        self.nome_var.set("")
        self.email_var.set("")
        self.telefone_var.set("")
        self.endereco_var.set("")
    
    def limpar_form_contato(self):
        self.contato_nome_var.set("")
        self.contato_telefone_var.set("")
        self.contato_email_var.set("")

def main():
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 