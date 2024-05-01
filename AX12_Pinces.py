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
        self.ax12_motor_1 = AX12_Control(3)
        self.ax12_motor_2 = AX12_Control(5)
        self.angle_ajustement_ax12_motor_1 = 580
        self.angle_ajustement_ax12_motor_2 = 150
        self.open_angle = 10
        self.reduce_angle = 50
        self.continuer_ajustement_motor_1 = True
        self.continuer_ajustement_motor_2 = True
        
        self.ax12_motor_1.connect()
        self.ax12_motor_2.connect()

        self.ax12_motor_1.move(580)  # environ 170°
        self.ax12_motor_2.move(150) 


    def open_pince(self):
        # Ouvrir la pince
        self.ax12_motor_1.move(380) # à peu près 135°
        self.ax12_motor_2.move(360) 
        time.sleep(DELAY)
        return True
        
    def open_pince_stepbystep(self):
        self.continuer_ajustement_motor_1 = True
        self.continuer_ajustement_motor_2 = True
        while self.continuer_ajustement_motor_1 or self.continuer_ajustement_motor_2:
            if self.angle_ajustement_ax12_motor_1 > 470:
                self.angle_ajustement_ax12_motor_1 -= self.open_angle
                self.ax12_motor_1.move(self.angle_ajustement_ax12_motor_1)
            else:
                self.continuer_ajustement_motor_1 = False
                
            if self.angle_ajustement_ax12_motor_2 < 270:
                self.angle_ajustement_ax12_motor_2 += self.open_angle
                self.ax12_motor_2.move(self.angle_ajustement_ax12_motor_2)
            else:
                self.continuer_ajustement_motor_2 = False
        time.sleep(DELAY)
        return True

    def close_pince(self):
        
        # Fermer la pince
        self.ax12_motor_1.move(580) 
        self.ax12_motor_2.move(140) 

        load_threshold = 150  # Définir le seuil de charge de travail approprié

        # Fermer la pince progressivement jusqu'à rencontrer une résistance
        while self.continuer_ajustement_motor_1 or self.continuer_ajustement_motor_2:
            self.continuer_ajustement_motor_1 = True
            self.continuer_ajustement_motor_2 = True
            
            time.sleep(0.75)
            # Obtenez la charge de travail actuelle des moteurs
            load_motor_1 = self.ax12_motor_1.read_load()
            load_motor_2 = self.ax12_motor_2.read_load()
            
            pos_motor_1 = self.ax12_motor_1.read_present_position()
            pos_motor_2 = self.ax12_motor_2.read_present_position()

            if (load_motor_1 < load_threshold):
                self.angle_ajustement_ax12_motor_1 += 20
                self.ax12_motor_1.move(self.angle_ajustement_ax12_motor_1)
                print(f"Ajustement du moteur {self.ax12_motor_1.DXL_ID} effectué")
            else:
                print(f"Ajustement du moteur {self.ax12_motor_1.DXL_ID} suffisant")
                self.continuer_ajustement_motor_1 = False

            if load_motor_2 < load_threshold:
                self.angle_ajustement_ax12_motor_2 -= 20
                self.ax12_motor_2.move(self.angle_ajustement_ax12_motor_2)
                print(f"Ajustement du moteur {self.ax12_motor_2.DXL_ID} effectué")
            else:
                print(f"Ajustement du moteur {self.ax12_motor_2.DXL_ID} suffisant")
                self.continuer_ajustement_motor_2 = False
        time.sleep(DELAY)
        return True

                
    def run(self):
        self.open_pince()
        self.close_pince()
        #self.open_pince_stepbystep()

# Exemple d'utilisation
if __name__ == "__main__":
    pince = AX12_Pinces()
    for i in range(10):
        pince.close_pince()