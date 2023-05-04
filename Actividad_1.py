from tkinter import *
from tkinter import ttk 
from tkinter import *
from Actividad_1 import *
import mysql.connector
from tkinter import messagebox

def main():
    root = Tk()
    root.wm_title("Registros")

    app = Ventana(root)
    app.mainloop()

if __name__ == "__main__":
    main()
    

class Ventana(Frame):
       
    def __init__(self, master=None):
        super().__init__(master,width=680, height=260)
        self.master = master
        self.pack()
        self.create_widgets()

        #Crud 
        self.habilitarCajas("normal")  
        self.habilitarBtnOper("normal")
        self.habilitarBtnGuardar("normal")  
        self.id=-1
        
    def habilitarCajas(self,estado):
        self.txtMatricula.configure(state=estado)
        self.txtNombre.configure(state=estado)
        self.txtEdad.configure(state=estado)
        self.txtMail.configure(state=estado)
        
    def habilitarBtnOper(self,estado):
        self.btnNuevo.configure(state=estado)                
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        
    def habilitarBtnGuardar(self,estado):
        self.btnGuardar.configure(state=estado)                
        self.btnCancelar.configure(state=estado)                
        
    def limpiarCajas(self):
        self.txtEdad.delete(0,END)
        self.txtMatricula.delete(0,END)
        self.txtNombre.delete(0,END)
        self.txtMail.delete(0,END)
        
    def limpiaGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)      
        
    def fNuevo(self):         
          # base de datos 
        matricula = self.txtMatricula.get()
        nombre = self.txtNombre.get()
        edad = self.txtEdad.get()
        mail = self.txtMail.get()
        conexion = mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = "",
        database = "alumnos")
        cursor = conexion.cursor()
        consulta = "INSERT INTO `registro alum`(`id`, `Matricula`, `Nombre`, `Edad`, `Mail`) VALUES (%s, %s, %s, %s)"
        valores = (matricula,nombre,edad,mail)
        cursor.execute(consulta,valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        self.limpiarCajas()        
        self.txtNombre.focus()
    
    def fGuardar(self):        
        pass
                 
    def fModificar(self):        
        # Obtener los identificadores de las filas seleccionadas
        seleccion = self.tree.selection()
        # Obtener el primer identificador de la selección (si hay uno)
        if len(seleccion) > 0:
            item = seleccion[0]
            # Objetos
            matricula = self.txtMatricula.get()
            nombre = self.txtNombre.get()
            edad = self.txtEdad.get()
            mail= self.txtMail.get()
            conexion = mysql.connector.connect(
            host= "localhost",
            user = "root",
            password = "",
            database = "alumnos")
            cursor = conexion.cursor()
            sql = "UPDATE `registro alum` SET `Matricula` = %s, `Nombre` = %s, `Edad` = %s WHERE `Mail` = %s"
            valores = (matricula,nombre,edad,mail)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()       
            self.txtNombre.focus()
            
            # Eliminar la fila correspondiente
            self.tree.delete(item)
            self.insert_data()
    
    def fEliminar(self):
                # Obtener los identificadores de las filas seleccionadas
        seleccion = self.tree.selection()
        # Obtener el primer identificador de la selección (si hay uno)
        if len(seleccion) > 0:
            # Variables 
            item = seleccion[0]
            datos = self.tree.item(seleccion[0])  # obtener los datos de la fila seleccionada
            nombre = datos['values'][0]  # obtener el valor de la columna 'Nombre'

            #Borrar datos de la BD
            conexion = mysql.connector.connect(
            host= "localhost",
            user = "root",
            password = "",
            database = "alumnos")
            cursor = conexion.cursor()
            sql = "DELETE FROM `registro alum` WHERE `Matricula` = %s"
            valores = [nombre]
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()       
            self.txtMatricula.focus()
            
            # Eliminar la fila correspondiente
            self.tree.delete(item)
            
        else:
            # Si no hay ninguna fila seleccionada, mostrar un mensaje de error
            messagebox.showerror("Error", "Debe seleccionar una fila para eliminar.")    

    def fCancelar(self):

        r = messagebox.askquestion("Calcelar", "Esta seguro que desea cancelar la operación actual")
        if r == messagebox.YES:
            self.limpiarCajas() 

    def create_widgets(self):
        frame1 = Frame(self, bg="light blue")
        frame1.place(x=0,y=0,width=93, height=259)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="chocolate", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="chocolate", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="chocolate", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)        
        frame2 = Frame(self,bg="Turquoise" )
        frame2.place(x=95,y=0,width=150, height=259) 

        lbl1 = Label(frame2,text="Matricula: ")
        lbl1.place(x=3,y=5)        
        self.txtMatricula=Entry(frame2)
        self.txtMatricula.place(x=3,y=29,width=100, height=20)   

        lbl2 = Label(frame2,text="Nombre: ")
        lbl2.place(x=3,y=55)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=79,width=100, height=20)  

        lbl3 = Label(frame2,text="Mail: ")
        lbl3.place(x=3,y=155)        
        self.txtMail=Entry(frame2)
        self.txtMail.place(x=3,y=129,width=100, height=20) 
               
        lbl4 = Label(frame2,text="Edad: ")
        lbl4.place(x=3,y=105)        
        self.txtEdad=Entry(frame2)
        self.txtEdad.place(x=3,y=179,width=50, height=20) 

        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=210,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=210,width=60, height=30)        
       

        frame3 = Frame(self,bg="white" )
        frame3.place(x=247,y=0,width=520, height=500)     
         # mostrar tabla    
        self.tree = ttk.Treeview(frame3, columns=("matricula", "nombre", "edad", "mail"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("matricula", text="Matricula")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("mail", text="Mail")
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("#1", width=60, minwidth=60, anchor=CENTER)
        self.tree.column("#2", width=90, minwidth=90, anchor=CENTER)
        self.tree.column("#3", width=90, minwidth=90, anchor=CENTER)
        self.tree.column("#4", width=90, minwidth=90, anchor=CENTER)

        self.tree.grid(row=0, column=0, sticky="nsew")

    def insert_data(self):
        matricula = self.txtMatricula.get()
        nombre = self.txtNombre.get()
        edad = self.txtEdad.get()
        mail = self.txtMail.get()
        if matricula and nombre and edad and mail:
            # Insertar los datos en la base de datos o en una lista
            # ...
            
            # Agregar los datos a la tabla
            self.tree.insert("", "end", text="1", values=(matricula, nombre, edad, mail))
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")
        