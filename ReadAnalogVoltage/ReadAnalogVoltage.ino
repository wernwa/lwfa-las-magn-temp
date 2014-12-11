/*
  Temperature analog read
  
  reads 9 temperature sensors and prints the numbers separated by space in 500ms invervall
  turn off the power supplies if temperature reaches the critical value
  
  it is possible to set and read the power status
  
  written by Ronny Große ronny.grosse@uni-jena.de
          and Walter Werner wernwa@gmail.com
          
  last Change 11.12.2014 by Ronny Große
 */

float temperature[9];
byte Portpin[] = {A0, A1, A2, A3, A4, A5, A6, A7, A8};
int cnt=9;

float critical_temp=100.0;

int power=12;
int led=13;
int power_status=1;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // initialize digital pin 13 as an output.
  pinMode(power, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(power, HIGH);   // turn the power on
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
}

// the loop routine runs over and over again forever:
void loop() {
 
  // read the input on analog pin 0 to cnt:
  for (int i = 0; i < cnt; i++)
  {      
      temperature[i] = analogRead(Portpin[i]) * (5.0 / 1023.0) * 100.0;
      Serial.print(temperature[i]);
      Serial.print(" ");
           
  }

  Serial.print("\n");
  
  // shut down the power if critical temperature is reached
  for (int i = 0; i < cnt; i++)
  {
    if (temperature[i] >= critical_temp)
    {
      digitalWrite(power, LOW);    // turn the power off
      digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)    
    }
  }
    
  // divide deley in 50 steps and check each time for serial input
  for (int i=0; i<500; i+=10){
    check_serial_input();
    delay(10);
  }
}

// listen to incomming bytes to execute a command
void check_serial_input(){
        // turn the powersupplies on/off via usb by sending 1/0 
    if (Serial.available() > 0) {
                // read the incoming byte:
                char b = Serial.read();
                // if 1 turn power on
                if (b==0){
                  digitalWrite(power, LOW);    // turn the power off
                  digitalWrite(led, HIGH);   // turn the LED on
                  power_status=0;        
                } else
                if (b==1){                
                  digitalWrite(power, HIGH);    // turn the power back on
                  digitalWrite(led, LOW);   // turn the LED off
                  power_status=1;
                }else
                if (b==2){                  // print the power on/off status
                  Serial.print("zps:switchbox ");
                  Serial.print(power_status);
                  Serial.print("\n");
                }                
    }
}



