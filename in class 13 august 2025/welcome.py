import os
choice = 0
filename = ""

def menu ():
    global choice
    print('menu\n 1.open Calulator\n 2.open Noteapad\n 3.world\n 4.Exit')
    choice = input('select menu :')

def open_notepad():
    filename = 'C:\\Windows\\Syswow64\\notepad.exe'
    print('Memorandum writing %s' % filename)
    os.system(filename)

def open_calulator():
    filename = 'C:\\Windows\\Syswow64\\calc.exe'
    print('Calculator Number %s' % filename)
    os.system(filename)

def open_world():
    filename = '"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"'
    print('World writing %s' % filename)
    os.system(filename)

while True:
    menu()
    if choice == '1':
        open_calulator()
    elif choice == '2':
        open_notepad()
    elif choice == '3':
        open_world()
    elif choice =='4':
        print('Exit')
        break
    else:
        print('Please select 1-3')