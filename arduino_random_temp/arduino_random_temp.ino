float t[7];

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // make the pushbutton's pin an input:
  //pinMode(pushButton, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  for (int i=0;i<7;i++){
    long randNumber = random(0, 100);
    int v=1;
    if(random(0,2) == 1){ v=-1;};
    t[i] = (float)randNumber / 100.0 + v*t[i]; 
    Serial.print(t[i]);
    Serial.print(" ");
  }
  Serial.print("\n");
    
  delay(500);        // delay in between reads for stability
}



