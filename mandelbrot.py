# by Antoni Gual Via 4/2015
# from http://code.activestate.com/recipes/579048-python-mandelbrot-fractal-with-tkinter/

from tkinter import Tk, Canvas, PhotoImage,NW,mainloop
from time import clock

def mandel_pixel(c):
  """ calculates the color index of the mandelbrot plane point passed in the arguments """
  maxIt = 256
  z =  c
  for i in range(maxIt):
      a = z * z
      z=a + c
      if a.real  >= 4.:
         return i
  return 256


# color string table in Photoimage format #RRGGBB
clr = [' #%02x%02x%02x' % (int(255 * ((i / 255) ** .5)), 0, 0) for i in range(256)]
clr.append(' #000000')  # append the color of the centre as index 256
#_clr = [(int(255 * ((i / 255) ** .5)), 0, 0) for i in range(256)]

def mandelbrot(xa,xb,ya,yb,x,y):
    """ returns a mandelbrot in a string for Tk PhotoImage"""
    print("mandelbrot calc:")
    t1 = clock()
    #calculate mandelbrot x,y coordinates for each screen pixel
    xm=[xa + (xb - xa) * kx /x  for kx in range(x)]
    ym=[ya + (yb - ya) * ky /y  for ky in range(y)]
    #build the Photoimage string by calling mandel_pixel to index in the color table
    ans = " ".join((("{"+" ".join(clr[mandel_pixel(complex(i,j))] for i in xm))+"}" for j in ym))
    #ans2 = [[clr[mandel_pixel(complex(i,j))] for i in xm] for j in ym]
    print("... took %1.4fs" % (clock()-t1))
    return ans


class Mandelbrot:
    def __init__(self):
        #window size
        self.x=640
        self.y=480
        self.old_x = None
        self.old_y = None
        #corners of  the mandelbrot plan to display
        self.xa = -2.0
        self.xb = 1.0
        self.ya = -1.27
        self.yb = 1.27

        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.x, height = self.y, bg = "#000000")
        self.init_canvas()

    def init_canvas(self):
        self.canvas.delete("all")
        self.canvas.pack()
        print("Image = %d x %d" % (self.x, self.y))
        #self.image = Image(width = self.x, height = self.y)
        #self.image = Image.new('RGBA', self.x, self.y)
        #self.img_data = self.image.load()
        #self.photo = PhotoImage(self.image)
        self.photo = PhotoImage(width = self.x, height = self.y)
        self.canvas.create_image((0, 0), image = self.photo, state ="normal", anchor = NW)

    def Draw(self):
        self.init_canvas()
        #do the mandelbrot
        t1=clock()
        self.photo.put(mandelbrot(self.xa, self.xb, self.ya, self.yb, self.x, self.y))
        print(clock()-t1, ' seconds')

    def zoom(self, a, b, x, zoom):
        # zoom
        range = b - a
        print("x_range = %f (%f - %f)" % (range, a, b))
        mid_point = a + x * range
        new_range = range * zoom
        a = mid_point - new_range / 2.0
        b = mid_point + new_range / 2.0
        return (a, b)

    def Zoom(self, event_x, event_y, magn):
        x = 1 - (self.x - event_x) / self.x
        y = 1 - (self.y - event_y) / self.y
        (self.xa, self.xb) = self.zoom(self.xa, self.xb, x, magn)
        (self.ya, self.yb) = self.zoom(self.ya, self.yb, y, magn)
        self.Draw()

    def ZoomIn(self, event):
        self.Zoom(event.x, event.y, 0.75)

    def ZoomOut(self, event):
        self.Zoom(event.x, event.y, 1.5)

    def ResizeWindow(self, event):
        redraw = False
        x_zoom = 1
        y_zoom = 1
        # print("resize: %d x %d" % (event.width, event.height))
        width = event.width - 4
        height = event.height - 4
        if self.old_x and self.old_x != width:
            print("change x")
            x_zoom = (width / self.x)
            self.x = width
            redraw = True
        if self.old_y and self.old_y != height:
            print("change y")
            y_zoom = (height / self.y)
            self.y = height
            redraw = True

        if redraw:
            # self.img.zoom(x_zoom, y_zoom)
            # self.img = PhotoImage(width=self.x, height=self.y)
            self.canvas.config(width=self.x, height=self.y)
            # rescale all the objects tagged with the "all" tag
            self.canvas.scale("all", 0, 0, x_zoom, y_zoom)

            self.Draw()

        self.old_x = width
        self.old_y = height

    def Go(self):
        self.window.bind("<Button-1>", self.ZoomIn)
        self.window.bind("<Button-3>", self.ZoomOut)
        self.window.bind("<Configure>", self.ResizeWindow)

        self.Draw()

        self.window.mainloop()

mandy = Mandelbrot()
mandy.Go()
