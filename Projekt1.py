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
def GrowthFilter(Growth,Temp,lowerBound,upperBound): 
    Growth[Growth >= upperBound] = 0
    Growth[Growth <= lowerBound] = 0
    Temp[Growth >= upperBound] = 0
    Temp[Growth <= lowerBound] = 0
    Growth = np.delete(Growth,Growth==0)
    Temp = np.delete(Temp,Temp==0)
    return Growth, Temp

def dataSort(data,Growthmin,Growthmax):
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
    if Growthmin and Growthmax != "":
        Salmonella,xSal = GrowthFilter(np.array(Salmonella),np.array(xSal),Growthmin,Growthmax)[0],GrowthFilter(np.array(Salmonella),np.array(xSal),Growthmin,Growthmax)[1]
        Bacillus,xBac = GrowthFilter(np.array(Bacillus),np.array(xBac),Growthmin,Growthmax)[0],GrowthFilter(np.array(Bacillus),np.array(xBac),Growthmin,Growthmax)[1]
        Listeria, xList = GrowthFilter(np.array(Listeria),np.array(xList),Growthmin,Growthmax)[0], GrowthFilter(np.array(Listeria),np.array(xList),Growthmin,Growthmax)[1]
        Brochothrix, xBroc = GrowthFilter(np.array(Brochothrix),np.array(xBroc),Growthmin,Growthmax)[0],GrowthFilter(np.array(Brochothrix),np.array(xBroc),Growthmin,Growthmax)[1]

    Bact = [np.ones(len(Salmonella)),2 * np.ones(len(Bacillus)), 3 * np.ones(len(Listeria)),4 * np.ones(len(Brochothrix))]
    return Salmonella, xSal, Bacillus, xBac, Listeria, xList, Brochothrix, xBroc, Bact

def dataHistogram(data):
    #Sorting data into categories
    #Plotting number of bacteria in a histogram
    Bact = data
    plt.hist(Bact,bins=[0.5,1.5,2.5,3.5,4.5],color = "blue")
    #Constructs correct legends
    labels = ["","Salmonella","Bacillus","Listeria","Brochothrix"]
    plt.xticks(range(len(labels)),labels, size = 'small')
    plt.title("Number of bacteria with filter {filter} and interval {min}-{max}".format(filter = Adam[m],min = Growthmin, max = Growthmax))
    plt.show()
    #Sorting data by bacteria for plot data

def dataScatterplot(sortedData,m,k):
    if m == 0:
        xSal = sortedData[1]
        Salmonella = sortedData[0]
        plt.plot(xSal,Salmonella, k ,color = "blue")
        plt.legend(["Salmonella"],loc="upper right")
    elif m == 2:
        xBac = sortedData[1]
        Bacillus= sortedData[0]
        plt.plot(xBac,Bacillus, k , color = "orange")
        plt.legend(["Bacillus"],loc="upper right")
    elif m == 4:
        xList = sortedData[1]
        Listeria = sortedData[0]
        plt.plot(xList,Listeria, k , color = "red")
        plt.legend(["Listeria"],loc="upper right")
    elif m == 6:
        xBroc = sortedData[1]
        Brochothrix = sortedData[0]
        plt.plot(xBroc,Brochothrix, k , color = "green")
        plt.legend(["Brochothrix"],loc="upper right")
    else:
        xSal = sortedData[1]
        Salmonella = sortedData[0]
        plt.plot(xSal,Salmonella, k ,color = "blue")
        xBac = sortedData[3]
        Bacillus= sortedData[2]
        plt.plot(xBac,Bacillus, k , color = "orange")
        xList = sortedData[5]
        Listeria = sortedData[4]
        plt.plot(xList,Listeria, k , color = "red")
        xBroc = sortedData[7]
        Brochothrix = sortedData[6]
        plt.plot(xBroc,Brochothrix, k , color = "green")
        plt.legend(["Salmonella","Bacillus","Listeria","Brochothrix"],loc="upper right")
    plt.title("Growth rate by temperature  with filter {filter} and interval {min}-{max}".format(filter = Adam[m],min = Growthmin, max = Growthmax))
    plt.xlabel("Temperature")
    plt.ylabel("Growth Rate")
    plt.xlim([10,60])
    plt.ylim([0,1.1])
    plt.show()
    #Plotting growth rate by temperature for the four types of bacteria

# Function for Statistics

# Function for Statistics
# dataStatistics returns mean values, standard deviation, row count and more
# for temperature and growth rate
#Input: Data from datasorted (numpy array) and statistics (string)
#Output: result of statistical value (float)    
def dataStatistics(data, statistic):
    ValidInput = ["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate", "Rows", "Mean Cold Growth rate", "Mean Hot Growth rate"]
    if statistic not in ValidInput:
        result = "Invalid input, please type valid input"
    else:
        #Mean temperature
        if statistic == ValidInput[0]:
            result = np.mean(data[1])
        #Mean growth rate
        elif statistic == ValidInput[1]:
            result = np.mean(data[0])
        #Std temperature
        elif statistic == ValidInput[2]:
            result = np.std(data[1])
        #Std growth rate
        elif statistic == ValidInput[3]:
            result = np.std(data[0])
        #Rows
        elif statistic == ValidInput[4]:
            result = len(data[1])
        #Mean of cold growth rate
        elif statistic == ValidInput[5]:
            result = np.mean(data[0][data[1] < 20])
        #Mean of hot growth rate
        elif statistic == ValidInput[6]:
            result = np.mean(data[0][data[1] > 50])
    return result

# Functions for menu

#Function for buttonprompt
# InputNumber: Takes in number and returns error message if invalid input
# Input: number (string)
# Output: number (float)
def inputNumber(prompt):
    while True:
        #Turns input to float
        try:
            num = float(input(prompt))
            break
        #Ensures valid input by returning error message
        except ValueError:
            print("Wrong Input, type the number of the menu you want to select")
            pass
    return num


#Function for menu and menu control
#Displaymenu: displays a numbered list of menu items
#Input: Options (string array)
#Output: formatted numbers and strings
def displayMenu(options):
    #For loop for displaying items from option
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    # Get a valid menu choice
    choice = 0
    #Ensures a valid choice input
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputNumber("Choose your next move: ")
    return choice

# DEFINITIONS
val = ["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate", "Rows", "Mean Cold Growth rate", "Mean Hot Growth rate","Return"]
menuItems = ["Load Data", "Filter Data", "Show Statistics", "Generate Diagrams", "Quit"]
menuDiagram = ["Number of Bacteria","Growth Rate by Temperature (without connecting lines)","Growth Rate by Temperature (with connecting lines)","Show all three","Return"]
menuData = ["Assign File","Return"]
menuFilter = ["Bacteria", "Growth Rate","Return"]
menuBacteria = ["Salmonella Enterica","Bacillus", "Listeria", "Brochothrix Thermosphacta","ALL OF THEM!!!"]
menuInterval = ["Assign interval","No Interval","Return"]
n = 0
data = []
Adam = ["Salmonella Enterica","","Bacillus", "","Listeria","", "Brochothrix Thermosphacta","No Filter"]
Growthmin = ""
Growthmax = ""
m = 7
l = 0
#FINAL LOOP
while True:

    while n == 0: # Main menu
        choice = displayMenu(menuItems) # Displays main menu
        if choice == 1:
            n = 1 # Stays in the main menu
        elif choice == 2:
            if len(data) == 0:
                print("Assign file first") 
            else:
                n = 2
        elif choice == 3:
            if len(data) == 0:
                print("Assign file first") 
            else:
                n = 3 # Changes to statistics menu
        elif choice == 4:
            if len(data) == 0:
                print("Assign file first")
            else:
                n = 4 # Changes to graph menu
        elif choice == 5:
             n = 5 # Closes the program
    while n == 1:
        choice = displayMenu(menuData)
        if choice == 1:
            filename = input("Enter filename: ")
            if os.path.exists(filename) == False:
                directory = input("Enter path: ")
                if os.path.exists(directory):
                    j = 1
                    os.chdir(directory)
                    if os.path.exists(filename):
                        data = dataLoad(filename,0)
                        L = dataSort(data,"","")
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
                L = dataSort(data,Growthmin,Growthmax)
                M = np.concatenate(dataSort(data,Growthmin,Growthmax)[8], axis = 0)
                L1 = [np.concatenate([L[0],L[2],L[4],L[6]]),np.concatenate([L[1],L[3],L[5],L[7]])]
        elif choice == 2:
            n = 0
    while n == 2:
        if l == 0:
            choice = displayMenu(menuInterval)
            if choice == 1:
                while True:
                    try:
                        Growthmin = float(input("Choose minimum growth rate value: "))
                        Growthmax = float(input("Choose maximum growth rate value: "))
                        break
                    except ValueError or Growthmin < 0 or Growthmax < Growthmin:
                        print("Growth interval accepts only numbers, such as 0.1")
                        pass
                if Growthmin < 0 or Growthmax < Growthmin:
                    print("invalid growth rate. Growth rate must be larger than 0 and minimum must be less the maximum")
                    n = 2
                l = 1
            elif choice == 2:
                Growthmin,Growthmax = "",""
                l = 1
            elif choice == 3:
                    n = 0
        elif l == 1:
            choice = displayMenu(menuBacteria)
            if choice == 1:
                L1 = dataSort(data,Growthmin,Growthmax)[0:2]
                L = L1
                m = 0
                M = dataSort(data,Growthmin,Growthmax)[8][0]
            elif choice == 2:
                L1= dataSort(data,Growthmin,Growthmax)[2:4]
                L = L1
                m = 2
                M = dataSort(data,Growthmin,Growthmax)[8][1]
            elif choice == 3:
                L1= dataSort(data,Growthmin,Growthmax)[4:6]
                L = L1
                m = 4
                M = dataSort(data,Growthmin,Growthmax)[8][2]
            elif choice == 4:
                L1 = dataSort(data,Growthmin,Growthmax)[6:8]
                L = L1
                m = 6
                M = dataSort(data,Growthmin,Growthmax)[8][3]
            else:
                L = dataSort(data,Growthmin,Growthmax)
                M = np.concatenate(dataSort(data,Growthmin,Growthmax)[8], axis = 0)
                print ( L)
                L1 = [np.concatenate([L[0],L[2],L[4],L[6]]),np.concatenate([L[1],L[3],L[5],L[7]])]
                m = 7
            l = 0
            n = 0    
    while n == 3: # Statistics menu
        choice = displayMenu(val) # Displays statistics menu
        # Prints values of the chosen choice
        # Prints mean value of temperature
        if choice == 1:
            print(dataStatistics(np.array(L1),val[0]))
        # Prints mean value of growth rate
        elif choice == 2:
            print(dataStatistics(np.array(L1),val[1]))
        # Prints std of temperature
        elif choice == 3:
            print(dataStatistics(np.array(L1),val[2]))
        # Prints std of growth rate
        elif choice == 4:
            print(dataStatistics(np.array(L1),val[3]))
        # Prints number of rows
        elif choice == 5:
            print(dataStatistics(np.array(L1),val[4]))
        # Prints mean value of cold growth rate 
        elif choice == 6:
            print(dataStatistics(np.array(L1),val[5]))
        # Prints mean value of hot growth rate
        elif choice == 7:
            print(dataStatistics(np.array(L1),val[6]))
        if choice != 8:
            print("With filter {filter} and interval {min}-{max}".format(filter = Filter[m],min = Growthmin, max = Growthmax))
        # Returns you to main menu
        elif choice == 8:
            n = 0
    
    while n == 4: # Graph menu

        choice = displayMenu(menuDiagram) # Displays graph menu
        if choice == 1:
            print(dataHistogram(M)) # Prints histogram of number of bacteria
        elif choice == 2:
            print(L)
            print(dataScatterplot(L,m,".")) # Prints scatterplot of growth rate by temperature
        elif choice == 3:
            print(dataScatterplot(L,m,"--")) # Prints scatterplot of growth rate by temperature with lines
        elif choice == 4:
            # Prints both
            print(dataHistogram(M))
            print(dataScatterplot(L,m,"."))
            print(dataScatterplot(L,m,"--"))
        # Returns to main menu
        elif choice == 5:
            n = 0
    if n == 5: # So we can close the program
        break
