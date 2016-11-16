import glob
import re


def enter_path():
    """
    Takes directory location as input and returns a list of files available in
    the directory.
    """
    path=raw_input("Enter path (format- /path/to/folder): ")
    file_list = glob.glob(path+"/*.txt")
    #enlists only the contents of directory, not the subdirectories-scope of improvement using regex or glob
    return file_list


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
    search_user= raw_input("Enter word to search: ")
    return search_user.lower()

def search_hash(word_input,hashtable):
    """
    Searches if the word input matches any entry in the hashtable. If yes, it
    returns document IDs and indices
    """
    if word_input in hashtable:
        return hashtable[word_input]
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

def display_content(file_list):
    """
    Displays file names containing the word. All entries from file_list displayed
    on single line.
    """
    if all_files!=None:
        for value in all_files:
            print value
    else:
        print "Word exists in none of the files"


files= enter_path()
hashtable, fileID_to_names= create_hash(files)
entry_by_user= input_word()
availability_info=search_hash(entry_by_user,hashtable)
all_files= files_containing(availability_info,fileID_to_names)
display_content(all_files)


#print availability_info
#print files, fileID_to_names, hashtable
