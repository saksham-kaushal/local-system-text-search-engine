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
    Creates inverted index of format {word:{documentID:[indeces of positions]}}
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

files=enter_path()
hashtable, fileID_to_names= create_hash(files)

print files, fileID_to_names, hashtable
