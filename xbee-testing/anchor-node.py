from xbee import XBee
import serial


class protocol():
    FIND = "FETCH"
    SYNCHRONIZE = "SYNC"
    QUERY = "QRY"
    VALUE = "VAL"
    SEPARATOR = ";"


if __name__ == "__main__":
    PORT = 'COM10'
    BAUD_RATE = 9600

    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE)
    xbee = XBee(ser)

    # Continuously read and print packets

    while True:
        try:
            # data = ser.readline()
            data = xbee.wait_read_frame()
            print("arrived")
            if data:
                # data = str(data, 'utf8')
                print(data)
                msg = data['rf_data']
                if msg.startswith(protocol.FIND):
                    # print("READY TO SYNC")
                    rssi = hex(ord(data['rssi']))
                    print(rssi)
                    # ser.write(bytes(protocol.SYNCHRONIZE + protocol.SEPARATOR + "0" + protocol.END_COMMAND, 'utf-8'))
                    xbee.send("tx", frame='B', dest_addr='\x00\x00',
                              data=protocol.SYNCHRONIZE)
                elif msg.startswith(protocol.QUERY):
                    requests = int(msg.split(protocol.SEPARATOR)[1])
                    for i in range(requests):
                        xbee.send("tx", frame='C', dest_addr='\x00\x00',
                                  data=protocol.VALUE)
        except KeyboardInterrupt:
            break
        except serial.SerialTimeoutException:
            print(serial.SerialTimeoutException.errno)
            break
        # except:
        # print("An unexpected error occurred")
        # break
    ser.close()
