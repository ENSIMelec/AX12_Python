import os
import time
from dynamixel_sdk import *
from Globals_Variables import *
import logging
import logging.config

# Control table ADDRess for AX-12
# EEPROM REGISTER ADDRESSES - Permanently stored in memory once changed
ADDR_AX_MODEL_NUMBER_L = 0
ADDR_AX_MODEL_NUMBER_H = 1
ADDR_AX_VERSION = 2
ADDR_AX_ID = 3
ADDR_AX_BAUD_RATE = 4
ADDR_AX_RETURN_DELAY_TIME = 5
ADDR_AX_CW_ANGLE_LIMIT_L = 6
ADDR_AX_CW_ANGLE_LIMIT_H = 7
ADDR_AX_CCW_ANGLE_LIMIT_L = 8
ADDR_AX_CCW_ANGLE_LIMIT_H = 9
ADDR_AX_SYSTEM_DATA2 = 10
ADDR_AX_LIMIT_TEMPERATURE = 11
ADDR_AX_MIN_LIMIT_VOLTAGE = 12
ADDR_AX_MAX_LIMIT_VOLTAGE = 13
ADDR_AX_MAX_TORQUE_L = 14
ADDR_AX_MAX_TORQUE_H = 15
ADDR_AX_RETURN_LEVEL = 16
ADDR_AX_ALARM_LED = 17
ADDR_AX_ALARM_SHUTDOWN = 18
ADDR_AX_OPERATING_MODE = 19
ADDR_AX_DOWN_CALIBRATION_L = 20
ADDR_AX_DOWN_CALIBRATION_H = 21
ADDR_AX_UP_CALIBRATION_L = 22
ADDR_AX_UP_CALIBRATION_H = 23

# RAM REGISTER ADDRESSES - resets after shut down
ADDR_AX_TORQUE_ENABLE = 24
ADDR_AX_LED = 25
ADDR_AX_CW_COMPLIANCE_MARGIN = 26
ADDR_AX_CCW_COMPLIANCE_MARGIN = 27
ADDR_AX_CW_COMPLIANCE_SLOPE = 28
ADDR_AX_CCW_COMPLIANCE_SLOPE = 29
ADDR_AX_GOAL_POSITION_L = 30
ADDR_AX_GOAL_POSITION_H = 31
ADDR_AX_GOAL_SPEED_L = 32
ADDR_AX_GOAL_SPEED_H = 33
ADDR_AX_TORQUE_LIMIT_L = 34
ADDR_AX_TORQUE_LIMIT_H = 35
ADDR_AX_PRESENT_POSITION_L = 36
ADDR_AX_PRESENT_POSITION_H = 37
ADDR_AX_PRESENT_SPEED_L = 38
ADDR_AX_PRESENT_SPEED_H = 39
ADDR_AX_PRESENT_LOAD_L = 40
ADDR_AX_PRESENT_LOAD_H = 41
ADDR_AX_PRESENT_VOLTAGE = 42
ADDR_AX_PRESENT_TEMPERATURE = 43
ADDR_AX_REGISTERED_INSTRUCTION = 44
ADDR_AX_PAUSE_TIME = 45
ADDR_AX_MOVING = 46
ADDR_AX_LOCK = 47
ADDR_AX_PUNCH_L = 48
ADDR_AX_PUNCH_H = 49

class AX12_Control:
    def __init__(self, dxl_id, name=None, baudrate=9600, devicename=AX12_SERIAL):
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("AX12")

        self.name = name
        self.DXL_ID = dxl_id
        self.BAUDRATE = baudrate
        self.DEVICENAME = devicename
        self.portHandler = PortHandler(self.DEVICENAME)
        self.packetHandler = PacketHandler(1.0) # Protocol version 1.0
        
    def connect(self):
        if self.portHandler.openPort():
            self.logger.info(f"[{self.name}] Port ouvert avec succès ID: {self.DXL_ID}")
        else:
            self.logger.error(f"[{self.name}] Échec de l'ouverture du port ID: {self.DXL_ID}")
            getch()
            quit()

        if self.portHandler.setBaudRate(self.BAUDRATE):
            self.logger.info(f"[{self.name}] Vitesse du port modifiée avec succès à {self.BAUDRATE} bps")
        else:
            self.logger.error("[{self.name}] Échec de modification de la vitesse du port à {self.BAUDRATE} bps")
            getch()
            quit()

        dxl_model_number, dxl_comm_result, dxl_error = self.packetHandler.ping(self.portHandler, self.DXL_ID)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (connect) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (connect) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Ping réussi. Numéro de modèle du Dynamixel : {dxl_model_number}")
        
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, 24, 1)  # Adresse pour activer le mode de torque

        return True

    def move(self, position):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_GOAL_POSITION_L, position)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (move) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (move) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Position réglée à {position} avec succès")
            return True
        
    def move_while(self, goal,tolerance=0.01):
        self.move(goal)
        tolerance = tolerance * 1024
        while not (goal - tolerance <= self.read_present_position() <= goal + tolerance):
            time.sleep(0.1)
        return True

    def read_load(self):
        dxl_present_load, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_PRESENT_LOAD_L)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"([{self.name}] read_load) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (read_load) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Load du servo : {dxl_present_load}")
            return dxl_present_load
    

    def write(self, address, value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, address, value)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (write) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (write) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Écriture réussie à l'adresse {address} avec la valeur {value}")
            return True

        
    def read_present_position(self):
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_PRESENT_POSITION_L)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (read_present_position) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (read_present_position) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Current pos :{dxl_present_position}")
            return dxl_present_position

    def set_speed(self, speed):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_GOAL_SPEED_L, speed)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_speed) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (set_speed) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Vitesse réglée à {speed} avec succès")
            return True
       
    def get_id(self):
        dxl_id, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_ID)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_id) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (get_id) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] ID actuel du servo: {dxl_id}")
            return dxl_id

    def set_id(self, new_id):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_ID, new_id)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_id) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"([{self.name}] set_id) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] ID du servo mis à jour à {new_id}")
            self.DXL_ID = new_id
            return True

    def get_angle_limit(self):
        dxl_cw_angle_limit, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_CW_ANGLE_LIMIT_L)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_cw_angle_limit) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (get_cw_angle_limit) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            dxl_cw_angle_limit2, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_CCW_ANGLE_LIMIT_L)
            if dxl_comm_result != COMM_SUCCESS:
                self.logger.error(f"[{self.name}] (get_ccw_angle_limit) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                self.logger.error(f"[{self.name}] (get_ccw_angle_limit) {self.packetHandler.getRxPacketError(dxl_error)}")
            else:
                if dxl_cw_angle_limit2 > dxl_cw_angle_limit :
                    self.logger.info(f"[{self.name}] Limite d'angle: {dxl_cw_angle_limit} à {dxl_cw_angle_limit2}")
                elif dxl_cw_angle_limit > dxl_cw_angle_limit2 :
                    self.logger.info(f"[{self.name}] Limite d'angle: {dxl_cw_angle_limit2} à {dxl_cw_angle_limit}")
                else :
                    self.logger.info(f"[{self.name}] Limite d'angle: {dxl_cw_angle_limit2} et {dxl_cw_angle_limit} donc continue")
                return dxl_cw_angle_limit,dxl_cw_angle_limit2

    def set_angle_limit(self, limit1,limit2):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_CW_ANGLE_LIMIT_L, limit1)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_cw_angle_limit) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (set_cw_angle_limit) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_CCW_ANGLE_LIMIT_L, limit2)
            if dxl_comm_result != COMM_SUCCESS:
                self.logger.error(f"[{self.name}] (set_cw_angle_limit) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
                return False
            elif dxl_error != 0:
                self.logger.error(f"[{self.name}] (set_cw_angle_limit) {self.packetHandler.getRxPacketError(dxl_error)}")
                return False
            else:
                if limit2 > limit1 :
                    self.logger.info(f"[{self.name}] Limite d'angle: {limit1} à {limit2} donc sens horaire (POV LED)")
                elif limit1 > limit2 :
                    self.logger.info(f"[{self.name}] Limite d'angle: {limit2} à {limit1} donc sens anti-horaire (POV LED)")
                else :
                    self.logger.info(f"[{self.name}] Limite d'angle: {limit2} et {limit1} donc continue")
                return True
        
    def get_baudrate(self):
        dxl_baudrate, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_BAUD_RATE)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_baudrate) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (get_baudrate) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Baudrate actuel: {dxl_baudrate}")
            return dxl_baudrate

    def set_baudrate(self, baudrate):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_BAUD_RATE, baudrate)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_baudrate) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
            return False
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (set_baudrate) {self.packetHandler.getRxPacketError(dxl_error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Baudrate mis à jour à {baudrate}")
            self.BAUDRATE = baudrate
            return True

    def get_present_speed(self):
        dxl_speed, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_PRESENT_SPEED_L)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_present_speed) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (get_present_speed) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Vitesse actuelle: {dxl_speed}")
            return dxl_speed

    def get_temperature(self):
        dxl_temp, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_PRESENT_TEMPERATURE)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_temperature) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (get_temperature) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Température actuelle: {dxl_temp}")
            return dxl_temp

    def get_voltage(self):
        dxl_voltage, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_PRESENT_VOLTAGE)
        if dxl_comm_result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_voltage) {self.packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            self.logger.error(f"[{self.name}] (get_voltage) {self.packetHandler.getRxPacketError(dxl_error)}")
        else:
            self.logger.info(f"[{self.name}] Tension actuelle: {dxl_voltage / 10.0}V")
            return dxl_voltage / 10.0

    def get_led(self):
        led_status, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_LED)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_led) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_led) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] LED status: {led_status}")
            return led_status

    def set_led(self, on_off):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_LED, on_off)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_led) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_led) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] LED set to {'on' if on_off else 'off'}")
            return True

    def get_return_delay_time(self):
        delay, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_RETURN_DELAY_TIME)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_return_delay_time) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_return_delay_time) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Return delay time: {delay}")
            return delay

    def set_return_delay_time(self, delay):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_RETURN_DELAY_TIME, delay)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_return_delay_time) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_return_delay_time) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Return delay time set to {delay}")
            return True
    
    def get_min_voltage_limit(self):
        voltage, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MIN_LIMIT_VOLTAGE)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_min_voltage_limit) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_min_voltage_limit) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Minimum Voltage Limit: {voltage}")
            return voltage

    def set_min_voltage_limit(self, voltage):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MIN_LIMIT_VOLTAGE, voltage)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_min_voltage_limit) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_min_voltage_limit) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Minimum Voltage Limit set to {voltage}")
            return True

    def get_max_voltage_limit(self):
        voltage, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MAX_LIMIT_VOLTAGE)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_max_voltage_limit) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_max_voltage_limit) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Maximum Voltage Limit: {voltage}")
            return voltage

    def set_max_voltage_limit(self, voltage):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MAX_LIMIT_VOLTAGE, voltage)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_max_voltage_limit) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_max_voltage_limit) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Maximum Voltage Limit set to {voltage}")
            return True

    def get_max_torque(self):
        torque, result, error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MAX_TORQUE_L)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_max_torque) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_max_torque) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Max Torque: {torque}")
            return torque

    def set_max_torque(self, torque):
        result, error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MAX_TORQUE_L, torque)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_max_torque) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_max_torque) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Max Torque set to {torque}")
            return True

    def get_torque_enable(self):
        torque_enable, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_TORQUE_ENABLE)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_torque_enable) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_torque_enable) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Torque Enable: {torque_enable}")
            return torque_enable

    def set_torque_enable(self, enable):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_TORQUE_ENABLE, enable)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_torque_enable) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_torque_enable) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Torque Enabled: {enable}")
            return True
        
    def get_alarm_led(self):
        alarm_led, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_ALARM_LED)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_alarm_led) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_alarm_led) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Alarm LED: {alarm_led}")
            return alarm_led

    def set_alarm_led(self, value):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_ALARM_LED, value)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_alarm_led) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_alarm_led) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Alarm LED set to {value}")
            return True

    def get_alarm_shutdown(self):
        alarm_shutdown, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_ALARM_SHUTDOWN)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_alarm_shutdown) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_alarm_shutdown) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Alarm Shutdown: {alarm_shutdown}")
            return alarm_shutdown

    def set_alarm_shutdown(self, value):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_ALARM_SHUTDOWN, value)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_alarm_shutdown) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_alarm_shutdown) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] Alarm Shutdown set to {value}")
            return True

    def get_registered_instruction(self):
        instruction, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_REGISTERED_INSTRUCTION)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_registered_instruction) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_registered_instruction) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Registered Instruction: {instruction}")
            return instruction

    def is_moving(self):
        moving, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_MOVING)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (is_moving) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (is_moving) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] Is Moving: {moving}")
            return moving

    def get_lock(self):
        lock, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_LOCK)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (get_lock) {self.packetHandler.getTxRxResult(result)}")
        elif error != 0:
            self.logger.error(f"[{self.name}] (get_lock) {self.packetHandler.getRxPacketError(error)}")
        else:
            self.logger.info(f"[{self.name}] EEPROM Lock: {lock}")
            return lock

    def set_lock(self, lock):
        result, error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, ADDR_AX_LOCK, lock)
        if result != COMM_SUCCESS:
            self.logger.error(f"[{self.name}] (set_lock) {self.packetHandler.getTxRxResult(result)}")
            return False
        elif error != 0:
            self.logger.error(f"[{self.name}] (set_lock) {self.packetHandler.getRxPacketError(error)}")
            return False
        else:
            self.logger.info(f"[{self.name}] EEPROM Lock set to {lock}")
            return True
        
    def set_continuous_rotation(self, enable):
        if enable:
            # Set both CW and CCW angle limits to 0 for continuous rotation
            self.write(ADDR_AX_CW_ANGLE_LIMIT_L, 0)
            self.write(ADDR_AX_CCW_ANGLE_LIMIT_L, 0)
        else:
            # Set to default values or specific angle limits for standard operation
            self.write(ADDR_AX_CW_ANGLE_LIMIT_L, 0)
            self.write(ADDR_AX_CCW_ANGLE_LIMIT_L, 1023)

    def raw_to_degree(self, raw_value):
        """ Convert raw value to degree based on AX-12 resolution """
        return raw_value * 300 / 1023

    def degree_to_raw(self, degree_value):
        """ Convert degree to raw value based on AX-12 resolution """
        return int(degree_value * 1023 / 300)
    
    def disconnect(self):
        self.portHandler.closePort()
