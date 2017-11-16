#define GREEN 11
#define RED 10
#define BLUE 9
#define WHITE 3
#define MAX_VALUE 255

#define NUMPINS 4
#define BUFSIZE 4

const int PINS[] = {RED, GREEN, BLUE, WHITE};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < NUMPINS; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  Serial.println("Initialized");
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
  unsigned char buf[BUFSIZE];
  int bytesRead;
  while (true) {
    if (Serial.available() >= BUFSIZE*sizeof(unsigned char)) {
      bytesRead = Serial.readBytes(buf, BUFSIZE);  
      if (bytesRead > 0) {
        setRGBW(buf[0], buf[1], buf[2], buf[3]);
        bytesRead = 0;
        Serial.println("Changed");
      }
    }
    
  }
}
