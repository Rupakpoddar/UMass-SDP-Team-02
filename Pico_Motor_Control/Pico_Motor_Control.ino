//Written By Rupak Poddar

int M1A = 2;
int M1B = 3;
int M2A = 4;
int M2B = 5;
int M3A = 6;
int M3B = 7;
int M4A = 8;
int M4B = 9;

String readString;

void setup() {
  Serial.begin(9600);

  analogWrite(M1A, 0);
  analogWrite(M1B, 0);
  analogWrite(M2A, 0);
  analogWrite(M2B, 0);
  analogWrite(M3A, 0);
  analogWrite(M3B, 0);
  analogWrite(M4A, 0);
  analogWrite(M4B, 0);
}

void loop() {
  while (Serial.available()) {
  delay(3); 
  char c = Serial.read();
  readString += c; 
  }
  if (readString.length() >0) {
  // Serial.println(readString);
   
  String speedStr = readString.substring(0, 3);
  String command = readString.substring(3, 4);
  Serial.println("Speed: " + speedStr);
  Serial.println("Command: " + command);
  Serial.println();
  int speed = speedStr.toInt();

  if (command == "f") 
  {
    analogWrite(M1A, speed);
    analogWrite(M2A, speed);
    analogWrite(M3A, speed);
    analogWrite(M4A, speed);
  }
  if (command == "b")
  {
    analogWrite(M1B, speed);
    analogWrite(M2B, speed);
    analogWrite(M3B, speed);
    analogWrite(M4B, speed);
  }
  if (command == "l")
  {
    analogWrite(M1B, speed);
    analogWrite(M2A, speed);
    analogWrite(M3B, speed);
    analogWrite(M4A, speed);
  }
  if (command == "r")
  {
    analogWrite(M1A, speed);
    analogWrite(M2B, speed);
    analogWrite(M3A, speed);
    analogWrite(M4B, speed);
  }
  if (command == "k")
  {
    analogWrite(M1B, speed);
    analogWrite(M2A, speed);
    analogWrite(M3A, speed);
    analogWrite(M4B, speed);
  }
  if (command == "l")
  {
    analogWrite(M1A, speed);
    analogWrite(M2B, speed);
    analogWrite(M3B, speed);
    analogWrite(M4A, speed);
  }
  if (command == "s")
  {
    analogWrite(M1A, 0);
    analogWrite(M1B, 0);
    analogWrite(M2A, 0);
    analogWrite(M2B, 0);
    analogWrite(M3A, 0);
    analogWrite(M3B, 0);
    analogWrite(M4A, 0);
    analogWrite(M4B, 0);
  }

  readString="";
  } 
}
