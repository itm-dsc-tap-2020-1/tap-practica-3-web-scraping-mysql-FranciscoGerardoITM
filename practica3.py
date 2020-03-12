from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector as mysql
import tkinter as tk
from tkinter import ttk

def boton():
    url = urlopen(pagina.get())
    print("\nExtraer los enlaces de la página Web: " + pagina.get() + "\n")
    bs = BeautifulSoup(url.read(), 'html.parser')
    conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='Enlaces' )
    operacion = conexion.cursor(buffered=True)
    for enlaces in bs.find_all("a"):
        print("href: {}".format(enlaces.get("href")))
        operacion.execute( 'INSERT INTO Datos values("'+enlaces.get("href")+'", False)')
        conexion.commit()
    operacion.execute( "SELECT * FROM Datos WHERE Status=0")
    for pag, st in operacion:
        print("\n"+"Se encontraron los siguientes enlaces en "+pag+"\n")
        try:
            html=urlopen(pag)
            bs=BeautifulSoup(html.read(), 'html.parser')
            for enlaces in bs.find_all("a"):
                print("href: {}".format(enlaces.get("href")))
                try:
                    operacion.execute( 'INSERT INTO Datos values("'+enlaces.get("href")+'", False)')
                except:
                    pass
        except:
            pass
        operacion.execute("UPDATE Datos SET Status=1 WHERE Pagina='"+pag+"'")
        conexion.commit()
        operacion.execute("SELECT * FROM Datos WHERE Status=0")   
    conexion.close()

ventana=tk.Tk()
ventana.title("Web Scraping")
boton=ttk.Button(ventana, text="Start", command=boton)
boton.grid(column=0,row=3, padx=50, pady=10)
ttk.Label(ventana, text="Ingrese enlace").grid(column=0,row=0, padx=5, pady=5)
pagina=tk.StringVar()
text=ttk.Entry(ventana, width=20, textvariable=pagina)
text.grid(column=0, row=1, padx=5, pady=5)

ventana.mainloop()