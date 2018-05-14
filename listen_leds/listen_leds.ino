#define GREEN 11
#define RED 10
#define BLUE 9
#define WHITE 3
#define MAX_VALUE 255

#define NUMPINS 4
#define BUFSIZE 5

const int PINS[] = {RED, GREEN, BLUE, WHITE};
unsigned char buf[BUFSIZE];
int bytesRead = 0;

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(50);
  for (int i = 0; i < NUMPINS; i++) {
    pinMode(PINS[i], OUTPUT);
  }
  memset(buf, BUFSIZE*sizeof(unsigned char), 0);
  Serial.println("I");
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

void panic() {
  for (int i = 0; i < 1000; i += 100) {
    setRGBW(i%MAX_VALUE, 0, 0, 0);
    delay(10);
  }
}

void printBuffer(unsigned char* buf) {
  String cur;
  cur.concat(buf[1]);
  cur.concat(' ');
  cur.concat(buf[2]);
  cur.concat(' ');
  cur.concat(buf[3]);
  cur.concat(' ');
  cur.concat(buf[4]);
  Serial.println(cur);
}

void loop() {
  if (Serial.available() >= BUFSIZE*sizeof(unsigned char)) {
    bytesRead = Serial.readBytes(buf, BUFSIZE);
    if (bytesRead == BUFSIZE) {
      if (buf[0] > 0) {
//        setRGBW(0, 0, 0, 0);
        Serial.flush();
      }
      else {
        setRGBW(buf[1], buf[2], buf[3], buf[4]);
        bytesRead = 0;      
//        printBuffer(buf);
        Serial.println("C");
        memset(buf, BUFSIZE*sizeof(unsigned char), 0);
      }
    }
  }
}
