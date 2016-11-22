#!/usr/bin/python

import re
import os
from os.path import join
from collections import Counter


def enter_path():
    """
    Takes directory location as input and returns a list of files available in
    the directory or in directory along with its subdirectories depending on
    another user input.
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
        raise SystemExit('\nenter correct choice "y" for yes and "n" for no.\n')

    return filenames


"""imp to debug ::: try except clause instead of SystemExit to avoid bug when entering incorrect input for the first time."""

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

    return hashtable, fileID_names

def input_word():
    """
    Takes word to be searched as an input from the user and returns it.
    """

    search_user= raw_input("Enter word(s) to search: ")
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

def files_containing(info,map_ds):
    """
    map_ds maps document IDs to document names. If document IDs are enlisted in
    info, a list of all the file names corresponding to the IDs is returned, and
    None otherwise.
    """

    if info==None:
        return None
    else:
        files= list()
        for key in info.keys():
            files.append(map_ds[key])
        return files


def search_user_entries(entry_by_user):
    """
    Support for searching multiple entries by the user. iterates over a list and
    searches for all entries in the hashtable.
    """

    ranks=Counter(dict())
    entry_by_user=entry_by_user.split()
    complete_file_set=set()
    for entry in entry_by_user:
        availability_info=search_hash(entry,hashtable)
        if availability_info:
            ranks+=ranking(availability_info,fileID_to_names)
        else:
            sorted_display(None)
                    #call ranking, pass availability_info
    sorted_display(ranks)


def sorted_display(ranks):
    """
    Displays file names containing the word. All entries from complete_file_set
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
    rank=Counter(dict())
    for key in availability_info.keys():
        rank[mapds[key]]=len(availability_info[key])
    return rank


#Function calls

files= enter_path()
hashtable, fileID_to_names= create_hash(files)
entry_by_user= input_word()
search_user_entries(entry_by_user)


#print availability_info
#print files, fileID_to_names, hashtable
