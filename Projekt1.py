import math
import numpy as np
def dataLoad(filename):
    #Opening and reading file to extract values
    file = open(filename, 'r')
    data = file.read()
    Temperature = []
    Growthrate = []
    Bacteria = []
    #Sorting data by lines
    M = data.split("\n")
    #Creating matrix with all values in Nx3 matrix
    for i in range(len(M)-1):
            Temperature.append(M[i].split(" ")[0])
            Growthrate.append(M[i].split(" ")[1])
            Bacteria.append(M[i].split(" ")[2])
            T = [float(i) for i in np.ravel(Temperature)]
            G = [float(i) for i in np.ravel(Growthrate)]
            B = [float(i) for i in np.ravel(Bacteria)]
    N = [T,G,B]
    N = np.transpose(N)
    #Excluding faulty data and printing error code
    data = []
    FaultyLines = []
    for j in range(len(M)-1):
        if N[j,0] < 10 or 60 < N[j,0]:
            np.delete(N,j,0)
            FaultyLines.append(j)
            #print("Error in line {}, Temperature is out of range".format(j))
        elif N[j,1] < 0:
            np.delete(N,j,0)
            FaultyLines.append(j)
            #print("Error in line {}, Growthrate is out of range".format(j))

        elif 1 > N[j,2] or N[j,2] > 4:
            np.delete(N,j, 0)
            FaultyLines.append(j)
            #print("Error in line {}, Bacteria is out of range".format(j))
        else:
            data.append([N[j,0],N[j,1],N[j,2]])    
            
    data = np.ravel(data)
    data = np.array([[data[0::3]], [data[1::3]],[data[2::3]]])
    #data = np.array(data)
    return data
#print(dataLoad("C:/Users/Bruger/OneDrive - Danmarks Tekniske Universitet/DTU/2. semester/02633 Introduktion til Programmering og Databehandling/Data files for projects/Data files for projects/Bacteria/test.txt"))

#data = dataLoad("C:/Users/Bruger/OneDrive - Danmarks Tekniske Universitet/DTU/2. semester/02633 Introduktion til Programmering og Databehandling/Data files for projects/Data files for projects/Bacteria/test.txt")


val = ["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate", "Rows", "Mean Cold Growth rate", "Mean Hot Growth rate"]

statistic = val[1]
data = dataLoad("C:/Users/Bruger/OneDrive - Danmarks Tekniske Universitet/DTU/2. semester/02633 Introduktion til Programmering og Databehandling/Data files for projects/Data files for projects/Bacteria/test.txt")

def dataStatistics(data, statistic):
    Temperature = np.ravel(data[0,:])
    GrowthRate = np.ravel(data[1,:])
    #print(Temperature)
    #print(GrowthRate)
    ValidInput = ["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate", "Rows", "Mean Cold Growth rate", "Mean Hot Growth rate"]
    if statistic not in ValidInput:
        result = "Invalid input, please type valid input"
    else:
        if statistic == ValidInput[0]:
            result = np.mean(Temperature)
        elif statistic == ValidInput[1]:
            result = np.mean(GrowthRate)
        elif statistic == ValidInput[2]:
            result = np.std(Temperature)
        elif statistic == ValidInput[3]:
            result = np.std(GrowthRate)
        elif statistic == ValidInput[4]:
            result = len(Temperature)
        elif statistic == ValidInput[5]:
            result = np.mean(GrowthRate[Temperature < 20])
        elif statistic == ValidInput[6]:
            result = np.mean(GrowthRate[Temperature > 50])
    return result

print(dataStatistics(data, statistic))
