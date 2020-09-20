work = input("Hello there! Please enter the work you want to do here: ")
time = input("Enter the time for which you want to do the work here:")
print("Are you sure you want to do",time, "Please answer in <yes/no> only")
while (input() == 'n'):
    time = input("Enter your duration time here ")
    print("Are you sure you want to do", time)
