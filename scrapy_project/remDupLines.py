"""
removes duplicate lines from a file
"""
import sys

try:
    infile = open(sys.argv[1], "r")
except:
    print "need a infilename"
    
lines_seen = set()    
for line in infile:
    if line not in lines_seen:  
        print line.replace('\n','')
        lines_seen.add(line)

