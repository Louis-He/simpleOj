import os
import subprocess
from subprocess import STDOUT, check_output

from random import randint

def compileProgram():
    print('Compile the programs')
    print('Executing the following commands.')
    print('gcc -o sample answer/answer.c')
    os.system('gcc -o sample answer/answer.c')

    print('gcc -o main submit/main.c')
    command = "gcc -o main submit/main.c"  # the shell command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Launch the shell command:
    output, error = process.communicate()
    error = error.decode('utf-8')

    if(error.find('error')!=-1):
        print('Error: compile time error occured')
        print()
        print('==========Error Information===========')
        print(error)
        return False
    elif(error!=''):
        print('==========Warning Information===========')
        print(error)

    return True

def generateInput():
    f = open('input/input.txt', 'w+')
    a = randint(0, 10)
    f.write(str(a) + '\n')
    f.close()

def runProgram():
    os.system('./sample < input/input.txt > output/answer.txt')

    command = "./main < input/input.txt > output/output.txt"  # the shell command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Launch the shell command:
    try:
        output, error = process.communicate(timeout = 1)
    except subprocess.TimeoutExpired:
        process = subprocess.Popen('pgrep main', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode('utf-8')
        output = output.replace('\n', '')
        print('Process ' + output + ' ran time out.')
        print('Kill process ' + output)
        os.system('kill ' + output)
        error = 'Time out Error.'.encode('utf-8')

    error = error.decode('utf-8')
    if(error != ''):
        print('RunTime Error')
        print(error)
        return False
    return True

def checkDiff():
    r = os.popen('diff output/answer.txt output/output.txt -c')
    text = r.read()
    r.close()
    if(text != ''):
        print()
        r = os.popen('diff output/answer.txt output/output.txt -y -W 50')
        text = r.read()
        r.close()
        print('Difference as follows: [Left: answer; Right: your output]')
        print(text)
        return False
    else:
        return True

if (compileProgram()):
    print('Program Compilation Passed.')
    print('=====================')
    passFlag = True
    print('Check difference..')

    for i in range(10):
        generateInput()
        if(runProgram()):
            if(not checkDiff()):
                passFlag = False
                print('Test Case #' + str(i + 1) + ': FAIL. Abort')
                print('input value')
                r = os.popen('cat input/input.txt')
                print(r.read())
                print('===================')
                print('Test Failed.')
                break
            else:
                print('Test Case #' + str(i + 1) + ': PASS')
        else:
            passFlag = False
            print('Test Case #' + str(i + 1) + ': FAIL. Abort')
            print('input value')
            r = os.popen('cat input/input.txt')
            print(r.read())
            print('===================')
            print('RunTime error occur. \nTest Failed.')
            break

    if passFlag:
        print('===================')
        print('Pass ALL Test Cases')
else:
    print('===================')
    print('Program Compile Failed.')
    print('Test Failed.')