import os
import random


def shuffle(folder, folderpath, filelist):
    i = 0
    rands = []
    random.seed()
    numfiles = len(filelist)

    print("Started shuffling files in " + folderpath)

    histfile = open(folder + "shufflehistory.txt", "w+")
    histfile.write("Shuffle History for /" + folder + "\noldfilename > newfilename\n")
    for filename in filelist:
        rand = random.randint(0, numfiles - 1)
        while rand in rands:
            rand = random.randint(0, numfiles - 1)
        histfile.write(filename + " > " + str(rand) + filename + "\n")
        os.rename(folderpath + '\\' + filename, folderpath + '\\' + str(rand) + filename)
        rands.append(rand)
        i += 1
        progress = i / numfiles
        if (progress*100) % 5 == 0:
            print(str(int(progress*100)) + "% shuffled!")

    histfile.close()
    print("Completed shuffling files in " + folderpath)


def unshuffle(folder, folderpath, filelist):
    numfiles = len(filelist)

    print("Started unshuffling files in " + folderpath)

    histfile = open(folder + "shufflehistory.txt", "r")
    histfile.readline()
    histfile.readline()
    oldnames = []
    newnames = []
    for item in histfile.readlines():
        names = item.split(" > ")
        oldnames.append(names[0])
        newnames.append(names[1][:-1])

    histfile.close()
    if os.path.exists(folder + "unshufflehistory.txt"):
        oldunhistfile = open(folder + "unshufflehistory.txt", "r")
        oldunhistfile.readline()
        oldunhistfile.readline()
    unhistfile = open(folder + "unshufflehistory.txt", "w+")
    unhistfile.write("Unshuffle History for /" + folder + "\noldfilename > newfilename\n")

    for i in range(numfiles):
        try:
            os.rename(folderpath + '\\' + newnames[i], folderpath + '\\' + oldnames[i])
            unhistfile.write(newnames[i] + " > " + oldnames[i] + "\n")
        except FileNotFoundError:
            unhistfile.write(oldunhistfile.readline())
            pass
        i += 1
        progress = i / numfiles
        if (progress*100) % 5 == 0:
            print(str(int(progress*100)) + "% unshuffled!")

    unhistfile.close()
    print("Completed unshuffling files in " + folderpath)


def get_folder_name(operation):
    folder = input("\nEnter the name of a folder to " + operation + ": ")
    while folder == "" or folder == "/" or folder == "\\":
        confirm = input("WAIT! Are you sure you want to " + operation + " the folder you are currently in? ("
                        + os.getcwd() + ")(Please enter yes or no): ").lower()
        while confirm != "yes" and confirm != "no":
            confirm = input("Please enter yes or no: ").lower()
        if confirm == "yes":
            break
        else:
            folder = input("\nEnter the name of a folder to " + operation + ": ")
    return folder


def get_operation():
    operation = input("Would you like to shuffle or unshuffle? ").lower()
    while operation != "shuffle" and operation != "unshuffle":
        operation = input("Please enter shuffle or unshuffle: ").lower()
    return operation


def main():
    operation = get_operation()
    done = False
    while not done:
        folder = get_folder_name(operation)
        try:
            folderpath = os.getcwd() + '\\' + folder
            filelist = os.listdir(os.getcwd() + '\\' + folder)
            if operation == "shuffle":
                done = True
            elif os.path.exists(folder + "shufflehistory.txt"):
                done = True
            else:
                print("ERROR: " + folderpath + " has never been shuffled before! Unable to unshuffle!\n")
                operation = get_operation()
        except FileNotFoundError as err:
            print(err)
            print("ERROR: Make sure 'shuffle.py' is in the same folder as the one you want to " + operation + "!")
    if operation == "shuffle":
        shuffle(folder, folderpath, filelist)
    else:
        unshuffle(folder, folderpath, filelist)


main()