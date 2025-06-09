# PyModbus Server
from pymodbus.client import ModbusTcpClient
import time
import sys
from Adafruit_IO import MQTTClient
import os
from dotenv import load_dotenv
import asyncio


# Below is the code for Adafruit IO MQTT Client
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_USERNAME = os.getenv("API_USERNAME")

ADAFRUIT_IO_KEY = API_KEY
ADAFRUIT_IO_USERNAME = API_USERNAME

# Define callback functions which will be called when certain events happen.
def connected(mqttclient):
    print('Listening for changes on ', group_name)
#    client.subscribe_group(group_name)

def disconnected(mqttclient):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(mqttclient, topic_id, payload):
    print('Topic {0} received new value: {1}'.format(topic_id, payload))

# Create an MQTT client instance.
mqttclient = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
mqttclient.on_connect    = connected
mqttclient.on_disconnect = disconnected
mqttclient.on_message    = message

group_name = 'AR_HQ_TRAILER_PARK_WELL'
pump_run = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-water-well-pump'
well_pump_i = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-water-well-pump-i'
drywell_delay = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-dry-well-delay'
sys_run = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-water-well-system-run'
dw_time_r = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-water-well-dry-well-time-remaining'
dw_count = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-water-well-dry-well-count'
well_ps = 'jakefreese/feeds/ar-hq-trailer-park-well.ar-hq-trailer-park-water-well-pressure-switch'

#End of Adafruit IO MQTT Client setup

Well_PS = int(0)
L_Well_PS = int(0)
Sys_run = int(0)
L_Sys_run = int(0)
Pump_Run = int(0)
L_Pump_Run = int(0)
Dry_Well = int(0)
L_Dry_Well = int(0)
Dry_Well_time = int(0)
L_Dry_Well_time = int(0)
Dry_Well_Count = int(0)
L_Dry_Well_Count = int(0)
Pump_I = float(0)
L_Pump_I = float(0)
last = 0
initial_sub = 0

mqttclient.connect()
if mqttclient.on_connect == connected:
    print("MQTT CONNECTED:")
else:()

client = ModbusTcpClient('192.168.2.134')
client.connect() # Connect to the Modbus Server
print("MODBUS CONNECTED:", client.connected)

#mqttclient.loop_background()

while True:
        if not mqttclient.is_connected:
            print("MQTT NOT CONNECTED, reconnecting and waiting 6seconds")
            mqttclient.connect()
            time.sleep(6)
            if not mqttclient.is_connected:
                print("MQTT NOT CONNECTED")
                time.sleep(10)
            else:
                print("MQTT RECONNECTED")

        mqttclient.loop_background()
        print("MODBUS CONNECTED:", client.connected)
        print("MQTT CONNECTED:", connected)
        time_of_day = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Current Time:", time_of_day)

        try:
            all = client.read_holding_registers(1, 7)
            if all.isError():
                raise ValueError("Error reading registers")
        except Exception as e:
            print(f"Error reading registers: {e}")
            time.sleep(60)
            client.connect()
            continue

        if client.connected == True:
            print("Reading Registers", (all.registers))
            Well_PS_v = client.read_holding_registers(1)  # %QW1
            Well_PS = (Well_PS_v.registers[0])
            print("Well_PS:", Well_PS)
            print("L_Well_PS:", L_Well_PS)
            Sys_run_v = client.read_holding_registers(2)  # %QW2
            Sys_run = (Sys_run_v.registers[0])
            print("Sys_run:", Sys_run)
            Pump_Run_v = client.read_holding_registers(3)  # %QW3
            Pump_Run = (Pump_Run_v.registers[0])
            print("Pump_Run:", Pump_Run)
            Dry_Well_v = client.read_holding_registers(4)  # %QW4
            Dry_Well = (Dry_Well_v.registers[0])
            print("Dry_Well:", Dry_Well)
            Dry_Well_time_v = client.read_holding_registers(5)  # %QW5
            Dry_Well_time = (Dry_Well_time_v.registers[0])
            print("Dry_Well_time:", Dry_Well_time)
            Dry_Well_Count_v = client.read_holding_registers(6)  # %QW6
            Dry_Well_Count = (Dry_Well_Count_v.registers[0])
            print("Dry_Well_Count:", Dry_Well_Count)           
            Pump_I_v = client.read_holding_registers(7)  # %QW7
            Pump_I = (((Pump_I_v.registers[0]) / 1000) * 2)
            print("Pump_I:", Pump_I)
            time.sleep(1)
        else:
            print("MODBUS NOT CONNECTED, reconnecting and waiting 6seconds")
            client.connect()
            time.sleep(6)
            if client.connected == True:
                print("MODBUS RECONNECTED")
            else:
                print("MODBUS NOT CONNECTED")
                time.sleep(10)


        if (time.time() - last) >= 10.0:

            if Well_PS != L_Well_PS:
                mqttclient.publish('well_ps', Well_PS, group_name)
                L_Well_PS = Well_PS
            else:()

            if Pump_Run != L_Pump_Run:
                mqttclient.publish('pump_run', Pump_Run, group_name)
                L_Pump_Run = Pump_Run
            else:()

            if  Pump_I < 1:
                Pump_I = 0         
            else:()

            if Well_PS == 0 and L_Well_PS == 1:
                mqttclient.publish('well_pump_i', Pump_I, group_name)
            else:()

            if Pump_I != L_Pump_I:
                mqttclient.publish('well_pump_i', Pump_I, group_name)
                L_Pump_I = Pump_I
            else:() 

            if  Pump_I > 1.1 * L_Pump_I:
                mqttclient.publish('well_pump_i', Pump_I, group_name)
                L_Pump_I = Pump_I
            else:()

            if Pump_I < 0.9 * L_Pump_I:
                mqttclient.publish('well_pump_i', Pump_I, group_name)
                L_Pump_I = Pump_I
            else:()

            if Dry_Well != L_Dry_Well:
                mqttclient.publish('drywell_delay', Dry_Well, group_name)
                L_Dry_Well = Dry_Well
            else:()

            if Sys_run != L_Sys_run:
                mqttclient.publish('sys_run', Sys_run, group_name)
                L_Sys_run = Sys_run
            else:()

            if Dry_Well_time != L_Dry_Well_time:
                mqttclient.publish('dw_time_r', Dry_Well_time, group_name)
                L_Dry_Well_time = Dry_Well_time
            else:()

            if Dry_Well_Count != L_Dry_Well_Count:
                mqttclient.publish('dw_count', Dry_Well_Count, group_name)
                L_Dry_Well_Count = Dry_Well_Count
            else:()
            last = time.time()  # Update the last time we published data

            if initial_sub == 0:
                mqttclient.publish('dw_count', Dry_Well_Count, group_name)
                mqttclient.publish('dw_time_r', Dry_Well_time, group_name)
                mqttclient.publish('sys_run', Sys_run, group_name)
                mqttclient.publish('drywell_delay', Dry_Well, group_name)
                mqttclient.publish('well_pump_i', Pump_I, group_name)
                mqttclient.publish('pump_run', Pump_Run, group_name)
                mqttclient.publish('well_ps', Well_PS, group_name)
                initial_sub = 1
            else:()

        time.sleep(10)  # Add a delay to avoid flooding the server with requests
# End of Modbus to MQTT code
