import json
import os
from typing import Dict, Any

class StatsManager:
    def __init__(self, save_file='player_stats.json'):
        self.save_file = save_file
        self.stats = self.load_stats()

    def load_stats(self) -> Dict[str, Any]:
        """Charge les statistiques depuis un fichier JSON."""
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return self._initialize_stats()

    def _initialize_stats(self) -> Dict[str, Any]:
        """Initialise les statistiques par défaut."""
        return {
            'points': 0,
            'level': 1,
            'grade': 'Rookie',
            'kills_bots': 0,
            'kills_players': 0,
            'loot_value': 0,
            'games_played': 0
        }

    def update_stats(self, action: str, value: int = 1):
        """Met à jour les statistiques selon l'action."""
        actions = {
            'bot_kill': (10, 'kills_bots'),
            'player_kill': (50, 'kills_players'),
            'loot': (5, 'loot_value'),
            'game_played': (20, 'games_played')
        }

        if action in actions:
            points, stat_key = actions[action]
            self.stats['points'] += points * value
            self.stats[stat_key] += value
            self._update_grade()
            self.save_stats()

    def _update_grade(self):
        """Met à jour le grade en fonction des points."""
        grades = [
            (0, 'Rookie'),
            (100, 'Elite'),
            (500, 'Master'),
            (1000, 'Legendary')
        ]
        
        for points_threshold, grade in reversed(grades):
            if self.stats['points'] >= points_threshold:
                self.stats['grade'] = grade
                break

    def save_stats(self):
        """Sauvegarde les statistiques dans un fichier JSON."""
        with open(self.save_file, 'w') as f:
            json.dump(self.stats, f, indent=4)

    def get_progress_percentage(self) -> float:
        """Calcule le pourcentage de progression vers le prochain grade."""
        grades = [0, 100, 500, 1000]
        current_points = self.stats['points']
        
        for i in range(len(grades) - 1):
            if current_points < grades[i+1]:
                return (current_points - grades[i]) / (grades[i+1] - grades[i]) * 100
        return 100
