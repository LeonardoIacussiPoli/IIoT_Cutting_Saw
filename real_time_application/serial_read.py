# Read Serial

import serial
import numpy as np
import json
import paho.mqtt.client as mqtt
import time 
from datetime import timedelta
 
def on_connect(client, userdata, flags, rc): 
    if rc==0: 
        client.connected_flag=True #set flag 
        print("connected OK") 
    else: 
        print("Bad connection Returned code=",rc) 


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


mqtt.Client.connected_flag=False
broker="172.20.10.2"
port = 1883
client = mqtt.Client("python1")             #create new instance  
client.username_pw_set(username="username",password="password")
client.on_connect=on_connect  #bind call back function 
client.loop_start() 
print("Connecting to broker ",broker) 
client.connect(broker)      #connect to broker 
while not client.connected_flag: #wait in loop 
    print("In wait loop") 
    time.sleep(1) 
print("in Main Loop") 


ser = serial.Serial('/dev/tty.usbmodem00000000001A1', 115200)
ser.flushInput()
ser.flushOutput()

post_process_window_len = 5
label_id_avg_vector = np.zeros((post_process_window_len))
accuracy_avg_vector = np.zeros((post_process_window_len))

# variable initialization for cutting time calculation
time_old_cutt = time.time()
cutting_time = 0
total_cutting_time = 0
cutting_time_str = ''
total_cutting_time_str = ''
time_calc_cutt = False             # flag (True time calculation active)

# variable initialization for working time calculation
time_old_on = time.time()
working_time = 0
total_working_time = 0
working_time_str = ''
total_working_time_str = ''
time_calc_on = False               # flag (True time calculation active)
 


while True:
    
    data_raw = ser.readline().decode("utf-8") 
    label_id = float(data_raw[13])
    accuracy = float(data_raw[28:34])
    
    
    # moving average of the prediction
    label_id_avg_vector[0:-1] = label_id_avg_vector[1:]
    label_id_avg_vector[-1] = label_id
    label_id_avg = np.mean(label_id_avg_vector)
        
    # accuracy 
    accuracy_avg_vector[0:-1] = accuracy_avg_vector[1:]
    accuracy_avg_vector[-1] = accuracy
    accuracy_avg = np.mean(accuracy_avg_vector)
    
    # define accuracy treshold
    if (label_id_avg <= 0.5):
        label_id_filt = 0
    elif (label_id_avg>=0.5 and label_id_avg<1.5 ):
        label_id_filt = 1
    elif (label_id_avg>=1.5 and label_id_avg<2.5):
        label_id_filt = 2
    elif (label_id_avg>=2.5):
        label_id_filt = 3
        
        
    # cutting time calculation 
    if (label_id_filt == 0 and time_calc_cutt == False):
        time_old_cutt = time.time()
        time_calc_cutt = True
    
    if (label_id_filt != 0 and time_calc_cutt == True):
        cutting_time = time.time() - time_old_cutt
        cutting_time_str = str(timedelta(seconds=cutting_time))[0:7]
        total_cutting_time = total_cutting_time + cutting_time
        total_cutting_time_str = str(timedelta(seconds=total_cutting_time))[0:7]
        print(cutting_time)
        time_calc_cutt = False
        
        
    # working time calculation 
    if (label_id_filt != 2 and time_calc_on == False):
        time_old_on = time.time()
        time_calc_on = True
    
    if (label_id_filt == 2 and time_calc_on == True):
        working_time = time.time() - time_old_on
        working_time_str = str(timedelta(seconds=working_time))[0:7]
        total_working_time = total_working_time + working_time
        total_working_time_str = str(timedelta(seconds=total_working_time))[0:7]
        print(working_time)
        time_calc_on = False


    
    MQTT_MSG=json.dumps({ 
            "label_id_avg":label_id_avg,
            "label_id_filt":label_id_filt,
            "accuracy_avg":accuracy_avg,
            "cutting_time":cutting_time_str,
            "total_cutting_time":total_cutting_time_str,
            "working_time":working_time_str,
            "total_working_time":total_working_time_str
        }) 
    
    ret= client.publish("mqtt",MQTT_MSG)   
    

  #%%  
    
client.loop_stop()    #Stop loop  
client.disconnect() # disconnect




