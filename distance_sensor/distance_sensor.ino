// defines pins numbers
const int trigPin = 22;
const int echoPin = 21;
// defines variables
long duration;
int distance;
void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication

  // Delay handshake

  Serial.println("Begin");

  byte var = 1;
  byte var2 = 1;
  int i = 0;

//  byte handshake = 00000001;
  while (Serial.available() == -1 || Serial.readStringUntil('\n') != "hello") {
    //wait while serial unavailable 
    // if either is true stay in the loop 
    Serial.println("waiting");

    if (i == 10) {
      Serial.println("hello");
    }
    i++;
  }

  Serial.print("Timestamp ");
  Serial.println(micros());


  //Serial.println(Serial.read(), DEC);
  while (1) {

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
  // Prints the distance on the Serial Monitor
  Serial.print(distance);
  Serial.print(" ");
  Serial.println(micros());
}
