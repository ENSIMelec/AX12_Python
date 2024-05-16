import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config


class AX12_Pinces:
    def __init__(self,interface=None):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("AX12")
        
        self.interface = interface
        # Initialisation des moteurs avec les IDs 3 et 5
        self.ax12_motor_gauche = AX12_Control(3,"Pince Gauche")
        self.ax12_motor_droit = AX12_Control(5,"Pince Droite")
        self.ouvert_gauche = 350
        self.ouvert_droit = 360
        self.fermer_gauche = 720
        self.fermer_droit = 0
        self.continuer_ajustement_motor_gauche = True
        self.continuer_ajustement_motor_droit = True
        
        self.ax12_motor_gauche.connect()
        self.ax12_motor_droit.connect()
        time.sleep(0.2)
        time.sleep(0.2)
        self.ax12_motor_gauche.set_speed(1023)
        self.ax12_motor_droit.set_speed(1023)
        time.sleep(0.2)

        self.ax12_motor_gauche.move(self.ouvert_gauche)  # par défaut ouverte la pince 
        self.ax12_motor_droit.move(self.ouvert_droit)

        self.logger.info("[Pinces] Pinces initialized.")

        if self.interface != None :
            self.interface.after(0, self.interface.AX12_Pinces_initialized())

    def move_while_pince(self,goal_pince_gauche,goal_pince_droite,tolerance=0.01,speed=1023):
        tolerance = tolerance * 1024
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(goal_pince_gauche)
        self.ax12_motor_droit.move(goal_pince_droite)
        goalG = True
        goalD = True
        while goalG or goalD :
            time.sleep(0.25)
            time.sleep(0.25)
            if goal_pince_gauche - tolerance <= self.ax12_motor_gauche.read_present_position() <= goal_pince_gauche + tolerance :
                goalG = False
            if goal_pince_droite - tolerance <= self.ax12_motor_droit.read_present_position() <= goal_pince_droite + tolerance :
                goalD = False
        return True

    def open_pince(self,speed=1023):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.ouvert_gauche)
        self.ax12_motor_droit.move(self.ouvert_droit)
        return True
    
    def open_pince_bloquant(self,speed=1023):
        return self.move_while_pince(self.ouvert_gauche,self.ouvert_droit,speed)
        
    def open_pinceV2(self):
        self.move_while_pince(self.ax12_motor_gauche.read_present_position()-25,self.ax12_motor_droit.read_present_position()+25,16)
        self.ax12_motor_gauche.set_speed(1023)
        self.ax12_motor_droit.set_speed(1023)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.ouvert_gauche)
        self.ax12_motor_droit.move(self.ouvert_droit)
        return True

    def close_pince(self,speed=32):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.fermer_gauche) 
        self.ax12_motor_droit.move(self.fermer_droit) 
        return True

    def close_pince_bloquant(self,speed=128):
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        time.sleep(0.25)
        self.ax12_motor_gauche.move(self.fermer_gauche) 
        self.ax12_motor_droit.move(self.fermer_droit) 
        time.sleep(0.25) # c le return delay 250 MS
        try :
            while(self.ax12_motor_gauche.get_present_speed() > 1 and self.ax12_motor_droit.get_present_speed() > 1):
                time.sleep(0.25)
        except :
            return True
        try :
            self.ax12_motor_gauche.move(self.ax12_motor_gauche.read_present_position()+10)
        except :
            return True
        try :
            self.ax12_motor_droit.move(max(self.ax12_motor_droit.read_present_position()-10,5))
        except :
            return True
        try :
            while(self.ax12_motor_gauche.get_present_speed() > 1 and self.ax12_motor_droit.get_present_speed() > 1):
                time.sleep(0.25)
        except :
            return True
        try :
            self.ax12_motor_gauche.move(self.ax12_motor_gauche.read_present_position()+10)
        except :
            return True
        try :
            self.ax12_motor_droit.move(max(self.ax12_motor_droit.read_present_position()-10,5))
        except :
            return True
        return True

                
    def run(self):
        self.open_pince()
        self.close_pince()
        #self.open_pince_stepbystep()

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Pinces()