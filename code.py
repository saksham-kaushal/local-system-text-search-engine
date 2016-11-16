import glob
import re

path=raw_input("Enter path (format- /path/to/folder): ")
file_list = glob.glob(path+"/*.txt")
print file_list


word_list= list()
hashtable= dict()
for each_file in file_list:
    with open(each_file,'r') as file_handle:
        for line in file_handle:
            wlist= re.findall(r"[\w']+",line)
            word_list.append(wlist)
        word_list=[x.lower() for word in word_list for x in word if len(x)>=3]
        docid = id(word_list)
        print word_list

        for each_word in word_list:
            doc=list()
            if each_word not in hashtable.keys():
                doc.append(docid)
                hashtable[each_word]=doc
            else:
                hashtable[each_word].append(docid)

print hashtable
