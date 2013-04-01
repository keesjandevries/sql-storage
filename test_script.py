import math
import random

test1=[i*0.01 for i in range(90,100,1)]
test2=[math.floor(random.random()*100) for i in range(10)]

#from plotting import *
import plotting as plot
plot.plotBars(test1,0.01,test2)


