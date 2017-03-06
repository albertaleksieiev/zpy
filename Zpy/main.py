import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Zpy.Cmd import Cmd

def main():
    Cmd().cmdloop()

if __name__ == "__main__":
    main()