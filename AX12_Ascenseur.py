import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config

class AX12_Ascenseur:
    def __init__(self):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

        # Créer un logger
        self.logger = logging.getLogger(f"AX12_Ascenseur")

        # Initialisation du moteur avec l'ID 6
        self.ax12_ascenseur = AX12_Control(6,"Ascenceur") 
        self.elevate_position = 0
        self.plant_position = 200
        self.lower_position = 850
        self.ax12_ascenseur.connect()
        self.ax12_ascenseur.set_speed(1023)
        self.ax12_ascenseur.move(self.lower_position)  # environ X°
        
    def elevate(self):
        # faire monter l'ascenseur
        return self.ax12_ascenseur.move(self.elevate_position)

    def lower(self):
        # faire descendre l'ascenseur
        return self.ax12_ascenseur.move(self.lower_position)
        
    def lower_for_plant(self):
        # faire descendre l'ascenseur
        return self.ax12_ascenseur.move_while(self.plant_position)

    def run(self):
        self.elevate()
        self.lower()

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Ascenseur()
    pince.lower_for_plant()
