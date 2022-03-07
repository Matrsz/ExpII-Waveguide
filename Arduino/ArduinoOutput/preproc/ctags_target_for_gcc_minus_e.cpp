# 1 "/home/inox/Documents/IB/4to Nivel/Experimental II/Guia de Ondas/Arduino/motor_completo_v3_/motor_completo_v3_.ino"
const int leftEnd = 2; // the number of the pushbutton pin
const int rightEnd = 3; // the number of the pushbutton pin
const int ledPin = 13; // the number of the LED pin
const int enable = 6;
const int step = 5;
const int dir = 4;

int J;
// Variables will change:
int ledState = 0x0; // the current state of the output pin
int leftState; // the current rightRead from the input pin
int lastLeftState = 0x1; // the previous rightRead from the input pin
int rightState; // the current rightRead from the input pin
int lastRightState = 0x1; // the previous rightRead from the input pin
// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 0; // the last time the output pin was toggled
long debounceDelay = 50; // the debounce time; increase if the output flickers
char receivedChar;
boolean newData = false;

void setup() {
  pinMode(leftEnd, 0x2);
  pinMode(rightEnd, 0x2);
  pinMode(ledPin, 0x1);
  pinMode(enable, 0x1); // Enable
  pinMode(step, 0x1); // Step
  pinMode(dir, 0x1); // Dir
  digitalWrite(enable, 0x0); // Set Enable low
  J = 2000;
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  digitalWrite(ledPin, ledState);
}

void loop() {
  int rightRead = digitalRead(rightEnd);
  int leftRead = digitalRead(leftEnd);
  if (rightRead != lastRightState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (rightRead != rightState) {
      rightState = rightRead;
      while (rightState == 0x0) {
        recvOneChar();
        if (newData == true && receivedChar == 's') {
          showNewData();
        // espera hasta que recive una a
        arrch:
          recvOneChar();
          while (newData != true)
            recvOneChar();
          if (receivedChar == 'a') { } // continua 
          else {
            goto arrch;
          }
          //                    delay(J);
        }
        ledState = 0x1;
        digitalWrite(4, 0x1);
        int leftRead = digitalRead(leftEnd);
        digitalWrite(5, 0x1); // Output high
        delayMicroseconds(1000); // Wait 1/2 a ms
        digitalWrite(5, 0x0); // Output low
        delayMicroseconds(1000); // Wait 1/2 a ms
        if (leftRead == 0x0) {
          Serial.println("R");
          break;
        }
      }
      digitalWrite(4, 0x0);
    }
  }
  if (leftRead != lastLeftState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (leftRead != leftState) {
      leftState = leftRead;

      while (leftState == 0x0) {
        recvOneChar();
        if (newData == true && receivedChar == 's') {
          showNewData();
        // espera hasta que recive una a
        // espera hasta que recive una a
        arrci:
          recvOneChar();
          while (newData != true)
            recvOneChar();
          if (receivedChar == 'a') {} // continua
          else {
            goto arrch;
          }
          recvOneChar();
          while (newData != true)
            recvOneChar();
          if (receivedChar == 'a') {} // continua
          else {
            goto arrci;
          }
          // delay(J);
        }
        ledState = 0x0;
        int rightRead = digitalRead(rightEnd);
        digitalWrite(4, 0x0);
        int leftRead = digitalRead(leftEnd);
        digitalWrite(5, 0x1); // Output high
        delayMicroseconds(1000); // Wait 1/2 a ms
        digitalWrite(5, 0x0); // Output low
        delayMicroseconds(1000); // Wait 1/2 a ms
        if (rightRead == 0x0) {
          Serial.println("L");
          break;
        }
      }
      digitalWrite(4, 0x1);
    }
  }
  digitalWrite(ledPin, ledState);
  lastRightState = rightRead;
  lastLeftState = leftRead;
}

void recvOneChar() {
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    newData = true;
  }
}

void showNewData() {
  if (newData == true) {
    Serial.print("This just in ... ");
    Serial.println(receivedChar);
    newData = false;
  }
}
