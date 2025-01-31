import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from billboard_scraper import fetch_songs_from_billboard
from spotify_manager import SpotifyManager


class SpotifyBillboardGUI:
    def __init__(self, root):
        # Colores corporativos de Spotify
        self.SPOTIFY_GREEN = "#1DB954"
        self.SPOTIFY_BLACK = "#191414"
        self.SPOTIFY_WHITE = "#FFFFFF"
        self.SPOTIFY_GREY = "#535353"

        self.root = root
        self.root.title("Creador de Lista Billboard Top 100")
        # Configurar tamaño de ventana y centrarla
        window_width = 1200
        window_height = 900
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # Calcular posición x,y para centrar la ventana
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        # Configurar geometría y posición
        self.root.geometry(
            f"{window_width}x{window_height}+{position_right}+{position_top}"
        )
        # Evitar que la ventana sea redimensionable
        self.root.resizable(False, False)
        self.root.configure(bg=self.SPOTIFY_BLACK)

        # Configuración del estilo
        style = ttk.Style()
        style.theme_use("clam")  # Usar un tema base limpio

        # Estilo para botones
        style.configure(
            "Spotify.TButton",
            padding=10,
            font=("Gotham", 12, "bold"),
            background=self.SPOTIFY_GREEN,
            foreground=self.SPOTIFY_WHITE,
        )
        style.map(
            "Spotify.TButton",
            background=[("active", self.SPOTIFY_GREEN), ("pressed", "#1ed760")],
            foreground=[("active", self.SPOTIFY_WHITE)],
        )

        # Estilo para etiquetas
        style.configure(
            "Spotify.TLabel",
            font=("Gotham", 11),
            background=self.SPOTIFY_BLACK,
            foreground=self.SPOTIFY_WHITE,
        )

        # Estilo para el título
        style.configure(
            "SpotifyTitle.TLabel",
            font=("Gotham", 32, "bold"),
            background=self.SPOTIFY_BLACK,
            foreground=self.SPOTIFY_WHITE,
        )

        # Estilo para el mensaje descriptivo
        style.configure(
            "SpotifyDesc.TLabel",
            font=("Gotham", 14),
            background=self.SPOTIFY_BLACK,
            foreground=self.SPOTIFY_GREEN,
            padding=(0, 10),
        )

        # Frame principal con fondo negro
        main_frame = ttk.Frame(root, padding="40", style="Spotify.TFrame")
        style.configure("Spotify.TFrame", background=self.SPOTIFY_BLACK)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Configurar el grid para expandirse
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)

        # Logo de Spotify (texto)
        title_label = ttk.Label(
            main_frame,
            text="Creador de Lista de 100 Canciones\nBasadas en Billboard",
            style="SpotifyTitle.TLabel",
            justify="center",
        )
        title_label.grid(row=0, column=0, pady=(10, 30), sticky="n")

        # Mensaje descriptivo para el usuario
        description_label = ttk.Label(
            main_frame,
            text="Introduce tu fecha deseada para descubrir las canciones\n"
            "más populares de ese día y crear tu playlist personalizada",
            style="SpotifyDesc.TLabel",
            justify="center",
            wraplength=800,
        )
        description_label.grid(row=1, column=0, pady=(0, 40), sticky="n")

        # Frame para la entrada de fecha con fondo negro
        date_frame = ttk.Frame(main_frame, style="Spotify.TFrame")
        date_frame.grid(row=2, column=0, pady=(0, 30), sticky="n")
        date_frame.grid_columnconfigure(0, weight=1)
        date_frame.grid_columnconfigure(1, weight=1)

        # Contenedor para centrar el campo de fecha
        center_frame = ttk.Frame(date_frame, style="Spotify.TFrame")
        center_frame.grid(row=0, column=0, columnspan=2)
        center_frame.grid_columnconfigure(1, weight=1)
        center_frame.grid_columnconfigure(2, weight=1)

        # Etiqueta de fecha
        date_label = ttk.Label(
            center_frame,
            text="Fecha (YYYY-MM-DD):",
            style="Spotify.TLabel",
            anchor="e",
        )
        date_label.grid(row=0, column=1, padx=(0, 10), sticky="e")

        # Estilo para el campo de entrada
        style.configure(
            "Spotify.TEntry",
            fieldbackground=self.SPOTIFY_GREY,
            foreground=self.SPOTIFY_WHITE,
            padding=7,
        )

        # Campo de entrada
        self.date_entry = ttk.Entry(
            center_frame,
            width=25,
            style="Spotify.TEntry",
            font=("Gotham", 12),
            justify="center",
        )
        self.date_entry.grid(row=0, column=2, padx=(10, 0), sticky="w")

        # Botón de crear playlist
        create_button = ttk.Button(
            main_frame,
            text="Crear Playlist",
            style="Spotify.TButton",
            command=self.create_playlist,
            width=25,
        )
        create_button.grid(row=3, column=0, pady=25, sticky="n")

        # Área de estado
        self.status_text = tk.Text(
            main_frame,
            height=10,
            width=70,
            wrap=tk.WORD,
            bg=self.SPOTIFY_GREY,
            fg=self.SPOTIFY_WHITE,
            font=("Gotham", 12),
            padx=10,
            pady=20,
            relief=tk.FLAT,
        )
        self.status_text.grid(row=4, column=0, pady=20, sticky="nsew", padx=40)
        self.status_text.config(state=tk.DISABLED)

        # Configurar tags para centrar el texto en el área de estado
        self.status_text.tag_configure("center", justify="center")

        def center_status_text(event):
            self.status_text.tag_add("center", "1.0", "end")

        self.status_text.bind("<Key>", center_status_text)
        self.status_text.bind("<Return>", center_status_text)

        self.spotify_manager = None

    def update_status(self, message):
        """Actualiza el área de estado con un nuevo mensaje"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n", "center")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()

    def is_valid_date(self, date_str):
        """Verifica si la fecha es válida y no está en el futuro"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj <= datetime.now()
        except ValueError:
            return False

    def create_playlist(self):
        """Maneja el proceso de creación de la playlist"""
        date = self.date_entry.get().strip()

        if not self.is_valid_date(date):
            messagebox.showerror(
                "Error",
                "Fecha inválida. Por favor ingrese una fecha válida en formato YYYY-MM-DD "
                "y asegúrese de que no sea una fecha futura.",
            )
            return

        try:
            if not self.spotify_manager:
                self.spotify_manager = SpotifyManager()
                self.update_status("Conectado a Spotify exitosamente.")

            self.update_status(f"Buscando canciones para la fecha {date}...")
            songs = fetch_songs_from_billboard(date)

            if not songs:
                messagebox.showwarning(
                    "Sin resultados",
                    "No se encontraron canciones para la fecha especificada.",
                )
                return

            self.update_status(f"Se encontraron {len(songs)} canciones.")
            user_id = self.spotify_manager.sp.current_user()["id"]

            self.update_status("Creando playlist en Spotify...")
            self.spotify_manager.create_spotify_playlist(user_id, date, songs)

            messagebox.showinfo(
                "Éxito", f"Playlist creada exitosamente para la fecha {date}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
