# LIBRARIES

import math
import numpy as np
import matplotlib.pyplot as plt 

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
            
    data = np.ravel(data)
    data = np.array([[data[0::3]], [data[1::3]],[data[2::3]]])
    if g == 0:
        return data
    elif g == 1:
        return dataError
    else:
        return "Error in function variable"


# Function for plotting diagrams

def dataHistogram(data):
    #Sorting data into categories
    #Plotting number of bacteria in a histogram
    plt.hist(Bact,bins=[0.5,1.5,2.5,3.5,4.5],color = "blue")
    #Constructs correct legends
    labels = ["","Salmonella","Bacillus","Listeria","Brochothrix"]
    plt.xticks(range(len(labels)),labels, size = 'small')
    plt.title("Number of bacteria")
    plt.show()
    #Sorting data by bacteria for plot data

def withLines():
    plt.plot(xSal,Salmonella, "--" ,color = "blue")
    plt.plot(xBac,Bacillus, "--" , color = "orange")
    plt.plot(xList,Listeria, "--" , color = "red")
    plt.plot(xBroc,Brochothrix, "--" , color = "green")
    plt.title("Growth rate by temperature")
    plt.xlabel("Temperature")
    plt.ylabel("Growth Rate")
    plt.xlim([10,60])
    plt.ylim([0,1.1])
    plt.legend(["Salmonella","Bacillus","Listeria","Bronchothrix"],loc="upper right")
    plt.show()
def withoutLines():
    plt.plot(xSal,Salmonella, "." ,color = "blue")
    plt.plot(xBac,Bacillus, "." , color = "orange")
    plt.plot(xList,Listeria, "." , color = "red")
    plt.plot(xBroc,Brochothrix, "." , color = "green")
    plt.title("Growth rate by temperature")
    plt.xlabel("Temperature")
    plt.ylabel("Growth Rate")
    plt.xlim([10,60])
    plt.ylim([0,1.1])
    plt.legend(["Salmonella","Bacillus","Listeria","Bronchothrix"],loc="upper right")
    plt.show()
def dataScatterplot(data,k):
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
    if k == 0:
        withoutLines()
    elif k == 1:
        withLines()
    #Plotting growth rate by temperature for the four types of bacteria

# Function for Statistics

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
arr = [menuItems,val,menuDiagram]
n = 0
data = dataLoad("test.txt",0)
# Plot def
#Sorting data into categories
Temp = np.ravel(data[0,:])
Growth = np.ravel(data[1,:])
Bact = np.ravel(data[2,:])
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
            n = 0 # Stays in the main menu
            print(dataLoad("test.txt",1)) #Prints Places of error in file
        elif choice == 2:
            n = 0 # Stays in the main menu
            print("Adam") # Prints "Adam"
        elif choice == 3:
            n = 1 # Changes to statistics menu
        elif choice == 4:
            n = 2 # Changes to graph menu
        elif choice == 5:
             n = 3 # Closes the program

    while n == 1: # Statistics menu
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
        
        # Returns you to main menu
        elif choice == 8:
            n = 0
    
    while n == 2: # Graph menu

        choice = displayMenu(menuDiagram) # Displays graph menu
        if choice == 1:
            print(dataHistogram(data)) # Prints histogram of number of bacteria
        elif choice == 2:
            print(dataScatterplot(data,0)) # Prints scatterplot of growth rate by temperature
        elif choice == 3:
            print(dataScatterplot(data,1)) # Prints scatterplot of growth rate by temperature with lines
        elif choice == 4:
            # Prints both
            print(dataHistogram(data))
            print(dataScatterplot(data,0))
            print(dataScatterplot(data,1))
        
        # Returns to main menu
        elif choice == 5:
            n = 0
    if n == 3: # So we can close the program
        break
