void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage0 = sensorValue * (5.0 / 1023.0);
  // print out the value you read:


  // sensor 2
  sensorValue = analogRead(A1);
  float voltage1 = sensorValue * (5.0 / 1023.0);   //sensor variables voltage0 & 1

  String comb = String(voltage0) + String(",") + voltage1;
  Serial.println(comb);
  delay(100);
}