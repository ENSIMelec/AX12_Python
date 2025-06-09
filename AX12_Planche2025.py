import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config


class AX12_Planche2025:
    def __init__(self,interface=None):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("AX12")
        
        self.interface = interface
        # Initialisation du moteur avec l'ID 4
        self.ax12_motor_planche = AX12_Control(4,"Pince Planche")

        self.point_zero = 1024//2
        self.ferme = 1023
        self.ouvert = 0

        self.ax12_motor_planche.connect()
        self.ax12_motor_planche.set_angle_limit(0,1023)

        #self.ax12_motor_planche.set_speed(1023)
        #self.ax12_motor_planche.move(self.point_zero)

        self.logger.info("[Planche] Planche initialized")



    def fermer_planche(self):
        return self.ax12_motor_planche.move(self.ferme)
    
    def ouvrir_planche(self):
        return self.ax12_motor_planche.move(self.ouvert)
        

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Planche2025()