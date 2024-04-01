import time
from AX12_Pinces import AX12_Pinces
from AX12_Ascenseur import AX12_Ascenseur

class AX12_Prendre_Plantes:
    def __init__(self):
        # Initialisation des instances des classes AX12_Pinces et AX12_Ascenseur
        self.ax12_pinces = AX12_Pinces()
        self.ax12_ascenseur = AX12_Ascenseur()

    def prendre_plantes(self):
        # Ouvrir la pince pour prendre les plantes
        self.ax12_pinces.open_pince()
        
        # Fermer la pince pour prendre les plantes
        self.ax12_pinces.close_pince()

        # Monter l'ascenseur
        self.ax12_ascenseur.elevate()
        
        time.sleep(10)

        # Descendre l'ascenseur
        self.ax12_ascenseur.lower_for_plant()

        # Ouvrir à nouveau la pince pour déposer les plantes
        self.ax12_pinces.open_pince_stepbystep()
        
        # Monter l'ascenseur
        self.ax12_ascenseur.elevate()
        
        # Fermer la pince à nouveau
        self.ax12_pinces.close_pince()

    def run(self):
        # Initialiser les moteurs des pinces et de l'ascenseur
        self.ax12_pinces.initialize_motors()
        self.ax12_ascenseur.initialize_motors()

        # Prendre les plantes
        self.prendre_plantes()

# Exemple d'utilisation
if __name__ == "__main__":
    prendre_plantes = AX12_Prendre_Plantes()
    prendre_plantes.run()
