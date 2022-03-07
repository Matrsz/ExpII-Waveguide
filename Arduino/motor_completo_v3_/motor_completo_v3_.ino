const int buttonPin3 = 2; // the number of the pushbutton pin
const int buttonPin = 3;  // the number of the pushbutton pin
const int ledPin = 13;    // the number of the LED pin
int J;
// Variables will change:
int ledState = LOW;          // the current state of the output pin
int buttonState3;            // the current reading from the input pin
int lastButtonState3 = HIGH; // the previous reading from the input pin
int buttonState;             // the current reading from the input pin
int lastButtonState = HIGH;  // the previous reading from the input pin
// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 0; // the last time the output pin was toggled
long debounceDelay = 50;   // the debounce time; increase if the output flickers
char receivedChar;
boolean newData = false;

void setup() {
  pinMode(buttonPin3, INPUT_PULLUP);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  pinMode(6, OUTPUT);   // Enable
  pinMode(5, OUTPUT);   // Step
  pinMode(4, OUTPUT);   // Dir
  digitalWrite(6, LOW); // Set Enable low
  J = 2000;
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  digitalWrite(ledPin, ledState);
}

void loop() {
  int reading = digitalRead(buttonPin);
  int reading3 = digitalRead(buttonPin3);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      while (buttonState == LOW) {
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
        int reading3 = digitalRead(buttonPin3);
        digitalWrite(5, HIGH);   // Output high
        delayMicroseconds(1000); // Wait 1/2 a ms
        digitalWrite(5, LOW);    // Output low
        delayMicroseconds(1000); // Wait 1/2 a ms
        if (reading3 == LOW) {
          Serial.println("R");
          break;
        }
      }
      digitalWrite(4, LOW);
    }
  }
  if (reading3 != lastButtonState3) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading3 != buttonState3) {
      buttonState3 = reading3;

      while (buttonState3 == LOW) {
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
        int reading = digitalRead(buttonPin);
        digitalWrite(4, LOW);
        int reading3 = digitalRead(buttonPin3);
        digitalWrite(5, HIGH);   // Output high
        delayMicroseconds(1000); // Wait 1/2 a ms
        digitalWrite(5, LOW);    // Output low
        delayMicroseconds(1000); // Wait 1/2 a ms
        if (reading == LOW) {
          Serial.println("L");
          break;
        }
      }
      digitalWrite(4, HIGH);
    }
  }
  digitalWrite(ledPin, ledState);
  lastButtonState = reading;
  lastButtonState3 = reading3;
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