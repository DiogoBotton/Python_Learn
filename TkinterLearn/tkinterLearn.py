from tkinter import *

tela = Tk()
tela.geometry("400x400")
tela.title("Cotações")

texto = Label(tela, text="Vanessa Byork")
texto.grid(column=0, row=0, padx=10, pady=10)

button = Button(tela, text="Não clique")
button.grid(column=5, row=1, padx=5, pady=5)

tela.mainloop()