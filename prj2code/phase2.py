import pymongo
import json
import re
from tkinter import *
import tkinter.messagebox as messagebox
import datetime

#connect to 291db
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['291db']
col_p = db['Posts']			#posts collection
col_v = db['Votes']			#votes collection
col_t = db['Tags']			#tags collection


class LogIn:
    #Login Window
    def __init__(self, master):
        self.root = master
        self.root.title('Login Screen')
        self.root.geometry('500x300+10+15')
        self.uid = StringVar()
        self.pwd = StringVar()
        self.window = Frame(self.root)
        self.create_window()
 
 
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uid).grid(row = 2, column = 1, sticky = E)
        Button(self.window, text='SIGN IN', width = 8, command = self.sign_in).grid(row = 4, column = 1, sticky = W, pady = 10)
        self.window.pack()

    def sign_in(self):
        user_info = col_p.find_one({"OwnerUserId": self.uid.get()})       #get all posts info of the user
        if user_info is None and self.uid.get() != '':
            messagebox.showerror('ERROR!', 'The user does not exist!')
        else:
            self.window.destroy()
            SignIn(self.uid.get(), self.root)


class SignIn:
    #Sign In Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Welcome!')
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.uid = uid
        self.create_window()
    
    
    def search(self):
        self.window.destroy()
        Search(self.uid, self.root)    

    def create_window(self):
        Button(self.window, text = 'POST QUESTION', width = 20, command = self.post_q).grid(row = 1, column = 0, sticky = W, pady = 10)
        Button(self.window, text = 'SEARCH', width = 20, command = self.search).grid(row = 2, column = 0, sticky = W, pady = 10)
        Button(self.window, text = 'VOTE', width = 20, command = self.vote).grid(row = 3, column = 0, sticky = W, pady = 10)
        Button(self.window, text = 'LOG OUT', width = 20, command = self.log_out).grid(row = 4, column = 0, sticky = W, pady = 10)
        self.diff_user()
        self.window.pack()

    def show_report(self):
        list_p = []
        list_q = []
        list_a = []
        list_v = []
        score_p = 0		#total score of posts
        score_a = 0		#total score of answers
        user_post = col_p.find({"OwnerUserId": self.uid})		#get all posts info of the user
        for i in user_post:
            list_p.append(i.get("Id"))
            if i.get("PostTypeId") == "1":		#if the post is a question
                list_q.append(i.get("Id"))
                score_p += int(i.get("Score"))
            elif i.get("PostTypeId") == "2":		#if the post is an answer
                list_a.append(i.get("Id"))
                score_a += int(i.get("Score"))
        for i in list_p:
            post_vote = col_v.find({"PostId": i})
            for j in post_vote:
                list_v.append(j.get("Id"))
        if len(list_q) != 0:
            ave_p = score_p / len(list_q)		#get average score of questions
        else:
            ave_p = 0
        if len(list_a) != 0:
            ave_a = score_a / len(list_a)		#get average score of answers
        else:
            ave_a = 0
        Label(self.window, text = 'Report').grid(row=5, column = 0, sticky = W, pady = 10)
        Label(self.window, text = 'Number of Questions: ').grid(row = 6, sticky = W, pady = 10)
        Label(self.window, text = len(list_q)).grid(row = 6, column = 1, sticky = E)
        Label(self.window, text = 'Average Score of Questions: ').grid(row = 7, sticky = W, pady = 10)
        Label(self.window, text = ave_p).grid(row = 7, column = 1, sticky = E)
        Label(self.window, text = 'Number of Answers: ').grid(row = 8, sticky = W, pady = 10)
        Label(self.window, text = len(list_a)).grid(row = 8, column = 1, sticky = E)
        Label(self.window, text = 'Average Score of Answers: ').grid(row = 9, sticky = W, pady = 10)
        Label(self.window, text = ave_a).grid(row = 9, column = 1, sticky = E)
        Label(self.window, text = 'Number of Votes: ').grid(row = 10, sticky = W, pady = 10)
        Label(self.window, text = len(list_v)).grid(row = 10, column = 1, sticky = E)     


    def diff_user(self):
        if self.uid != '':
            self.show_report()



    def post_q(self):
        self.window.destroy()
        PostQ(self.uid, self.root)

    def vote(self):
        self.window.destroy()
        Vote(self.uid, self.root)

    def log_out(self):
        self.window.destroy()
        LogIn(self.root)



class PostQ:
    #Post A Question Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Post A Question')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.tag = StringVar()
        self.uid = uid
        self.create_window()
        

    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'TITLE:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.title).grid(row = 2, column = 1, sticky = E)
        Label(self.window, text = 'TEXTS:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.body).grid(row = 3, column = 1, sticky = E)
        Label(self.window, text = 'TAGS:').grid(row = 4, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.tag).grid(row = 4, column = 1, sticky = E)
        Button(self.window, text='CONFIRM', width = 8, command = self.post).grid(row = 5, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 6, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)


    def post(self):
        if len(self.title.get()) == 0 or len(self.body.get()) == 0:
            messagebox.showerror('ERROR!', 'The title/body can not be empty!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            number = col_p.estimated_document_count() #total post number
            post_id = "{:03d}".format(number + 1)           #get unique post id
            if self.uid != '':
                post_dic = {
                         "Id": post_id,
                         "PostTypeId": "1",
                         "CreationDate": date,
                         "Score": 0,
                         "ViewCount": 0,
                         "Body": self.body.get(),
                         "OwnerUserId": self.uid,
                         "LastActivityDate": date,
                         "Title": self.title.get(),
                         "Tags": self.tag.get(),
                         "AnswerCount": 0,
                         "CommentCount": 0,
                         "FavoriteCount": 0,
                         "ContentLicense": "CC BY-SA 2.5"
                    }
            else:
                post_dic = {
                         "Id": post_id,
                         "PostTypeId": "1",
                         "CreationDate": date,
                         "Score": 0,
                         "ViewCount": 0,
                         "Body": self.body.get(),
                         "LastActivityDate": date,
                         "Title": self.title.get(),
                         "Tags": self.tag.get(),
                         "AnswerCount": 0,
                         "CommentCount": 0,
                         "FavoriteCount": 0,
                         "ContentLicense": "CC BY-SA 2.5"
                    }
            col_p.insert_one(post_dic)
            self.window.destroy()
            SignIn(self.uid, self.root)


class Vote:
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Vote A Post')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.select = StringVar()
        self.uid = uid
        self.create_window()

    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)  
        Label(self.window, text = 'INPUT THE SELECT ID:').grid(row = 2, column = 0, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 3, column = 0, sticky = W, pady = 10)
        Button(self.window, text='VOTE', width = 10, command = self.vote_post).grid(row = 4, column = 0, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 5, column = 0, sticky = W, pady = 10)
        self.window.pack()


    def vote_post(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')    #get date
        v_number = col_v.estimated_document_count()
        vote_id = "{:03d}".format(v_number + 1)
        if self.uid != '':
            voted = col_v.find_one({"PostId": self.select.get(), "UserId": self.uid})      #check if the user voted the post before
            if voted == None:
                vote_dic = {
                            "Id": vote_id,
                            "PostId": self.select.get(),
                            "VoteTypeId": "2",
                            "UserId": self.uid,
                            "CreationDate": vote_date
                        }
                col_v.insert_one(vote_dic)
                select_p = col_p.find_one({"Id": self.select.get()}).get("Score")       #get selected post's info
                score = {"Score": select_p}
                new_score = {"$set": { "Score": select_p + 1 } }
                col_p.update_one(score, new_score)            #update post score
                messagebox.showinfo('Succeeded!', 'You vote the post successfully!')
                self.window.destroy()
                SignIn(self.uid, self.root)
            else:
                messagebox.showerror('ERROR!', 'You have already voted this post!')
        else:
            vote_dic = {
                        "Id": vote_id,
                        "PostId": self.select.get(),
                        "VoteTypeId": "2",
                        "CreationDate": vote_date
                }
            col_v.insert_one(vote_dic)
            select_p = col_p.find_one({"Id": self.select.get()}).get("Score")       #get selected post's info
            score = {"Score": select_p}
            new_score = {"$set": { "Score": select_p + 1 } }
            col_p.update_one(score, new_score)            #update post score
            messagebox.showinfo('Succeeded!', 'You vote the post successfully!')
            self.window.destroy()
            SignIn(self.uid, self.root)



    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
        



class Search:
    #Search A Post Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Search A Question')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.keyword = StringVar()
        self.create_window()
        self.uid = uid


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'KEYWORD:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.keyword).grid(row = 2, column = 1, sticky = E)
        Button(self.window, text='SEARCH', width = 8, command = self.done).grid(row = 3, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
        
    
    def done(self):
        result_list = []
        inp = self.keyword.get()
        keywords = inp.split(',')
        n = len(keywords)
        if len(inp) == 0:
                messagebox.showerror('ERROR!', 'The input can not be empty!')    #The input can not be empty
        else:
            #print(keywords)
            for i in range(len(keywords)):   #find question contain the keyword either in title, body, or tag fields, and the match is case-insensitive
                keyword = keywords[i]
                keyword = keyword.lower()
                #print(keyword)
                user_post = col_p.find({"PostTypeId": "1", "$or": [{"terms": {'$regex': keyword}}, {"Tags": {'$regex': keyword}}]}) 
                #print(keyword)
                #print(len(user_post))
                for post in user_post:
                    result_list.append(post.get("Id"))
                #print(result_list)
            result = []
            for item in result_list:    #delete duplicate Id
                if item not in result:
                    result.append(item)            
            #print(result)
            
        if len(result) == 0:
            messagebox.showerror('ERROR!', 'No match!')
        else:
            self.window.destroy()  
            ShowResult(self.uid, result, self.root)          
                  
    

class ShowResult:
    def __init__(self, uid, return_list, master=None):
        self.root = master
        self.root.title('SHOW THE RESULT')
        self.root.geometry('1100x800')
        self.window = Frame(self.root)
        self.return_list = return_list
        self.length_list = 0
        self.select = StringVar()
        self.uid = uid
        self.c = None
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)  
        Label(self.window, text = 'INPUT THE SELECT ID:').grid(row = 2, column = 0, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 3, column = 0, sticky = W, pady = 10)
        Button(self.window, text='SELECT', width = 15, command = self.selecttheitem).grid(row = 4, column = 0, sticky = W, pady = 10)
        Button(self.window, text='SEARCHMORE', width = 15, command = self.searchmore).grid(row = 5, column = 0, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 6, column = 0, sticky = W, pady = 10)
        if len(self.return_list) > 0 and len(self.return_list) < 5:    #if len(self.return_list) < 5
            for i in range(len(self.return_list)):
                each_post = col_p.find({"Id": self.return_list[i]})     #find the row
                for x in each_post:
                    choose = 'Id: ' + x.get("Id") + ' | Title: ' + x.get("Title") + ' | CreationDate: ' + x.get("CreationDate") + ' | Score: ' + str(x.get("Score")) + ' | AnswerCount: ' +  str(x.get("AnswerCount"))     #show Id, Title, CreationDate, Score , and AnswerCount
                Label(self.window, text = choose).grid(row = 7 + i, column = 0, sticky = W, pady = 10)             
        else:
            for i in range(5):
                each_post = col_p.find({"Id": self.return_list[i]})   #find the row
                for x in each_post:
                    choose = 'Id: ' + x.get("Id") + ' | Title: ' + x.get("Title") + ' | CreationDate: ' + x.get("CreationDate") + ' | Score: ' + str(x.get("Score")) + ' | AnswerCount: ' +  str(x.get("AnswerCount"))      #show Id, Title, CreationDate, Score , and AnswerCount
                Label(self.window, text = choose).grid(row = 7 + i, column = 0, sticky = W, pady = 10)                 
                       
        del self.return_list[0:5]      #Delete the first five Ids
        self.window.pack()        
        
        
    def searchmore(self):
        if len(self.return_list) == 0:
            messagebox.showerror('ERROR!', 'No more result!')
        else:
            self.window.destroy()
            ShowResult(self.uid, self.return_list, self.root)    #show more results
    
        
    def selecttheitem(self):
        if len(self.select.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            user_post = col_p.find({"Id": self.select.get()})
            for x in user_post:
                if x.get("Id") == None:
                    messagebox.showerror('ERROR!', 'The input is not exist!')      
                else:
                    self.c = self.select.get()
                    self.window.destroy()
                    view_count = x.get("ViewCount")
                    col_p.update_one({"Id": x.get("Id")},{"$set":{"ViewCount": view_count + 1}})     #update the ViewCount
                    PerformPostAction(self.uid, self.c, self.root)     #go to PerformPostAction class                 
                    
       
    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)



class PerformPostAction:
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Perform A Post Action')
        self.root.geometry('1300x700')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.c = c
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.user()
        self.window.pack()    


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)


    def vote(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')    #get date
        v_number = col_v.estimated_document_count()
        vote_id = "{:03d}".format(v_number + 1)
        if self.uid != '':
            voted = col_v.find_one({"PostId": self.c, "UserId": self.uid})      #check if the user voted the post before
            if voted == None:
                vote_dic = {
                            "Id": vote_id,
                            "PostId": self.c,
                            "VoteTypeId": "2",
                            "UserId": self.uid,
                            "CreationDate": vote_date
                        }
                col_v.insert_one(vote_dic)
                select_p = col_p.find_one({"Id": self.c}).get("Score")       #get selected post's info
                score = {"Score": select_p}
                new_score = {"$set": { "Score": select_p + 1 } }
                col_p.update_one(score, new_score)            #update post score
                messagebox.showinfo('Succeeded!', 'You vote the post successfully!')
                self.window.destroy()
                SignIn(self.uid, self.root)
            else:
                messagebox.showerror('ERROR!', 'You have already voted this post!')
        else:
            vote_dic = {
                        "Id": vote_id,
                        "PostId": self.c,
                        "VoteTypeId": "2",
                        "CreationDate": vote_date
                }
            col_v.insert_one(vote_dic)
            select_p = col_p.find_one({"Id": self.c}).get("Score")       #get selected post's info
            score = {"Score": select_p}
            new_score = {"$set": { "Score": select_p + 1 } }
            col_p.update_one(score, new_score)            #update post score
            messagebox.showinfo('Succeeded!', 'You vote the post successfully!')
            self.window.destroy()
            SignIn(self.uid, self.root)


    
    def answer(self):
        Answer(self.uid, self.c, self.root)
        self.window.destroy()

    def user(self):
        user_post = col_p.find({"Id": self.c})
        for x in user_post:     #see all fields of the question
            self.accept_id = x.get("AcceptedAnswerId")
            if x.get("AcceptedAnswerId") == None:
                accepted_answer_id = "None"
            else:
                accepted_answer_id = x.get("AcceptedAnswerId") 
            if x.get("CommunityOwnedDate") == None:
                community_owned_date = "None"
            else:
                community_owned_date = x.get("CommunityOwnedDate")  
            if x.get("Score") == None:
                score = "None"
            else:
                score = str(x.get("Score"))  
            if x.get("ViewCount") == None:
                viewcount = "None"
            else:
                viewcount = str(x.get("ViewCount"))      
            if x.get("LastEditorUserId") == None:
                last_editor_user_id = "None"
            else:
                last_editor_user_id = x.get("LastEditorUserId")       
            if x.get("CreationDate") == None:
                creationdate = "None"
            else:
                creationdate = x.get("CreationDate")              
            if x.get("LastEditDate") == None:
                last_edit_date = "None"
            else:
                last_edit_date = x.get("LastEditDate")  
            if x.get("LastActivityDate") == None:
                last_activity_date = "None"
            else:
                last_activity_date = x.get("LastActivityDate") 
            if x.get("Tags") == None:
                tags = "None"
            else:
                tags = x.get("Tags") 
            if x.get("AnswerCount") == None:
                answer_count = "None"
            else:
                answer_count = str(x.get("AnswerCount"))  
            if x.get("CommentCount") == None:
                comment_count = "None"
            else:
                comment_count = str(x.get("CommentCount"))   
            if x.get("FavoriteCount") == None:
                favorite_count = "None"
            else:
                favorite_count = str(x.get("FavoriteCount"))
            if x.get("ContentLicense") == None:
                content_license = "None"
            else:
                content_license = x.get("ContentLicense") 
            if x.get("Title") == None:
                title = "None"
            else:
                title = x.get("Title")  
            if x.get("Body") == None:
                body = "None"
            else:
                body = x.get("Body")  
            if x.get("OwnerUserId") == None:
                owner_user_id = "None"
            else:
                owner_user_id = x.get("OwnerUserId")              
            
            choose1 = 'Id: ' + x.get("Id") + ' | PostTypeId: ' + x.get("PostTypeId") + ' | AcceptedAnswerId: ' + accepted_answer_id + ' | CreationDate: ' +  creationdate
            choose2 = 'Score: ' + score + ' | ViewCount: ' + viewcount       #print all the fields
            body_li = list(body)
            for i in range(len(body_li)):
                if body_li[i] == '.':
                    body_li.insert(i+1,'\n')
            body = ''.join(body_li)    
            choose3 = 'Body: ' + body
            choose4 = 'OwnerUserId: ' +  owner_user_id
            choose5 = 'LastEditorUserId: ' + last_editor_user_id + ' | LastEditDate: ' + last_edit_date + ' | LastActivityDate: ' + last_activity_date + ' | Title: ' +  title
            choose6 = 'Tags: ' + tags + ' | AnswerCount: ' + answer_count + ' | CommentCount: ' + comment_count + ' | FavoriteCount: ' +  favorite_count
            choose7 = "CommunityOwnedDate: " + community_owned_date + ' | ContentLicense: ' + content_license            
              
        Label(self.window, text = choose1).grid(row = 1, column = 0, sticky = W, pady = 10)  
        Label(self.window, text = choose2).grid(row = 2, column = 0, sticky = W, pady = 10) 
        Label(self.window, text = choose3).grid(row = 3, column = 0, sticky = W, pady = 10)  
        Label(self.window, text = choose4).grid(row = 4, column = 0, sticky = W, pady = 10)
        Label(self.window, text = choose5).grid(row = 5, column = 0, sticky = W, pady = 10)
        Label(self.window, text = choose6).grid(row = 6, column = 0, sticky = W, pady = 10)
        Label(self.window, text = choose7).grid(row = 7, column = 0, sticky = W, pady = 10)        
        Button(self.window, text='VOTE', width = 10, command = self.vote).grid(row = 8 , column = 0, sticky = W, pady = 10)
        Button(self.window, text='ANSWER', width = 10, command = self.answer).grid(row = 9 , column = 0, sticky = W, pady = 10)
        Button(self.window, text='SHOW ALL ANSWERS', width = 20, command = self.showallanswers).grid(row = 10 , column = 0, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 11 , column = 0, sticky = W, pady = 10) 
        
    
    def showallanswers(self):
        self.window.destroy()
        answer_list = []
        answer_list.append(self.accept_id)        

        post_answer = col_p.find({"PostTypeId": "2", "ParentId": self.c})
        for answer in post_answer:
            if answer.get('Id') == self.accept_id:
                pass
            else:
                answer_list.append(answer.get("Id"))
        
        ShowAnswer(self.uid, self.c, answer_list, self.accept_id, self.root)  
    
    
        
class Answer:
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Post An Action-Answer')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.body = StringVar()    
        self.uid = uid
        self.c = c
        self.create_window()        
    
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)        
        Label(self.window, text = 'TEXT:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.body).grid(row = 2, column = 1, sticky = E)        
        Button(self.window, text='CONFIRM', width = 8, command = self.confirm_answer).grid(row = 3, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)    
        self.window.pack()
        
        
    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
        
        
    def confirm_answer(self):
        if len(self.body.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')        
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            number = col_p.estimated_document_count()          
            post_id = "{:03d}".format(number + 1)             
            if self.uid != '':
                post_dic = {            
                         "Id": post_id,
                         "PostTypeId": "2",
                         "ParentId": self.c,
                         "CreationDate": date,
                         "Score": 0,
                         "Body": self.body.get(),
                         "OwnerUserId": self.uid,
                         "LastActivityDate": date,
                         "CommentCount": 0,
                         "ContentLicense": "CC BY-SA 2.5"
                    }
            else:
                post_dic = {
                         "Id": post_id,
                         "PostTypeId": "2",
                         "ParentId": self.c,
                         "CreationDate": date,
                         "Score": 0,
                         "OwnerUserId": self.uid,
                         "LastActivityDate": date,
                         "CommentCount": 0,
                         "ContentLicense": "CC BY-SA 2.5"
                    }            
            col_p.insert_one(post_dic)        #insert answer
            user_post = col_p.find({"Id": self.c})
            for x in user_post:
                answer_count = x.get("AnswerCount")
                col_p.update_one({"Id": self.c},{"$set":{"AnswerCount": answer_count + 1}})       #update answercount
            messagebox.showinfo('Succeeded!', 'You answer the question successfully!')
            self.window.destroy()
            SignIn(self.uid, self.root)        #go to SignIn
            
        

class ShowAnswer:
    def __init__(self, uid, c, answer_list, accept_id, master=None):
        self.root = master
        self.root.title('Show All Answers')
        self.root.geometry('1100x800')
        self.window = Frame(self.root)
        self.body = StringVar()    
        self.uid = uid
        self.c = c
        self.answer_list = answer_list
        self.accept_id = accept_id
        self.select = StringVar()
        self.create_window()        
    
    
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1) 
        Label(self.window, text = 'INPUT THE SELECT ID:').grid(row = 2, column = 0, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 3, column = 0, sticky = W, pady = 10)
        Button(self.window, text='SELECT', width = 15, command = self.selecttheitem).grid(row = 4, column = 0, sticky = W, pady = 10)        
        Button(self.window, text='SEARCHMORE', width = 15, command = self.searchmoreanswer).grid(row = 5, column = 0, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 6, column = 0, sticky = W, pady = 10) 
        if len(self.answer_list) > 0 and len(self.answer_list) < 5:    #if len(self.return_list) < 5
            for i in range(len(self.answer_list)):
                each_post = col_p.find({"Id": self.answer_list[i]})     #find the row
                for x in each_post:
                    if x.get("Body") == None:
                        body = "None"
                    else:
                        body = x.get("Body") 
                        if len(body) <= 80:
                            show_body = body
                        else:
                            show_body = body[0:80]
                    if x.get("CreationDate") == None:
                        creationDate = "None"
                    else:
                        creationDate = x.get("CreationDate")  
                    if x.get("Score") == None:
                        score = "None"
                    else:
                        score = str(x.get("Score")) 
                    if x.get("Id") == self.accept_id:
                        choose = '*Id: ' + x.get("Id") + ' | Body: ' + show_body + ' | CreationDate: ' + creationDate + ' | Score: ' + score    #show Id, Body, CreationDate, Score
                    else:
                        choose = 'Id: ' + x.get("Id") + ' | Body: ' + show_body + ' | CreationDate: ' + creationDate + ' | Score: ' + score    #show Id, Body, CreationDate, Score
                Label(self.window, text = choose).grid(row = 7 + i, column = 0, sticky = W, pady = 10)             
        else:
            for i in range(5):
                each_post = col_p.find({"Id": self.answer_list[i]})  #find the row
                for x in each_post:
                    if x.get("Body") == None:
                        show_body = "None"
                    else:
                        body = x.get("Body") 
                        if len(body) <= 80:
                            show_body = body
                        else:
                            show_body = body[0:80]
                    if x.get("CreationDate") == None:
                        creationDate = "None"
                    else:
                        creationDate = x.get("CreationDate")  
                    if x.get("Score") == None:
                        score = "None"
                    else:
                        score = str(x.get("Score"))                         
                    if x.get("Id") == self.accept_id:
                        choose = '*Id: ' + x.get("Id") + ' | Body: ' + show_body + ' | CreationDate: ' + creationDate + ' | Score: ' + score    #show Id, Body, CreationDate, Score
                    else:
                        choose = 'Id: ' + x.get("Id") + ' | Body: ' + show_body + ' | CreationDate: ' + creationDate + ' | Score: ' + score    #show Id, Body, CreationDate, Score
                Label(self.window, text = choose).grid(row = 7 + i, column = 0, sticky = W, pady = 10)                 
                       
        del self.answer_list[0:5]      #Delete the first five Ids
        self.window.pack()                

    
    def searchmoreanswer(self):
        if len(self.answer_list) == 0:
            messagebox.showerror('ERROR!', 'No more result!')
        else:
            self.window.destroy()
            ShowAnswer(self.uid, self.c, self.answer_list, self.accept_id, self.root)    #show more answers        
    
    
    def selecttheitem(self):
        if len(self.select.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            user_post = col_p.find({"Id": self.select.get()})
            for x in user_post:
                if x.get("Id") == None:
                    messagebox.showerror('ERROR!', 'The input is not exist!')      
                else:
                    self.c = self.select.get()
                    self.window.destroy()
                    PerformPostAction2(self.uid, self.c, self.root)     #go to PerformPostAction class                 
    
    
    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
        


class PerformPostAction2:
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Perform A Post Action')
        self.root.geometry('2000x2000')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.select = StringVar()
        self.c = c
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.user()
        self.window.pack()    


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
    
    def answer(self):
        Answer(self.uid, self.c, self.root)
        self.window.destroy()

    def vote(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')    #get date
        v_number = col_v.estimated_document_count()
        vote_id = "{:03d}".format(v_number + 1)
        if self.uid != '':
            voted = col_v.find_one({"PostId": self.c, "UserId": self.uid})      #check if the user voted the post before
            if voted == None:
                vote_dic = {
                            "Id": vote_id,
                            "PostId": self.c,
                            "VoteTypeId": "2",
                            "UserId": self.uid,
                            "CreationDate": vote_date
                        }
                col_v.insert_one(vote_dic)
                select_p = col_p.find_one({"Id": self.c}).get("Score")       #get selected post's info
                score = {"Score": select_p}
                new_score = {"$set": { "Score": select_p + 1 } }
                col_p.update_one(score, new_score)            #update post score
                messagebox.showinfo('Succeeded!', 'You vote the post successfully!')
                self.window.destroy()
                SignIn(self.uid, self.root)
            else:
                messagebox.showerror('ERROR!', 'You have already voted this post!')
        else:
            vote_dic = {
                        "Id": vote_id,
                        "PostId": self.c,
                        "VoteTypeId": "2",
                        "CreationDate": vote_date
                }
            col_v.insert_one(vote_dic)
            select_p = col_p.find_one({"Id": self.c}).get("Score")       #get selected post's info
            score = {"Score": select_p}
            new_score = {"$set": { "Score": select_p + 1 } }
            col_p.update_one(score, new_score)            #update post score
            messagebox.showinfo('Succeeded!', 'You vote the post successfully!')
            self.window.destroy()
            SignIn(self.uid, self.root)

    
    def user(self):
        user_post = col_p.find({"Id": self.c})
        for x in user_post:     #see all fields of the question
            self.accept_id = x.get("AcceptedAnswerId")
            print(self.accept_id)
            if x.get("AcceptedAnswerId") == None:
                accepted_answer_id = "None"
            else:
                accepted_answer_id = x.get("AcceptedAnswerId") 
            if x.get("CommunityOwnedDate") == None:
                community_owned_date = "None"
            else:
                community_owned_date = x.get("CommunityOwnedDate")  
            if x.get("ViewCount") == None:
                viewcount = "None"
            else:
                viewcount = str(x.get("ViewCount"))         
            if x.get("CreationDate") == None:
                creationdate = "None"
            else:
                creationdate = x.get("CreationDate")                     
            if x.get("Score") == None:
                score = "None"
            else:
                score = str(x.get("Score"))  
            if x.get("LastEditorUserId") == None:
                last_editor_user_id = "None"
            else:
                last_editor_user_id = x.get("LastEditorUserId")   
            if x.get("LastEditDate") == None:
                last_edit_date = "None"
            else:
                last_edit_date = x.get("LastEditDate")  
            if x.get("LastActivityDate") == None:
                last_activity_date = "None"
            else:
                last_activity_date = x.get("LastActivityDate") 
            if x.get("Tags") == None:
                tags = "None"
            else:
                tags = x.get("Tags") 
            if x.get("AnswerCount") == None:
                answer_count = "None"
            else:
                answer_count = str(x.get("AnswerCount"))  
            if x.get("CommentCount") == None:
                comment_count = "None"
            else:
                comment_count = str(x.get("CommentCount"))   
            if x.get("FavoriteCount") == None:
                favorite_count = "None"
            else:
                favorite_count = str(x.get("FavoriteCount"))
            if x.get("ContentLicense") == None:
                content_license = "None"
            else:
                content_license = x.get("ContentLicense") 
            if x.get("Title") == None:
                title = "None"
            else:
                title = x.get("Title")  
            if x.get("Body") == None:
                body = "None"
            else:
                body = x.get("Body")  
            if x.get("OwnerUserId") == None:
                owner_user_id = "None"
            else:
                owner_user_id = x.get("OwnerUserId")              
            choose1 = 'Id: ' + x.get("Id") + ' | PostTypeId: ' + x.get("PostTypeId") + ' | AcceptedAnswerId: ' + accepted_answer_id + ' | CreationDate: ' +  creationdate
            choose2 = 'Score: ' + score + ' | ViewCount: ' + viewcount          #print all the fields
            body_li = list(body)
            for i in range(len(body_li)):
                if body_li[i] == '.':
                    body_li.insert(i+1,'\n')
            body = ''.join(body_li)    
            choose3 = 'Body: ' + body
            choose4 = 'OwnerUserId: ' +  owner_user_id
            choose5 = 'LastEditorUserId: ' + last_editor_user_id + ' | LastEditDate: ' + last_edit_date + ' | LastActivityDate: ' + last_activity_date + ' | Title: ' +  title
            choose6 = 'Tags: ' + tags + ' | AnswerCount: ' + answer_count + ' | CommentCount: ' + comment_count + ' | FavoriteCount: ' +  favorite_count
            choose7 = "CommunityOwnedDate: " + community_owned_date + ' | ContentLicense: ' + content_license   
        Label(self.window, text = choose1).grid(row = 1, column = 0, sticky = W, pady = 1)  
        Label(self.window, text = choose2).grid(row = 2, column = 0, sticky = W, pady = 1) 
        Label(self.window, text = choose3).grid(row = 3, column = 0, sticky = W, pady = 1)  
        Label(self.window, text = choose4).grid(row = 4, column = 0, sticky = W, pady = 1)
        Label(self.window, text = choose5).grid(row = 5, column = 0, sticky = W, pady = 1)
        Label(self.window, text = choose6).grid(row = 6, column = 0, sticky = W, pady = 1)
        Label(self.window, text = choose7).grid(row = 7, column = 0, sticky = W, pady = 1)
        Button(self.window, text='VOTE', width = 10, command = self.vote).grid(row = 10 , column = 0, sticky = W, pady = 10) 
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 11 , column = 0, sticky = W, pady = 10) 
        
    
    def showallanswers(self):
        self.window.destroy()
        answer_list = []
        answer_list.append(self.accept_id)        

        post_answer = col_p.find({"PostTypeId": "2", "ParentId": self.c})
        for answer in post_answer:
            if answer.get('Id') == self.accept_id:
                pass
            else:
                answer_list.append(answer.get("Id"))        #add all answers to answer_list
        ShowAnswer(self.uid, self.c, answer_list, self.accept_id, self.root)  
 
        
        
        
if __name__ == '__main__':
    root = Tk()
    LogIn(root)
    root.mainloop()
    client.close()   