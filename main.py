import time
import tkinter as tk
from tkinter import ttk

events = [] #List of user's events that grows with each input
duration = [] #List of user's event duration corresponding with the event[] list with shared index
organizedSchedule = [] #List of 3 tuples: (Event, EventStartTime, EventEndTime)

wakeTime = -1 #User's chosen time to wake up
sleepDuration = -1 #User's chosen amount of sleep IN HOURS

def addMinutes(mins, time): #Does appropriate math to add given Minutes to Time in military time
    minsToHours = mins // 60
    tensOnes = time % 100
    tensOnes += mins
    newTensOnes = tensOnes % 60
    hoursToAdd = tensOnes // 60
    thousHunds = time // 100
    newThousHunds = thousHunds + hoursToAdd
    if (newThousHunds > 23):
        newThousHunds %= 24
    newTime = (newThousHunds * 100) + newTensOnes
    return newTime

#Assumes 10s and 1s is <60
def militaryToSeconds(milTime): 
    tensOnes = milTime % 100
    #ones = milTime % 1000
    totalSeconds = (milTime / 100) * 60 * 60 #Converts hours to seconds
    totalSeconds += tensOnes * 60 #Converts minutes to seconds
    return totalSeconds

def timeConvert(seconds):
    return time.strftime("%H:%M", time.gmtime(seconds))

############ MAIN STARTS HERE ################
#debug prints
print(str(addMinutes(90, 2300)).zfill(4))

#basic variable initializations
while True:
    try:
        sleepDuration = int(input("How long do you plan on sleeping for in hours? (Must be 6+ hours): "))
    except ValueError:
        print("Invalid input: Enter a number!")
        continue
    if (sleepDuration < 6):
        print("Invalid input: You should start sleeping for at least 6 hours or more!")
        continue
    else:
        break

while True:
    try:
        wakeTime = int(input("When do you plan to wake up? (Military time): "))
    except ValueError:
        print("Invalid input: Enter a number!")
        continue
    if (wakeTime < 0 or wakeTime > 2359):
        print("Invalid input: Enter a number >= 0000 and < 2359!")
        continue
    else:
        break


#adding events
while True:
    try:
        createEvent = input("Do you have any work to do? <yes/no>: ")
    except:
        continue
    if (createEvent == 'n' or createEvent == 'no'):
        break
    if (createEvent == 'y' or createEvent == 'yes'):
        events.append(input("Enter event: "))
        #First duration input
        while True:
            try:
                time = int(input("What's the expected time to complete this work? (mins): "))
            except ValueError:
                print("Invalid input: Enter a number!")
                continue
            if (time < 0):
                print("Invalid input: Enter a number > 0!")
                continue
            else:
                break

        #Duration confirmation
        while True:
            try:
                print("Are you sure you want to do work for", time, "minutes? Please answer <yes/no>: ")
                confirmDuration = input()
            except:
                continue
            if (confirmDuration == 'y' or confirmDuration == 'yes'):
                break
            if (confirmDuration == 'n' or confirmDuration == 'no'):
                #Confirmation failed, user enters input duration again until 'y'
                while True:
                    try:
                        time = int(input("What's the expected time to complete this work? (mins): "))
                    except ValueError:
                        print("Invalid input: Enter a number!")
                        continue
                    if (time < 0):
                        print("Invalid input: Enter a number > 0!")
                        continue
                    else:
                        break
            else:
                print("Invalid input: Enter yes/no")
                continue
        duration.append(time)
        print("Event added.")
        continue
    else:
        print("Invalid input: Enter yes/no")
        continue


#more debug prints
print("Events list: ", events)
print("Duration list: ", duration)

#create organizedSchedule
currentTime = wakeTime
eventCounter = 0
didExercise = False
newCurrentTime = 0
for event in events:
    eventDurationIndex = events.index(event)
    newCurrentTime = addMinutes(int(duration[eventDurationIndex]), currentTime)
    organizedSchedule.append((event, currentTime, newCurrentTime))
    currentTime = newCurrentTime
    eventCounter += 1
    if (eventCounter == 3):
        organizedSchedule.append(("30 Minute Break!", newCurrentTime, addMinutes(30, newCurrentTime)))
        currentTime = addMinutes(30, newCurrentTime)
        #eventCounter = 0
    if (eventCounter == 6 and didExercise == False):
        organizedSchedule.append(("60 Minute Exercise!", newCurrentTime, addMinutes(60, newCurrentTime)))
        currentTime = addMinutes(60, newCurrentTime)
        didExercise = True
    elif (eventCounter == 6 and didExercise):
        organizedSchedule.append(("30 Minute Break!", newCurrentTime, addMinutes(30, newCurrentTime)))
        currentTime = addMinutes(30, newCurrentTime)
        eventCounter = 0

if (not events):
    print("No events filled out!")
    newCurrentTime = wakeTime

#brute force find bedtime
sleepDurationMins = sleepDuration * 60
bedTime = 0
#add 1 to bedTime until the correct value is found, when bedTime + sleepDuration == wakeTime
while (int(addMinutes(sleepDurationMins, bedTime)) != int(wakeTime)):
    bedTime = addMinutes(1, bedTime)

#print schedule
for event in organizedSchedule:
    print(str(event[1]).zfill(4), "to", str(event[2]).zfill(4), ":", event[0])

    #print freetime/bedtime
    print(str(newCurrentTime).zfill(4), "to", str(bedTime).zfill(4),": Freetime!")
    print(str(bedTime).zfill(4), "to", str(wakeTime).zfill(4), ": Sleep!")
    print("If you have a lot of free time and haven't exercised yet, make sure you get some!")


window = tk.Tk()
window.title("Brainhack Schedule App")
window.minsize(600,400)

instructionLabel = ttk.Label(window, text = "Enter")
