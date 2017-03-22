from display import *
from matrix import *
import math

def add_circle( points, cx, cy, cz, r, step ):
    xi = cx
    yi = cy+r
    u = 0
    z = 0
    while (u<=1+step):
        theta = 2*math.pi*u
        x = cx+r*math.sin(theta)
        y = cy+r*math.cos(theta)
        add_edge(points, xi, yi, z, x, y, z)
        xi = x
        yi = y
        u +=step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if (curve_type=="hermite"):
        #curve between (x0,y0) (x1,y1)
            #(rx0,ry0) (rx1,ry1)
        add_hermite(points,x0,y0,x1,y1,x2,y2,x3,y3,step)
    if (curve_type=="bezier"):
        #curve between (x0,y0) (x3,y3)
            #(x1,y1) (x2,y2)
        add_bezier(points,x0,y0,x1,y1,x2,y2,x3,y3,step)

def add_hermite(points, x0,y0, x1,y1, rx0,ry0, rx1,ry1, step ):
    xcoefs = generate_curve_coefs(x0,x1,rx0,rx1, "hermite")
    ycoefs = generate_curve_coefs(y0,y1,ry0,ry1, "hermite")

    xi=x0
    yi=y0
    u = 0
    z = 0
    while (u <= 1+step):
        x = xcoefs[0]*(u**3) + xcoefs[1]*(u**2) + xcoefs[2]*u + xcoefs[3]
        y = ycoefs[0]*(u**3) + ycoefs[1]*(u**2) + ycoefs[2]*u + ycoefs[3]
        add_edge(points, xi, yi, z, x, y, z)
        xi = x
        yi = y
        u +=step

def add_bezier(points, x0,y0, x1,y1, x2,y2, x3,y3, step ):
    xcoefs = generate_curve_coefs(x0,x1,x2,x3, "bezier")
    ycoefs = generate_curve_coefs(y0,y1,y2,y3, "bezier")

    xi=x0
    yi=y0
    u = 0
    z = 0
    while (u <= 1+step):
        x = xcoefs[0]*(u**3) + xcoefs[1]*(u**2) + xcoefs[2]*u + xcoefs[3]
        y = ycoefs[0]*(u**2) + ycoefs[1]*(u**2) + ycoefs[2]*u + ycoefs[3]
        add_edge(points, xi, yi, z, x, y, z)
        xi = x
        yi = y
        u +=step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line

