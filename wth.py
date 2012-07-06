#
#
# WhereTheHell (aka MeckDisk) is a disk analyzer written in python
# It analyzes the disk displaying file size ditribution as a tree map
# and number of instances of file-type-x (e.g. .jpg, .pdf and so on) 
# as bar-chart  or pie-chart  
# All reports are generated as stand alone html files so 
# using google chart tools.
#
# Date:     06.07.2012. (My wifes birthday;)
# Author:   khz@tzi.org
# Github:   See 
#
from optparse import OptionParser
import sys, os, datetime

def analyze(dir, out_file = "./out.csv"):
    """Walks down the given dir tree and analyzes its contents for size and number of files.
        Writes an output csv that is used by generate_report() to generate a report ;)
        TODO: use (sqlite3)DB instead of csv file.
        input parameters:
                dir         -   name of root dir for analysis
        output:
                3-tupel     -   (total_files, total_dirs, out_file)
                                number of total files
                                number iof total dirs
                                absolutte path of output file
    """
    total_files = 0
    total_dirs = 0
    
    for path,dirs,files in os.walk(os.path.normpath(dir)):
        #print path
        #print dirs
        total_dirs += len(dirs)
        #print files
        total_files += len(files)
        
    
    ofile = open(os.path.normpath(out_file), "w")
    ofile.close()
    return (total_files, total_dirs, os.path.abspath(out_file))

if __name__ == "__main__":
    """Walk the given start dir and analyze it (size and file extension distribution)"""

    parser = OptionParser()
    #mode = MODE_CREATE
    parser.add_option("-d", "--dir",  action="store", type="string", dest="dir", 
        help="base dir for tree walk analysis", default ="./")
    #parser.add_option("-f", "--force",  action="store_true",  dest="force", 
    #    help="forces overrides of existing app", default="False")
    #parser.add_option("-c", "--comment",  action="store", type="string", dest="comment", 
    #    help="defines a comment for this migration.", default ="No Comment")


    (options, args) = parser.parse_args()
    #print options, args
    print "... starting analysis from: ", options.dir
    start = datetime.datetime.now()

    (total_files, total_dirs, out_file) = analyze(os.path.normpath(options.dir))

    end = datetime.datetime.now()
    duration = None
    duration = end - start
    print " -- finished analyzing", total_dirs, " directories and ",total_files, " files in ",str(duration), "seconds"
    sys.exit(0)