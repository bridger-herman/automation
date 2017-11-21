import sys
sys.path.append('../led')
from led_single import SingleLED
from led_fade import LEDLinearFade
from serial_wrapper import SerialWrapper

from flask import Flask, render_template, request

# Initialize
app = Flask(__name__)
ser = SerialWrapper(sys.argv[1])

current_color = [0, 0, 0, 0]
led_obj = LEDLinearFade(ser, current_color, current_color, 1, 10)

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_color
    if len(request.form) > 0:
        led_vals = [int(v) for k, v in request.form.items()]
        led_obj.__init__(ser, current_color, led_vals, 1, 30)
        led_obj.start()
        current_color = led_vals
        return render_template('index.html',
                red_value=request.form['red'],
                green_value=request.form['green'],
                blue_value=request.form['blue'],
                white_value=request.form['white']
        )
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
