# FinalProjectMay2026

# Title: Mqtt2Excel
# Description: The goal is to create a python app which will subscribe to an mqtt broker, and enter the received message to an excel 
#              spreadsheet along with a time stamp.

# Installation Instructions: Use the terminal to install the paho-mqtt library and xlwings. You will also need Excel installed. 

# Feature List: The program creates a spreadsheet in the project folder, and stores data to the next available blank row. It's handy for    #               storing received data for later review and charting.
#
# pip install paho-mqtt
# pip install xlwings
# be sure to have Microsoft Excel installed as well


# Usage Guide: Before running the program, you should edit the topics in the python program. In the code found here, I used topic names which are from data being published by an ESP32 in my laundry room. I used broker.hivemq.com 
