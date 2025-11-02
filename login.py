import tkinter as tk
from tkinter import messagebox
from admin_dashboard import open_admin_dashboard
from db import verify_user

def login_screen():
    def attempt_login():
        username = entry_username.get()
        password = entry_password.get()
        user = verify_user(username, password)
        if user:
            messagebox.showinfo("Éxito", f"Bienvenido {user['username']}!")
            root.destroy()
            if user['role'] == 'admin':
                open_admin_dashboard(user)
            else:
                messagebox.showwarning("Acceso denegado", "Solo administradores pueden acceder al panel.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    root = tk.Tk()
    root.title("Login - Hotel Manager")
    root.geometry("300x200")

    tk.Label(root, text="Usuario").pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Contraseña").pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Login", command=attempt_login).pack(pady=20)

    root.mainloop()
