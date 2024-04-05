import time
import os
from dynamixel_sdk import *
from AX12_Control import AX12_Control


def bouger_panneau_droit():
    # Initialisation des moteurs avec les IDs 4 et 6
    ax12_motor_1 = AX12_Control(4, 9600, '/dev/ttyACM0')
    ax12_motor_1.connect()    
    for i in range(6):
        # Position initiale
        ax12_motor_1.move(520)
        time.sleep(5)
        
        # Toucher le panneau
        ax12_motor_1.move(615)
        time.sleep(3)
        
        ax12_motor_1.move(520)
        time.sleep(5)
    ax12_motor_1.disconnect()