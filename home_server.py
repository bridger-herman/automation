import web
import serial

#  ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
render = web.template.render('templates/')
urls = ('/', 'index')

class Index:
    def __init__(self):
        print('initialized')

    def GET(self):
        #  global floorLamp
        #  global deskLampZ
        #  global deskLampB
        #  global bedLamp

        #  data = web.input(c = None)

        # Floor Lamp
        #  if data.c == "floorLamp" and floorLamp:
            #  print('got')
            #  ser.write("floorLampOff")
            #  floorLamp = False
        #  return render.index(data.c, floorLamp, deskLampZ, deskLampB, bedLamp)
        return 'Hello world!'

    def __del__(self):
        print('del')

if __name__ == "__main__":
    app = web.application(urls, {'index': Index})
    app.run()
