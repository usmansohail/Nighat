import sys, getopt
# import interpretation_classes
import system_tools

def main(argv):
    symbol_file = None
    observation_file = None
    got_symbols = False
    got_observations = False

    try:
        opts, args = getopt.getopt(argv, "s:o:h")
    except getopt.GetoptError:
        print("must include a symbols file, and an observations file")
        sys.exit()
    for opt, arg in opts:
        # print(opt, arg)
        if opt == "-s":
            symbol_file = open(arg, 'r')
            print(symbol_file.read())
            got_symbols = True
        if opt == "-o":
            observation_file = open(arg, 'r')
            print(observation_file.read())
            got_observations = True
        if opt == "-h":
            print("provide a file for the symbol input, and observations. i.e. -i symbols.txt -o observation.txt")
            sys.exit()
    if not got_symbols:
        print("please input symbols")
    if not got_observations:
        print("please input observation file")
    if not got_observations or not got_symbols:
        sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
else:
    print("whoops")
