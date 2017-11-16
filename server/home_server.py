import web
import serial

#  ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
render = web.template.render('templates/')
urls = ('/', 'index')

formy = web.form.Form(
    web.form.Textbox(name='red', value='0')
)

class index:
    def __init__(self):
        print('initialized')

    def GET(self):
        return render.index(formy())

    def POST(self):
        f = formy()
        print('posted')
        print(f)
        print('value', f['red'].value)


    def __del__(self):
        print('del')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
