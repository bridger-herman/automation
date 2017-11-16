#define GREEN 11
#define RED 10
#define BLUE 9
#define WHITE 3
#define MAX_VALUE 255

#define NUMPINS 4
#define BUFSIZE 4

const int PINS[] = {RED, GREEN, BLUE, WHITE};
unsigned char buf[BUFSIZE];
int bytesRead;
bool writeReady;

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(50);
  for (int i = 0; i < NUMPINS; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  writeReady = true;
}

void setRGBW(int value) {
  for (int i = 0; i < NUMPINS; i++) {
    analogWrite(PINS[i], value);
  }
}

void setRGBW(int r, int g, int b, int w) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
  analogWrite(WHITE, w);
}

void loop() {
  if (writeReady) {
    Serial.println("Ready");
    writeReady = false;
  }
  if (Serial.available() >= BUFSIZE*sizeof(unsigned char)) {
    bytesRead = Serial.readBytes(buf, BUFSIZE);  
    if (bytesRead > 0) {
      setRGBW(buf[0], buf[1], buf[2], buf[3]);
      bytesRead = 0;
      Serial.println("Changed");
      writeReady = true;
    }
  }
  
}
