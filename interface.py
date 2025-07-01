import tkinter as tk
from tkinter import messagebox
from ABB import SGBD, Registro

class Application(tk.Tk):
    def __init__(self, sgbd):
        super().__init__()
        self.sgbd = sgbd
        self.title("Banco de Dados ABB")
        self.geometry("500x400")
        
        # Labels e Entradas
        self.lbl_cpf = tk.Label(self, text="CPF (11 dígitos):")
        self.lbl_cpf.pack()
        self.ent_cpf = tk.Entry(self)
        self.ent_cpf.pack()

        self.lbl_nome = tk.Label(self, text="Nome:")
        self.lbl_nome.pack()
        self.ent_nome = tk.Entry(self)
        self.ent_nome.pack()

        self.lbl_data = tk.Label(self, text="Data de Nascimento (YYYY-MM-DD):")
        self.lbl_data.pack()
        self.ent_data = tk.Entry(self)
        self.ent_data.pack()

        # Botões
        self.btn_inserir = tk.Button(self, text="Inserir", command=self.inserir)
        self.btn_inserir.pack(pady=5)
        self.btn_buscar = tk.Button(self, text="Buscar", command=self.buscar)
        self.btn_buscar.pack(pady=5)
        self.btn_remover = tk.Button(self, text="Remover", command=self.remover)
        self.btn_remover.pack(pady=5)

        # Resultado
        self.txt_result = tk.Text(self, height=6, width=45)
        self.txt_result.pack(pady=10)

    def inserir(self):
        cpf = self.ent_cpf.get().strip()
        nome = self.ent_nome.get().strip()
        data = self.ent_data.get().strip()
        if len(cpf) != 11 or not cpf.isdigit():
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos numéricos.")
            return
        if not nome or not data:
            messagebox.showerror("Erro", "Nome e data de nascimento são obrigatórios.")
            return
        if self.sgbd.buscar_por_cpf(cpf):
            messagebox.showerror("Erro", "Já existe um registro com esse CPF.")
            return
        registro = Registro(cpf, nome, data)
        self.sgbd.inserir_registro(registro)
        messagebox.showinfo("Sucesso", "Registro inserido com sucesso.")
        self.limpar_campos()

    def buscar(self):
        cpf = self.ent_cpf.get().strip()
        if len(cpf) != 11 or not cpf.isdigit():
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos numéricos.")
            return
        registro = self.sgbd.buscar_por_cpf(cpf)
        self.txt_result.delete("1.0", tk.END)
        if registro:
            self.txt_result.insert(tk.END, str(registro))
        else:
            self.txt_result.insert(tk.END, "Registro não encontrado.")

    def remover(self):
        cpf = self.ent_cpf.get().strip()
        if len(cpf) != 11 or not cpf.isdigit():
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos numéricos.")
            return
        registro = self.sgbd.buscar_por_cpf(cpf)
        if not registro:
            messagebox.showerror("Erro", "Registro não encontrado.")
            return
        self.sgbd.remover_registro(cpf)
        messagebox.showinfo("Sucesso", "Registro removido.")
        self.limpar_campos()

    def limpar_campos(self):
        self.ent_cpf.delete(0, tk.END)
        self.ent_nome.delete(0, tk.END)
        self.ent_data.delete(0, tk.END)
        self.txt_result.delete("1.0", tk.END)

if __name__ == "__main__":
    sgbd = SGBD()
    app = Application(sgbd)
    app.mainloop()