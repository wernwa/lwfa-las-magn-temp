float t[9];
int cnt=9;

int power=12;
int led=13;
int power_status=1;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // make the pushbutton's pin an input:
  //pinMode(pushButton, INPUT);
  
  // init sensors to roum temperature
  for (int i=0;i<cnt;i++){
    t[i] = 20.0;
  }
  
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
  
}

// the loop routine runs over and over again forever:
void loop() {
  for (int i=0;i<cnt;i++){
    long randNumber = random(0, 100);
    float v=1.0;
    if(random(0,2) >= 1){ v=-1.0;};
    t[i] = (float)v*randNumber / 100.0 + t[i]; 
    Serial.print(t[i]);
    Serial.print(" ");
  }
  Serial.print("\n");
  
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



