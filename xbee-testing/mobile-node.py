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
    xbee = XBee(ser)

    # Continuously read and print packets
    while True:
        try:
            if state == 0:
                # msg = bytes(protocol.FIND + protocol.END_COMMAND, 'utf-8')
                # print(msg)
                # ser.write(msg)
                msg = protocol.FIND
                xbee.send("tx", frame='A', dest_addr='\xFF\xFF', data=msg)
                timeout = int(round(time.time() * 1000))
                while int(round(time.time() * 1000)) - timeout < 1500:
                    # if ser.in_waiting:
                    # data = ser.readline()
                    data = None
                    try:
                        data = xbee.wait_read_frame(0.3)
                    except:
                        # print("Wait timeout")
                        data = None
                    if data:
                        print(data)
                        msg = data['rf_data']
                        if msg.startswith(protocol.SYNCHRONIZE):
                            addr = data['source_addr']
                            if addr not in anchors:
                                print("ADDING")
                                anchors[addr] = 0
                print("SYNC timeout")
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
