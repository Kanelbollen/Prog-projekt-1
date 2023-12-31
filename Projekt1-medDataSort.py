# LIBRARIES

import math
import numpy as np
import matplotlib.pyplot as plt 
import os
import random

# FUNCTIONS

# Function for sorting data

def dataLoad(filename,g):
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
    dataError = []
    for j in range(len(M)-1):
        if N[j,0] < 10 or 60 < N[j,0]:
            np.delete(N,j,0)
            FaultyLines.append(j)
            dataError.append("Error in line {}, Temperature is out of range".format(j))
        elif N[j,1] < 0:
            np.delete(N,j,0)
            FaultyLines.append(j)
            dataError.append("Error in line {}, Growthrate is out of range".format(j))

        elif 1 > N[j,2] or N[j,2] > 4:
            np.delete(N,j, 0)
            FaultyLines.append(j)
            dataError.append("Error in line {}, Bacteria is out of range".format(j))
        else:
            data.append([N[j,0],N[j,1],N[j,2]])    
    if g == 0:
        return data
    elif g == 1:
        return dataError
    else:
        return "Error in function variable"


#FILTER

def dataFilter(data, Bacteria, Growthrange):
    data = np.ravel(data)
    data = np.array([[data[0::3]], [data[1::3]],[data[2::3]]])
    GrowthFilter = data[:,(data[1,:] <= Growthmax) & (data[1,:] >= Growthmin)] 
    if FilterType[:] == ["bacteria"]:
        for i in range(len(BacteriaTypes[0,:])):
            if Bacteria == BacteriaTypes[0,i]: 
                BacteriaFilter = data[:,data[2,:] == i+1]
        Filter = BacteriaFilter
        #GrowthFilter = data[:,Growth <= Growthmax or Growth >= Growthmin]
    if FilterType[:] == ["growth rate"]:
        Filter = GrowthFilter
    if FilterType[:] == ["bacteria","growth rate"] or FilterType[:] == ["growth rate","bacteria"]:
        for i in range(len(BacteriaTypes[0,:])):
            if Bacteria == BacteriaTypes[0,i]: 
                BacteriaFilter = GrowthFilter[:,GrowthFilter[2,:] == i+1]
        Filter = BacteriaFilter
    return Filter

# Function for plotting diagrams

def dataSort(data):
    data = np.ravel(data)
    data = np.array([[data[0::3]], [data[1::3]],[data[2::3]]])
    Temp = np.ravel(data[0,:])
    Growth = np.ravel(data[1,:])
    Bact = np.ravel(data[2,:])
    sort_index = np.argsort(Temp)
    for i in range(len(sort_index)):
        SortedTemp.append(Temp[sort_index[i]])
        SortedGrowth.append(Growth[sort_index[i]])
        SortedBact.append(Bact[sort_index[i]])
    
    #Sorting data by bacteria for plot data
    for i in range(len(Bact)):
        if SortedBact[i] == 1:
            Salmonella.append(SortedGrowth[i])
            xSal.append(SortedTemp[i])
        if SortedBact[i] == 2:
            Bacillus.append(SortedGrowth[i])
            xBac.append(SortedTemp[i])
        if SortedBact[i] == 3:
            Listeria.append(SortedGrowth[i])
            xList.append(SortedTemp[i])
        if SortedBact[i] == 4:
            Brochothrix.append(SortedGrowth[i])
            xBroc.append(SortedTemp[i])
    return Salmonella, xSal, Bacillus, xBac, Listeria, xList, Brochothrix, xBroc

def dataHistogram(data):
    #Sorting data into categories
    #Plotting number of bacteria in a histogram
    data = np.ravel(data)
    data = np.array([[data[0::3]], [data[1::3]],[data[2::3]]])
    Bact = np.ravel(data[2,:])
    plt.hist(Bact,bins=[0.5,1.5,2.5,3.5,4.5],color = "blue")
    #Constructs correct legends
    labels = ["","Salmonella","Bacillus","Listeria","Brochothrix"]
    plt.xticks(range(len(labels)),labels, size = 'small')
    plt.title("Number of bacteria with {:d}".format(Adam))
    plt.show()
    #Sorting data by bacteria for plot data

def dataScatterplot(Salmonella, xSal, Bacillus, xBac, Listeria, xList, Brochothrix, xBroc,k):
    plt.plot(xSal,Salmonella, k ,color = "blue")
    plt.plot(xBac,Bacillus, k , color = "orange")
    plt.plot(xList,Listeria, k , color = "red")
    plt.plot(xBroc,Brochothrix, k , color = "green")
    plt.title("Growth rate by temperature with {:d}".format(Adam))
    plt.xlabel("Temperature")
    plt.ylabel("Growth Rate")
    plt.xlim([10,60])
    plt.ylim([0,1.1])
    plt.legend(["Salmonella","Bacillus","Listeria","Bronchothrix"],loc="upper right")
    plt.show()
    #Plotting growth rate by temperature for the four types of bacteria

# Function for Statistics

def dataStatistics(data, statistic):
    data = np.ravel(data)
    data = np.array([[data[0::3]], [data[1::3]],[data[2::3]]])
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

# Funktioner til menu

#Function for buttonprompt
def inputNumber(prompt):
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            pass
    return num
    
#Function for menu and menu control
def displayMenu(options):
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    # Get a valid menu choice
    choice = 0
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputNumber("Choose your next move: ")
    return choice

# DEFINITIONS
val = ["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate", "Rows", "Mean Cold Growth rate", "Mean Hot Growth rate","Return"]
menuItems = ["Load Data", "Filter Data", "Show Statistics", "Generate Diagrams", "Quit"]
menuDiagram = ["Number of Bacteria","Growth Rate by Temperature (without connecting lines)","Growth Rate by Temperature (with connecting lines)","Show all three","Return"]
menuData = ["Assign File","Return"]
n = 0
data = []
Adam = 1
Growthmin = 0
Growthmax = 0
FilterType = 0
BacteriaType = 0
Growthrange = np.array([float(Growthmin),float(Growthmax)])
BacteriaTypes = np.array([["salmonella enterica","bacillus", "listeria", " brochothrix thermosphacta"],[1,2,3,4]])
# Plot def
#Sorting data into categories
Salmonella = []
xSal = []
Bacillus = []
xBac = []
Listeria = []
xList = []
Brochothrix = []
xBroc = []
SortedTemp = []
SortedGrowth = []
SortedBact = []



#FINAL LOOP
while True:

    while n == 0: # Main menu
        choice = displayMenu(menuItems) # Displays main menu
        if choice == 1:
            n = 1 # Stays in the main menu
        elif choice == 2:
            n = 0 # Stays in the main menu
            #i = random.randint(0,len(Woof)-1)
            print("Bacteria filter or growth rate filter")
            FilterType = input("Choose filter types: ").lower().split(" and ")
            if FilterType[:] == ["bacteria"]:
                print(BacteriaTypes[0,:])
                Bacteria = input("Choose bacteria types: ").lower()
            if FilterType[:] == ["growth rate"]:
                Growthmin = float(input("Choose minimum growth rate value: "))
                Growthmax = float(input("Choose maximum growth rate value: "))
                if Growthmin < 0 or Growthmax < Growthmin:
                    print("invalid growth rate. Growth rate must be larger than 0 and minimum must be less the maximum")
            if FilterType[:] == ["bacteria","growth rate"] or FilterType[:] == ["growth rate","bacteria"] :
                Bacteria = input("Choose bacteria types: ").lower()
                Growthmin = float(input("Choose minimum growthrate value: "))
                Growthmax = float(input("Choose maximum growthrate value: "))
            else: 
                "invalid input"
            Growthrange = np.array([float(Growthmin),float(Growthmax)])
            BacteriaTypes = np.array([["salmonella enterica","bacillus", "listeria", " brochothrix thermosphacta"],[1,2,3,4]])
            print(dataFilter(dataLoad(L,0), Bacteria, Growthrange))
            
            
        elif choice == 3:
            if len(data) == 0:
                print("Assign file first") 
            else:
                n = 2 # Changes to statistics menu
        elif choice == 4:
            if len(data) == 0:
                print("Assign file first")
            else:
                n = 3 # Changes to graph menu
        elif choice == 5:
             n = 4 # Closes the program
    while n == 1:
        choice = displayMenu(menuData)
        if choice == 1:
            j = 0
            filename = input("Enter filename: ")
            if os.path.exists(filename) == False:
                directory = input("Enter path: ")
                if os.path.exists(directory):
                    j = 1
                    os.chdir(directory)
                    if os.path.exists(filename):
                        data = dataLoad(filename,0)
                        L = dataSort(data)
                        print(dataLoad(filename,1))
                        n = 0
                else:
                    if j == 0:
                        print("Invalid Path")
                    elif j == 1:
                        print("Invalid Filename")
            else:
                data = dataLoad(filename,0)
                print(dataLoad(filename,1))
                n = 0
                L = dataSort(data)
        elif choice == 2:
            n = 0


            
    while n == 2: # Statistics menu
        choice = displayMenu(val) # Displays statistics menu
        
        # Prints values of the chosen choice
        if choice == 1:
            print(dataStatistics(data,val[0]))
        elif choice == 2:
            print(dataStatistics(data,val[1]))
        elif choice == 3:
            print(dataStatistics(data,val[2]))
        elif choice == 4:
            print(dataStatistics(data,val[3]))
        elif choice == 5:
            print(dataStatistics(data,val[4]))
        elif choice == 6:
            print(dataStatistics(data,val[5]))
        elif choice == 7:
            print(dataStatistics(data,val[6]))
        if choice != 8:
            print("With {:d}".format(Adam))
        # Returns you to main menu
        elif choice == 8:
            n = 0
    
    while n == 3: # Graph menu

        choice = displayMenu(menuDiagram) # Displays graph menu
        if choice == 1:
            print(dataHistogram(data)) # Prints histogram of number of bacteria
        elif choice == 2:
            print(dataScatterplot(L[0],L[1],L[2],L[3],L[4],L[5],L[6],L[7],".")) # Prints scatterplot of growth rate by temperature
        elif choice == 3:
            print(dataScatterplot(L[0],L[1],L[2],L[3],L[4],L[5],L[6],L[7],"--")) # Prints scatterplot of growth rate by temperature with lines
        elif choice == 4:
            # Prints both
            print(dataHistogram(data))
            print(dataScatterplot(L[0],L[1],L[2],L[3],L[4],L[5],L[6],L[7],"."))
            print(dataScatterplot(L[0],L[1],L[2],L[3],L[4],L[5],L[6],L[7],"--"))

        
        # Returns to main menu
        elif choice == 5:
            n = 0
    if n == 4: # So we can close the program
        break
