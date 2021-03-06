from xbee import XBee
from xbee.backend.base import TimeoutException
import sys
import serial
import time


class protocol():
    FIND = "FETCH"
    SYNCHRONIZE = "SYNC"
    QUERY = "QRY"
    VALUE = "VAL"
    SEPARATOR = ";"
    RSSI = "RSSI"
    SYNC_PROC = "SYNC_PROC"


if __name__ == "__main__":
    PORT = sys.argv[1]
    BAUD_RATE = 9600
    REQUESTS = int(sys.argv[2])

    # Open serial port
    ser = serial.Serial(PORT, BAUD_RATE)
    state = 0
    protocol = protocol()
    anchors = {}
    processors = {}
    xbee = XBee(ser)
    timeout = 0

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
                while int(round(time.time() * 1000)) - timeout < 1000:
                    # if ser.in_waiting:
                    # data = ser.readline()
                    data = None
                    try:
                        data = xbee.wait_read_frame(0.3)
                    except TimeoutException:
                        # print("Wait timeout")
                        data = None
                    if data:
                        print(data)
                        msg = data['rf_data']
                        if msg == protocol.SYNC_PROC:
                            addr = data['source_addr']
                            if addr not in anchors:
                                print("PROCESSOR ADDED")
                                processors[addr] = 0
                        elif msg == protocol.SYNCHRONIZE:
                            addr = data['source_addr']
                            if addr not in anchors:
                                print("ANCHOR ADDED")
                                anchors[addr] = 0

                print("SYNC TIMEOUT")
                if len(anchors) > 0:
                    state += 1
                    timeout = int(round(time.time() * 1000))
            elif state == 1:
                if int(round(time.time() * 1000)) - timeout < 10000:
                    for anch in anchors:
                        msg = protocol.QUERY + protocol.SEPARATOR + str(REQUESTS)
                        xbee.send("tx", frame='A', dest_addr=anch, data=msg)
                        anchors[anch] = 0
                        received = 0
                        for i in range(REQUESTS):
                            try:
                                data = xbee.wait_read_frame(0.3)
                            except TimeoutException:
                                print("REQUEST TIMEOUT")
                                continue
                            print(data)
                            received += 1
                            cmd = data['rf_data']
                            if cmd == protocol.VALUE:
                                addr = data['source_addr']
                                anchors[addr] += ord(data['rssi'])
                        if anchors[anch] > 0:
                            anchors[anch] /= received
                        print(anchors[anch])
                    for proc in processors:
                        xbee.send("tx", frame='A', dest_addr=proc, data=(protocol.RSSI+protocol.SEPARATOR+str(anchors)))
                else:
                    state = 0
                    anchors = {}
                    processors = {}
        except KeyboardInterrupt:
            break
        except serial.SerialTimeoutException:
            print(serial.SerialTimeoutException.errno)
            break
    print("Anchors Found: " + str(anchors))
    ser.close()
