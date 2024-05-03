import time
import os
from dynamixel_sdk import *
from AX12_Python.AX12_Control import AX12_Control
from Globals_Variables import *
import logging
import logging.config


class AX12_Pinces:
    def __init__(self):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

        # Créer un logger
        self.logger = logging.getLogger(f"AX12_Pinces")

        # Initialisation des moteurs avec les IDs 3 et 5
        self.ax12_motor_gauche = AX12_Control(3,"Pince Gauche")
        self.ax12_motor_droit = AX12_Control(5,"Pince Droite")
        self.angle_ajustement_ax12_motor_gauche = 580
        self.angle_ajustement_ax12_motor_droit = 150
        self.open_angle = 10
        self.reduce_angle = 50
        self.continuer_ajustement_motor_gauche = True
        self.continuer_ajustement_motor_droit = True
        
        self.ax12_motor_gauche.connect()
        self.ax12_motor_droit.connect()

        self.ax12_motor_gauche.move(580)  # environ 170°
        self.ax12_motor_droit.move(150) 

    def move_while_pince(self,goal_pince_gauche,goal_pince_droite,tolerance=0.01,speed=1023):
        tolerance = tolerance * 1024
        self.ax12_motor_gauche.set_speed(speed)
        self.ax12_motor_droit.set_speed(speed)
        self.ax12_motor_gauche.move(goal_pince_gauche)
        self.ax12_motor_droit.move(goal_pince_droite)
        goalG = True
        goalD = True
        while goalG or goalD :
            time.sleep(0.1)
            if goal_pince_gauche - tolerance <= self.ax12_motor_gauche.read_present_position() <= goal_pince_gauche + tolerance :
                goalG = False
            if goal_pince_droite - tolerance <= self.ax12_motor_droit.read_present_position() <= goal_pince_droite + tolerance :
                goalD = False
        return True

    def open_pince(self):
        return self.move_while_pince(380,360)
        
    def open_pince_stepbystep(self):
        self.continuer_ajustement_motor_gauche = True
        self.continuer_ajustement_motor_droit = True
        while self.continuer_ajustement_motor_gauche or self.continuer_ajustement_motor_droit:
            if self.angle_ajustement_ax12_motor_gauche > 470:
                self.angle_ajustement_ax12_motor_gauche -= self.open_angle
                self.ax12_motor_gauche.move(self.angle_ajustement_ax12_motor_gauche)
            else:
                self.continuer_ajustement_motor_gauche = False
                
            if self.angle_ajustement_ax12_motor_droit < 270:
                self.angle_ajustement_ax12_motor_droit += self.open_angle
                self.ax12_motor_droit.move(self.angle_ajustement_ax12_motor_droit)
            else:
                self.continuer_ajustement_motor_droit = False
        time.sleep(DELAY)
        return True

    def close_pince(self):
        self.ax12_motor_gauche.move(720) 
        self.ax12_motor_droit.move(0) 
        time.sleep(0.2)
        self.ax12_motor_gauche.move(self.ax12_motor_gauche.read_present_position()+10)
        self.ax12_motor_droit.move(self.ax12_motor_droit.read_present_position()-10)
        return True

                
    def run(self):
        self.open_pince()
        self.close_pince()
        #self.open_pince_stepbystep()

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Pinces()
    pince.close_pince_test()
    # pince.open_pince()