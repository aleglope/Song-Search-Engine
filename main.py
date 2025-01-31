import tkinter as tk
from gui import SpotifyBillboardGUI


def main():
    """
    Función principal que inicia la aplicación con interfaz gráfica.
    """
    root = tk.Tk()
    app = SpotifyBillboardGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
