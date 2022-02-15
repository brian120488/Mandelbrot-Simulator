# Acknowledgements:
# https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set
# Numberphile Videos about Mandelbrot
# https://www.youtube.com/watch?v=NGMRB4O922I
# https://www.youtube.com/watch?v=FFftmWSzgmk
# Color algorithms and scaling
# https://theses.liacs.nl/pdf/2018-2019-JonckheereLSde.pdf

import math

width, height = 600, 600

# default
LEFT_BOUND = -2.0
RIGHT_BOUND = 1.0
TOP_BOUND = 1.5
BOTTOM_BOUND = -1.5

# main bulb zoom
# LEFT_BOUND = -1.4
# RIGHT_BOUND = -1.2
# TOP_BOUND = 0.1
# BOTTOM_BOUND = -0.1

# valley zoom
# LEFT_BOUND = -1.3
# RIGHT_BOUND = -1.2
# TOP_BOUND = 0.1
# BOTTOM_BOUND = 0.0


dx = abs(LEFT_BOUND - RIGHT_BOUND)
dy = abs(TOP_BOUND - BOTTOM_BOUND)
pixelSize = float(dx) / width
MAX_ITER = 100
pxls = []
scrollX, scrollY = 0, 0
cyclesIsOn = False

def setup():
    size(width, height)

    # create 2d array 
    global pxls
    pxls = create2D(height, width)
  
    # create mandelbrot
    for row in range(height):
        for col in range(width):
            a = LEFT_BOUND + col * pixelSize
            b = TOP_BOUND - row * pixelSize
            c = complex(a, b)
            iter = mandelbrot(c)
            pxls[row][col] = getColorOfIter(iter)

def draw():
    frameRate(144)
    background(255)
    
    # display all pixels
    for row in range(height):
        for col in range(width):
            stroke(pxls[row][col])
            point(col, row)
    
    # display cycles (only works on default zoom, no scroll)
    if cyclesIsOn: # press "c" key to toggle
        drawCycles()

def keyPressed():
    global scrollX, scrollY, pxls

    if keyCode == UP:
        scrollY += 1
    elif keyCode == DOWN:
        scrollY -= 1
    elif keyCode == LEFT:
        scrollX -= 1
    elif keyCode == RIGHT:
        scrollX += 1
    
    if keyCode == UP:
        pxls.pop() # pop bottom row
        newRow = []
        for col in range(width):
            a = LEFT_BOUND + (col + scrollX) * pixelSize
            b = TOP_BOUND + scrollY * pixelSize
            c = complex(a, b)
            iter = mandelbrot(c)
            newRow.append(getColorOfIter(iter))
        pxls.insert(0, newRow)
    elif keyCode == DOWN:
        pxls.pop(0) # pop top row
        newRow = []
        for col in range(width):
            a = LEFT_BOUND + (col + scrollX) * pixelSize
            # b = BOTTOM_BOUND + scrollY * pixelSize
            b = TOP_BOUND - (height - scrollY) * pixelSize
            c = complex(a, b)
            iter = mandelbrot(c)
            newRow.append(getColorOfIter(iter))
        pxls.append(newRow)
    elif keyCode == LEFT:
        for row in range(height):
            pxls[row].pop() # pop left column
            a = LEFT_BOUND + scrollX * pixelSize
            b = TOP_BOUND - (row - scrollY) * pixelSize
            c = complex(a, b)
            iter = mandelbrot(c)
            pxls[row].insert(0, getColorOfIter(iter))
    elif keyCode == RIGHT:
        for row in range(height):
            pxls[row].pop(0) # pop left column
            a = LEFT_BOUND + (width + scrollX) * pixelSize
            b = TOP_BOUND - (row - scrollY) * pixelSize
            c = complex(a, b)
            iter = mandelbrot(c)
            pxls[row].append(getColorOfIter(iter))

def create2D(rows, cols):
    L = []
    for row in range(rows):
        L.append([0] * cols)
    return L

def mandelbrot(c):
    z = 0
    for iter in range(MAX_ITER):
        if abs(z) > 2: break
        z = z ** 2 + c
    return iter

def getColorOfIter(iter):
    t = float(iter) / MAX_ITER
    
    # smooth functions for colors
    r = 9 * (1 - t) ** 1 * t ** 3 * 255
    g = 15 * (1 - t) ** 2 * t ** 2 * 255
    b = 8.5 * (1 - t) ** 3 * t ** 1 * 255
    
    return color(r,g,b)

def keyReleased():
    global cyclesIsOn
    if key == "c": 
        cyclesIsOn = not cyclesIsOn
        
def drawCycles():
    stroke(255)
    a = LEFT_BOUND + mouseX * pixelSize
    b = TOP_BOUND - mouseY * pixelSize
    c = complex(a, b)
    print(a, b)
    z = 0
    prevX = mouseX
    prevY = mouseY
    for i in range(25):
        z = z ** 2 + c
        x = width / 3 + float(z.real) / pixelSize
        y = height / 2 - float(z.imag) / pixelSize
        line(prevX, prevY, x, y)
        prevX = x
        prevY = y
