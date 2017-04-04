# -*- coding: utf-8 -*-
"""
This file is used for indexing FedWeb2014.

@author: Shuo Zhang
"""
import os
import tarfile
from bs4 import BeautifulSoup
from Elastic import Elastic

def fedweb14_index(index_name,output_file):

    elastic = Elastic(index_name) 
    mappings = {
        # "id": Elastic.notanalyzed_field(),
        "title": Elastic.analyzed_field(),
        "content": Elastic.analyzed_field()
    }
    
    elastic.create_index(mappings=mappings, force=True)
    
    maindir = "/data/collections/fedwebgh/search_data/fedweb14/FW14-sample-search"
    num_doc = 0
    f_feb = open(output_file,"w")
    for d in os.listdir(maindir):
        if d.startswith("md") or d.startswith("sni"):
            continue       
        inpath = os.path.join(maindir, d)   
        tar = tarfile.open(inpath,"r:gz")
        tar.extractall()
        docs = {}
        for member_info in tar.getmembers():            
            if len(member_info.name)>23:
                f = open(member_info.name)               
                soup = BeautifulSoup(f,"lxml")
                for snippets in soup.find_all("snippet"):   
                    doc_dict = {}
                    doc_id = snippets.get("id").lower()
                    f_feb.write(doc_id+" "+"FW14-"+doc_id[5:9]+"\n")
                    try:
                        title = snippets.title.text
                    except:
                        title = ""
                    try:
                        content = snippets.description.text
                    except:
                        content = ""
                    doc_dict["title"] = title
                    doc_dict["content"] = content
                    docs[doc_id] = doc_dict
                    num_doc += 1
        "continous update docs and add into index"
        elastic.add_docs_bulk(docs)
        print ("finish parse and index for file: ",inpath)
    print(num_doc," indexed")

                    
                
if __name__ == "__main__":
    index_name = "fedweb14"
    fedweb14_index(index_name,"assoc_fed14.txt")
            
            
