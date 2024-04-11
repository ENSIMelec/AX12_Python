import time
import os
from dynamixel_sdk import *
from AX12_Control import AX12_Control

class AX12_Ascenseur:
    def __init__(self):
        # Initialisation du moteur avec l'ID 6
        self.ax12_ascenseur = AX12_Control(6, 9600, '/dev/ttyACM0')

    def initialize_motors(self):
        # On leur donne une position initiale
        self.ax12_ascenseur.connect()

        self.ax12_ascenseur.move(1020)  # environ X°

        time.sleep(2)

    def elevate(self):
        # faire monter l'ascenseur
        self.ax12_ascenseur.move(2) # à peu près X°

        time.sleep(2) 

    def lower(self):
        # faire descendre l'ascenseur
        self.ax12_ascenseur.move(1020) # à peu près X°
        time.sleep(2)
        
    def lower_for_plant(self):
        # faire descendre l'ascenseur
        self.ax12_ascenseur.move(335) # à peu près X°
        time.sleep(2)

    def run(self):
        self.initialize_motors()
        #self.elevate()
        self.lower()

# Exemple d'utilisation
# if __name__ == "__main__":
#     pince = AX12_Ascenseur()
#     pince.run()
