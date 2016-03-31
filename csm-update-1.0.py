# Community Symbol Map (CSM) batch updater
import sys
# ----------------------------------------


# Set up some fancy terminal colors for fun
class bcolors:
    BLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def blueify(input):
    return bcolors.BLUE + input + bcolors.ENDC


def warningify(input):
    return bcolors.WARNING + input + bcolors.ENDC


def failify(input):
    return bcolors.FAIL + input + bcolors.ENDC

# Put in the same folder as your symbol map which should be
# named 'GALE01.map', also include a file named 'update.txt'
# which contains a list of symbol address and names to update.
# update.txt should be formatted as [address] [symbol_name]
# example:
#          80abc123 my_symbol_name
# each symbol gets its own line.

# Open the files needed
try:
    csm = open("GALE01.map", "r+")
    outfile = open("GALE01updated.map", "w")
    updatefile = open("update.txt", "r")
except IOError as e:
    print bcolors.FAIL + """
    Error opening the required files
    make sure they're named 'GALE01.txt' and 'update.txt'
    case-sensitive!
    """ + bcolors.ENDC
    sys.exit()

# print "Name of the file: ", csm.name
# print "Closed or not : ", csm.closed
# print "Opening mode : ", csm.mode
# print "Softspace flag : ", csm.softspace

# Declare our variables
csm_string = csm.read()
updatefile_string = updatefile.read()
updates_dictionary = dict()

# Populate a dictionary with key-value pairs from update.txt
for line in updatefile_string.strip().split("\n"):
    line_array = line.split()
    updates_dictionary[line_array[0]] = line_array[1]


def create_output_string(input_string):
    change_count = 0
    output = ""

    for line in input_string.strip().split("\n"):
        if line[:8] in updates_dictionary:
            newname = updates_dictionary[line[:8]]
            oldname = line.strip()[29:]

            if " zz_" in line:
                output += line.replace(line[29:], newname) + "\n"
                print oldname + " ---> " + blueify(newname)
                change_count += 1

                continue
            else:
                # raw_input returns the empty string for "enter"
                yes = set(['yes', 'y', 'ye', ''])
                no = set(['no', 'n'])

                print "Overwrite " + blueify(oldname) + \
                      " with " + blueify(newname) + "?: "

                while True:
                    choice = raw_input().lower()
                    if choice in yes:
                        output += line.replace(
                                    line[29:], newname) + "\n"
                        print oldname + " ---> " + blueify(newname)
                        change_count += 1
                        break
                    elif choice in no:
                        break
                    else:
                        print "Please respond with 'yes' or 'no' \
                        (you may hit enter in place of 'yes')\n"

                continue
        output += line + "\n"

    print "Successfully updated %i symbol names." % change_count
    return output

outfile.write(create_output_string(csm_string))
