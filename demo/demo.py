from serial import Serial

arduino = Serial(port='/dev/tty.usbmodem14101', baudrate=28800, timeout=.1)

