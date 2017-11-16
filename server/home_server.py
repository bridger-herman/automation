import sys
sys.path.append('../led')
from led_single import SingleLED

from flask import Flask, render_template, request
app = Flask(__name__)

led_changer = SingleLED((0, 0, 0, 0))

@app.route('/', methods=['GET', 'POST'])
def index():
    if len(request.form) > 0:
        led_vals = [int(v) for k, v in request.form.items()]
        led_changer.set_color(led_vals)
        led_changer.start()
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
