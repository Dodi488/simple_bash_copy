import sys
import os
from pathlib import Path
import subprocess

builtins = ["exit", "echo", "type", "pwd", "cd"]
path = os.environ.get("PATH", "")
old_cwd = ""

def exit(commands: list):
    sys.exit(0)

def echo(commands: list):
    print(" ".join(commands[1:]))

def type(commands: list):
    if commands[1] in builtins:
        print(f"{commands[1]} is a shell builtin")
    else:
        command = commands[1]
    
        found_path = next(
        (os.path.join(d, command) for d in path.split(os.pathsep) if os.path.isfile(os.path.join(d, command)) and os.access(os.path.join(d, command), os.X_OK)), None)

        if found_path:
            print(f"{command} is {found_path}")
        else:
            print(f"{command}: not found")

def pwd(commands: list):
    print(Path.cwd())

def cd(commands: list):
    new_dir = commands[1]
    global od_cwd

    if new_dir == "~":
        new_dir = os.getenv("HOME")

    if Path(new_dir).exists():
        old_cwd = Path.cwd()
        os.chdir(new_dir)
    else:
        print(f"cd: {new_dir}: No such file or directory")

def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        commands = input()
        if commands == None or commands.isspace():
            continue

        commands = commands.split(" ")

        builtins = {
            "exit": exit,
            "echo": echo,
            "type": type,
            "pwd": pwd,
            "cd": cd
        }

        handler = builtins.get(commands[0])
        if handler:
            handler(commands)
        else:
            found_path = next(
                (os.path.join(d, commands[0]) for d in path.split(os.pathsep) 
                 if os.path.isfile(os.path.join(d, commands[0])) and os.access(os.path.join(d, commands[0]), os.X_OK)), 
                None
            )
            
            if found_path:
                subprocess.run([commands[0]] + commands[1:])
            else:
                print(f"{commands[0]}: command not found")

if __name__ == "__main__":
    main()
