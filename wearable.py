import random
import time
import math
import numpy as np
import os

mock = False 

if not mock: 
        import board
        import neopixel

# LED strip configuration:
# LED_COUNT      = 5      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
# LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# Linear palette
# https://mycolor.space/gradient3?ori=to+left+top&hex=%23C92942&hex2=%23D910AE&hex3=%23FBC95F&submit=submit
# https://en.wikibooks.org/wiki/Color_Theory/Color_gradient

palettes = {
        "warm1": [
                [0, 0.3, 1],
                [255, 0, 0],
                [100, 100, 0],
                [50, 150, 0],
        ],
        "fireflies": [
                [0, 0.3, 1],
                [165, 234, 41],
                [224, 212, 49],
                [143, 72, 53],
        ]
}

class MockPixels:
        RESET = '\033[0m'
        def __init__(self, LED_COUNT=5):
                self.n = LED_COUNT
                self.vals = [(0, 0, 0)] * LED_COUNT

        def fill(self, color):
                for i in range(self.n):
                        self.vals[i] = color
                self.draw()

        def __setitem__(self, index, color):
                self.vals[index] = color
                self.draw()

        def draw(self):
                panel = ""
                for val in self.vals:
                        color = val
                        s = MockPixels.get_color_escape(*color)
                        width = os.get_terminal_size().columns
                        s += "█" * int(width / self.n)
                        panel += s
                print(panel, end="\r")

        def get_color_escape(r, g, b, background=False):
                return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

class Dazzled:
        def __init__(self, LED_COUNT=5, mock=True):
                if mock:
                        self.pixels = MockPixels(LED_COUNT)
                else: 
                        self.pixels = neopixel.NeoPixel(board.D18, LED_COUNT, pixel_order=neopixel.RGB)
                self.n = LED_COUNT

                if not mock:
                    self.pixels.fill((0, 0, 0))

        def set_color(self, color):
                self.pixels.fill(color)

        def set_color(self, color, index):
                self.pixels[index] = color

        def off(self):
                self.pixels.fill((0,0,0))

        def interpolate(self, color1, color2, steps):
                r1, g1, b1 = color1
                r2, g2, b2 = color2
                r = np.linspace(r1, r2, steps)
                g = np.linspace(g1, g2, steps)
                b = np.linspace(b1, b2, steps)
                # print(f"r: {r}, g: {g}, b: {b}")
                return zip(r, g, b)

        def gradient_fill(self, palette_name: str, iters=100, duration=1.0):
                for i in range(iters):
                        locations = palettes[palette_name][0]
                        colors = palettes[palette_name][1:]
                        print('colors', colors)
                        for c in self._linear_gradient(colors, locations, count=iters):
                                self.pixels.fill(c)
                                time.sleep(1)

        def _linear_gradient(self, colors, locations, count=100):
                """
                A generator function that yields a linear sequence of colors
                :param colors: A list of colors, each in the form of (r, g, b), each ranging from 0 to 255
                :param locations: A list of floats between 0 and 1 that represent the location of each color
                :param count: The number of colors to generate between each pair of colors
                """
                assert(len(colors) == len(locations))
                n_colors = len(colors)

                # if locations[0] != 0:
                #         locations = [0] + locations
                #         colors = [colors[0]] + colors
                #         n_colors += 1
                # if locations[-1] != 1:
                #         locations = locations + [1]
                #         colors = colors + [colors[-1]]
                #         n_colors += 1
                # print('n_colors', n_colors)
                for t in range(n_colors):
                        if t == n_colors - 1:
                                break
                        num_steps = int((locations[t + 1] - locations[t]) * count)
                        # print(locations, locations[t+1], locations[t], count, num_steps)
                        for c in self.interpolate(colors[t], colors[t+1], num_steps):
                                yield c
        
        def slide_through_colors(self, palette="fireflies", iters=100):
            locations = palettes[palette][0]
            colors = palettes[palette][1:]
            while True:
                for c in self._linear_gradient(colors, locations, count=iters):
                    yield c
                for c in reversed(list(self._linear_gradient(colors, locations, count=iters))):
                    yield c


        def wave(self, index, color, duration=1.0, iters=20):
                x = 0
                while x < math.pi:
                        alpha = math.sin(x)
                        self.pixels[index] = \
                                (int(color[0]*alpha), int(color[1]*alpha), int(color[2]*alpha))
                        x += math.pi / (iters * duration)
                        time.sleep(duration / iters)

        def waves(self, duration=1.0, iters=50):
            for i in range(self.n):
                color = (int(random.randint(0, 256)), int(random.randint(0, 100)), 0)
                self.wave(i, color, duration=duration, iters=iters)

        def startup(self):
                for i in range(5):
                        self.pixels[i] = (230,10,10)
                        time.sleep(0.2)
                        self.pixels[i] = (0,0,0)

        def spectrum(self, iters=None):
                def color(t, pallet="warm1"):
                        a, b, c, d = palettes[pallet]
                        a, b, c, d = np.array(a), np.array(b), np.array(c), np.array(d)
                        c = a + b * np.cos(2 * math.pi * (c * t + d))

                        return (c * 256) % 256

                i = 0
                while iters is None or i < iters:
                        for p in range(self.n):
                                i += 1
                                t = (i * 0.001) % 1
                                r, g, b = color(t)
                                # if (i % 100 == 0):
                                #         print(t, r, g, b)
                                self.pixels[p] = (r, g, b)

                        time.sleep(0.01)

        def fire_fly(self, i, color=(255, 255, 255), duration=1.0, iters=50):
                """
                A firefly effect, needs to be called in its own thread
                """

                # # send a guassian pulse to the pixel
                for j in range(iters):
                        alpha = math.exp(-j**2 / (2 * 10**2)) # TODO verify this
                        self.pixels[i] = (int(color[0]*alpha), int(color[1]*alpha), int(color[2]*alpha))
                        time.sleep(duration / iters)


        def fly_fireflies(self, duration=1.0, iters=100):
                import threading
                fireflies = [Firefly(self, a = 0.08, b = 2) for fly in range(self.n)]
                delay = 0.1

                pixel_buffer = np.zeros((self.n, iters, 3))

                colors = self.slide_through_colors()

                while True:
                        pixels = pixel_buffer[:, 0, :]
                        # set the pixel
                        for i, f in enumerate(fireflies):
                                f.update(fireflies, pixel_buffer)
                                self.pixels[i] = (int(pixels[i, 0]), int(pixels[i, 1]), int(pixels[i, 2]))
                                
                        # delete the first pixel column in the buffer
                        pixel_buffer = np.delete(pixel_buffer, 0, axis=1)

                        # add a new column at the end
                        pixel_buffer = np.append(pixel_buffer, np.zeros((self.n, 1, 3)), axis=1)
                        
                        Firefly.COLOR = next(colors)

                # for i in range(iters):
                while True:
                        for f in fireflies:
                                # t = threading.Thread(target=self.fire_fly, args=(f.index, 1.0, 1))
                                # t.start()
                                f.update(fireflies)
                        time.sleep(delay)
                        self.pixels.fill((0, 0, 0))

                
class Firefly:
        # Simulated Fireflies The firefly algorithm synchronizes
        # agents as an emergent effect of each agent running a simple
        # procedure. Each agent increments an internal counter up to
        # a predetermined threshold over time. Once it reaches that
        # threshold, the agent flashes a light. If one agent sees another
        # agent flash, it will increment its own counter by a set amount
        # (referred to as jumping). As a result, all agents that can see
        # each other for an extended period of time will synchronize
        # to the same frequency (see (Tyrrell et al., 2006) for details).

        # https://watermark.silverchair.com/978-0-262-32621-6-ch116.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAAAuEwggLdBgkqhkiG9w0BBwagggLOMIICygIBADCCAsMGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQM3FxUg320byHQBtOIAgEQgIIClHcmkz5KUTjwtJL6sJRIdJf8Iw6Ig3jSw-9PKx1xxhXiyoaSjq54brindbKyM7DyHjMZfZ2oqwMynJ_CTSAes6uSGy-y0vExGYmUZ3bePKf6BwCh1Kb0g83HWZXnvJmO5Rso-bqZum9RHE_4vJHb6QcfMz6FyopZaxG6Fw0FLYFXD4sfk5s9UgJbmaieNGVRByK7hFVA7L52VZGSOYiVSP6Md1ooD3_y2UdHAxvlYVWOYMfI1fOqb5lreA7uoB9EJEbztGqsozNQ80wQosdN-2RgHen6pCf0SSkG7DUzNlEeLtqSlvPwgkq9MDvQGHhkeM74jPpLz85DgMSuVglBiZWKh1X9ee7VwoarT3V1tJD8-9pG9M5GsPGEnhhgScZaWF_fn9Gbh9e-6FuKNwrhw-RaXNyBxzzcdcQml5uJloxikyz1iGTukPdEdKe8ig5S6n6B5YMYmJXtPf-fs1A42e1EzHZMpeQ9x0jGVoJdldYZlOtub5MqX7pqt-fZiQyjbwvuNMTQ1tasO2j8jsGwIlRhEAuN7xiC7YnXYs4R8aGbfv_utPHy-CZo5J2-PpEsWlO4zhEH4_egRI-Ub-dV2QSqFRqL1gEoQc7osC-JFDkgDzxmdGPm0skcX84nvsGbmrIU6sPdPL6gTXEvpSKkM5FOUbEDCrEnLZP9rRgZs4YyU4pGx9rO5JhyuGyVigcxLZJGWB-u6_ipQzEYjFd6MCP-xrNeFrKVGUSWZ4UqS6syREnaBjkdLnLnVYtm-J7r1l6bxpcUvaI2C8J6HZ_UvD3kEVtlpYCCy22FivuMCT68o6cI6b-blNeaILJnBwZYAbx8qPHXigdmMM7p_HfvgOdlPRHc6BN-oLkOxtwRY1kr7LjZbA

        I = 0
        COLOR = (255, 255, 255)
        def __init__(self, dazzled, a=.1, b=1, thresh=20):
                """
                a = .1 b = 1
                """
                self.index = Firefly.I
                Firefly.I += 1

                self.a = a
                self.e_in = self.a
                self.b_in = b

                self.thresh = thresh

                self.dazzled = dazzled

                self.action_potential = random.uniform(0, self.thresh)

        def do_flash(self, buffer):
                buffer = buffer[self.index]
                for i in range(len(buffer)):
                        std = 2
                        b = 3
                        alpha =  math.exp(-(i - b)**2 / (2 * std**2))
                        buffer[i] = alpha * np.array(Firefly.COLOR)
                

                # self.dazzled.fire_fly(self.index, self.duration)
                # self.dazzled.pixels[self.index] = Firefly.COLOR

        def flash(self, fireflies, buffer):
                self.do_flash(buffer)
                
                # send to other fireflies
                self.broadcast(fireflies)

        def update(self, fireflies, pixel_buffer):
                if self.action_potential >= self.thresh:
                        self.flash(fireflies, pixel_buffer)
                        self.action_potential = 0
                        return
                self.action_potential += self.a

                
        def broadcast(self, fireflies, neighbors_only=True):
                def fuzz(x):
                        return random.uniform(0.95 * x, 1.05 * x)
                e = fuzz(self.e_in)
                b = fuzz(self.b_in)
                a = math.exp(b * e)
                B = (math.exp(b * e) - 1) / (math.exp(b) - 1)

                if neighbors_only:
                        others = fireflies[self.index-1:self.index+2]
                else:
                        others = fireflies

                for other in others:
                        if other.index != self.index:
                                new_ap = min(a * other.action_potential + B, other.thresh)
                                other.action_potential = new_ap

                avg = sum([abs(fireflies[i].action_potential - fireflies[i-1].action_potential) for i in range(1, len(fireflies))]) / (len(fireflies) - 1)
                # print(avg)
                # print(e, b, a, B, other.action_potential, new_ap, avg)
                

if __name__ == "__main__":
        d = Dazzled(5, mock=False)
        
        print("fireflies")
        d.fly_fireflies()

        exit()
        print('linear gradient')
        d.gradient_fill("warm1")
        print("startup")
        d.startup()
        print("\nwaves")
        d.waves(duration=random.uniform(0.5, 2), iters = 40)
        exit()
        i = 0   
        while True:
                for p in range(LED_COUNT):
                        i += 1
                        t = (i * 0.001) % 1
                        
                        r, g, b = color(t)
                        
                        if (i % 100 == 0):
                                print(t, r, g, b)
                        pixels[p] = (r, g, b)

                time.sleep(0.01)
