
import getopt, sys, string

def parse_input(args):
    """Returns a the input and output filenames based on sys.argv input."""
    ifilename = ''
    ofilename = ''

    try:
        opts, args = getopt.getopt(args, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print_help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            ifilename = arg
        elif opt in ("-o", "--ofile"):
            ofilename = arg

    if ifilename == "":
        print_help()
        sys.exit(2)

    return (ifilename, ofilename)

def print_help():
    print "script_prep.py -i <input.script> [-o <output.java>]"

def write_output(ofilename, output):
    with open(ofilename, "w") as java_file:
        java_file.write(output)

def build_package_name(filename):
    filename = filename.replace(".scriptlib", "")
    filename = filename.replace(".script", "")

    pos = filename.find("script/")
    if pos >= 0:
        filename = filename[pos:]
    elif filename[0] == "/":
        filename = filename[1:]
    elif filename[0] == ".":
        filename = filename[2:]

    pos = filename.rfind("/")
    filename = filename[:pos]

    filename = filename.replace("/", ".")

    return filename

def build_class_name(filename):
    filename = filename.replace(".scriptlib", "")
    filename = filename.replace(".script", "")
    pos = filename.rfind("/")
    filename = filename[pos+1:]
    return filename

def get_script_base(filename):
    pos = filename.find("script/")

    if pos > 0:
        return filename[:pos]
    if pos == 0:
        return "."

    return ""



def is_library(filename):
    return filename.find(".scriptlib") > 0
