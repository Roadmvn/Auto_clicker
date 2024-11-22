import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

class AutoClickerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Auto-Clicker Pro")
        self.root.minsize(400, 500)
        
        # Variables
        self.always_on_top = tk.BooleanVar(value=False)
        self.delay_ms = tk.StringVar(value="1000")
        self.status_var = tk.StringVar(value="Prêt")
        
        self.setup_style()
        self.setup_gui()
        self.clicker = AutoClicker(self)

    def setup_style(self):
        self.root.configure(bg='#f5f5f5')
        style = ttk.Style()
        style.configure('Custom.TButton', padding=5, font=('Arial', 10))
        style.configure('Custom.TLabel', padding=5, font=('Arial', 10))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        # Titre
        ttk.Label(
            main_frame,
            text="Auto-Clicker Pro",
            font=('Arial', 16, 'bold')
        ).grid(row=0, column=0, pady=(0, 10))

        # Options
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Checkbutton(
            options_frame,
            text="Toujours visible",
            variable=self.always_on_top,
            command=self.toggle_always_on_top
        ).grid(row=0, column=0, sticky="w")

        # Capture
        capture_frame = ttk.LabelFrame(main_frame, text="📍 Capture", padding=10)
        capture_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        self.capture_btn = ttk.Button(
            capture_frame,
            text="Démarrer la capture (F2)",
            command=self.toggle_capture
        )
        self.capture_btn.grid(row=0, column=0, sticky="ew")

        # Configuration
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuration", padding=10)
        config_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(config_frame, text="Délai (ms):").grid(row=0, column=0, padx=(0, 5))
        ttk.Entry(
            config_frame,
            textvariable=self.delay_ms,
            width=10
        ).grid(row=0, column=1, sticky="w")

        # Liste des positions
        positions_frame = ttk.LabelFrame(main_frame, text="📋 Positions capturées", padding=10)
        positions_frame.grid(row=4, column=0, sticky="nsew", pady=(0, 10))
        positions_frame.grid_columnconfigure(0, weight=1)
        positions_frame.grid_rowconfigure(0, weight=1)

        # Treeview avec menu contextuel
        self.tree = ttk.Treeview(
            positions_frame,
            columns=("pos", "x", "y", "clicks"),
            show="headings",
            height=8
        )
        
        self.tree.heading("pos", text="#")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.heading("clicks", text="Clics")
        
        self.tree.column("pos", width=50)
        self.tree.column("x", width=100)
        self.tree.column("y", width=100)
        self.tree.column("clicks", width=100)
        
        # Menu contextuel
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Modifier nombre de clics", command=self.modify_clicks)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        scrollbar = ttk.Scrollbar(positions_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Boutons d'action
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Button(
            actions_frame,
            text="▶️ Exécuter",
            command=self.execute_clicks
        ).grid(row=0, column=0, padx=5, sticky="ew")
        
        ttk.Button(
            actions_frame,
            text="🗑️ Effacer tout",
            command=self.clear_positions
        ).grid(row=0, column=1, padx=5, sticky="ew")

        # Status
        ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Arial', 9, 'italic')
        ).grid(row=6, column=0)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def modify_clicks(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item = selected_item[0]
        current_values = self.tree.item(item)['values']
        index = int(current_values[0]) - 1
        
        try:
            new_clicks = tk.simpledialog.askinteger(
                "Modifier les clics",
                "Nombre de clics :",
                initialvalue=current_values[3],
                minvalue=1,
                maxvalue=100
            )
            
            if new_clicks:
                x, y, _ = self.clicker.coordinates[index]
                self.clicker.coordinates[index] = (x, y, new_clicks)
                self.update_positions_display()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def toggle_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top.get())

    def toggle_capture(self):
        if not hasattr(self, 'is_capturing'):
            self.is_capturing = False
            
        if not self.is_capturing:
            self.is_capturing = True
            self.capture_btn.configure(text="Arrêter la capture (F3)")
            self.clicker.start_capture()
        else:
            self.stop_capture()

    def stop_capture(self):
        self.is_capturing = False
        self.capture_btn.configure(text="Démarrer la capture (F2)")
        self.clicker.stop_capture()

    def execute_clicks(self):
        try:
            delay = int(self.delay_ms.get())
            if delay < 0:
                raise ValueError
            self.clicker.delay_ms = delay
            self.clicker.execute_clicks()
        except ValueError:
            messagebox.showerror("Erreur", "Le délai doit être un nombre positif")

    def clear_positions(self):
        self.clicker.coordinates.clear()
        self.update_positions_display()
        self.status_var.set("Positions effacées")

    def update_positions_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, (x, y, clicks) in enumerate(self.clicker.coordinates, 1):
            self.tree.insert("", "end", values=(i, x, y, clicks))

    def run(self):
        self.root.mainloop()




class AutoClicker:
    def __init__(self, gui):
        self.gui = gui
        self.coordinates = []
        self.delay_ms = 1000
        self.is_capturing = False
        self.last_params = {'coordinates': [], 'delay_ms': 0}
        self.has_executed = False
        pyautogui.FAILSAFE = True

    def start_capture(self):
        self.is_capturing = True
        capture_thread = threading.Thread(target=self.capture_listener)
        capture_thread.daemon = True
        capture_thread.start()

    def capture_listener(self):
        keyboard.on_press_key('F2', lambda _: self.capture_position())
        keyboard.on_press_key('F3', lambda _: self.stop_capture())
        keyboard.on_press_key('esc', lambda _: self.quit_program())
        
        while self.is_capturing:
            time.sleep(0.1)

    def capture_position(self):
        if self.is_capturing:
            x, y = pyautogui.position()
            self.coordinates.append((x, y, 1))
            self.gui.update_positions_display()
            self.gui.status_var.set(f"Position capturée: ({x}, {y})")

    def stop_capture(self):
        self.is_capturing = False
        self.cleanup_listeners()
        self.gui.status_var.set("Capture terminée")

    def execute_clicks(self):
        if not self.coordinates:
            messagebox.showwarning("Attention", "Aucune position capturée")
            return False
            
        self.gui.status_var.set("Exécution des clics...")
        execution_thread = threading.Thread(target=self.execute_clicks_thread)
        execution_thread.daemon = True
        execution_thread.start()
        return True

    def execute_clicks_thread(self):
        try:
            for x, y, nb_clics in self.coordinates:
                for _ in range(nb_clics):
                    pyautogui.click(x, y)
                    time.sleep(self.delay_ms / 1000)
                    
            self.last_params['coordinates'] = self.coordinates.copy()
            self.last_params['delay_ms'] = self.delay_ms
            self.has_executed = True
            self.gui.status_var.set("Exécution terminée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution: {str(e)}")
            self.gui.status_var.set("Erreur d'exécution")

    def cleanup_listeners(self):
        keyboard.unhook_all()

    def quit_program(self):
        self.cleanup_listeners()
        self.gui.root.quit()


if __name__ == "__main__":
    app = AutoClickerGUI()
    app.run()