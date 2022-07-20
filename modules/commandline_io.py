import sys
import getopt

_getoptSTRING = "hi:o:v"
_getoptOptionsARRAY = ["help","import-file=","export-directory=","version","data-type=","data-format=","verbose"]

def readCommandlineArguments(argv,settingsDICT):

    try:
        opts, args = getopt.getopt(argv,_getoptSTRING,_getoptOptionsARRAY)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print("Help")
                sys.exit()
            elif opt in ("-i", "--import-file"):
                settingsDICT["import"]["filepath"] = arg
            elif opt in ("-o", "--export-directory"):
                settingsDICT["export"]["directory"] = arg
            elif opt == "--data-type=":
                settingsDICT["import"]["datatype"] = arg
            elif opt == "--data-format=":
                settingsDICT["import"]["dataformat"] = arg
            elif opt in ("-v", "--version"):
                print("VERSION")
            elif opt == "--verbose":
                print("VERBOSE")

    except getopt.GetoptError:
        print("Getopt Error")
        sys.exit()

    return settingsDICT

    

