__author__ = 'ejm2095'
import random

def gen_colors(n):
    colors = []
    for i in range(0,n):
        r = lambda: random.randint(0,255)
        colors.append('#%02X%02X%02X' % (r(),r(),r()))
    return {"colors":colors}
