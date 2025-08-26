from tkinter import *
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("actividad.db")
cursor = conn.cursor()


conn.commit()


ventana = Tk()
ventana.title("Mantenimiento de Vehículos")
ventana.geometry("500x600")
ventana.config(padx=20, pady=20)


patente = StringVar()
marca = StringVar()
modelo = StringVar()
anio = StringVar()

# Servicios
id_vehiculo = StringVar()
descripcion = StringVar()
fecha = StringVar()
costo = StringVar()

# === FUNCIONES ===
def guardar_vehiculo():
    try:
        cursor.execute("""
            INSERT INTO vehiculos (patente, marca, modelo, anio)
            VALUES (?, ?, ?, ?)""",
            (patente.get(), marca.get(), modelo.get(), int(anio.get()))
        )
        conn.commit()
        messagebox.showinfo("Éxito", "Vehículo guardado correctamente.")
        limpiar_campos_vehiculo()
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar vehículo:\n{e}")

def guardar_servicio():
    try:
        cursor.execute("""
            INSERT INTO servicios (id_vehiculo, descripcion, fecha, costo)
            VALUES (?, ?, ?, ?)""",
            (int(id_vehiculo.get()), descripcion.get(), fecha.get(), float(costo.get()))
        )
        conn.commit()
        messagebox.showinfo("Éxito", "Servicio guardado correctamente.")
        limpiar_campos_servicio()
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar servicio:\n{e}")

def mostrar_inner_join():
    try:
        cursor.execute("""
            SELECT vehiculos.patente, vehiculos.marca, servicios.descripcion, servicios.fecha, servicios.costo
            FROM vehiculos
            INNER JOIN servicios ON vehiculos.id = servicios.id_vehiculo
        """)
        resultados = cursor.fetchall()
        if resultados:
            texto = ""
            for r in resultados:
                texto += f"Patente: {r[0]}, Marca: {r[1]}\nServicio: {r[2]}, Fecha: {r[3]}, Costo: ${r[4]}\n\n"
            messagebox.showinfo("Servicios realizados", texto)
        else:
            messagebox.showinfo("Sin datos", "No hay servicios registrados.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar el INNER JOIN:\n{e}")

def limpiar_campos_vehiculo():
    patente.set("")
    marca.set("")
    modelo.set("")
    anio.set("")

def limpiar_campos_servicio():
    id_vehiculo.set("")
    descripcion.set("")
    fecha.set("")
    costo.set("")

# === FORMULARIO VEHÍCULOS ===
Label(ventana, text="Registro de Vehículos", font=("Arial", 12, "bold")).pack(pady=10)

Label(ventana, text="Patente").pack()
Entry(ventana, textvariable=patente).pack()

Label(ventana, text="Marca").pack()
Entry(ventana, textvariable=marca).pack()

Label(ventana, text="Modelo").pack()
Entry(ventana, textvariable=modelo).pack()

Label(ventana, text="Año").pack()
Entry(ventana, textvariable=anio).pack()

Button(ventana, text="Guardar Vehículo", command=guardar_vehiculo).pack(pady=10)

# === FORMULARIO SERVICIOS ===
Label(ventana, text="Registro de Servicios", font=("Arial", 12, "bold")).pack(pady=10)

Label(ventana, text="ID del Vehículo").pack()
Entry(ventana, textvariable=id_vehiculo).pack()

Label(ventana, text="Descripción del Servicio").pack()
Entry(ventana, textvariable=descripcion).pack()

Label(ventana, text="Fecha (YYYY-MM-DD)").pack()
Entry(ventana, textvariable=fecha).pack()

Label(ventana, text="Costo").pack()
Entry(ventana, textvariable=costo).pack()

Button(ventana, text="Guardar Servicio", command=guardar_servicio).pack(pady=10)

# === BOTÓN JOIN ===
Button(ventana, text="Mostrar Servicios Realizados (INNER JOIN)", command=mostrar_inner_join, bg="lightblue").pack(pady=20)

ventana.mainloop()
conn.close()
