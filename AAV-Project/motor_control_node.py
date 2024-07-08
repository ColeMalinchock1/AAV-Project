#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

import serial
import threading
import curses
import time

# Initializes the global variables
manual_throttle = manual_steer = auto_throttle = auto_steer = mode = received = 0

# Initializes the received message
last_response = received_message = "No Response"

last_time_received = time.time()

# Intializes the terminal screen
stdscr = curses.initscr()

def manual_throttle_callback(msg):
    """Callback for manual throttle to control the DC motors of the vessel.
    msg:
    Type: Int64
    Range: [-500, 500]"""

    global manual_throttle

    manual_throttle = msg.data

def manual_steer_callback(msg):
    """Callback for manual steer to control the servo motors of the vessel.
    msg:
    Type: Int64
    Range: [-90, 90]"""
    
    global manual_steer

    manual_steer = msg.data

def auto_throttle_callback(msg):
    """Callback for autonomous throttle to control the DC motors of the vessel.
    msg:
    Type: Int64
    Range: [-500, 500]"""
    
    global auto_throttle

    auto_throttle = msg.data

def auto_steer_callback(msg):
    """Callback for the autonomous steer to control the servo motors of the vessel.
    msg:
    Type: Int64
    Range: [-90, 90]"""
    
    global auto_steer

    auto_steer = msg.data

def mode_control_topic(msg):
    """Callback for the mode of the boat as either autonomous or manual.
    msg:
    Type: Int64
    Range: [0, 1]"""

    global mode

    mode = msg.data

def serial_send(ser, throttle, steer):
    """Transmits the throttle and steer commands to the Arduino via serial communication
    ser:
    Type: Serial
    Baudrate: 115200
    Port: /dev/ttyUSB0
    
    throttle:
    Type: Int64
    Range: [1000, 2000]
    
    steer:
    Type: Int64
    Range: [0, 180]"""

    # Setting up the command with the throttle and steer comma separated
    command = f'{throttle},{steer}\n'

    # Sending the command encoded
    ser.write(command.encode())

def serial_receive(ser):
    """Receives messages from serial communication"""

    global last_time_received, last_response

    # Checking if there are messages waiting to be received
    # Else if it has been less than 2 second
    # Else returns no response
    if ser.in_waiting > 0:
        # Reads the response, not currently needed
        response = ser.readline().decode().strip()

        last_time_received = time.time()

        last_response = response

        return response
    elif time.time() - last_time_received < 5:
        return last_response
    else:
        return "No response"


def main(args=None):
    """Main method for running the ROS2 node"""

    global manual_throttle, manual_steer, auto_throttle, auto_steer, mode, received_message

    rclpy.init(args=args)
    node = Node("motor_control_node")
    
    # List of subscriptions
    sub_manual_throttle = node.create_subscription(Int64, "manual_throttle_topic", manual_throttle_callback, 1)
    sub_manual_steer = node.create_subscription(Int64, "manual_steer_topic", manual_steer_callback, 1)
    sub_mode_control = node.create_subscription(Int64, "mode_control_topic", mode_control_topic, 1)
    sub_auto_throttle = node.create_subscription(Int64, "auto_throttle_topic", auto_throttle_callback, 1)
    sub_auto_steer = node.create_subscription(Int64, "auto_steer_topic", auto_steer_callback, 1)

    thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
    thread.start()

    rate = node.create_rate(20, node.get_clock())

    # Initializes connected
    connected = False

    # Repeats display until serial is connected
    while not connected:
        try:
            ser = serial.Serial('/dev/ttyACM0', 115200)
            connected = True
        except:
            stdscr.refresh()

            stdscr.addstr(1 , 5 , 'MOTOR CONTROL NODE')

            stdscr.addstr(3, 5, 'Not Connected')    


    while rclpy.ok():
        
        # Checks if it is in mode 0 (manual) or mode 1 (auto)
        if mode == 0:
            throttle = manual_throttle
            throttle = 50
            steer = manual_steer
            str_mode = "Manual"
        elif mode == 1:
            throttle = auto_throttle
            steer = auto_steer
            str_mode = "Auto"

        # Converts the throttle to the correct pwm value
        # 1000 = full reverse, 1500 = stop, 2000 = full forward
        pwm_throttle = throttle + 1500

        # Converts the steering to the correct servo value
        # 0 = left, 90 = straight, 180 = right
        servo_steer = steer + 90

        # Checks if the serial was received and then sends throttle and steer
        received_message = serial_receive(ser)
        serial_send(ser, pwm_throttle, servo_steer)

        # Display of all the important messages
        stdscr.refresh()
        stdscr.addstr(1 , 5 , 'MOTOR CONTROL NODE')

        stdscr.addstr(3, 5, 'Mode: %s                 ' % str_mode)

        stdscr.addstr(5, 5, 'Manual Throttle: %d                 ' % manual_throttle)
        stdscr.addstr(6, 5, 'Manual Steer: %d                 ' % manual_steer)

        stdscr.addstr(8, 5, 'Auto Throttle: %d                 ' % auto_throttle)
        stdscr.addstr(9, 5, 'Auto Steer: %d                 ' % auto_steer)

        stdscr.addstr(11, 5, 'Received Message: %s                 ' % received_message)

        rate.sleep()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()