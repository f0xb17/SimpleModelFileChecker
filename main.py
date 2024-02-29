from platform import system
from pathlib import PureWindowsPath, PurePosixPath

def readModelFile(filePath):
    ###
    # Attempts to read in a .cfg file. 
    # The aim is to find every line that contains an .o3d at the end.
    ###
    lines = []
    try:
        with open(filePath, 'r') as configFile:
            for line in configFile:
                if line.strip().endswith('.o3d'):
                    lines.append(line.strip())
    except FileNotFoundError as err:
        print(f"Error: File '{filePath}' not found: ", err)
    except IsADirectoryError as err:
        print(f"Error: Current path '{filePath}' is a Directory? ", err)
    return lines


def main():
    file = readModelFile('S416LE_1-1-0.cfg')
    try:
        if file:
            print('The following .o3d files were found:')
            for line in file:
                ####
                # The path read in is converted from a Windows path to a POSIX path. 
                # This is necessary because only the Windows convention is ever used in a model file.
                ####
                if system() == "Linux" or system() == "Darwin":
                    print(PurePosixPath(*PureWindowsPath(line).parts))
                else:
                    print(PureWindowsPath(line))
        else:
            raise IOError
    except IOError as err:
        print(f"No .o3d files found? Are you sure it was the correct file? ", err)

if __name__ == "__main__":
    main()