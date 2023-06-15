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

#Interval filter for growthrate
#Growth and Temp are both numpy arrays, while lowerBound and upperBound are float
def GrowthFilter(Growth,Temp,lowerBound,upperBound):
    #Turns all numbers inside Growth and Temp outside the interval lowerBound-upperBound into empty string ""
    Growth[Growth >= upperBound] = ""
    Growth[Growth <= lowerBound] = ""
    Temp[Growth >= upperBound] = ""
    Temp[Growth <= lowerBound] = ""
    #Deletes all empty strings within arrays Growth and Temp
    Growth = np.delete(Growth,Growth=="")
    Temp = np.delete(Temp,Temp=="")
    #Returns the numpy arrays Growth and Temp
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

#Definitions for different menus
val = ["Mean Temperature","Mean Growth rate","Std Temperature","Std Growth rate", "Rows", "Mean Cold Growth rate", "Mean Hot Growth rate","Return"]
menuItems = ["Load Data", "Filter Data", "Show Statistics", "Generate Diagrams", "Quit"]
menuDiagram = ["Number of Bacteria","Growth Rate by Temperature (without connecting lines)","Growth Rate by Temperature (with connecting lines)","Show all three","Return"]
menuData = ["Assign File","Return"]
menuFilter = ["Bacteria", "Growth Rate","Return"]
menuBacteria = ["Salmonella Enterica","Bacillus", "Listeria", "Brochothrix Thermosphacta","ALL OF THEM!!!"]
menuInterval = ["Assign interval","No Interval","Return"]
#Variable for changing to different menus
n = 0
#List for our data
data = []
#List which is used for filter names
Filter = ["Salmonella Enterica","","Bacillus", "","Listeria","", "Brochothrix Thermosphacta","No Filter"]
#Minimum value of growthrate
Growthmin = ""
#Maximum value of growthrate
Growthmax = ""
#Variable for the different filters, as long as it isnt inbetween 0 and 6 there is no filter
m = 7
#Variable for filter menu, so that no matter your choice of interval you get pushed to the bacteria filter menu.
l = 0
#Variable for checking if is path input that is incorrect or filename input that is incorrect
j = 0

#FINAL LOOP
while True:
    #Main menu
    while n == 0: 
        #Displays main menu
        choice = displayMenu(menuItems)
        #Statemenets for which input is returned
        #If choice is not the first, the program will check if file is assigned
        if choice == 1:
            #Changes menu to file menu
            n = 1
        elif choice == 2:
            if len(data) == 0:
                print("Assign file first") 
            else:
                #Changes to filter menu
                n = 2 
        elif choice == 3:
            if len(data) == 0:
                print("Assign file first") 
            else:
                #Changes to statistics menu
                n = 3 
        elif choice == 4:
            if len(data) == 0:
                print("Assign file first")
            else:
                #Changes to graph menu
                n = 4
        elif choice == 5:
             # Closes the program
             n = 5
    #Menu for loading data
    while n == 1:
        #Displays loading data menu
        choice = displayMenu(menuData)
        #Choice for fileassignment
        if choice == 1:
            #File is assigned
            filename = input("Enter filename: ")
            #If statement for checking if file is valid
            if os.path.exists(filename) == False:
                #If file is not in the same directory as python file, directory is asked
                directory = input("Enter path: ")
                #Sort data with the file and directory assigned
                if os.path.exists(directory):
                    j = 1
                    os.chdir(directory)
                    if os.path.exists(filename):
                        #Loads data and sorts data
                        data = dataLoad(filename,0)
                        L = dataSort(data,Growthmin,Growthmax)
                        M = np.concatenate(dataSort(data,Growthmin,Growthmax)[8], axis = 0)
                        L1 = [np.concatenate([L[0],L[2],L[4],L[6]]),np.concatenate([L[1],L[3],L[5],L[7]])]
                        #Prints all errors in data
                        print("There are errors in your file, so i removed them. Here they are: ")
                        print(dataLoad(filename,1))
                        #Returns you to main menu
                        n = 0
                else:
                    #j Checks where theres an error
                    if j == 0:
                        print("Invalid Path")
                    elif j == 1:
                        print("Invalid Filename")
            else:
                #If the file is in directory it starts loading data
                data = dataLoad(filename,0)
                #Prints errors
                print("There are errors in your file, so i removed them. Here they are: ")
                print(dataLoad(filename,1))
                #Sorts data
                L = dataSort(data,Growthmin,Growthmax)
                M = np.concatenate(dataSort(data,Growthmin,Growthmax)[8], axis = 0)
                L1 = [np.concatenate([L[0],L[2],L[4],L[6]]),np.concatenate([L[1],L[3],L[5],L[7]])]
                #Returns to main menu
                n = 0
        #Return to main menu
        elif choice == 2:
            n = 0
    #Filter menu
    while n == 2:
        #By default l is 0 and so interval menu is default
        if l == 0:
            #Menu for changing interval
            choice = displayMenu(menuInterval)
            #Assign interval
            if choice == 1:
                #Asks for floats, if they are not it prints an error message
                while True:
                    try:
                        Growthmin = float(input("Choose minimum growth rate value: "))
                        Growthmax = float(input("Choose maximum growth rate value: "))
                        break
                    except ValueError or Growthmin < 0 or Growthmax < Growthmin:
                        print("Growth interval accepts only numbers, such as 0.1")
                        pass
                #If the interval is invalid it returns you to the interval menu and prints an error message
                if Growthmin < 0 or Growthmax < Growthmin:
                    print("invalid growth rate. Growth rate must be larger than 0 and minimum must be less the maximum")
                    n = 2
                #l is changed to 1 so we change to the menu with bacterial filters
                l = 1

            #No interval / Clear interval
            elif choice == 2:
                #Assigns Growthmin and Growthmax to what the code defines as N/A
                Growthmin,Growthmax = "",""
                #l is changed to 1 so we change to the menu with bacterial filters
                l = 1
            #Return to main menu
            elif choice == 3:
                    n = 0
        #Menu for bacterial filters
        elif l == 1:
            #Displays bacteria menu
            choice = displayMenu(menuBacteria)
            #Salmonella
            if choice == 1:
                #L1 is a list for statistics
                L1 = dataSort(data,Growthmin,Growthmax)[0:2]
                #L is a list for scatterplots
                L = L1
                #m is a marker for the filter
                m = 0
                #M is a list for histograms
                M = dataSort(data,Growthmin,Growthmax)[8][0]
            #Bacillus
            elif choice == 2:
                L1= dataSort(data,Growthmin,Growthmax)[2:4]
                L = L1
                m = 2
                M = dataSort(data,Growthmin,Growthmax)[8][1]
            #Listeria
            elif choice == 3:
                L1= dataSort(data,Growthmin,Growthmax)[4:6]
                L = L1
                m = 4
                M = dataSort(data,Growthmin,Growthmax)[8][2]
            #Brochothrix
            elif choice == 4:
                L1 = dataSort(data,Growthmin,Growthmax)[6:8]
                L = L1
                m = 6
                M = dataSort(data,Growthmin,Growthmax)[8][3]
            #All of them
            else:
                #We need different lists to make 'All of them' work as they come in different formats and are used in different ways
                L = dataSort(data,Growthmin,Growthmax)
                M = np.concatenate(dataSort(data,Growthmin,Growthmax)[8], axis = 0)
                L1 = [np.concatenate([L[0],L[2],L[4],L[6]]),np.concatenate([L[1],L[3],L[5],L[7]])]
                #m just needs to be asigned anything else but 0,2,4,6
                m = 7
            #We change l to 0 again so that if we enter the menu we choose interval first
            l = 0
            #We return to main menu
            n = 0 
   
    #Statistics menu
    while n == 3:
        #Displays statistics menu
        choice = displayMenu(val)

        #Prints values of the chosen choice
        if choice == 1:
            print(dataStatistics(np.array(L1),val[0]))
        elif choice == 2:
            print(dataStatistics(np.array(L1),val[1]))
        elif choice == 3:
            print(dataStatistics(np.array(L1),val[2]))
        elif choice == 4:
            print(dataStatistics(np.array(L1),val[3]))
        elif choice == 5:
            print(dataStatistics(np.array(L1),val[4]))
        elif choice == 6:
            print(dataStatistics(np.array(L1),val[5]))
        elif choice == 7:
            print(dataStatistics(np.array(L1),val[6]))
        #Prints which filter is used so long choice isnt return
        if choice != 8:
            print("With bacterialfilter {filter} and growthrateinterval {min}-{max}".format(filter = Filter[m],min = Growthmin, max = Growthmax))
        #Returns you to main menu
        elif choice == 8:
            n = 0
    
    #Graph menu
    while n == 4:
        #Displays graph menu
        choice = displayMenu(menuDiagram) 

        if choice == 1:
            #Prints histogram of number of bacteria
            print(dataHistogram(M)) 
        elif choice == 2:
            #Prints scatterplot of growth rate by temperature
            print(dataScatterplot(L,m,".")) 
        elif choice == 3:
            #Prints scatterplot of growth rate by temperature with lines
            print(dataScatterplot(L,m,"--"))
        elif choice == 4:
            #Prints alle three
            print(dataHistogram(M))
            print(dataScatterplot(L,m,"."))
            print(dataScatterplot(L,m,"--"))
        # Returns to main menu
        elif choice == 5:
            n = 0
    #If true it closes the program
    if n == 5:
        break
