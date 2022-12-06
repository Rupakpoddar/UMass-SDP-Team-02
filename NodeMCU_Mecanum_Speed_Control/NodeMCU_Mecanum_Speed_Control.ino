//Written By Rupak Poddar
//www.youtube.com/RupakPoddar

int a1 = 5;
int a2 = 4;
int b1 = 10;
int b2 = 2;
int c1 = 14;
int c2 = 12;
int d1 = 13;
int d2 = 15;

String readString;

void setup() {
  Serial.begin(9600);

  analogWrite(a1, 0);
  analogWrite(a2, 0);
  analogWrite(b1, 0);
  analogWrite(b2, 0);
  analogWrite(c1, 0);
  analogWrite(c2, 0);
  analogWrite(d1, 0);
  analogWrite(d2, 0);
}

void loop() {
  while (Serial.available()) {
  delay(3); 
  char c = Serial.read();
  readString += c; 
  }
  if (readString.length() >0) {
  // Serial.println(readString);
    if (readString == "s")
  {
    analogWrite(a1, 0);
    analogWrite(a2, 0);
    analogWrite(b1, 0);
    analogWrite(b2, 0);
    analogWrite(c1, 0);
    analogWrite(c2, 0);
    analogWrite(d1, 0);
    analogWrite(d2, 0);
    Serial.println("Command: s");
    Serial.println();
  }
  else {
    String speedStr = readString.substring(0, 3);
    String command = readString.substring(3);
    Serial.println("Speed: " + speedStr);
    Serial.println("Command: " + command);
    Serial.println();
    int speed = speedStr.toInt();

    if (command == "f") 
    {
      analogWrite(a1, speed);
      analogWrite(b1, speed);
      analogWrite(c1, speed);
      analogWrite(d1, speed);
    }
    if (command == "b")
    {
      analogWrite(a2, speed);
      analogWrite(b2, speed);
      analogWrite(c2, speed);
      analogWrite(d2, speed);
    }
    if (command == "aw")
    {
      analogWrite(a2, speed);
      analogWrite(c2, speed);
      analogWrite(b1, speed);
      analogWrite(d1, speed);
    }
    if (command == "cw")
    {
      analogWrite(a1, speed);
      analogWrite(c1, speed);
      analogWrite(b2, speed);
      analogWrite(d2, speed);
    }
    if (command == "l")
    {
      analogWrite(b1, speed);
      analogWrite(d2, speed);
      analogWrite(a2, speed);
      analogWrite(c1, speed);
    }
    if (command == "r")
    {
      analogWrite(b2, speed);
      analogWrite(d1, speed);
      analogWrite(a1, speed);
      analogWrite(c2, speed);
    }
    if (command == "fl"){}
    if (command == "bl"){}
    if (command == "fr"){}
    if (command == "br"){}
  }

  readString="";
  } 
}
