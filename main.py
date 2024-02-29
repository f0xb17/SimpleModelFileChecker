from platform import system
from pathlib import PureWindowsPath, PurePosixPath
from os import path


existingFiles = []
noneExistingFiles = []

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

def fileExists(filePath):
    ####
    # Checks whether the specified file exists within the file path or not.
    ####
    if path.exists(filePath):
        existingFiles.append(filePath)
    else:
        noneExistingFiles.append(filePath)

def main():
    file = readModelFile('S416LE_1-1-0.cfg')
    try:
        if file:
            for line in file:
                ####
                # The path read in is converted from a Windows path to a POSIX path. 
                # This is necessary because only the Windows convention is ever used in a model file.
                ####
                if system() == "Linux" or system() == "Darwin":
                    ####
                    # Converts a Windows file path to a POSIX file path, if user is using Linux or macOS. 
                    ####
                    fileExists(PurePosixPath(*PureWindowsPath(line).parts))
                else:
                    ####
                    # Or simply use the normal Windows file path, if user is using Windows or any other OS. 
                    # Philosophical question: Is there anything other than Windows file paths or POSIX file paths?
                    ####
                    fileExists(PureWindowsPath(line))
            print("---------------------------------------------------")
            print('The following .o3d file(s) could be found:')
            print("---------------------------------------------------")
            for existingFile in existingFiles:
                print(existingFile)
            print("---------------------------------------------------")
            print('The following .o3d file(s) could not be found:')
            print("---------------------------------------------------")
            for noneExistingFile in noneExistingFiles:
                print(noneExistingFile)
        else:
            raise IOError
    except IOError as err:
        print(f"No .o3d files found? Are you sure it was the correct file? ", err)

if __name__ == "__main__":
    main()