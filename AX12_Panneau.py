import time
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config


class AX12_Panneau:
    def __init__(self,app=None):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

        # Créer un logger
        self.logger = logging.getLogger(f"AX12_Panneau")

        self.app = app
        # Initialisation des moteurs avec les IDs id_1 et id_2
        self.AX12_Panneau_Droit = AX12_Control(4,"Bras Droit")
        self.AX12_Panneau_Gauche = AX12_Control(8,"Bras Gauche")
        self.AX12_Panneau_Droit.connect()
        self.AX12_Panneau_Gauche.connect()
        self.ramener_AX12_droit()
        self.ramener_AX12_gauche()
        
    
    def ramener_AX12_droit(self):
        self.AX12_Panneau_Droit.set_speed(1023)
        return self.AX12_Panneau_Droit.move(750)
    
    def ramener_AX12_gauche(self):  
        self.AX12_Panneau_Gauche.set_speed(1023)
        return self.AX12_Panneau_Gauche.move(495)
    
    
    def bouger_panneau_droit(self):
        self.AX12_Panneau_Droit.set_speed(128)
        return self.AX12_Panneau_Droit.move_while(660)

    def bouger_panneau_gauche(self):
        self.AX12_Panneau_Gauche.set_speed(128)
        return self.AX12_Panneau_Gauche.move_while(590)
        
    
    def disconnect(self):
        self.AX12_Panneau_Droit.disconnect()
        #self.AX12_Panneau_Gauche.disconnect()
        time.sleep(DELAY)
        return True

if __name__ == '__main__':
    AX12_Panneau = AX12_Panneau()
    AX12_Panneau.bouger_panneau_droit()
    AX12_Panneau.ramener_AX12_droit()
    AX12_Panneau.bouger_panneau_gauche()
    AX12_Panneau.ramener_AX12_gauche()
    AX12_Panneau.disconnect()