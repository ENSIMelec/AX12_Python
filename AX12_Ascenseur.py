import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import DELAY

class AX12_Ascenseur:
    def __init__(self):
        # Initialisation du moteur avec l'ID 6
        self.ax12_ascenseur = AX12_Control(6) 
        self.initial_position = 200
        self.plant_position = 335
        self.final_position = 1020
        self.ax12_ascenseur.connect()
        self.ax12_ascenseur.move(1020)  # environ X°
        
    def elevate(self):
        # faire monter l'ascenseur
        self.ax12_ascenseur.move(self.initial_position) # à peu près X°
        time.sleep(DELAY)
        return True

    def lower(self):
        # faire descendre l'ascenseur
        self.ax12_ascenseur.move(self.final_position) # à peu près X°
        time.sleep(DELAY)
        return True
        
    def lower_for_plant(self):
        # faire descendre l'ascenseur
        self.ax12_ascenseur.move(self.plant_position) # à peu près X°
        time.sleep(DELAY)
        return True

    def run(self):
        #self.elevate()
        self.lower()

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Ascenseur()
    pince.run()
