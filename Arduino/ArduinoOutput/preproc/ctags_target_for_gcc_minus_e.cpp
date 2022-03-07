# 1 "/home/inox/Documents/IB/4to Nivel/Experimental II/Guia de Ondas/Arduino/motor_completo_v3_/motor_completo_v3_.ino"
const int buttonPin3 = 2; // the number of the pushbutton pin
const int buttonPin = 3; // the number of the pushbutton pin
const int ledPin = 13; // the number of the LED pin
int J;
// Variables will change:
int ledState = 0x0; // the current state of the output pin
int buttonState3; // the current reading from the input pin
int lastButtonState3 = 0x1; // the previous reading from the input pin
int buttonState; // the current reading from the input pin
int lastButtonState = 0x1; // the previous reading from the input pin
// the following variables are long's because the time, measured in miliseconds,
// will quickly become a bigger number than can be stored in an int.
long lastDebounceTime = 0; // the last time the output pin was toggled
long debounceDelay = 50; // the debounce time; increase if the output flickers
char receivedChar;
boolean newData = false;

void setup() {
  pinMode(buttonPin3, 0x2);
  pinMode(buttonPin, 0x2);
  pinMode(ledPin, 0x1);
  pinMode(6,0x1); // Enable
  pinMode(5,0x1); // Step
  pinMode(4,0x1); // Dir
  digitalWrite(6,0x0); // Set Enable low
  J=2000;
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
            while (buttonState == 0x0) {
              recvOneChar();
                  if(newData==true && receivedChar == 's'){
                    showNewData();
                    //espera hasta que recive una a
                    arrch:
                    recvOneChar();
                    while(newData!=true)recvOneChar();
                    if(receivedChar == 'a'){//continua
                    }
                    else{goto arrch;}
//                    delay(J);
                  }
            ledState = 0x1;
            digitalWrite(4,0x1);
            int reading3 = digitalRead(buttonPin3);
            digitalWrite(5,0x1); // Output high
            delayMicroseconds(1000); // Wait 1/2 a ms
            digitalWrite(5,0x0); // Output low
            delayMicroseconds(1000); // Wait 1/2 a ms
            if (reading3 == 0x0) break;
            }
          digitalWrite(4,0x0);
          }
      }
   if (reading3 != lastButtonState3) {
      lastDebounceTime = millis();
  }

    if ((millis() - lastDebounceTime) > debounceDelay) {
            if (reading3 != buttonState3) {
            buttonState3 = reading3;

                while (buttonState3 == 0x0) {
                  recvOneChar();
                  if(newData==true && receivedChar == 's'){
                    showNewData();
                    //espera hasta que recive una a
                    //espera hasta que recive una a
                    arrci:
                    recvOneChar();
                    while(newData!=true)recvOneChar();
                    if(receivedChar == 'a'){//continua
                    }
                    else{goto arrch;}
                    recvOneChar();
                    while(newData!=true)recvOneChar();
                    if(receivedChar == 'a'){//continua
                    }
                    else{goto arrci;}
                    //delay(J);
                  }
                ledState = 0x0;
                int reading = digitalRead(buttonPin);
                digitalWrite(4,0x0);
                int reading3 = digitalRead(buttonPin3);
                digitalWrite(5,0x1); // Output high
                delayMicroseconds(1000); // Wait 1/2 a ms
                digitalWrite(5,0x0); // Output low
                delayMicroseconds(1000); // Wait 1/2 a ms
                if (reading == 0x0) break;
                }
            digitalWrite(4,0x1);
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
