 #define in_photo 8
#define out_photo A0

void setup() {
  pinMode(in_photo, OUTPUT);
  pinMode(out_photo, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(in_photo, HIGH);
  int val = analogRead(out_photo);
  Serial.println(val);
}
