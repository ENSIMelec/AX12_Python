import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config

class AX12_Ascenseur2025:
    def __init__(self,interface=None):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("AX12")

        self.interface=interface
        # Initialisation du moteur avec l'ID 7
        self.ax12_ascenseur = AX12_Control(7,"Ascenceur") 
        self.position_basse_max = 1000
        self.position_haute_max = 122
        self.position_pour_attraper = 770
        self.position_planche_attrapee = 950
        self.position_poser_etape = 160 #200
        self.position_enlever_element_etage = 850
        self.position_mouvement_avec_jeu = 900 #600
        self.position_lever_banderole = 735
        self.position_poser_banderole = 680
        self.position_sortir_triple_etage = 135

        # self.soulever_position = 122
        # self.construction_position = 700
        # self.soulever_mouvement = 650
        # self.attraper_position = 830
        # self.back_position = 50
        # self.deposer_position = 1000
        # self.deposer_gradin = 1000
        # self.attraper_gradin = 880

        
        self.ax12_ascenseur.connect()
        self.ax12_ascenseur.set_angle_limit(0,1023) #sens horaire pour que le 1023 en bas
        # 103 mm d'amplitude pour l'ascenseur
        self.ax12_ascenseur.move(self.position_lever_banderole)
        
        self.logger.info("[Ascenceur] Ascenseur initialized.")
        
        # if self.interface != None :
        #     self.interface.after(0, self.interface.AX12_Ascenceur_initialized())
        
    def elevate_pos_max(self):
        return self.ax12_ascenseur.move(self.position_haute_max)
    
    def lower_pos_max(self):
        return self.ax12_ascenseur.move(self.position_basse_max)
    
    def hauteur_pour_aller_attraper(self):
        return self.ax12_ascenseur.move(self.position_pour_attraper)

    def hauteur_pour_attraper(self):
        return self.ax12_ascenseur.move(self.position_planche_attrapee)
    
    def hauteur_poser_etage(self):
        return self.ax12_ascenseur.move(self.position_poser_etape)
    
    def hauteur_reculer_element_etage(self):
        return self.ax12_ascenseur.move(self.position_enlever_element_etage)

    def hauteur_mouvement_avec_jeu(self):
        return self.ax12_ascenseur.move(self.position_mouvement_avec_jeu)
    
    def hauteur_lever_banderole(self):
        return self.ax12_ascenseur.move(self.position_lever_banderole)
    
    def hauteur_poser_banderole(self):
        return self.ax12_ascenseur.move(self.position_poser_banderole)
    
    def hauteur_sortir_triple_etage(self):
        return self.ax12_ascenseur.move(self.position_sortir_triple_etage)
    
    # def elevate_poser_gradin(self):
    #     # faire monter l'ascenseur pour faire un gradin
    #     return self.ax12_ascenseur.move(self.soulever_position)
    
    # def elevate_construction_gradin(self):
    #     # faire monter l'ascenseur pour faire un gradin
    #     return self.ax12_ascenseur.move(self.construction_position)

    # def elevate_en_mouvement(self):
    #     # faire monter legerement l'ascenseur pour transporter le jeu
    #     return self.ax12_ascenseur.move(self.soulever_mouvement)
    
    # def elevate_for_back(self):
    #     # faire monter legerement l'ascenseur pour transporter le jeu
    #     return self.ax12_ascenseur.move(self.back_position)

    # def lower(self):
    #     # faire descendre l'ascenseur pour deposer au sol
    #     return self.ax12_ascenseur.move(self.deposer_position)

    # def lower_poser_gradin(self):
    #     # faire descendre l'ascenseur pour poser le gradin
    #     return self.ax12_ascenseur.move(self.deposer_gradin)

    # def lower_attraper_gradin(self):
    #     # faire descendre l'ascenseur pour attraper le gradin
    #     return self.ax12_ascenseur.move(self.attraper_gradin)
# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Ascenseur2025()
