import tkinter as tk
from tclab_gui import TCLabGUI

def main():
    # Crea la ventana principal
    root = tk.Tk()
    # Crea una instancia de la GUI
    gui = TCLabGUI(root)
    # Inicia el bucle principal de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
