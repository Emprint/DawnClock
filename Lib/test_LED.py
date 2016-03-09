#!/usr/bin/python
import RPi.GPIO as GPIO, time, math

dev = "/dev/spidev0.0"
num_leds = 25
fps = 24
delay = 0.08
bright = 255
red = [bright, 0, 0]
yellow = [bright, bright, 0]
green = [0, bright, 0]
cyan = [0, bright, bright]
blue = [0, 0, bright]
magenta = [bright, 0, bright]
black = [0, 0, 0]
white = [bright, bright, bright]
grey = [20, 20, 20]

color_name = "red"
color = eval(color_name)

mixWeight = 0.5

spidev = file(dev, "wb")
print "Loading"

# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
gamma = bytearray(256)
for i in range(256):
	gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)


def mixChannel(color1, color2, channel, weight):
	colorC = int(math.floor(color1[channel]*weight + color2[channel]*(1 - weight)));
	return colorC;


def mixColors(color1, color2):
	return mixColorsWeight(color1, color2, mixWeight);

def mixColorsWeight(color1, color2, weight):
	return [mixChannel(color1, color2, 0, weight), mixChannel(color1, color2, 1, weight), mixChannel(color1, color2, 2, weight)];


def setPixel(leds, pixel, color):
	pixel = pixel * 3
	leds[pixel] = color[0]
	leds[pixel + 1] = color[1]
	leds[pixel + 2] = color[2]


def fillRange(rColor):
	leds = bytearray(num_leds * 3 + 1)
	for l in range(num_leds):
		setPixel(leds, l, rColor)

	return leds

def fillRangeChase(pos, color1, color2):
	leds = bytearray(num_leds * 3 + 1)
	for l in range(num_leds):
		setPixel(leds, l, color1)	
		pos_before = pos - 1
		pos_before1 = pos - 2
		if pos_before < 0:
			pos_before = num_leds - 2
			pos_before1 = num_leds - 3
                if pos_before1 < 0:
                        pos_before1 = num_leds - 2
		
		pos_after = pos + 1
		pos_after1 = pos + 2
		if pos_after == num_leds:
			pos_after = 0
			pos_after1 = 1
                if pos_after1 == num_leds:
                        pos_after1 = 0

		setPixel(leds, pos, color2)
		mix =  mixColorsWeight(color2, color1, .8)
		mix1 = mixColorsWeight(color2, color1, .4)
		setPixel(leds, pos_before, mix)
		setPixel(leds, pos_after, mix)
		setPixel(leds, pos_before1, mix1)
		setPixel(leds, pos_after1, mix1)
		
	return leds;


def colorTransition(color1, color2, duration):
        print("colorTransition")
	steps = float(duration * fps)
	position = 0.0
	
	while position <= 1.0:
		dColor = mixColorsWeight(color1, color2, 1.0 - position)
		spidev.write(fillRange(dColor))
		spidev.flush()
		position = float(position + 1/steps)
		time.sleep(1.0/fps)

	#Ensure last color is the final color
	spidev.write(fillRange(color2))
	spidev.flush()


def colorChase(color1, color2, duration):
	colorChaseLoop(color1, color2, duration, False)
	
def colorChaseInfinite(color1, color2, duration):
	colorChaseLoop(color1, color2, duration, True)

def colorChaseLoop(color1, color2, duration, infinite):
	print("ColorChase")
	position = 0

	while infinite or position < num_leds:
		spidev.write(fillRangeChase(position, color1, color2))
		spidev.flush()

		position = position + 1
		if infinite and position == num_leds:
			position = 0
		time.sleep((1.0/num_leds)*duration)


def colorDim(color1, color2, duration):
	print("ColorDim")
	direction = 1

	while True:
                if direction == 1:
                        colorTransition(color1, color2, duration)
                        direction = -1
                else:
                        colorTransition(color2, color1, duration)
                        direction = 1

def colorCycle(colors, duration):
        colorCycleLoop(colors, duration, False)
        
def colorCycleInfinite(colors, duration):
        colorCycleLoop(colors, duration, True)

def colorCycleLoop(colors, duration, infinite):
        print("ColorCycle")
        currentColor = 0
        position = 0

        while currentColor < len(colors) - 1:
                colorTransition(colors[currentColor], colors[currentColor+1], float(duration)/float(len(colors) - 1))
                currentColor = currentColor + 1
                if infinite and currentColor >= len(colors) - 1:
                        currentColor=0

def fillColor(color1):
        print("fillColor")
        spidev.write(fillRange(color1))
	spidev.flush()


fillColor(red)
#colorChaseInfinite(yellow, black, 1)
#colorDim(blue, [0, 0, 50], .5)
colorCycleLoop([black, blue, red, yellow, white], 20, True)
