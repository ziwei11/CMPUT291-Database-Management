from tkinter import *   #GUI
import sqlite3
import tkinter.messagebox as messagebox
import datetime
import random
import sys


connection = None
cursor = None
dbPath = str(sys.argv[1])  #path of database
post_id = None


class LogIn:
    #Login Window
    def __init__(self, master):
        self.root = master
        self.root.title('Login Screen')    #create login window
        self.root.geometry('500x300+10+15')
        self.uid = StringVar()    #get user id
        self.pwd = StringVar()    #get user password
        self.window = Frame(self.root)
        self.create_window()
 
    # Create Window
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uid).grid(row = 2, column = 1, sticky = E)	#input user id
        Label(self.window, text = 'PASSWORD:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.pwd, show = '*').grid(row = 3, column = 1, sticky = E)	#input user password
        Button(self.window, text='SIGN IN', width = 8, command = self.sign_in).grid(row = 4, column = 1, sticky = W, pady = 10)
        Button(self.window, text='SIGN UP', width = 8, command = self.sign_up).grid(row = 5, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def sign_in(self):
        query = "SELECT uid, pwd FROM users WHERE LOWER(uid) = ?;"		#get uid and pwd from database
        val = [self.uid.get().lower()]
        cursor.execute(query, val)
        c = cursor.fetchall()
        if len(c) == 0:
            messagebox.showerror('ERROR!', 'The user does not exist!')
        elif c[0][0].isalnum() == False or c[0][1].isalnum() == False or len(c[0][0]) != 4:		#follow uid and pwd format
            messagebox.showerror('ERROR!', 'Invalid user!')
        else:
            us, pw = c[0]
            if us.lower() == self.uid.get().lower() and pw == self.pwd.get():		#test if the user is in the database
                user_id = self.uid.get().lower()
                self.window.destroy()
                SignIn(self.uid.get().lower(), self.root)		#jump to Sign in page
            else:
                messagebox.showwarning('ERROR!', 'The password is wrong!')


    def sign_up(self):
        self.window.destroy()
        SignUp(self.root)
 
 

class SignUp:
    #Register Window
    def __init__(self, master=None):
        self.root = master
        self.root.title('Sign Up')		#create Sign Up window
        self.root.geometry('500x300')
        self.uid = StringVar()		#get user id
        self.name = StringVar()		#get user name
        self.city = StringVar()		#get user city
        self.pwd = StringVar()		#get user password
        self.window = Frame(self.root)
        self.create_window()

    # Create Window
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uid).grid(row = 2, column = 1, sticky = E)	#input uid
        Label(self.window, text = 'USER NAME:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.name).grid(row = 3, column = 1, sticky = E)	#input user name
        Label(self.window, text = 'CITY:').grid(row = 4, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.city).grid(row = 4, column = 1, sticky = E)	#input user city
        Label(self.window, text = 'PASSWORD:').grid(row = 5, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.pwd).grid(row = 5, column = 1, sticky = E)	#input pwd
        Button(self.window, text='SIGN IN', width = 8, command = self.sign_in).grid(row=6, column = 1, sticky=W, pady=10)
        Button(self.window, text = 'BACK', width = 8, command = self.back).grid(row = 7, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def sign_in(self):
        if len(self.uid.get()) == 0 or len(self.name.get()) == 0 or len(self.city.get()) == 0 or len(self.pwd.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        elif len(self.uid.get()) != 4:
            messagebox.showerror('ERROR!', 'The user id must be four characters!')
        elif self.pwd.get().isalnum() == False or self.uid.get().isalnum() == False:		#follow uid and pwd format
            messagebox.showerror('ERROR!', 'The user id and password will only contain alphanumeric characters!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')		#get date
            query = 'INSERT INTO users VALUES (?,?,?,?,?);'		#insert user information into database
            val = [self.uid.get().lower(), self.name.get().lower(), self.city.get().lower(), date, self.pwd.get()]
            try:
                cursor.execute(query, val)
                self.window.destroy()
                SignIn(self.uid.get().lower(), self.root)		#jump to Sign in page
            except sqlite3.IntegrityError:
                messagebox.showerror('ERROR!', 'The user already exists!')		#test if the user already existed or not


    def back(self):
        self.window.destroy()
        LogIn(self.root)
 


class SignIn:
    #Sign In Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Welcome!')		#create Sign In window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.uid = uid
        self.create_window()

    # Create Window
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.diff_user()
        self.window.pack()
        
        
    #def quit(self):
        #self.window.destroy()
 
 
    def log_out(self):
        self.window.destroy()
        LogIn(self.root)
 
 
    def post_q(self):
        self.window.destroy()
        PostQ(self.uid, self.root)       


    def search(self):
        self.window.destroy()
        Search(self.uid, self.root)


    def diff_user(self):
        cursor.execute("SELECT r.uid FROM privileged r;")		#judge if the user is privileged user
        users = cursor.fetchall()
        uid_list = []
        for i in range(len(users)):
            uid_list.append(users[i][0])
        if self.uid in uid_list:
        	#menu for privileged user
            Button(self.window, text = 'POST QUESTION', width = 20, command = self.post_q).grid(row = 1, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'SEARCH', width = 20, command = self.search).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'GIVE BADGE', width = 20, command = self.give).grid(row = 3, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'LOG OUT', width = 20, command = self.log_out).grid(row = 4, column = 1, sticky = W, pady = 10)
            #Button(self.window, text = 'QUIT', width = 20, command = self.root.quit).grid(row = 5, column = 1, sticky = W, pady = 10)            
        else:
        	#menu for normal user
            Button(self.window, text = 'POST QUESTION', width = 20, command = self.post_q).grid(row = 1, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'SEARCH', width = 20, command = self.search).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'LOG OUT', width = 20, command = self.log_out).grid(row = 3, column = 1, sticky = W, pady = 10)
            #Button(self.window, text = 'QUIT', width = 20, command = self.root.quit).grid(row = 4, column = 1, sticky = W, pady = 10)            
            
            
    def give(self):
        self.window.destroy()
        GiveB(self.uid, self.root)



#Action for Privileged users
class GiveB:
	#Give Badge Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Choose one user and give badge')		#create give badge window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.conn = sqlite3.connect(dbPath)
        self.uid = uid
        self.uname = StringVar()	#get uid
        self.bname = StringVar()	#get badge name
        self.create_window()
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uname).grid(row = 2, column = 1, sticky = E)		#input uid
        Label(self.window, text = 'BADGE NAME:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.bname).grid(row = 3, column = 1, sticky = E)		#input badge name
        Button(self.window, text='SELECT', width = 8, command = self.confirm).grid(row=4, column = 1, sticky=W, pady=10)
        Button(self.window, text = 'BACK', width = 8, command = self.back).grid(row = 5, column =1, sticky = W, pady = 10)    
        self.window.pack()
        
        
    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)        
    
    
    def confirm(self):
        give_date = datetime.datetime.now().strftime('%Y-%m-%d')	#get date
        chosen_user = self.uname.get().lower()
        badge_name = self.bname.get().lower()
        cursor.execute("SELECT u.uid FROM users u;")	#get all users' uid
        total_user = cursor.fetchall()
        total_uid = []
        for i in range(len(total_user)):
            total_uid.append(total_user[i][0].lower())
        if len(chosen_user) == 0 or len(badge_name) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        elif chosen_user in total_uid:
            try:
                cursor.execute('INSERT INTO ubadges VALUES (?,?,?);',(chosen_user,give_date,badge_name,))	#insert uid, date, badge name into database
                messagebox.showerror('Succeeded!', 'You have given a badge to user {}!'.format(chosen_user))	#show which user get badge
                self.window.destroy()
                SignIn(self.uid,self.root)
            except sqlite3.IntegrityError:
                messagebox.showerror('ERROR!', 'This user has had a badged today!')		#a user can only get one badge a day
        else:
            messagebox.showerror('ERROR!', 'The user does not exist!')




class PostQ:
    #Post A Question Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Post A Question')		#create post question window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()	#get post title
        self.body = StringVar()		#get post body
        self.uid = uid
        self.create_window()
        

    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'TITLE:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.title).grid(row = 2, column = 1, sticky = E)		#input title
        Label(self.window, text = 'TEXTS:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.body).grid(row = 3, column = 1, sticky = E)		#input body
        Button(self.window, text='CONFIRM', width = 8, command = self.post).grid(row = 4, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 5, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)


    def post(self):
        if len(self.title.get()) == 0 or len(self.body.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')		#get date
            query = "SELECT pid FROM posts;"
            cursor.execute(query)
            c = cursor.fetchall()
            number = len(c)
            post_id = 'p' + '{:03d}'.format(number + 1)		#A unique pid is assigned by the system
            query = 'INSERT INTO posts VALUES (?,?,?,?,?);'		#insert pid, date, ptitle, pbody, uid into database
            val = [post_id, date, self.title.get(), self.body.get(), self.uid]
            cursor.execute(query, val)
            
            query2 = 'INSERT INTO questions VALUES (?,?);'		#insert pid, answer post id into database
            theaid = None
            val2 = [post_id, theaid]
            cursor.execute(query2, val2)            
            
            self.window.destroy()
            SignIn(self.uid, self.root)
        


class Search:
    #Search A Post Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Search A Question')	#create search post window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.keyword = StringVar()		#get keyword(s)
        self.create_window()
        self.uid = uid


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'KEYWORD:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.keyword).grid(row = 2, column = 1, sticky = E)		#input keyword(s)
        Button(self.window, text='SEARCH', width = 8, command = self.done).grid(row = 3, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
    
    
    def done(self):
        result_list = []
        pid_list = []
        return_list = []
        inp = self.keyword.get()
        keywords = inp.split(',')
        n = len(keywords)
        if len(inp) == 0:
                messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            for i in range(len(keywords)):
                keyword = keywords[i]
                #The user provides one or more keywords, and the system will retrieve all posts that contain at least one keyword either in title, body, or tag fields
                #get pid that meets the requirements
                query = "SELECT p.pid FROM posts p WHERE p.title like '%'||?||'%' UNION SELECT p.pid FROM posts p WHERE p.body like '%'||?||'%' UNION SELECT p.pid FROM posts p, tags t WHERE t.pid = p.pid AND t.tag like '%'||?||'%';"
                cursor.execute(query,(keyword,keyword,keyword))
                c = cursor.fetchall()
                for k in range(len(c)):
                    result_list.append(c[k][0])
            query2 = "SELECT p.pid FROM posts p;"
            cursor.execute(query2)
            c2 = cursor.fetchall()
            for j in range(len(c2)):
                pid_list.append(c2[j][0])
            #The result is ordered based on the number of matching keywords with posts matching the largest number of keywords listed on top
            while n > 0:
                for t in range(len(pid_list)):
                    num = result_list.count(pid_list[t])
                    if num == n:
                        return_list.append(pid_list[t])
                n -= 1         
        if len(return_list) == 0:
            messagebox.showerror('ERROR!', 'No match!')
        else:
            self.window.destroy()  
            ShowResult(self.uid, return_list, self.root)            #jump to the show result window



class ShowResult:
	#Show Result window
    def __init__(self, uid, return_list, master=None):
        self.root = master
        self.root.title('SHOW THE RESULT')		#create Show Result window
        self.root.geometry('800x500')
        self.window = Frame(self.root)
        self.return_list = return_list
        self.length_list = 0
        self.select = StringVar()	#get selected pid
        self.uid = uid
        self.c = None
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        q_list = []
        a_list = []
        #get all posts
        total_q = '''SELECT p.pid
                     FROM posts p, questions q
                     WHERE p.pid = q.pid'''
        cursor.execute(total_q)
        q_all = cursor.fetchall()
        for m in range(len(q_all)):
            q_list.append(q_all[m])
        #get all answers
        total_a = '''SELECT p.pid
                     FROM posts p, answers a
                     WHERE p.pid = a.pid'''
        cursor.execute(total_a)
        a_all = cursor.fetchall()
        for n in range(len(a_all)):
            a_list.append(a_all[n])

        #If there are less than 5 matching posts
        if len(self.return_list) > 0 and len(self.return_list) < 5:
        	#For each matching post
        	#In addition to the columns of posts table, the number of votes, and the number of answers if the post is a question (or zero if the question has no answers) could be displayed
            for i in range(len(self.return_list)):
                query_q = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0'), IFNULL(answer_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                                         left outer join (SELECT p.pid as ppi, COUNT(*) as answer_number
                                                          FROM posts p, answers a 
                                                          WHERE p.pid = a.qid
                                                          GROUP BY p.pid) on p.pid = ppi
                           WHERE p.pid = ?;'''         
                query_a = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                           WHERE p.pid = ?;'''
                val = [self.return_list[i]]
                no_match = 'No Match!'
                #If the post is a question
                for j in range(len(q_list)):
                    if val[0] == q_list[j][0]:
                        cursor.execute(query_q, val)
                #If the post is an answer
                for j in range(len(a_list)):
                    if val[0] == a_list[j][0]:
                        cursor.execute(query_a, val)
                c = cursor.fetchone()  
                Label(self.window, text = c).grid(row = 2+i, sticky = W)	#show result
            del self.return_list[0:len(self.return_list)]
            self.length_list = 0
            
        #If there are more than 5 matching posts
        else:
            for i in range(5):
                query_q = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0'), IFNULL(answer_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                                         left outer join (SELECT p.pid as ppi, COUNT(*) as answer_number
                                                          FROM posts p, answers a 
                                                          WHERE p.pid = a.qid
                                                          GROUP BY p.pid) on p.pid = ppi
                           WHERE p.pid = ?;'''         
                query_a = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                           WHERE p.pid = ?;'''
                val = [self.return_list[i]]
                #If the post is a question
                for j in range(len(q_list)):
                    if val[0] == q_list[j][0]:
                        cursor.execute(query_q, val)
                #If the post is an answer
                for j in range(len(a_list)):
                    if val[0] == a_list[j][0]:
                        cursor.execute(query_a, val)
                c = cursor.fetchone() 
                Label(self.window, text = c).grid(row = 2+i, sticky = W)	#show result
            del self.return_list[0:5] 
            self.length_list = len(self.return_list)             
            
        Label(self.window, text = 'INPUT THE SELECT PID:').grid(row = 7, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 8, sticky = W, pady = 10)		#input your selected pid
        Button(self.window, text='SELECT', width = 15, command = self.selecttheitem).grid(row = 8, sticky = E, column = 1)
        Button(self.window, text='SEARCHMORE', width = 15, command = self.searchmore).grid(row = 9, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 10, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)


    #If there are more than 5 matching posts
    #at most 5 matches will be shown at a time, letting the user select a post or see more matches.
    def searchmore(self):
        if self.length_list == 0:
            messagebox.showerror('ERROR!', 'No more result!')
        else:
            self.window.destroy()
            ShowResult(self.uid, self.return_list, self.root)       


    def selecttheitem(self):
        if len(self.select.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            query = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
            val = [self.select.get()]
            cursor.execute(query, val)
            c = cursor.fetchone()
            
            query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
            val2 = [self.select.get()]
            cursor.execute(query2, val2)
            c2 = cursor.fetchone()                
            #If the selected post is an answer
            if c == None:
                self.c = c2
                self.window.destroy()
                PerformPostAction2(self.uid, self.c, self.root)    
            #If the selected post is a question
            else:
                self.c = c
                self.window.destroy()
                PerformPostAction(self.uid, self.c, self.root)      



#If the selected post is a question, the user can vote it or answer it
class PerformPostAction:
    #Post An Action-Answer Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Perform A Post Action')	#create window
        self.root.geometry('500x400')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.c = c
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.diff_user()
        self.window.pack()    


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)
        
        
    def answer(self):
        self.window.destroy()
        InputActionA(self.uid, self.c, self.root)
        
      
    def vote(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')	#get date
        query = "SELECT v.vno FROM votes v WHERE v.pid = (?);"		#insert vote number into database
        val = [(self.c)[0]]
        cursor.execute(query, val)
        c = cursor.fetchall()
        number = len(c)
        vote_number = number + 1
        query = 'INSERT INTO votes VALUES (?,?,?,?);'	#insert pid, vote number, date, uid into database
        post_id = (self.c)[0]
        val = [post_id, vote_number, vote_date, self.uid]
        cursor.execute(query, val)        
        self.window.destroy()
        Search(self.uid, self.root)  
        
        
    def diff_user(self):
    	#judge if the user is privileged user
        query = "SELECT r.uid FROM privileged r;"
        cursor.execute(query)
        users = cursor.fetchall()
        uid_list = []
        for i in range(len(users)):
            uid_list.append(users[i][0])
        #if the user is privileged user
        if self.uid in uid_list:
            Button(self.window, text='ANSWER IT', width = 10, command = self.answer).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 3, column = 1, sticky = W, pady = 10)           
            Button(self.window, text='MARK', width = 10, command = self.show_answer).grid(row = 4, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'ADD TAG', width = 10, command = self.add_tag).grid(row = 5, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'EDIT', width = 10, command = self.edit_post).grid(row = 6, column = 1, sticky = W, pady = 10)
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 7, column = 1, sticky = W, pady = 10) 
        #if the user is not privileged user
        else:
            Button(self.window, text='ANSWER IT', width = 10, command = self.answer).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 3, column = 1, sticky = W, pady = 10)          
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)            
            
            
    def show_answer(self):
        self.window.destroy()
        Answers(self.uid, self.c, self.root)


    def add_tag(self):
        self.window.destroy()
        AddTag(self.uid, self.c, self.root)


    def edit_post(self):
        self.window.destroy()
        EditP(self.uid, self.c, self.root)



#If the selected post is an answer, the user can only vote
class PerformPostAction2:
    #Post An Action-Answer Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Perform A Post Action')	#create window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.c = c
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.diff_user()
        self.window.pack()


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)
        
        
    def vote(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')	#get date
        query = "SELECT v.vno FROM votes v WHERE v.pid = (?);"		#insert vote number into database
        val = [(self.c)[0]]
        cursor.execute(query, val)
        c = cursor.fetchall()
        number = len(c)
        vote_number = number + 1
        query = 'INSERT INTO votes VALUES (?,?,?,?);'		#insert pid, vote number, date, uid into database
        post_id = (self.c)[0]
        val = [post_id, vote_number, vote_date, self.uid]
        cursor.execute(query, val)        
        self.window.destroy()
        Search(self.uid, self.root)               


    def diff_user(self):
    	#judge if the user is privileged user
        query = "SELECT r.uid FROM privileged r;"
        cursor.execute(query)
        users = cursor.fetchall()
        uid_list = []
        for i in range(len(users)):
            uid_list.append(users[i][0])
        if self.uid in uid_list:
        #if the user is privileged user
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 2, column = 1, sticky = W, pady = 10)           
            Button(self.window, text = 'ADD TAG', width = 10, command = self.add_tag).grid(row = 3, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'EDIT', width = 10, command = self.edit_post).grid(row = 4, column = 1, sticky = W, pady = 10)
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 5, column = 1, sticky = W, pady = 10) 
        #if the user is not privileged user
        else:
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 2, column = 1, sticky = W, pady = 10)          
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 3, column = 1, sticky = W, pady = 10)            
            

    def add_tag(self):
        self.window.destroy()
        AddTag(self.uid, self.c, self.root)


    def edit_post(self):
        self.window.destroy()
        EditP(self.uid, self.c, self.root)
    


#Action for Privileged users
class Answers:
	#Mark the Answer Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Here Are All Answers')		#create Mark the Answer Window
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.select = StringVar()		#get selected answer's pid
        self.uid = uid
        self.c = c
        self.create_window()
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        n = 0
        answers_list = []
        #get all of answers of the selected pid
        query = "SELECT a.pid FROM answers a WHERE a.qid = (?);"
        quesid = self.c[0]
        val = [quesid]
        cursor.execute(query,val)
        c = cursor.fetchall()
        for i in range(len(c)):
            answers_list.append(c[i][0])
        ##get all of answers' information of the selected pid
        for j in range(len(answers_list)):
            query = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                       FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                       WHERE p.pid = ?;'''
                    
            val = [answers_list[j]]
            cursor.execute(query,val)
            c2 = cursor.fetchone() 
            Label(self.window, text = c2).grid(row = 2+j, sticky = W) 
            n += 1
            
        Label(self.window, text = 'INPUT THE SELECTED ANSWER:').grid(row = 2+n, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 3+n, sticky = W, pady = 10)        #input selected answer's pid
        Button(self.window, text='SELECT', width = 10, command = self.confirm).grid(row = 3 + n, sticky = E, column = 0)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 4 + n, sticky = E, pady = 10)        
        self.window.pack()
        
        
    def back(self):
        self.window.destroy()
        PerformPostAction(self.uid, self.c, self.root)


    def confirm(self):
        quesid = self.c[0]
        cursor.execute('SELECT q.theaid FROM questions q WHERE q.pid = (?);',(quesid,))
        c = cursor.fetchone()
        #Mark or change the answer
        if c[0] == None:
            cursor.execute("UPDATE questions SET theaid = (?);",(self.select.get(),))	#update the answer of the question in database
            messagebox.showerror('Succeeded!', 'You have already set it as the accepted answer of question {}!'.format(self.c[0]))            
        else:
            self.window.destroy()
            Confirm(self.uid, self.c, self.select, self.root)
  
       


#Confirm your marked answer
class Confirm:
	#Confirm Window
    def __init__(self, uid, c, select, master=None):
        self.root = master
        self.root.title('Confirm your choose')	#create Confirm Window
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.select = select
        self.uid = uid
        self.c = c
        self.create_window() 
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)        
        #make sure your answer
        Label(self.window, text = 'Are You Sure You Want To Change The Accepted Answer?').grid(row = 2, sticky = W, pady = 10)
        Button(self.window, text='CONFIRM', width = 10, command = self.yes).grid(row = 3, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)
        self.window.pack()
        
        
    def yes(self):
        self.window.destroy()
        Compare(self.uid, self.c, self.select, self.root)


    def back(self):
        self.window.destroy()
        Answers(self.uid, self.c, self.root)
            
   
   
#Compare the answer you want to mark to the original one
class Compare:
	#Compare Window
    def __init__(self, uid, c, select, master=None):
        self.root = master
        self.root.title('Compare the two potential accepted answers')	#create Compare Window
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.select = select
        self.uid = uid
        self.c = c
        self.create_window()
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)        
        Label(self.window, text = 'Here are the two potential accepted answers').grid(row = 2, sticky = W, pady = 10)
        Label(self.window, text = 'The original one:').grid(row = 3, sticky = W, pady = 10)
        self.original()
        Label(self.window, text = 'The new one:').grid(row = 5, sticky = W, pady = 10)
        self.new_choice()
        Button(self.window, text='KEEP PREVIOUS', width = 15, command = self.previous).grid(row = 7, column = 1, sticky = W, pady = 10)
        Button(self.window, text='CHANGE', width = 15, command = self.change).grid(row = 8, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 15, command = self.back).grid(row = 9, column = 1, sticky = W, pady = 10)
        self.window.pack()
        
        
    def original(self):
    	#select the question
        cursor.execute("SELECT q.theaid FROM questions q WHERE q.pid = (?);",(self.c[0],))
        result = cursor.fetchone()
        #select the original answer
        #show information of the original answer
        query2 = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                 FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                FROM posts p, votes v 
                                                WHERE v.pid = p.pid
                                                GROUP BY p.pid) on p.pid = pi
                 WHERE p.pid = ?;'''       
        val2 = [result[0]]
        cursor.execute(query2,val2)
        c2 = cursor.fetchall()
        Label(self.window, text = c2).grid(row = 4, sticky = W, pady = 10)
        
        
    def new_choice(self):
    	#select the new answer
    	#show information of the new answer
        query = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                               FROM posts p, votes v 
                                               WHERE v.pid = p.pid
                                               GROUP BY p.pid) on p.pid = pi
                WHERE p.pid = ?;'''
        val = [self.select.get()]
        cursor.execute(query,val)
        c = cursor.fetchall()
        Label(self.window, text = c).grid(row = 6, sticky = W, pady = 10)
        
    
    #do not change the answer
    def previous(self):
        messagebox.showinfo('Notification', 'You keep your original choice.') 
    
    
    #change the answer
    def change(self):
        cursor.execute("UPDATE questions SET theaid = (?);",(self.select.get(),))
        messagebox.showinfo('Succeeded!', 'You have changed the accepted answer of question {}'.format(self.c[0]))
        self.window.destroy()
        Answers(self.uid, self.c, self.root)
        
        
    def back(self):
        self.window.destroy()
        Confirm(self.uid, self.c, self.select, self.root)
             
        


#Action for Privileged users
class AddTag:
	#Add Tag Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Add A Tag')	#create Add Tag Window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.uid = uid
        self.c = c
        self.ttext = StringVar()	#get tag text
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        #get all of the tags of the selected post
        check = 'SELECT t.tag FROM tags t WHERE t.pid = ?;'
        val = [self.c[0]]
        cursor.execute(check, val)
        t_tag = cursor.fetchall()
        Label(self.window, text = 'Your tags: ').grid(row = 2, sticky = W)		#show all of the tags of the selected post
        Label(self.window, text = t_tag).grid(row = 2, column = 1, sticky = E, pady = 10)
        Label(self.window, text = 'TAG:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.ttext).grid(row = 3, column = 1, sticky = E)		#input tag text
        Button(self.window, text = 'CONFIRM', width = 8, command = self.add).grid(row = 4, column =1, sticky = W, pady = 10)
        Button(self.window, text = 'BACK', width = 8, command = self.back).grid(row = 5, column =1, sticky = W, pady = 10)
        self.window.pack()


    def add(self):
        if len(self.ttext.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            query = 'INSERT INTO tags VALUES (?,?);'	#insert tag pid and tag text into database
            val = [self.c[0], self.ttext.get()]
            try:
                cursor.execute(query, val)
                messagebox.showinfo('Succeeded!', 'You add the tag successfully!')
                self.window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror('ERROR!', 'The tag already exists!')	#cannot insert tha same tag for one post
            
            query1 = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
            val1 = [self.c[0]]
            cursor.execute(query1, val1)
            c = cursor.fetchone()
            
            query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
            val2 = [self.c[0]]
            cursor.execute(query2, val2)
            c2 = cursor.fetchone()                
            if c == None:
                self.c = c2
                self.window.destroy()
                PerformPostAction2(self.uid, self.c, self.root)    
            else:
                self.c = c
                self.window.destroy()
                PerformPostAction(self.uid, self.c, self.root)                


    def back(self):
        self.window.destroy()
        query = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
        val = [self.c[0]]
        cursor.execute(query, val)
        c = cursor.fetchone()
        
        query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
        val2 = [self.c[0]]
        cursor.execute(query2, val2)
        c2 = cursor.fetchone()                
        if c == None:
            self.c = c2
            self.window.destroy()
            PerformPostAction2(self.uid, self.c, self.root)    
        else:
            self.c = c
            self.window.destroy()
            PerformPostAction(self.uid, self.c, self.root)              
        


#Action for Privileged users
class EditP:
	#Edit Post Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Edit Post')	#create Edit Post Window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.uid = uid
        self.c = c
        self.ptitle = StringVar()	#get new post title
        self.pbody = StringVar()	#get new post body
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        #get the original post
        check = 'SELECT p.title, p.body FROM posts p WHERE p.pid = ?;'
        val = [self.c[0]]
        cursor.execute(check, val)
        old_post = cursor.fetchall()
        Label(self.window, text = 'Original post: ').grid(row = 2, sticky = W)
        Label(self.window, text = old_post).grid(row = 2, column = 1, sticky = E, pady = 10)
        Label(self.window, text = 'TITLE:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.ptitle).grid(row = 3, column = 1, sticky = E)	#input new post title
        Label(self.window, text = 'TEXTS:').grid(row = 4, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.pbody).grid(row = 4, column = 1, sticky = E)		#input new post body
        Button(self.window, text='CONFIRM', width = 10, command = self.edit).grid(row = 5, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 6, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def edit(self):
        if len(self.ptitle.get()) == 0 or len(self.pbody.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            cursor.execute("UPDATE posts SET title = (?) WHERE pid = ?;", (self.ptitle.get(), self.c[0]))	#update new post title into database
            cursor.execute("UPDATE posts SET body = (?) WHERE pid = ?;", (self.pbody.get(), self.c[0]))		#update new post body into database
            messagebox.showinfo('Succeeded!', 'You edit the post successfully!')
            query1 = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
            val1 = [self.c[0]]
            cursor.execute(query1, val1)
            c = cursor.fetchone()
            
            query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
            val2 = [self.c[0]]
            cursor.execute(query2, val2)
            c2 = cursor.fetchone()                
            if c == None:
                self.c = c2
                self.window.destroy()
                PerformPostAction2(self.uid, self.c, self.root)    
            else:
                self.c = c
                self.window.destroy() 
                PerformPostAction(self.uid, self.c, self.root)    


    def back(self):
        self.window.destroy()
        query = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
        val = [self.c[0]]
        cursor.execute(query, val)
        c = cursor.fetchone()
        
        query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
        val2 = [self.c[0]]
        cursor.execute(query2, val2)
        c2 = cursor.fetchone()                
        if c == None:
            self.c = c2
            self.window.destroy()
            PerformPostAction2(self.uid, self.c, self.root)    
        else:
            self.c = c
            self.window.destroy() 
            PerformPostAction(self.uid, self.c, self.root) 

            
            
#Post An Answer Action
class InputActionA:
	#Post An Answer Window
    def __init__(self, uid, qid, master=None):
        self.root = master
        self.root.title('Post An Action-Answer')	#create Post An Answer Window
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()	#get answer title
        self.body = StringVar()		#get answer body
        self.qid = qid[0]
        self.uid = uid
        self.c = qid
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'POST TITLE:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.title).grid(row = 2, column = 1, sticky = E)		#input answer title
        Label(self.window, text = 'POST TEXTS:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.body).grid(row = 3, column = 1, sticky = E)		#input answer body
        Button(self.window, text='CONFIRM', width = 8, command = self.confirm_answer).grid(row = 4, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 5, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        PerformPostAction(self.uid, self.c, self.root)   
        
        
    def confirm_answer(self):
        if len(self.title.get()) == 0 or len(self.body.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')		#get date
            query = "SELECT pid FROM posts;"
            cursor.execute(query)
            c = cursor.fetchall()
            number = len(c)
            post_id = 'p' + '{:03d}'.format(number + 1)		#A unique pid is assigned by the system
            query = 'INSERT INTO posts VALUES (?,?,?,?,?);'		#insert pid, date, answer title, answer body, uid into database
            val = [post_id, date, self.title.get(), self.body.get(), self.uid]
            cursor.execute(query, val)
            
            query2 = 'INSERT INTO answers VALUES (?,?);'	##insert answer pid and its question's pid into database
            val2 = [post_id, self.qid]
            cursor.execute(query2, val2)
            self.window.destroy()
            Search(self.uid, self.root)  
        
        
       

if __name__ == '__main__':
    root = Tk()
    connection = sqlite3.connect(dbPath)	#connect to database
    cursor = connection.cursor()    
    LogIn(root)		#run the project loop
    root.mainloop()
    connection.commit()		#push the query into database
    connection.close()    #close the database