import math 
import numpy as np
from statistics import mean

def fermentationRate(measuredRate,lowerBound,upperBound):
    n = np.size(measuredRate)
    for i in range(n):
        if (lowerBound < measuredRate[i] < upperBound):
            measuredRate[i] = measuredRate[i]
        else :
            measuredRate[i] = 0
        k = measuredRate[measuredRate > 0]
        averageRate = np.mean(k)
    return averageRate
print(fermentationRate(np.array([20.1, 19.3, 1.1, 18.2, 19.7, 121.1, 20.3, 20.0]), 15, 25))

