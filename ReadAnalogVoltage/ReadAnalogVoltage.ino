/*
  ReadAnalogVoltage
  Reads an analog input on pin 0, converts it to voltage, and prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

 This example code is in the public domain.
 */

float temperature[9];
byte Portpin[] = {A0, A1, A2, A3, A4, A5, A6, A7, B0};
int cnt=9;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // initialize digital pin 13 as an output.
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, HIGH);   // turn the power on
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  // int sensorValue = analogRead(A0);  
  
  // read the input on analog pin 0 to 7:



  for (int i = 0; i < cnt; i++)
  {      
      temperature[i] = analogRead(Portpin[i]) * (5.0 / 1023.0) * 100.0;
      Serial.print(temperature[i]);
      Serial.print(" ");
           
  }

  Serial.print("\n");
  
  
  for (int i = 0; i < cnt; i++)
  {
    if (temperature[i] >= 100.0)
    {
      digitalWrite(12, LOW);    // turn the power off
      digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)    
    }
    // else
    // {
    //   digitalWrite(12, HIGH);   // turn the power on
    //   digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW    
    // }    
  }  
  delay(500);                   // wait for a second
}


