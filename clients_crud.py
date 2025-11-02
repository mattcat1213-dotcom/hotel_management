import tkinter as tk
from tkinter import ttk, messagebox
from db import create_connection

# --------------------------------------------
# Función para abrir el formulario de cliente
# --------------------------------------------
def open_cliente_form(root, mode="add", cliente_data=None, refresh_callback=None):
    form = tk.Toplevel(root)
    form.title("Agregar Cliente" if mode=="add" else "Editar Cliente")
    form.geometry("400x450")
    form.grab_set()  # Modal

    labels = ["Nombre", "Apellido", "DNI", "Teléfono", "Email", "Dirección"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(form, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label.lower()] = entry

    # ComboBox para País
    tk.Label(form, text="País").grid(row=len(labels), column=0, padx=10, pady=5, sticky="w")
    pais_var = tk.StringVar()
    pais_combobox = ttk.Combobox(form, textvariable=pais_var,
                                 values=["Argentina", "Brasil", "Chile", "Uruguay", "Paraguay"], state="readonly")
    pais_combobox.grid(row=len(labels), column=1, padx=10, pady=5)
    pais_combobox.current(0)

    # ComboBox para Estado
    tk.Label(form, text="Estado").grid(row=len(labels)+1, column=0, padx=10, pady=5, sticky="w")
    estado_var = tk.StringVar()
    estado_combobox = ttk.Combobox(form, textvariable=estado_var, values=["Activo", "Inactivo"], state="readonly")
    estado_combobox.grid(row=len(labels)+1, column=1, padx=10, pady=5)
    estado_combobox.current(0)

    # Si es editar, cargar datos
    if mode == "edit" and cliente_data:
        for i, key in enumerate(labels):
            entries[key.lower()].insert(0, cliente_data[i+1])  # +1 porque id no se edita
        pais_combobox.set(cliente_data[7])
        estado_combobox.set(cliente_data[8])

    def guardar():
        data = tuple(entry.get() for entry in entries.values()) + (pais_var.get(), estado_var.get())
        if not data[0] or not data[1] or not data[2]:
            messagebox.showerror("Error", "Nombre, Apellido y DNI son obligatorios")
            return

        conn = create_connection()
        cursor = conn.cursor()
        try:
            if mode == "add":
                cursor.execute("""
                    INSERT INTO clients (nombre, apellido, dni, telefono, email, direccion, pais, estado)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, data)
            else:
                cursor.execute("""
                    UPDATE clients SET nombre=%s, apellido=%s, dni=%s, telefono=%s, email=%s, direccion=%s, pais=%s, estado=%s
                    WHERE id=%s
                """, data + (cliente_data[0],))
            conn.commit()
            messagebox.showinfo("Éxito", f"Cliente {'agregado' if mode=='add' else 'actualizado'} correctamente.")
            if refresh_callback:
                refresh_callback()
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
        finally:
            cursor.close()
            conn.close()

    btn_text = "Agregar" if mode == "add" else "Actualizar"
    tk.Button(form, text=btn_text, width=15, command=guardar).grid(row=len(labels)+2, column=0, columnspan=2, pady=15)

    # Centrar ventana
    form.update_idletasks()
    x = (form.winfo_screenwidth() - form.winfo_width()) // 2
    y = (form.winfo_screenheight() - form.winfo_height()) // 2
    form.geometry(f"+{x}+{y}")

# --------------------------------------------
# Función principal del CRUD
# --------------------------------------------
def clients_screen():
    root = tk.Tk()
    root.title("Gestión de Clientes - Hotel Manager")
    root.geometry("1000x600")

    # Frame superior para botones
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Tabla para mostrar clientes
    columns = ("id", "nombre", "apellido", "dni", "telefono", "email", "direccion", "pais", "estado")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True, pady=10)

    # Función para cargar datos de la BD
    def cargar_datos():
        for row in tree.get_children():
            tree.delete(row)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        cursor.close()
        conn.close()

    cargar_datos()  # Carga inicial

    # Botones
    tk.Button(frame, text="Agregar Cliente", width=20,
              command=lambda: open_cliente_form(root, mode="add", refresh_callback=cargar_datos)).grid(row=0, column=0, padx=5)
    tk.Button(frame, text="Editar Cliente", width=20,
              command=lambda: editar_cliente()).grid(row=0, column=1, padx=5)
    tk.Button(frame, text="Eliminar Cliente", width=20,
              command=lambda: eliminar_cliente()).grid(row=0, column=2, padx=5)

    # Función de editar
    def editar_cliente():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona", "Seleccione un cliente para editar")
            return
        cliente_data = tree.item(seleccionado[0])["values"]
        open_cliente_form(root, mode="edit", cliente_data=cliente_data, refresh_callback=cargar_datos)

    # Función de eliminar
    def eliminar_cliente():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona", "Seleccione un cliente para eliminar")
            return
        cliente_data = tree.item(seleccionado[0])["values"]
        if messagebox.askyesno("Confirmar", f"¿Eliminar cliente {cliente_data[1]} {cliente_data[2]}?"):
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id=%s", (cliente_data[0],))
            conn.commit()
            cursor.close()
            conn.close()
            cargar_datos()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")

    root.mainloop()
