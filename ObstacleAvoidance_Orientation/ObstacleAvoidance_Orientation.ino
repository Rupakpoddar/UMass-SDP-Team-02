#include <Wire.h>
#include <SoftwareSerial.h>
#include "SparkFun_VCNL4040_Arduino_Library.h"
#include <SparkFun_I2C_Mux_Arduino_Library.h>

QWIICMUX myMux;
VCNL4040 proximitySensor;
int ports[4] = {0, 3, 4, 7};
unsigned int proxValue1, proxValue2, proxValue3, proxValue4;
int values[4] = {proxValue1, proxValue2, proxValue3, proxValue4};
String readString;
String lastCommand;
String command;

SoftwareSerial BluetoothModule (2, 3);  // Rx, Tx
SoftwareSerial CustomPCB (4, 5);  // Rx, Tx

void setup() {
  Serial.begin(9600);
  CustomPCB.begin(9600);
  myMux.begin(9600); 
  BluetoothModule.begin(9600);
  Wire.begin(9600);

  if (myMux.begin() == false)
  {
    Serial.println("Mux not detected. Freezing...");
    while (1);
  }
}

void loop() {
  while (BluetoothModule.available()) {
  delay(3); 
  char c = BluetoothModule.read();
  readString += c; 
  }

  if (readString.length() >0) {
    Serial.println(readString);
    CustomPCB.print(readString.c_str());
    lastCommand = readString;

    if (lastCommand != "s"){
      command = lastCommand.substring(3);
    }
  }

  readString = "";

  for (int i=0; i<4; i++){
    myMux.setPort(ports[i]);
    if (proximitySensor.begin() == false)
    {
      Serial.println("Device not found. Please check wiring.");
      while (1); //Freeze!
    }

    values[i] = proximitySensor.getProximity();
    // Serial.print(String(values[i]) + "\t");
  }

  if (command == "f") 
  {
    if (values[0] > 30){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
  if (command == "b") 
  {
    if (values[2] > 30){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
  if (command == "l") 
  {
    if (values[1] > 30){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
  if (command == "r") 
  {
    if (values[3] > 30){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
}
