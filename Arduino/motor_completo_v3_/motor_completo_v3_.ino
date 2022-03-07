const int leftEnd = 2; // the number of the pushbutton pin
const int rightEnd = 3;  // the number of the pushbutton pin
const int ledPin = 13;    // the number of the LED pin
const int enable = 6;
const int step = 5;
const int dir = 4;

int J;
// Variables will change:
int ledState = LOW;          // the current state of the output pin
int leftState;            // the current leftRead from the input pin
int lastLeftState = HIGH; // the previous leftRead from the input pin
int rightState;             // the current rightRead from the input pin
int lastRightState = HIGH;  // the previous rightRead from the input pin
// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 0; // the last time the output pin was toggled
long debounceDelay = 50;   // the debounce time; increase if the output flickers
char receivedChar;
boolean newData = false;

void setup() {
  pinMode(leftEnd, INPUT_PULLUP);
  pinMode(rightEnd, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  pinMode(enable, OUTPUT);   // Enable
  pinMode(step, OUTPUT);   // Step
  pinMode(dir, OUTPUT);   // Dir
  digitalWrite(enable, LOW); // Set Enable low
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
      while (rightState == LOW) {
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
        ledState = HIGH;
        digitalWrite(4, HIGH);
        int leftRead = digitalRead(leftEnd);
        digitalWrite(5, HIGH);   // Output high
        delayMicroseconds(1000); // Wait 1/2 a ms
        digitalWrite(5, LOW);    // Output low
        delayMicroseconds(1000); // Wait 1/2 a ms
        if (leftRead == LOW) {
          Serial.println("R");
          break;
        }
      }
      digitalWrite(4, LOW);
    }
  }
  if (leftRead != lastLeftState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (leftRead != leftState) {
      leftState = leftRead;

      while (leftState == LOW) {
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
        ledState = LOW;
        int rightRead = digitalRead(rightEnd);
        digitalWrite(4, LOW);
        int leftRead = digitalRead(leftEnd);
        digitalWrite(5, HIGH);   // Output high
        delayMicroseconds(1000); // Wait 1/2 a ms
        digitalWrite(5, LOW);    // Output low
        delayMicroseconds(1000); // Wait 1/2 a ms
        if (rightRead == LOW) {
          Serial.println("L");
          break;
        }
      }
      digitalWrite(4, HIGH);
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