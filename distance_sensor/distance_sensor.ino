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
  //detect event, only send timestamp of event
  //sensing delay is so small / noexistent / negliagilble
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


  if (distance <= distance_threshold && prev_distance > distance_threshold) { // Event detected
    Serial.print("Event #");
    Serial.print(event);
    Serial.print(": ");
    event++;
  }
  Serial.println(micros());
  prev_distance = distance;
}
