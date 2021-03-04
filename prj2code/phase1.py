from pymongo import MongoClient
from string import punctuation
import re
import json
import time

def get_terms(item):
    terms = []
    if 'Title' in item:
        title = item['Title']
        # split sentence accroding to white space and/or punctuation
        split = re.split(r'\W+', title.strip(punctuation))
        for word in split:
            if len(word) >= 3:
                terms.append(word)
        result = no_repeat(terms)
    if 'Body' in item:
        body = item['Body']
        split = re.split(r'\W+', body.strip(punctuation))
        for word in split:
            if len(word) >= 3:
                terms.append(word) 
        result = no_repeat(terms)
    # put the terms array into Post collection
    item['terms'] = json.dumps(result)

def no_repeat(terms):
    result = []
    for i in range(len(terms)):
        terms[i] = terms[i].lower()
    for item in terms:
        if item not in result:
            result.append(item)
    return result

def main():
    cur_time = time.time()
    # create mongo client for connecting mongodb
    client = MongoClient('mongodb://localhost:27017')
    db = client["291db"]   
    # get the collections
    collectionNames = db.list_collection_names()
    
    # read Tags.json and convert data type 
    with open('Tags.json','r') as f:
        tagRowCollection = json.load(f)['tags']['row']  
    # if the collection exist, drop it
    if 'Tags' in collectionNames:
        db.drop_collection('Tags')
    # create collection then insert it to db
    tag_collection = db['Tags']
    tag_collection.insert_many(tagRowCollection)    
    
    # read Votes.json and convert data type
    with open('Votes.json','r') as f:
        voteRowCollection = json.load(f)['votes']['row']
    if 'Votes' in collectionNames:
        db.drop_collection('Votes')
    vote_collection = db['Votes']
    vote_collection.insert_many(voteRowCollection)
    
    # read Posts.json and convert data type
    with open('Posts.json','r') as f:
        postRowCollection = json.load(f)['posts']['row']
        # for each item in result of previous step, prepare for get their terms
        for item in postRowCollection:
            get_terms(item)
        
    if 'Posts' in collectionNames:
        db.drop_collection('Posts')
    post_collection = db['Posts']
    post_collection.insert_many(postRowCollection)
    # build index to terms
    post_collection.create_index([("terms", 1)], unique=False)
    now_time = time.time()
    cost_time = now_time-cur_time    
    print('Total time is: ', cost_time)
main()