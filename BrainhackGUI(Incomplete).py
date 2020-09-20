import tkinter as tk
from tkinter import ttk
import time

events = [] #List of user's events that grows with each input
duration = [] #List of user's event duration corresponding with the event[] list with shared index
organizedSchedule = [] #List of 3 tuples: (Event, EventStartTime, EventEndTime)

wakeTime = -1 #User's chosen time to wake up
sleepDuration = -1 #User's chosen amount of sleep IN HOURS


def clickSubmitSleep():
    #basic variable initializations
    entry = entryTextbox.get()
    try:
        if (int(entry) < 6):
            errorLabel.configure(text = "Invalid input: You should start sleeping for at least 6 hours or more!")
        else:
            sleepDuration = int(entry)
            errorLabel.configure(text = "Sleep duration accepted!")
            instructionLabel.configure(text = "When do you plan to wake up? (Military time): ")
            sleepDurationLabel.configure(text = int(entry))
    except ValueError:
        errorLabel.configure(text = "Invalid input: Enter a number!")

def clickSubmitWake():
    entry = entryTextbox.get()
    try:
        if (int(entry) < 0 or int(entry) > 2359):
            errorLabel.configure(text = "Invalid input: Enter a number >= 0000 and < 2359!")
        else:
            wakeTime = int(entry)
            errorLabel.configure(text = "Wake time accepted!")
            instructionLabel.configure(text = "Input an event name and submit, then its duration and submit")
            WakeLabel.configure(text = entry.zfill(4))
    except ValueError:
        errorLabel.configure(text = "Invalid input: Enter a number!")

def clickSubmitEvent():
    entry = entryTextbox.get()
    events.append(entry)
    errorLabel.configure(text = "Event name submitted!")

def clickSubmitDuration():
    entry = entryTextbox.get()
    try:
        if (int(entry) < 0):
            errorLabel.configure(text = "Invalid input: Enter a number > 0!")
        else:
            wakeTime = int(entry)
            errorLabel.configure(text = "Event duration accepted!")
            instructionLabel.configure(text = "Input an event name and submit, then its duration and submit")
            duration.append(entry)
            #WakeLabel.configure(text = entry.zfill(4))
    except ValueError:
        errorLabel.configure(text = "Invalid input: Enter a number!")
    
def clickSchedule():
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

    if (newCurrentTime > bedTime):
        print("Your schedule is too large to fit in one day!")
    else:
    #print schedule
        for event in organizedSchedule:
            print(str(event[1]).zfill(4), "to", str(event[2]).zfill(4), ":", event[0])

        #print freetime/bedtime
        print(str(newCurrentTime).zfill(4), "to", str(bedTime).zfill(4),": Freetime!")
        print(str(bedTime).zfill(4), "to", str(wakeTime).zfill(4), ": Sleep!")
        print("If you have a lot of free time and haven't exercised yet, make sure you get some!")


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

window = tk.Tk()
window.title("Brainhack Schedule App")
window.minsize(600,400)

instructionLabel = ttk.Label(window, text = "How long do you plan on sleeping for in hours? (Must be 6+ hours): ")
instructionLabel.grid(column = 0, row = 0)
#instructionLabel.configure(text = "test")

entry = tk.StringVar()
#entry = ""
entryTextbox = ttk.Entry(window, width = 15, textvariable = entry)
entryTextbox.grid(column = 0, row = 1)

errorLabel = ttk.Label(window, text = "")
errorLabel.grid(column = 0, row = 2)

submitSleepButton = ttk.Button(window, text = "Submit Sleep Duration", command = clickSubmitSleep)
submitSleepButton.grid(column= 0, row = 3)
submitWakeButton = ttk.Button(window, text = "Submit Wakeup Time", command = clickSubmitWake)
submitWakeButton.grid(column= 0, row = 4)
submitEventButton = ttk.Button(window, text = "Submit Event", command = clickSubmitEvent)
submitEventButton.grid(column= 0, row = 5)
submitDurationButton = ttk.Button(window, text = "Submit Event Duration", command = clickSubmitDuration)
submitDurationButton.grid(column= 0, row = 6)

sleepDurationLabel = ttk.Label(window, text = str(sleepDuration))
sleepDurationLabel.grid(column = 8, row = 1)
sleepDurationLabel2= ttk.Label(window, text = "Sleep Duration: ")
sleepDurationLabel2.grid(column = 7, row = 1)
WakeLabel = ttk.Label(window, text = str(wakeTime))
WakeLabel.grid(column = 8, row = 2)
WakeLabel2= ttk.Label(window, text = "Wakeup Time: ")
WakeLabel2.grid(column = 7, row = 2)

scheduleLabel = ttk.Label(window, text = "Schedule:")
scheduleLabel.grid(column = 7, row = 4)
#scheduleOutput = ttk.

button = ttk.Button(window, text = "Create Schedule", command = clickSchedule)
button.grid(column= 0, row = 10)

window.mainloop()
