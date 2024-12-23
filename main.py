import sys
from os.path import expanduser
import os
import shlex
import subprocess

def execute_command(command,command_args, outputFile=sys.stdout,isTwo=False):
    arr = ['echo', 'exit', 'type', 'pwd','cd']
    PATH=os.environ["PATH"]
    if (command == "echo"):
        result = subprocess.run(["echo"]+command_args, capture_output=True, text=True)
        if (result.stdout and isTwo==False):
            outputFile.write(result.stdout)
        elif (result.stdout):
            sys.stdout.write(result.stdout)
        if (result.stderr):
            outputFile.write(result.stderr)
    elif (command == "pwd"):
        print(os.getcwd(),file=outputFile)
    elif (command == "cd"):
        if len(command_args)==0:
            print("cd: missing argument",file=outputFile)
        else:
            togoPath = command_args[0]
            try:
                os.chdir(expanduser(togoPath))
            except OSError:
                print(f"cd: {togoPath}: No such file or directory",file=outputFile)
    elif (command == "type"):
        if (len(command_args) > 0):
            target_cmd=command_args[0]
            if (target_cmd in arr):
                print(f'{target_cmd} is a shell builtin',file=outputFile)
            else:
                cmd_path = None
                splittedPath = PATH.split(":")
                for path in splittedPath:
                    if ( os.path.isfile(f'{path}/{target_cmd}')):
                        cmd_path = f'{path}/{target_cmd}'
                        break

                if (cmd_path):
                    print(f'{target_cmd} is {cmd_path}',file=outputFile)
                else:
                    print(f'{target_cmd}: not found',file=outputFile)
        else:
            print("Usage: type <command>",file=outputFile)
    else:
        paths = PATH.split(":")
        fullPath = None
        for path in paths:
            if (os.path.isfile(f'{path}/{command}')):
                fullPath = f'{path}/{command}'
                break
        if (fullPath):
            #run file
            try:
                result = subprocess.run([fullPath]+command_args, capture_output=True, text=True)
                if (result.stdout and isTwo==False):
                    outputFile.write(result.stdout)
                elif (result.stdout):
                    sys.stdout.write(result.stdout)
                if (result.stderr):
                    if isTwo:
                        outputFile.write(result.stderr)
                    else:
                        sys.stdout.write(result.stderr)
            except Exception as e:
                print(f"Error executing {command}: {e} ",file=outputFile)
            
        else:
            print(f'{command}: command not found',file=outputFile)

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command_input = input().strip()
        if command_input == "exit 0" or command_input == "exit":
            break
        if ('>>' in command_input):
            commandPart, redirectionPart = command_input.split('>>',1);
            commandPart = commandPart.strip()
            filePath = redirectionPart.strip()

            # Handle optional file descriptor (e.g., "1>" or "2>")
            isTwo = False
            if commandPart.endswith("1"):
                commandPart = commandPart[:-2].strip()
            if commandPart.endswith("2"):
                isTwo = True
                commandPart = commandPart[:-2].strip()
            if not filePath:
                print("Syntax error: no file specified for redirection")
                continue

            splittedCommand = shlex.split(commandPart)
            commandName = splittedCommand[0]
            command_args = splittedCommand[1:]
            try:
                with open(filePath, 'a') as outputFile:
                    execute_command(commandName,command_args, outputFile=outputFile,isTwo=isTwo)
            except Exception as e:
                continue
        if ('>' in command_input):
            commandPart, redirectionPart = command_input.split('>',1);
            commandPart = commandPart.strip()
            filePath = redirectionPart.strip()

            # Handle optional file descriptor (e.g., "1>" or "2>")
            isTwo = False
            if commandPart.endswith("1"):
                commandPart = commandPart[:-2].strip()
            if commandPart.endswith("2"):
                isTwo = True
                commandPart = commandPart[:-2].strip()
            if not filePath:
                print("Syntax error: no file specified for redirection")
                continue

            splittedCommand = shlex.split(commandPart)
            commandName = splittedCommand[0]
            command_args = splittedCommand[1:]
            try:
                with open(filePath, 'w') as outputFile:
                    execute_command(commandName,command_args, outputFile=outputFile,isTwo=isTwo)
            except Exception as e:
                continue
        else:
            splittedCommand = shlex.split(command_input)
            commandName = splittedCommand[0]
            command_args = splittedCommand[1:]
            execute_command(commandName,command_args)


if __name__ == "__main__":
    main()
