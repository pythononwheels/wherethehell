#
#
# WhereTheHell (aka MeckDisk) is a disk analyzer written in python
# It analyzes the disk displaying file size ditribution as a tree map
# and number of instances of file-type-x (e.g. .jpg, .pdf and so on) 
# as bar-chart  or pie-chart  
# All reports are generated as stand alone html files so 
# using google chart tools AND smart_chart.
# Smart_chart produces the google-charts automatically from csv files. 
# 
# OK, I admit that smart_chart is also made by me ;) But for a different use
# so now nice reuse option. 
# 
# Date:     06.07.2012. (My wifes birthday;)
# Author:   khz@tzi.org
# Github:   https://github.com/pythononwheels/wherethehell
# uses:     python                  www.python.org
#           google-chart-tools      https://developers.google.com/chart/
#           smart_chart             https://github.com/pythononwheels/smart_chart
        

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
    # format olist = [ [inner_olist1],[inner_olist2]...[inner_olistn] ]
    olist = []
    # format inner_olist = [ path, size, [ (ext1, numfiles, size), (ext2, numfiles, size) ] ]
    inner_olist = []
    
    for path,dirs,files in os.walk(os.path.normpath(dir)):
        #print path
        #print dirs
        total_dirs += len(dirs)
        print path, files
        total_files += len(files)
        current_total_size = 0
        current_dict = {}
        for afile in files:
            absfile = os.path.abspath(os.path.normpath(os.path.join(path, afile)))
            if os.path.exists(os.path.normpath(absfile)):
                filename,ext = os.path.splitext(absfile)
                size = os.path.getsize(os.path.normpath(absfile))
                print filename, ext, " --> ", size, "Byte.  kB: ", str(size/1024)
            else:
                print "...does not exists ", afile, os.path.normpath(absfile)
    
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