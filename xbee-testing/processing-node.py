from xbee import XBee
import sys
import serial
import socket
import ast


class protocol():
    FIND = "FETCH"
    RSSI = "RSSI"
    SYNC_PROC = "SYNC_PROC"
    SEPARATOR = ";"


if __name__ == "__main__":
    PORT = sys.argv[1]
    BAUD_RATE = 9600
    HOST = 'localhost'
    PROC_PORT = int(sys.argv[2])

    ser = serial.Serial(PORT, BAUD_RATE)
    xbee = XBee(ser)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PROC_PORT))
    sock.listen(1)

    conn, PROC_IP = sock.accept()
    print("PROCESSOR CONNECTED")

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
                              data=protocol.SYNC_PROC)
                elif msg.startswith(protocol.RSSI):
                    msg = msg.replace(protocol.RSSI + protocol.SEPARATOR, "")
                    rssi_values = ast.literal_eval(msg)
                    print(rssi_values)
                    for anchors in rssi_values:
                        rssi = rssi_values[anchors]
                        cod = map(ord, anchors)
                        id = cod[0] * 256 + cod[1]
                        try:
                            conn.send(str(id)+protocol.SEPARATOR+str(rssi))
                            print("DATA SENT")
                        except socket.error:
                            print("PROC CONNECTION ERROR")
                            conn, PROC_IP = sock.accept()
                            break
        except KeyboardInterrupt:
            break
        except serial.SerialTimeoutException:
            print(serial.SerialTimeoutException.errno)
            break
        # except:
        # print("An unexpected error occurred")
        # break
    ser.close()
    conn.close()
    sock.close()
