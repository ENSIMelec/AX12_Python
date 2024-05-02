import os
import time
from dynamixel_sdk import *
from Globals_Variables import *
import logging
import logging.config

class AX12_Control:
    def __init__(self, dxl_id, name=None, baudrate=9600, devicename=AX12_SERIAL):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

        # Créer un logger
        self.logger = logging.getLogger(f"AX12_Control({name})")

        self.name = name
        self.DXL_ID = dxl_id
        self.BAUDRATE = baudrate
        self.DEVICENAME = devicename
        self.portHandler = PortHandler(self.DEVICENAME)
        self.packetHandler = PacketHandler(1.0) # Protocol version 1.0
        self.torque_limit = 1023
        self.ADDR_MX_PRESENT_POSITION = 36
        self.ADDR_AX_MOVING_SPEED = 32
        self.ADDR_AX_SLOP = 29
        
    def connect(self):
        if self.portHandler.openPort():
            self.logger.info(f"Port ouvert avec succès ID: {self.DXL_ID}")
        else:
            self.logger.error(f"Échec de l'ouverture du port ID: {self.DXL_ID}")
            getch()
            quit()

        if self.portHandler.setBaudRate(self.BAUDRATE):
            self.logger.info(f"Vitesse du port modifiée avec succès à {self.BAUDRATE} bps")
        else:
            self.logger.error("Échec de modification de la vitesse du port à {self.BAUDRATE} bps")
            getch()
            quit()

        dxl_model_number, dxl_comm_result, dxl_error = self.packetHandler.ping(self.portHandler, self.DXL_ID)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(connect) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"(connect) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"Ping réussi. Numéro de modèle du Dynamixel : {dxl_model_number}")
        
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, 24, 1)  # Adresse pour activer le mode de torque

        return True

    def move(self, position):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, 30, position)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(move) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"(move) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"Position réglée à {position} avec succès")
            return True
        
    def move_while(self, goal,tolerance=0.01):
        self.move(goal)
        while not (goal * (1-tolerance) <= self.read_present_position() <= goal * (1+tolerance)):
            time.sleep(0.1)
        return True

    def read_load(self):
        dxl_present_load, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, 40)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(read_load) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"(read_load) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"Load du servo : {dxl_present_load}")
            return dxl_present_load
    

    def write(self, address, value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, address, value)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(write) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"(write) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"Écriture réussie à l'adresse {address} avec la valeur {value}")
            return True

        
    def read_present_position(self):
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(read_present_position) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"(read_present_position) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"Current pos :{dxl_present_position}")
            return dxl_present_position

    def set_speed(self, speed):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_AX_MOVING_SPEED, speed)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(set_speed) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"(set_speed) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"Vitesse réglée à {speed} avec succès")
            return True
            
    def set_slop(self, slop):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_AX_SLOP, slop)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"(set_slop) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"(set_slop) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"Slop réglé à {slop} avec succès")
            return True
       
    def disconnect(self):
        self.portHandler.closePort()

#Exemple d'utilisation


# Actionneurs panneaux solaires
#for _ in range(6):
#   ax12.move(520)
#   time.sleep(5)

#    ax12.move(615)
#    time.sleep(3)

#    ax12.move(520)
#    time.sleep(5)

#ax12.disconnect()
