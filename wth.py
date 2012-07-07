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


def update_dict( adict, ext, size ):
   
    if adict.has_key(ext):
        # add file to total number of files
        #print "found key:", ext
        num_size = int(adict[ext][0] + size)
        num_files = int(adict[ext][1] + 1)
        new_tupel = ( num_size, num_files )
        adict[ext] = new_tupel
    else:
        adict[ext] = (size,1)
    return adict
    
def analyze(dir, out_ext_file = "./out_ext.csv", out_file = "./out.csv"):
    """Walks down the given dir tree and analyzes its contents for size and number of files.
        Writes an output csv that is used by generate_report() to generate a report ;)
        TODO: use (sqlite3)DB instead of csv file.
        input parameters:
                dir         -   name of root dir for analysis
        output:
                3-tupel     -   (total_files, total_dirs, out_file)
                                number of total files
                                number iof total dirs
                                absolute path of output file
    """
    total_files = 0
    total_dirs = 0
    # format olist = [ [inner_olist1],[inner_olist2]...[inner_olistn] ]
    olist = []
    # format inner_olist = [ path, dir, size, [ (ext1,size, numfiles), (ext2,size, numfiles) ... ] ]
    inner_olist = []
    # current dict[ext]: (size, numfiles) - represents the 3-tupel for inner_olist 
    current_dict = {}
    overall_exts_dict = {}
    for path,dirs,files in os.walk(os.path.normpath(dir)):
        #print path
        #print dirs
        total_dirs += len(dirs)
        #print path, files
        total_files += len(files)
        current_total_size = 0
        current_dict = {}
        for adir in dirs:
            #print "...processing path: ", path, " dir: ", adir
            for afile in files:
                absfile = os.path.abspath(os.path.normpath(os.path.join(path, afile)))
                if os.path.exists(os.path.normpath(absfile)):
                    filename,ext = os.path.splitext(absfile)
                    if ext == "":
                        ext = "NONE"
                    size = os.path.getsize(os.path.normpath(absfile))
                    current_total_size += size
                    current_dict = update_dict(current_dict, ext, size)
                    overall_exts_dict = update_dict(overall_exts_dict, ext, size)
                    #print filename, ext, " --> ", size, "Byte.  kB: ", str(size/1024)
                else:
                    print "...does not exist ", afile, os.path.normpath(absfile)
        
        olist.append( [ path, adir, current_total_size, current_dict] )
    #print current_dict
    ofile = open(os.path.normpath(out_ext_file), "w")
    print "...writing to file: ", os.path.normpath(out_file)
    ofile.write("Extension, Total Size in Bytes, Total Number of files with this extension" + os.linesep)
    
    #print overall_exts_dict
    for elem in overall_exts_dict:
        #print "elem:", elem, "-elem Ende"
        #if elem == "":
        #    print "NONE", "  ", str(overall_exts_dict[elem][0]), " ", str(overall_exts_dict[elem][1])
        #else:
        #    print elem, "  ", str(overall_exts_dict[elem][0]), " ", str(overall_exts_dict[elem][1])
        ofile.write(elem + "," + str(overall_exts_dict[elem][0]) + "," + str(overall_exts_dict[elem][1]) + os.linesep)
    ofile.close()
    ofile = open(os.path.normpath(out_file), "w")  
    ofile.write("""Path, Directory, total size of files in this dir, Extension, Total Size in Bytes , Total Size in KB,  Total Size in MB, Total Number of files with this extension""" + os.linesep)
    for sublist in olist:
        # sublist is: [ path, adir, current_total_size, current_dict]
        ostr = ""
        pre_str = sublist[0] + "," + sublist[1] + "," + str(sublist[2]) 
        for key in sublist[3].keys():
            # format: { "ext1" : ( size, numfiles ) }
            ostr = pre_str + "," + str(key) + "," + str(sublist[3][key][0]) + "," 
            ostr += str(int(sublist[3][key][0])/1024) + "," 
            ostr += str(int(sublist[3][key][0])/(1024*1024)) + "," 
            ostr += str(sublist[3][key][1]) + os.linesep
            ofile.write(ostr)
            ostr = ""
            
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