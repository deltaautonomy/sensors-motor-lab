float Inch=0.00;
float cm=0.00;
float SonarPin=A0;
int sensorValue;
void setup(){
pinMode(SonarPin,INPUT);
Serial.begin(9600);
}
void loop(){
sensorValue=analogRead(SonarPin);
delay(50);
Inch= (sensorValue*0.497*2);
cm=Inch*2.54;
//Serial.println(sensorValue);
Serial.print(Inch);
Serial.println("inch");
//Serial.print(cm);
//Serial.println(" cm");
delay(100);
}
