float t[9];
int cnt=9;

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
    
  delay(500);        // delay in between reads for stability
}



