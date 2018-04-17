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
    PORT = 'COM14'
    BAUD_RATE = 9600

    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE)

    # Continuously read and print packets

    while True:
        try:
            data = ser.readline()
            if data:
                data = str(data, 'utf8')
                print(data)
                if data.startswith(protocol.FIND):
                    #print("READY TO SYNC")
                    ser.write(b'+++')
                    time.sleep(2)
                    ser.write(b'ATDB')
                    rssi = ser.read()
                    ser.write(b'ATCN')
                    print(rssi)
                    time.sleep(1)
                    ser.write(bytes(protocol.SYNCHRONIZE + protocol.SEPARATOR + "0" + protocol.END_COMMAND, 'utf-8'))
        except KeyboardInterrupt:
            break
        except serial.SerialTimeoutException:
            print(serial.SerialTimeoutException.errno)
            break
        # except:
        # print("An unexpected error occurred")
        # break
    ser.close()
