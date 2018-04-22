#include <Arduino.h>
#include <Xbee.h>

const String FIND="FETCH";
const String SYNCHRONIZE="SYNC";
const String QUERY="QRY";
const String VALUE="VAL";
const String SEPARATOR=";";

XBee xbee = XBee();

// allocate two bytes for to hold a 10-bit analog reading
//uint8_t payload[];

Rx16Response rx16 = Rx16Response();
Rx64Response rx64 = Rx64Response();

void processCommand(uint8_t data[], uint8_t dataLength){
  String command = "";
  for (int i = 0; i < dataLength; i++) {
    command+= String(data[i]);
  }
  if(command.startsWith(FIND)){
    uint8_t payload[sizeof(SYNCHRONIZE)];
    for (uint8_t i = 0; i < sizeof(SYNCHRONIZE); i++) {
      payload[i] = (uint8_t) SYNCHRONIZE.charAt(i);
    }
    Tx16Request  tx = Tx16Request (0x0, payload, sizeof(payload));
    xbee.send(tx);
  }else if(command.startsWith(QUERY)){
      command.replace((QUERY+SEPARATOR), "");
      int reqs = command.toInt();
      uint8_t payload[sizeof(VALUE)];
      for (uint8_t i = 0; i < sizeof(VALUE); i++) {
        payload[i] = (uint8_t) VALUE.charAt(i);
      }
      Tx16Request  tx = Tx16Request (0x0, payload, sizeof(payload));
      while(reqs-->0){
        xbee.send(tx);
      }
  }
}

void setup() {
  Serial.begin(9600);
  xbee.setSerial(Serial);
}

void loop() {
    xbee.readPacket();
    if (xbee.getResponse().isAvailable()) {
        // got something
      if (xbee.getResponse().getApiId() == RX_16_RESPONSE || xbee.getResponse().getApiId() == RX_64_RESPONSE) {
          // got a rx packet
          if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
                  xbee.getResponse().getRx16Response(rx16);
                  processCommand(rx16.getData(), rx16.getDataLength());
          }else {
                xbee.getResponse().getRx64Response(rx64);
        	      processCommand(rx64.getData(), rx64.getDataLength());
        }
      }
    } else if (xbee.getResponse().isError()) {
        xbee.getResponse().getErrorCode();
    }
}
