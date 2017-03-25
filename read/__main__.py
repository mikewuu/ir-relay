#!/usr/bin/python

import weaver
import reader
import atexit
import time
import socket
import RPi.GPIO as GPIO

def main():

	# Initialize GPIO for LED
	GPIO.setmode(GPIO.BOARD)
	# BOARD 16 = BCM 23
	GPIO.setup(16, GPIO.OUT)

	# when started
	start_time = time.time()

	print('Fetching proxy address...')
	# get weaver address
	proxyAddress = weaver.fetchProxyAddress().split('://')[1].split(':')
	TCP_IP = proxyAddress[0]
	TCP_PORT = int(proxyAddress[1])
	# Try to connect to server
	print('Connecting to socket @ ' + proxyAddress[0] + ':' + proxyAddress[1])
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	print('Waiting for signal...')
	# Turn LED ON
	GPIO.output(16, GPIO.HIGH)
	# Close socket on exit
	def closeSocket():
		s.close()
	atexit.register(closeSocket)
	# Start reading signals
	while True:

		# if program has been running for more than 25 mins
		if int(time.time() - start_time) > 1500:
			break

		binaryCode = reader.read()
		if binaryCode:
			# Flash LED
			GPIO.output(16, GPIO.LOW)
			GPIO.output(16, GPIO.HIGH)
			GPIO.output(16, GPIO.LOW)
			# Send to server
			print('sent: ' + binaryCode)
			s.send(binaryCode)
			# Turn LED back on - ready for new signal
			GPIO.output(16, GPIO.HIGH)

	# Close socket
	print('Timeout! Cleaning up and restarting...')
	closeSocket()
	# delay to let socket terminate
	# time.sleep(180)
	# restart
	main()

if __name__ == "__main__":
	main()