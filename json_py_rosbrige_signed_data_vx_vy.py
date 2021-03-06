from json import dumps
from json import loads
from ws4py.client.threadedclient import WebSocketClient
import serial
import math
from time import time
import numpy
import transformations as tf




ser=serial.Serial('/dev/ttyUSB0')
ser.baudrate=19200
ser.close()
ser.open()
import transformations
print "sucess"

import time, threading
odometry_x_=0.0
odometry_y_=0.0
odometry_yaw_=0.0
right_encoder_prev=0.0
left_encoder_prev=0.0
current_time=0.0
data_publish_flag=1

	 	

class GetLoggersClient(WebSocketClient):
     

     def get_loggers(self):
         msg1 = {'op': 'advertise', 'topic': '/encoder1', 'type': 'std_msgs/UInt64'}
         msg2 = {'op': 'advertise', 'topic': '/encoder2', 'type': 'std_msgs/UInt64'}
         msg3={'op':'advertise', 'topic':'/sonar1', 'type': 'sensor_msgs/Range'}
         msg4={'op':'advertise', 'topic':'/sonar2', 'type': 'sensor_msgs/Range'}   
         msg5={'op':'advertise', 'topic':'/sonar3', 'type': 'sensor_msgs/Range'}
         msg6={'op':'advertise', 'topic':'/sonar4', 'type': 'sensor_msgs/Range'} 
         msg7={'op':'advertise', 'topic':'/sonar5', 'type': 'sensor_msgs/Range'}
         msg8={'op':'advertise', 'topic':'/sonar6', 'type': 'sensor_msgs/Range'}  
         msg9={'op':'advertise', 'topic':'/sonar7', 'type': 'sensor_msgs/Range'}
         msg10={'op':'advertise', 'topic':'/sonar8', 'type': 'sensor_msgs/Range'}
         msg11={'op':'advertise', 'topic':'/odom', 'type': 'nav_msgs/Odometry'}        
         self.send(dumps(msg1))
         self.send(dumps(msg2))
         self.send(dumps(msg3))
         self.send(dumps(msg4))
         self.send(dumps(msg5))
         self.send(dumps(msg6))
         self.send(dumps(msg7))
         self.send(dumps(msg8))
         self.send(dumps(msg9))
         self.send(dumps(msg10))
         self.send(dumps(msg11))

     def ros_subscribe(self):
         msg1 =  {'op': 'subscribe', 'topic': '/encoder1', 'type':'std_msgs/UInt64'}
         self.send(dumps(msg1))
         msg2 =  {'op': 'subscribe', 'topic': '/encoder2', 'type':'std_msgs/UInt64'}
         msg3={'op':'subscribe', 'topic':'/sonar1', 'type': 'sensor_msgs/Range'}
         msg4={'op':'subscribe', 'topic':'/sonar2', 'type': 'sensor_msgs/Range'}
         msg5={'op':'subscribe', 'topic':'/sonar3', 'type': 'sensor_msgs/Range'}
         msg6={'op':'subscribe', 'topic':'/sonar4', 'type': 'sensor_msgs/Range'} 
         msg7={'op':'subscribe', 'topic':'/sonar5', 'type': 'sensor_msgs/Range'}
         msg8={'op':'subscribe', 'topic':'/sonar6', 'type': 'sensor_msgs/Range'}  
         msg9={'op':'subscribe', 'topic':'/sonar7', 'type': 'sensor_msgs/Range'}
         msg10={'op':'subscribe', 'topic':'/sonar8', 'type': 'sensor_msgs/Range'}
         msg11={'op':'subscribe', 'topic':'/odom', 'type': 'nav_msgs/Odometry'}
         msg12={'op':'subscribe', 'topic':'/cmd_vel_mux/input/teleop', 'type': 'geometry_msgs/Twist'}
           
         self.send(dumps(msg2))
         self.send(dumps(msg3))
         self.send(dumps(msg4))
         self.send(dumps(msg5))
         self.send(dumps(msg6))
         self.send(dumps(msg7))
         self.send(dumps(msg8))
         self.send(dumps(msg9))
         self.send(dumps(msg10))
         self.send(dumps(msg11))
         self.send(dumps(msg12))
     
     def ros_publisher(self):
                 global odometry_x_
                 global odometry_y_
                 global odometry_yaw_
                 global right_encoder_prev
                 global left_encoder_prev 
                 global current_time
                 global data_publish_flag

		 ser.write('S')
		 print ser.inWaiting()
		 ser_data=''
		 
		 if ser.inWaiting()==27:
			 ser_data=ser.read(27)
			 data="hello"
			 #print type(data), len(data)
			 #print type(ser_data), len(ser_data)
			 encoder1_data=ord(ser_data[2])*255+ord(ser_data[3])*255+ord(ser_data[4])*255+ord(ser_data[5])
			 encoder2_data=ord(ser_data[6])*255+ord(ser_data[7])*255+ord(ser_data[8])*255+ord(ser_data[9])
			 #print 'raw'
                         #print encoder1_data
                         #print encoder2_data
                         encoder1='0x{0:08X}.format(encoder1_data)'
                         encoder2='0x{0:08X}.format(encoder2_data)'
                         signed_encoder1=~(0xffffffff - int(encoder1,16))+1
                         signed_encoder2=~(0xffffffff - int(encoder2,16))+1
                         print 'raw'
                         print signed_encoder1
                         print signed_encoder2
			 msg1 =  {'op': 'publish', 'topic': '/encoder1', 'msg':{'data' : encoder1_data}}
			 msg2 =  {'op': 'publish', 'topic': '/encoder2', 'msg':{'data' : encoder2_data}}
			 msg3 =  {'op': 'publish', 'topic': '/sonar1', 'msg':{'range': ord(ser_data[10])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar1'}}}
			 msg4 =  {'op': 'publish', 'topic': '/sonar2', 'msg':{'range': ord(ser_data[11])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar'}}}
			 msg5 =  {'op': 'publish', 'topic': '/sonar3', 'msg':{'range': ord(ser_data[12])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar3'}}}
			 msg6 =  {'op': 'publish', 'topic': '/sonar4', 'msg':{'range': ord(ser_data[13])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar4'}}}
			 msg7 =  {'op': 'publish', 'topic': '/sonar5', 'msg':{'range': ord(ser_data[14])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar5'}}}
			 msg8 =  {'op': 'publish', 'topic': '/sonar6', 'msg':{'range': ord(ser_data[15])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar6'}}}
			 msg9 =  {'op': 'publish', 'topic': '/sonar7', 'msg':{'range': ord(ser_data[16])/10.0, 'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar7'}}}
			 msg10=  {'op': 'publish', 'topic': '/sonar8', 'msg':{'range': ord(ser_data[17])/10.0,'radiation_type' : 0, 'field_of_view' : 0.1, 'min_range':0.05, 'max_range': 2.00,'header':{'frame_id':'sonar8'}}}
			 
			 
			 self.send(dumps(msg1))
			 self.send(dumps(msg2))
			 self.send(dumps(msg3))
			 self.send(dumps(msg4))
			 self.send(dumps(msg5))
			 self.send(dumps(msg6))
			 self.send(dumps(msg7))
			 self.send(dumps(msg8))
			 self.send(dumps(msg9))
			 self.send(dumps(msg10))
			 
                         last_x=odometry_x_
                         last_y=odometry_y_
                         last_yaw=odometry_yaw_
             
                         right_enc_dif=(encoder1_data-right_encoder_prev)*0.0008888
                         left_enc_dif=(encoder2_data-left_encoder_prev)*0.0008888
                         #print 'enc dif'
                         #print right_encoder_prev
                         #print encoder1_data
                         #print left_encoder_prev
                         #print encoder2_data
                         #print right_enc_dif
                         #print left_enc_dif
             
                         #calculate odometry
                         dist=(right_enc_dif+left_enc_dif)/2.0
                         ang=(right_enc_dif-left_enc_dif)/0.28
                         #print 'ang'
                         #print ang
                         #print dist
             
                         right_encoder_prev=encoder1_data
                         left_encoder_prev=encoder2_data
                         
                             
             
                         odometry_yaw_ = math.atan2(math.sin(odometry_yaw_+ang), math.cos(odometry_yaw_+ang))
                         odometry_x_=odometry_x_+dist*math.cos(odometry_yaw_)
                         odometry_y_=odometry_y_+dist*math.sin(odometry_yaw_)
                         #print 'odom'
                         #print odometry_x_
                         #print odometry_y_
                         #print odometry_yaw_
             
                         last_time=current_time
                         current_time=time.time()
                         #print current_time
                         #print 'odom'
                         
                         
             
                         dt=(current_time-last_time)
                         vel=dist/dt
                         vel_x=(odometry_x_-last_x)/dt
                         vel_y=(odometry_y_-last_y)/dt
                         vel_yaw=(odometry_yaw_-last_yaw)/dt
                         #print 'time'
                         #print (odometry_x_ - last_x)
                         #print dt
                         #print 'twist msgs'
                         #print vel
                         #print vel_x
                         #print vel_yaw             
                         orient=tf.quaternion_from_euler(0,0,odometry_yaw_)
                                                  
                         msg11=  {'op': 'publish', 'topic': '/odom', 'msg': {'pose': {'pose':{'position':{'x':odometry_x_, 'y':odometry_y_, 'z':0.0},'orientation': {'x':orient.item(1), 'y':orient.item(2), 'z':orient.item(3), 'w':orient.item(0) }}},'child_frame_id': 'base_link','twist' : {'twist':{'linear':{'x':vel_x, 'y':vel_y }, 'angular':{'z':vel_yaw} }},'header':{'frame_id':'odom'}}}
                         self.send(dumps(msg11))
                         I=transformations.identity_matrix()
                         #print I
			 
		 else:
			 ser.flushInput()
				 
		 #data="hello"
		 #print type(data), len(data)
		 #print type(ser_data), len(ser_data)
		 #msg =  {'op': 'publish', 'topic': '/rosbridge_example', 'msg':{'data' : data}}
		 #self.send(dumps(msg))
		 threading.Timer(0.08,self.ros_publisher).start()
		 
		 

     def opened(self):
         print "Connection opened..."
         self.get_loggers()
         self.ros_subscribe()
         self.ros_publisher()

     def closed(self, code, reason=None):
         print code, reason

     def received_message(self, m):
         json_encoded=m
         #print json_encoded
         #print type(TextMessage('%s' % json_encoded))
         if m.is_text:                                #decode json encoded value to string
           recvStr=m.data.decode("utf-8")
           #print recvStr
         ##print "receive", m
           data=loads(recvStr)                          #decode json string to python dict value
           #print data
           str_topic= data['topic']
           if(str_topic=='/cmd_vel_mux/input/teleop'):
              #print 'Twist msgs'
              #print data['msg']['linear']['x']
              #print data['msg']['angular']['z']
              x_cmd=data['msg']['linear']['x']
              z_cmd=data['msg']['angular']['z']
              x_cmd_to_FB=128-(128/0.6)*x_cmd
              z_cmd_yaw=z_cmd*0.28
              z_cmd_to_FB_R=128-(128/0.6)*z_cmd_yaw
              z_cmd_to_FB_L=128+(128/0.6)*z_cmd_yaw
              
              
              #print 'FB Cmds'
              ser.write('H')
              ser.write(chr(128))
              ser.write(chr(128))
              
              
              
              if (x_cmd!=0):
                 ser.write('H')
                 ser.write(chr(int(x_cmd_to_FB)))
                 ser.write(chr(int(x_cmd_to_FB)))
                 #print x_cmd_to_FB
              if (z_cmd!=0):
                 ser.write('H')
                 ser.write(chr(int(z_cmd_to_FB_R/10)))
                 ser.write(chr(int(z_cmd_to_FB_L/10)))
                 #print z_cmd_to_FB_R
                 #print z_cmd_to_FB_L
              
               
if __name__=="__main__":
     try: 
         ws = GetLoggersClient('ws://127.0.0.1:9090/')
         ws.connect()
         ws.run_forever()
         
     except KeyboardInterrupt:
         ws.close() 

