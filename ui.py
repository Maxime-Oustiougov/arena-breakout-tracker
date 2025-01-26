import tkinter as tk
from tkinter import ttk
from stats_manager import StatsManager

class ProgressApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Arena Breakout Progression Tracker")
        self.master.geometry("400x600")

        self.stats_manager = StatsManager()
        self.create_widgets()

    def create_widgets(self):
        # Menu hamburger
        self.hamburger_btn = tk.Button(self.master, text="☰", command=self.toggle_sidebar)
        self.hamburger_btn.pack(anchor='nw', padx=10, pady=10)

        # Sidebar
        self.sidebar = tk.Frame(self.master, width=250, bg='lightgray')
        self.sidebar.place(x=-250, height=600)

        tk.Label(self.sidebar, text="Arena Breakout Tracker", font=('Arial', 16)).pack(pady=20)

        # Statistiques dans la sidebar
        self.create_sidebar_stats()

        # Écran principal
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill='both')

        self.grade_label = tk.Label(self.main_frame, text=f"Grade: {self.stats_manager.stats['grade']}", font=('Arial', 20))
        self.grade_label.pack(pady=20)

        self.points_label = tk.Label(self.main_frame, text=f"Points: {self.stats_manager.stats['points']}", font=('Arial', 16))
        self.points_label.pack()

        # Barre de progression
        self.progress_bar = ttk.Progressbar(self.main_frame, length=300, mode='determinate')
        self.progress_bar['value'] = self.stats_manager.get_progress_percentage()
        self.progress_bar.pack(pady=20)

        # Boutons de test
        tk.Button(self.main_frame, text="Bot Kill", command=lambda: self.update_stats('bot_kill')).pack()
        tk.Button(self.main_frame, text="Player Kill", command=lambda: self.update_stats('player_kill')).pack()
        tk.Button(self.main_frame, text="Loot", command=lambda: self.update_stats('loot')).pack()
        tk.Button(self.main_frame, text="Game Played", command=lambda: self.update_stats('game_played')).pack()

    def create_sidebar_stats(self):
        stats = self.stats_manager.stats
        stat_labels = [
            f"Grade: {stats['grade']}",
            f"Kills de bots: {stats['kills_bots']}",
            f"Kills de joueurs: {stats['kills_players']}",
            f"Butin récupéré: {stats['loot_value']}",
            f"Games jouées: {stats['games_played']}"
        ]
        
        for stat in stat_labels:
            tk.Label(self.sidebar, text=stat, bg='lightgray').pack(pady=5)

    def toggle_sidebar(self):
        x = self.sidebar.winfo_x()
        if x == 0:
            self.sidebar.place(x=-250)
        else:
            self.sidebar.place(x=0)

    def update_stats(self, action):
        self.stats_manager.update_stats(action)
        self.refresh_ui()

    def refresh_ui(self):
        stats = self.stats_manager.stats
        self.grade_label.config(text=f"Grade: {stats['grade']}")
        self.points_label.config(text=f"Points: {stats['points']}")
        self.progress_bar['value'] = self.stats_manager.get_progress_percentage()
        
        # Mise à jour de la sidebar
        for widget in self.sidebar.winfo_children()[1:]:
            widget.destroy()
        self.create_sidebar_stats()
