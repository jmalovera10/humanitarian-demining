from xbee import XBee
import serial
import time


class protocol():
    FIND = "FETCH"
    SYNCHRONIZE = "SYNC"
    QUERY = "QRY"
    RSSI = "RSSI"
    VALUES = "VALS"
    VALUE = "VAL"
    SEPARATOR = ";"
    END_COMMAND = "\n"


if __name__ == "__main__":
    PORT = 'COM13'
    BAUD_RATE = 9600

    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE)
    state = 0
    protocol = protocol()
    anchors = {}

    # Continuously read and print packets
    while True:
        try:
            if state == 0:
                msg = bytes(protocol.FIND + protocol.END_COMMAND, 'utf-8')
                # print(msg)
                ser.write(msg)
                timeout = int(round(time.time() * 1000))
                while int(round(time.time() * 1000)) - timeout < 500:
                    if ser.in_waiting:
                        data = ser.readline()
                        if data:
                            data = data.replace(b'\n', b'')
                            data = str(data, 'utf8')
                            if data.startswith(protocol.SYNCHRONIZE):
                                print("ADDING")
                                params = data.split(protocol.SEPARATOR)
                                anchors[params[1]] = 0
                if len(anchors) > 0:
                    state += 1
            elif state == 1:
                print("State change")
                break

        except KeyboardInterrupt:
            break
        except serial.SerialTimeoutException:
            print(serial.SerialTimeoutException.errno)
            break
    print(anchors)
    ser.close()
