import time
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config


class AX12_Panneau:
    def __init__(self):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

        # Créer un logger
        self.logger = logging.getLogger(f"AX12_Panneau")

        # Initialisation des moteurs avec les IDs id_1 et id_2
        self.AX12_Panneau_Droit = AX12_Control(4)
        self.AX12_Panneau_Gauche = AX12_Control(8)
        self.AX12_Panneau_Droit.connect()
        self.AX12_Panneau_Gauche.connect()
        self.AX12_Panneau_Droit.set_slop(0xFE)
        self.AX12_Panneau_Gauche.set_slop(0xFE)
        self.ramener_AX12_droit()
        self.ramener_AX12_gauche()
        
    
    def ramener_AX12_droit(self):
        self.AX12_Panneau_Droit.move(750)
        time.sleep(DELAY)
        return True
    
    def ramener_AX12_gauche(self):  
        self.AX12_Panneau_Gauche.move(495) 
        time.sleep(DELAY)
        return True
    
    
    def bouger_panneau_droit(self):
        self.AX12_Panneau_Droit.move(660)
        time.sleep(DELAY)
        return True

    def bouger_panneau_gauche(self):
        self.AX12_Panneau_Gauche.move(590)
        time.sleep(DELAY) #Pour laisser le temps de stabiliser le panneau
        return True
        
    
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