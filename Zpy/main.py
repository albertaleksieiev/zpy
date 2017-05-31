import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Zpy.CmdNew import Cmd



if len(sys.argv) == 2:
    Cmd().process_file(sys.argv[1])

    exit(0)

def main():
    Cmd().cmdloop()

if __name__ == "__main__":
    main()
    #pass
