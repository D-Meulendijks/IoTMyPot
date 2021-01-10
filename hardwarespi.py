#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys

CLK = 29
MISO = 31
MOSI = 33
CS = 35


def setupSpiPins(clkPin, misoPin, mosiPin, csPin):
    ''' Set all pins as an output except MISO (Master Input, Slave Output)'''
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(misoPin, GPIO.IN)
    GPIO.setup(mosiPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)


def readAdc(channel, clkPin, misoPin, mosiPin, csPin):
    if (channel < 0) or (channel > 7):
        print("Invalid ADC Channel number, must be between [0,7]")
        return -1

    # Datasheet says chip select must be pulled high between conversions
    GPIO.output(csPin, GPIO.HIGH)

    # Start the read with both clock and chip select low
    GPIO.output(csPin, GPIO.LOW)
    GPIO.output(clkPin, GPIO.HIGH)

    # read command is:
    # start bit = 1
    # single-ended comparison = 1 (vs. pseudo-differential)
    # channel num bit 2
    # channel num bit 1
    # channel num bit 0 (LSB)
    read_command = 0x18
    read_command |= channel

    sendBits(read_command, 5, clkPin, mosiPin)

    adcValue = recvBits(12, clkPin, misoPin)

    # Set chip select high to end the read
    GPIO.output(csPin, GPIO.HIGH)

    return adcValue


def sendBits(data, numBits, clkPin, mosiPin):
    ''' Sends 1 Byte or less of data'''

    data <<= (8 - numBits)

    for bit in range(numBits):
        # Set RPi's output bit high or low depending on highest bit of data field
        if data & 0x80:
            GPIO.output(mosiPin, GPIO.HIGH)
        else:
            GPIO.output(mosiPin, GPIO.LOW)

        # Advance data to the next bit
        data <<= 1

        # Pulse the clock pin HIGH then immediately low
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)


def recvBits(numBits, clkPin, misoPin):
    '''Receives arbitrary number of bits'''
    retVal = 0

    for bit in range(numBits):
        # Pulse clock pin
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)

        # Read 1 data bit in
        if GPIO.input(misoPin):
            retVal |= 0x1

        # Advance input to next bit
        retVal <<= 1

    # Divide by two to drop the NULL bit
    return (retVal / 2)


def setup_spi(clk_input = 21, miso_input = 20, mosi_input = 16, cs_input = 19):
    global CLK
    global MISO
    global MOSI
    global CS
    CLK = clk_input
    MISO = miso_input
    MOSI = mosi_input
    CS = cs_input
    try:
        GPIO.setmode(GPIO.BCM)
        setupSpiPins(CLK, MISO, MOSI, CS)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)


def read_spi(pin):
    return readAdc(pin, CLK, MISO, MOSI, CS)


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        setupSpiPins(CLK, MISO, MOSI, CS)

        while True:
            val1 = readAdc(0, CLK, MISO, MOSI, CS)
            val2 = readAdc(1, CLK, MISO, MOSI, CS)
            val3 = readAdc(2, CLK, MISO, MOSI, CS)
            val4 = readAdc(3, CLK, MISO, MOSI, CS)
            val5 = readAdc(4, CLK, MISO, MOSI, CS)
            val6 = readAdc(5, CLK, MISO, MOSI, CS)
            val7 = readAdc(6, CLK, MISO, MOSI, CS)
            val8 = readAdc(7, CLK, MISO, MOSI, CS)
            print(f"LDR 1: {val7:7}, LDR 2: {val3:7}, LDR 3: {val5:7}, Moisture sensor: {val1:7}")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)