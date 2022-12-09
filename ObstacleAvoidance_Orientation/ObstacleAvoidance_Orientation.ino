#include <Wire.h>
#include <SoftwareSerial.h>
#include "SparkFun_VCNL4040_Arduino_Library.h"
#include <SparkFun_I2C_Mux_Arduino_Library.h>

QWIICMUX myMux;
VCNL4040 proximitySensor;
int ports[5] = {0, 2, 3, 4, 7};
unsigned int proxValue1, proxValue2, proxValue3, proxValue4, proxValue5;
int values[5] = {proxValue1, proxValue2, proxValue3, proxValue4, proxValue5};
String readString;
String lastCommand;
String command;
int val3low;
int val3high;
int val4low;
int val4high;

SoftwareSerial BluetoothModule (2, 3);  // Rx, Tx
SoftwareSerial CustomPCB (4, 5);  // Rx, Tx

void setup() {
  Serial.begin(9600);
  CustomPCB.begin(9600);
  myMux.begin(9600); 
  BluetoothModule.begin(9600);
  Wire.begin(9600);
  pinMode(13, OUTPUT);

  if (myMux.begin() == false)
  {
    Serial.println("Mux not detected. Freezing...");
    while (1);
  }
}

void loop() {
  while (BluetoothModule.available() > 0) {
  delay(3); 
  char c = BluetoothModule.read();
  readString += c; 
  }

  if (readString.length() > 0) {
    Serial.println(readString);
    CustomPCB.print(readString.c_str());
    lastCommand = readString;
  }

  if (lastCommand != "s"){
      command = lastCommand.substring(3);
      if ((command == "fr") || (command == "fl") || (command == "br") || (command == "bl")) {
        autoOrient();
      }
      else {
        obstacleAvoidance();
      }
    }

  readString = "";
}

void obstacleAvoidance() {
  for (int i=0; i<5; i++){
    myMux.setPort(ports[i]);
    if (proximitySensor.begin() == false)
    {
      Serial.print("Device not found at port ");
      Serial.print(ports[i]);
      Serial.println(". Please check wiring.");
      CustomPCB.print("s");
      while (1) {
        digitalWrite(13, HIGH);
        delay(100);
        digitalWrite(13, LOW);
        delay(100);
      }
    }

    values[i] = proximitySensor.getProximity();
    // Serial.print(String(values[i]) + "\t");
  }

  if (command == "f") 
  {
    if (values[1] > 30){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
  // if (command == "b") 
  // {
  //   if (values[?] > 30){
  //     Serial.println("s");
  //     CustomPCB.print("s");
  //     command = "";
  //   }
  // }
  if (command == "l") 
  {
    if ((values[3] > 20) || (values[4] > 20)){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
  if (command == "r") 
  {
    if ((values[0] > 20) || (values[2] > 20)){
      Serial.println("s");
      CustomPCB.print("s");
      command = "";
    }
  }
}

void autoOrient() {
  autoOrientHelper();
  if(values[4] < val3low){
    delay(100);
    CustomPCB.print("030cw");
  }
  if(values[4] > val3high){
    delay(100);
    CustomPCB.print("030aw");
  }
  while((values[4] < val3low) || (values[4] > val3high)) {
    Serial.println(String(val3low)+ "\t" + String(values[4]) + "\t" + String(val3high));
    autoOrientHelper();
  }
  delay(100);
  CustomPCB.print("s");
}

void autoOrientHelper() {
  myMux.setPort(ports[3]);
  values[3] = proximitySensor.getProximity();
  val3low = values[3] - (values[3]*0.1);
  val3high = values[3] + (values[3]*0.1);
  // Serial.print(String(values[3]) + "\t");
  myMux.setPort(ports[4]);
  values[4] = proximitySensor.getProximity();
  val4low = values[4] - (values[4]*0.1);
  val4high = values[4] + (values[4]*0.1);
  // Serial.println(String(values[4]));
}
