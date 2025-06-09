import time
import os
import  numpy as np
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config


class AX12_Pinces2025:
    def __init__(self,interface=None):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("AX12")
        
        self.interface = interface
        # Initialisation des moteurs pinces avec les IDs 3, 8, 5 et 6
        self.ax12_motor_gauche = AX12_Control(3,"Pince Gauche")
        self.ax12_motor_gauche_milieu = AX12_Control(8,"Pince Gauche Milieu")
        self.ax12_motor_droit_milieu = AX12_Control(5,"Pince Droite Milieu")
        self.ax12_motor_droit = AX12_Control(6,"Pince Droite")

        # # Initialisation des moteurs rotation avec les IDs 1 et 2
        self.ax12_motor_rotation_gauche = AX12_Control(2,"Pince Rotation Gauche")
        self.ax12_motor_rotation_droit = AX12_Control(1,"Pince Rotation Droite")


        #OUVERTURE ALL PINCES
        self.ouvert_gauche = 600
        self.ouvert_gauche_milieu = 550
        self.ouvert_droit_milieu = 550
        self.ouvert_droit = 600

        #PINCES EXTERIEURES
        self.perimetre_non_deploye_rotation_gauche =460
        self.perimetre_non_deploye_rotation_droit = 560

        self.en_face_rotation_gauche = 570
        self.en_face_rotation_droit = 480
        

        self.tourne_rotation_gauche = 710 #710
        self.tourne_rotation_droit = 280 #370


        #FERMETURE ALL PINCES
        self.ferme_gauche = 480
        self.ferme_gauche_milieu = 480
        self.ferme_droit_milieu = 480
        self.ferme_droit = 480

       
        self.continuer_ajustement_motor_gauche = True
        self.continuer_ajustement_motor_gauche_milieu = True
        self.continuer_ajustement_motor_droit_milieu = True
        self.continuer_ajustement_motor_droit = True
        
        self.continuer_ajustement_motor_rotation_gauche = True
        self.continuer_ajustement_motor_rotation_droit = True

        self.ax12_motor_gauche.connect()
        self.ax12_motor_gauche_milieu.connect()
        self.ax12_motor_droit_milieu.connect()
        self.ax12_motor_droit.connect()
        self.ax12_motor_rotation_droit.connect()
        self.ax12_motor_rotation_gauche.connect()

        #time.sleep(0.2)
        time.sleep(0.2)
        self.ax12_motor_gauche.set_speed(1023)
        self.ax12_motor_gauche_milieu.set_speed(1023)
        self.ax12_motor_droit_milieu.set_speed(1023)
        self.ax12_motor_droit.set_speed(1023)
        self.ax12_motor_rotation_droit.set_speed(1023)
        self.ax12_motor_rotation_gauche.set_speed(1023)
        time.sleep(0.2)

        self.ax12_motor_gauche.move(self.ferme_gauche)  # par défaut fermée la pince 
        self.ax12_motor_gauche_milieu.move(self.ferme_gauche_milieu)
        self.ax12_motor_droit_milieu.move(self.ferme_droit_milieu)
        self.ax12_motor_droit.move(self.ferme_droit)

        self.ax12_motor_rotation_droit.move(self.perimetre_non_deploye_rotation_droit)
        self.ax12_motor_rotation_gauche.move(self.perimetre_non_deploye_rotation_gauche)

        self.logger.info("[Pinces] Pinces initialized.")



    def open_all_pinces(self,speed=1023):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_gauche_milieu.set_speed(speed)
        self.ax12_motor_droit_milieu.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.ouvert_gauche)
        self.ax12_motor_gauche_milieu.move(self.ouvert_gauche_milieu)
        self.ax12_motor_droit_milieu.move(self.ouvert_droit_milieu)
        self.ax12_motor_droit.move(self.ouvert_droit)
        return True
    
    def close_all_pinces(self,speed=1023):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_gauche_milieu.set_speed(speed)
        self.ax12_motor_droit_milieu.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.ferme_gauche) 
        self.ax12_motor_gauche_milieu.move(self.ferme_gauche_milieu) 
        self.ax12_motor_droit_milieu.move(self.ferme_droit_milieu) 
        self.ax12_motor_droit.move(self.ferme_droit) 
        return True
    
    def close_pinces_inte(self,speed=1023):
        self.ax12_motor_gauche_milieu.set_speed(speed)
        self.ax12_motor_droit_milieu.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche_milieu.move(self.ferme_gauche_milieu) 
        self.ax12_motor_droit_milieu.move(self.ferme_droit_milieu) 
        return True
    
    def close_pinces_exte(self,speed=1023):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.ferme_gauche) 
        self.ax12_motor_droit.move(self.ferme_droit) 
        return True
    
    def open_pinces_exte(self,speed=1023):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.ouvert_gauche)
        self.ax12_motor_droit.move(self.ouvert_droit)
        return True
    
    def open_pinces_inte(self,speed=1023):
        self.ax12_motor_gauche_milieu.set_speed(speed)
        self.ax12_motor_droit_milieu.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche_milieu.move(self.ouvert_gauche_milieu)
        self.ax12_motor_droit_milieu.move(self.ouvert_droit_milieu)
        return True

    def en_face_pinces_exte(self,speed=1023):
        self.ax12_motor_rotation_droit.set_speed(speed)
        self.ax12_motor_rotation_gauche.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_rotation_droit.move(self.en_face_rotation_droit)
        self.ax12_motor_rotation_gauche.move(self.en_face_rotation_gauche)
        return True
    
    def tourne_pinces_exte(self,speed=1023):
        self.ax12_motor_rotation_droit.set_speed(speed)
        self.ax12_motor_rotation_gauche.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_rotation_droit.move(self.tourne_rotation_droit)
        self.ax12_motor_rotation_gauche.move(self.tourne_rotation_gauche)
        return True

    def replier_pinces_exte(self,speed=1023):
        self.ax12_motor_rotation_droit.set_speed(speed)
        self.ax12_motor_rotation_gauche.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_rotation_droit.move(self.perimetre_non_deploye_rotation_droit)
        self.ax12_motor_rotation_gauche.move(self.perimetre_non_deploye_rotation_gauche)
        return True
                
    
# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Pinces2025()