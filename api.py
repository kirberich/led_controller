import json

from twisted.web import http
from twisted.web.http import HTTPChannel
from twisted.internet import reactor
import threading

class BotHandler(http.Request, object):
    def __init__(self, api, *args, **kwargs):
        self.api = api
        super(BotHandler, self).__init__(*args, **kwargs)

    def render(self, content, headers):
        for (header_name, header_value) in headers:
            self.setHeader(header_name, header_value)
        self.write(content)
        self.finish()

    def simple_render(self, content, content_type="text/plain"):
        self.render(content, [("Content-Type", content_type)])

    def not_found(self, message=None):
        self.setResponseCode(404, message)
        return self.simple_render("no no...")

    def process(self):
        path = [x for x in self.path.split("/") if x]
        from led_controller import Led
        try:
            if self.method == 'POST':
                for led_index, color_string in self.args.items():
                    color_string = color_string[0]
                    self.api.led_controller.leds[int(led_index)] = Led(int(led_index), *[int(x) for x in color_string.split(",")])
                self.api.led_controller.update()
                return self.simple_render("Done.")
            else:
                f = open("main.html")
                content = f.read()
                return self.simple_render(content, content_type="text/html")
        except Exception, e:
            return self.simple_render(e.message)

        return self.not_found()


class BotHandlerFactory(object):
    def __init__(self, api):
        self.api = api

    def __call__(self, *args, **kwargs):
        return BotHandler(self.api, *args, **kwargs)


class StreamFactory(http.HTTPFactory):
    protocol = HTTPChannel


class Api:
    def __init__(self, led_controller):
        self.led_controller = led_controller
        HTTPChannel.requestFactory = BotHandlerFactory(api=self)
        self.events = []

    def demonize(self, port=8080):
        reactor.listenTCP(port, StreamFactory())
        t = threading.Thread(target=reactor.run)
        t.daemon = True
        t.start()

    def run(self, port=8080):
        reactor.listenTCP(port, StreamFactory())
        reactor.run()

    def trigger(self, event, **kwargs):
        for x in range(len(self.events)):
            if self.events[x][0] == event:
                self.events[x] = (event, kwargs)
                return
        self.events.append((event, kwargs))
                                              
