// defines pins numbers
const int trigPin = 22;
const int echoPin = 21;
// defines variables
long duration;
int distance;
int prev_distance;
int distance_threshold = 10;
int event;

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication

  // Delay handshake

  Serial.println("Begin");

  byte var = 1;
  byte var2 = 1;
  int i = 0; 

  while (true) {
    if (Serial.available()) {
      if (Serial.readStringUntil('\n') == "hello") {
        Serial.println("Timestamp " + String(micros()));
        break;
      }
    }
  }
}



void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor if event detected
  if (distance < 10) {
    Serial.print(distance);
    Serial.print(" ");
    Serial.println(micros());
  }
}
