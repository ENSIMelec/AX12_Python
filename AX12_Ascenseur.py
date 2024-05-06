import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config

class AX12_Ascenseur:
    def __init__(self,interface=None):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("AX12")

        self.interface=interface
        # Initialisation du moteur avec l'ID 6
        self.ax12_ascenseur = AX12_Control(6,"Ascenceur") 
        self.elevate_position = 10
        self.plant_position = 310
        self.lower_position = 970
        self.ax12_ascenseur.connect()
        self.ax12_ascenseur.set_angle_limit(0,1023) #sens horaire pour que le 1023 en bas
        # 103 mm d'amplitude pour l'ascenseur
        self.ax12_ascenseur.move(self.lower_position)
        
        self.logger.info("[Ascenceur] Ascenseur initialized.")
        
        if self.interface != None :
            self.interface.after(0, self.interface.AX12_Ascenceur_initialized())
        
    def elevate(self):
        # faire monter l'ascenseur
        return self.ax12_ascenseur.move(self.elevate_position)

    def lower(self):
        # faire descendre l'ascenseur
        return self.ax12_ascenseur.move(self.lower_position)
        
    def lower_for_plant(self):
        # faire descendre l'ascenseur
        return self.ax12_ascenseur.move_while(self.plant_position)

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Ascenseur()
    pince.elevate()
