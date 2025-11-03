import tkinter as tk
from tkinter import ttk
import clients_crud

def open_admin_dashboard(user):
    root = tk.Tk()
    root.title("Panel de Administración - Hotel Manager")
    root.geometry("600x400")

    tk.Label(root, text=f"Bienvenido, {user['username']} (Admin)", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    def open_clients():
        root.destroy()
        clients_crud.clients_screen()

    ttk.Button(frame, text="Gestión de Clientes", width=25, command=open_clients).grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(frame, text="Cerrar Sesión", width=25, command=root.destroy).grid(row=1, column=0, pady=20)

    root.mainloop()
