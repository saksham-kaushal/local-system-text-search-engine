#!/usr/bin/python

import re
            #for regular expressions
import os
            #for file system path traversal
from os.path import join
            #for joining paths and file names
from collections import Counter
            #for importing Counter dictionaries in ranking

import itertools
import threading
import time
import sys
            #all 4 used for Loading animation


def enter_path():
    """
    Takes directory location and choice of searching subdirectories as inputs and
    returns a list of files available in the directory or in directory along
    with its subdirectories. In case of incorrect input to yes/no, ValueError is
    raised.
    """

    path_input=raw_input("Enter path (format- /path/to/folder): ")
    subs= raw_input("Do you want to search subdirectories (y/n): ").lower()
    filenames=list()
    if subs == "y":
        for root, dirs, files in os.walk(path_input):
            files=filter(lambda x: x.endswith(".txt"), files)
                            #only files with .txt extension considered
            filenames+=[join(root,name) for name in files]
            for item in dirs:
                if item.startswith("."):
                    #hidden folders removed from dirs list
                    dirs.remove(item)

    elif subs == "n":
        filenames = filter(lambda x: x.endswith(".txt"), [os.path.join(path_input,file_add) \
                for file_add in next(os.walk(path_input))[2]])

    else:
        raise ValueError

    return filenames



def create_hash(file_list):
    """
    Creates inverted index of format {word:{documentID:[indices of positions]}}
    """

    hashtable= dict()
    fileID_names= dict()


    for each_file in file_list:
        with open(each_file,'r') as file_handle:
            word_list= list()
            for line in file_handle:
                wlist= re.findall(r"[\w']+",line)
                                #removes punctuation except ' and _
                word_list.append(wlist)
            word_list=[word.lower() for elements in word_list for word in elements if len(word)>=3]
                                #removing a, an, as, in etc.
            docid = id(word_list)
            fileID_names[docid]=each_file


            for each_word in word_list:
                doc=dict()
                doc[docid]=[i for i, j in enumerate(word_list) if j == each_word]
                if each_word not in hashtable.keys():
                    hashtable[each_word]=doc
                else:
                    hashtable[each_word][docid]=doc[docid]
                                #if word is contained in previously indexed file


    #print hashtable
    #print fileID_names
    return hashtable, fileID_names



def input_word():
    """
    Takes word to be searched as an input from the user and returns it.
    """

    search_user= raw_input("\nEnter word(s) to search: ")
    return search_user.lower()



def search_hash(word_input,hashtable):
    """
    Searches if the word input matches any entry in the hashtable. If yes, it
    returns document IDs and indices
    """

    if word_input in hashtable:
        return hashtable[word_input]
    else:
        return None



def search_user_entries(entry_by_user):
    """
    Support for searching multiple entries by the user. iterates over a list and
    searches for all entries in the hashtable.
    """

    ranks=Counter(dict())
    entry_by_user=entry_by_user.split()
    #complete_file_set=set()
    for entry in entry_by_user:
        availability_info=search_hash(entry,hashtable)
        if availability_info:
            ranks+=ranking(availability_info,fileID_to_names)
        else:
            sorted_display(None)
                    #call ranking, pass availability_info
    #print ranks
    sorted_display(ranks)



def sorted_display(ranks):
    """
    Displays file names containing the word. All entries from rank counter
    displayed on single line.
    """

    if ranks!=None:
        rank=1
        while ranks:
            outputs=[key for m in [max(ranks.values())] for key,val in ranks.iteritems() if val == m]
            for output in outputs:
                print rank, output
                del ranks[output]
                rank+=1
    else:
        print "Word exists in none of the files"



def ranking(availability_info,mapds):
    """
    Ranks results in the form of key-value pairs as counter dictionary where
    values represents number of occurances. This can be arranged in ascending
    order to get the rank.
    """
    rank=Counter(dict())
    for key in availability_info.keys():
        rank[mapds[key]]=len(availability_info[key])
    #print rank
    return rank



def animate():
    """
    Implements animation of Loading while hastable is being built.
    """
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rLoading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
                    #prefer sys.stdout instead of print for continuously updating
                    #the Loading animation


#Function calls
while True:
    try:
        files= enter_path()
        if not files:
            raise NameError
        done=False
        t = threading.Thread(target=animate)
        t.start()
        hashtable, fileID_to_names= create_hash(files)
        time.sleep(1)
        done = True
        print "\nDone building index!!"
        entry_by_user= input_word()
        search_user_entries(entry_by_user)
        break
    except ValueError:
        print '\nenter correct choice "y" for yes and "n" for no.\n'
    except NameError:
        print '\nInvalid or incorrect address entered.\n'


#print availability_info
#print files, fileID_to_names, hashtable
