#App conectada a base de datos

from tkinter import ttk
from tkinter import *

import sqlite3


class Product:

    db_name = 'database.db'

    def __init__(self, windows):
        self.wind = window
        self.wind.title("Products Application")

        #Frame container
        frame = LabelFrame(self.wind, text = 'Register a new product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price input
        Label(frame, text = ' Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        #Button add product
        ttk.Button(frame, text = 'save product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        #Ouput messages
        self.messages = Label(text = '', fg = 'red')
        self.messages.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text='Precio', anchor= CENTER)

        #Buttons Eliminar and Editar
        ttk.Button(text = 'Eliminar', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        #Fill rows
        self.get_product()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_product(self):
        #Clean table
        records = self.tree.get_children()
        for elements in records:
            self.tree.delete(elements)

        #Get data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)

        #Fill data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    #Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    #Add product
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.messages['text'] = 'El producto {} se agrego correctamente'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.messages['text'] = 'Es necesario el nombre y el precio'
        self.get_product()

    #Delete product
    def delete_product(self):
        self.messages['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.messages['text'] = 'Seleccione un registro'
            return    
        self.messages['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.messages['text'] = 'El registro {} se elimino correctamente'.format(name)
        self.get_product()

    #Edit product
    def edit_product(self):
        self.messages['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.messages['text'] = 'Seleccione un registro'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar producto'

        #Old name
        Label(self.edit_wind, text = 'Nombre anterior: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        #New name
        Label(self.edit_wind, text = 'Nuevo nombre: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)
        
        #Old price
        Label(self.edit_wind, text = 'Precio anterior: ').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        #New price
        Label(self.edit_wind, text = 'Nuevo precio: ').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)

    #Edit records
    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.messages['text'] = 'Registro {} actualizado correctamente'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()