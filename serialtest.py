import serial

# Configure the serial port
ser = serial.Serial('COM3', 9600)  # Replace 'COM1' with your serial port
ser.close()
ser.open()

def write_to_serial(command):
    # Output the string "tko\n"
    utf = command.decode('utf-8')
    ser.write(utf)
    # Close the serial port

write_to_serial(b'tko\n')