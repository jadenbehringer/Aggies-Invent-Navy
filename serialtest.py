import serial

# Configure the serial port
ser = serial.Serial('COM3', 9600)  # Replace 'COM1' with your serial port

# Output the string "tko\n"
ser.write(b'tko\n')

# Close the serial port
ser.close()

