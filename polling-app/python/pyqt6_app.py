import sys, random, string
import time as t
from PyQt6.QtWidgets import * 
from PyQt6 import uic
from appdb import *

ui_path = connect_to_ui() # path to .ui file
db_connection = connect_to_db() # sqlite3 Connection object
cursor = db_connection.cursor()
# alert box dims = (341, 51)
# option box dims = (301, 31)
# close alert button dims = (21, 21)

class Gui(QMainWindow):
    
    def __init__(self):

        super(Gui, self).__init__()
        self.__load_gui__()
        self.pages = self.findChild(QStackedWidget, "stackedWidget")
        self.__setup__()
        self.__show_login__()
        


    def __load_gui__(self):

        uic.loadUi(ui_path, self)
        self.show()


    def __setup__(self): # execute all setup methods

        self.__setup_wrappers__()
        self.__setup_inputs__()
        self.__setup_labels__()
        self.__add_general_button_actions__()
        self.__setup_options__()
        self.__setup_view_polls__()
        self.__setup_userpoll__()
        self.last_vote = 0
        self.user_poll_index = 0


    def __sniff__(self, instance): # sniff out suspicious inputs

        self.sqlblacklist = [
            "'", "\"", "/*", "--", ";", "xp_", "exec", 
            "sp_", "delete", "insert", "update", "drop", 
            "truncate", "union", "select", " ",
            ]
        
        for element in instance:
            temp = element.strip(r'"').lower()
            if temp in self.sqlblacklist:
                return False
        return True

# ----------- ..... ------------ SETUP ----------- ..... ------------ #


    def __add_general_button_actions__(self):

        # in-place action
        self.submit_login = self.pages.findChild(QPushButton, "login")
        self.submit_register = self.findChild(QPushButton, "signup")
        self.submit_captcha = self.findChild(QPushButton, "go")
        self.sign_out = self.findChild(QPushButton, "signout")
        self.close_alert = self.findChild(QPushButton, "close_alert")
        self.reset_votes = self.findChild(QPushButton, "resetvotes")
        self.post_poll = self.findChild(QPushButton, "create")
        self.delete_acc = self.findChild(QPushButton, "deleteacc")
        self.close_acc_alert = self.findChild(QPushButton, "closeaccalert")

        # page accesser
        self.create_poll_page = self.findChild(QPushButton, "create_poll")
        self.vote_poll_page = self.findChild(QPushButton, "view_poll")
        self.account_page = self.findChild(QPushButton, "view_account")
        self.go_home = self.findChild(QPushButton, "home")
        self.view_polls = self.findChild(QPushButton, "viewpolls")
        self.return_home = self.findChild(QPushButton, "returnhome")

        # slot connections
        self.create_poll_page.clicked.connect(self.__show_createpoll__)
        self.vote_poll_page.clicked.connect(self.__show_viewpoll__)
        self.account_page.clicked.connect(self.__show_account__)
        self.go_home.clicked.connect(self.__show_main__)
        self.submit_login.clicked.connect(self.__login__)
        self.submit_register.clicked.connect(self.__process_signup__)
        self.submit_captcha.clicked.connect(self.__verify_captcha__)
        self.sign_out.clicked.connect(self.__signout__)
        self.close_alert.clicked.connect(self.__close_alert__)
        self.reset_votes.clicked.connect(self.__reset_votes__)
        self.post_poll.clicked.connect(self.__post_poll__)
        self.close_acc_alert.clicked.connect(self.__close_account_alert__)
        self.view_polls.clicked.connect(self.__show_user_polls__)
        self.return_home.clicked.connect(self.__show_main__)
        self.delete_acc.clicked.connect(self.__delete_account__)

   
    def __setup_inputs__(self):

        # register/login inputs
        self.username_input = self.findChild(QLineEdit, "username_input")
        self.password_input = self.findChild(QLineEdit, "password_input")
        self.captcha_input = self.findChild(QLineEdit, "captcha_input")
        self.poll_prompt_input = self.findChild(QLineEdit, "promptinput")

    
    def __setup_userpoll__(self):

        self.user_poll_index = 1
        self.nextpoll = self.findChild(QPushButton, "next")
        self.prevpoll = self.findChild(QPushButton, "prev")
        self.deletepoll = self.findChild(QPushButton, "deletepoll")

        self.nextpoll.clicked.connect(self.__next_user_poll__) 
        self.prevpoll.clicked.connect(self.__prev_user_poll__) 
        self.deletepoll.clicked.connect(self.__delete_user_poll__)  

        self.user_poll_prompt = self.findChild(QLabel, "userprompt")
        self.user_poll_option_one = self.findChild(QLabel, "useroption1")
        self.user_poll_option_two = self.findChild(QLabel, "useroption2")
        self.user_poll_option_three = self.findChild(QLabel, "useroption3")
        self.user_poll_option_four = self.findChild(QLabel, "useroption4")
        self.user_poll_option_five = self.findChild(QLabel, "useroption5")

        self.user_poll_option_labels = [
            self.user_poll_option_one, 
            self.user_poll_option_two,
            self.user_poll_option_three,
            self.user_poll_option_four,
            self.user_poll_option_five,
        ]

        self.user_poll_option_one_votes = self.findChild(QLabel, "useroption1vote")
        self.user_poll_option_two_votes = self.findChild(QLabel, "useroption2vote")
        self.user_poll_option_three_votes = self.findChild(QLabel, "useroption3vote")
        self.user_poll_option_four_votes = self.findChild(QLabel, "useroption4vote")
        self.user_poll_option_five_votes = self.findChild(QLabel, "useroption5vote")

        self.user_poll_option_vote_labels = [
            self.user_poll_option_one_votes, 
            self.user_poll_option_two_votes,
            self.user_poll_option_three_votes,
            self.user_poll_option_four_votes,
            self.user_poll_option_five_votes,
        ]

        self.user_poll_index_label = self.findChild(QLabel, "index")
        self.user_poll_total_votes = self.findChild(QLabel, "totalvotes")
        self.user_poll_votes_sum = self.findChild(QLabel, "usertotalvote")


    def __setup_labels__(self):

        # create basic label connections
        self.alert = self.findChild(QLabel, "alert")
        self.user_account_alert = self.findChild(QLabel, "accalertlabel")
        self.captcha_box = self.findChild(QLabel, "captchabox")
        self.welcome_msg = self.findChild(QLabel, "welcomemsg")
        self.user_intro = self.findChild(QLabel, "introuser")
        

    def __setup_wrappers__(self):
        
        # group-box widget connections
        self.alertbox = self.findChild(QGroupBox, "alert_box")
        self.accountalertbox = self.findChild(QGroupBox, "account_alert")
        self.pollbox = self.findChild(QGroupBox, "poll")
        self.userpollbox = self.findChild(QGroupBox, "userpoll_gb")
        

    def __setup_options__(self):

        # create poll
        self.option_one = self.findChild(QLineEdit, "option1input")
        self.option_two = self.findChild(QLineEdit, "option2input")
        self.option_three = self.findChild(QLineEdit, "option3input")
        self.option_four = self.findChild(QLineEdit, "option4input")
        self.option_five = self.findChild(QLineEdit, "option5input")
        self.options = [self.option_one, self.option_two, self.option_three, self.option_four, self.option_five]

        self.rm_op_three = self.findChild(QPushButton, "rm_option_3")
        self.rm_op_four = self.findChild(QPushButton, "rm_option_4")
        self.rm_op_five = self.findChild(QPushButton, "rm_option_5")
        self.rm_op_three.clicked.connect(self.__remove_poll_option__)
        self.rm_op_four.clicked.connect(self.__remove_poll_option__)
        self.rm_op_five.clicked.connect(self.__remove_poll_option__)

        self.add_option = self.findChild(QPushButton, "add_option")
        self.add_option.clicked.connect(self.__add_poll_option__)


    def __setup_view_polls__(self):

        # vote option labels and buttons
        self.poll_prompt = self.findChild(QLabel, "prompt")
        self.dp_option_one = self.findChild(QRadioButton, "option1")
        self.dp_option_two = self.findChild(QRadioButton, "option2")
        self.dp_option_three = self.findChild(QRadioButton, "option3")
        self.dp_option_four = self.findChild(QRadioButton, "option4")
        self.dp_option_five = self.findChild(QRadioButton, "option5")

        self.dp_options = [
            self.dp_option_one,
            self.dp_option_two,
            self.dp_option_three,
            self.dp_option_four,
            self.dp_option_five, 
        ]

        # small widgets to fill a gap in GUI
        self.dp_option1_color = self.findChild(QWidget, "op1color")         
        self.dp_option2_color = self.findChild(QWidget, "op2color")
        self.dp_option3_color = self.findChild(QWidget, "op3color")
        self.dp_option4_color = self.findChild(QWidget, "op4color")
        self.dp_option5_color = self.findChild(QWidget, "op5color")

        self.dp_op_colors = [
            self.dp_option1_color,
            self.dp_option2_color,
            self.dp_option3_color,
            self.dp_option4_color,
            self.dp_option5_color,
        ]

        # number / percent of votes labels
        self.dp_option_one_votes = self.findChild(QLabel, "option1vote")
        self.dp_option_two_votes = self.findChild(QLabel, "option2vote")
        self.dp_option_three_votes = self.findChild(QLabel, "option3vote")
        self.dp_option_four_votes = self.findChild(QLabel, "option4vote")
        self.dp_option_five_votes = self.findChild(QLabel, "option5vote")
        
        self.dp_option_vote_list = [
            self.dp_option_one_votes,
            self.dp_option_two_votes,
            self.dp_option_three_votes,
            self.dp_option_four_votes,
            self.dp_option_five_votes,
        ]

        self.poll_votes_widj = self.findChild(QLabel, "numvotes")
        self.poll_thank_you = self.findChild(QLabel, "thanks")

        # option vote slots
        self.dp_option_one.clicked.connect(self.__vote_option_one__)
        self.dp_option_two.clicked.connect(self.__vote_option_two__)
        self.dp_option_three.clicked.connect(self.__vote_option_three__)
        self.dp_option_four.clicked.connect(self.__vote_option_four__) 
        self.dp_option_five.clicked.connect(self.__vote_option_five__)

        # clear placeholders
        self.dp_option_one_votes.setText('')
        self.dp_option_two_votes.setText('')
        self.dp_option_three_votes.setText('')
        self.dp_option_four_votes.setText('') 
        self.dp_option_five_votes.setText('') 
        self.poll_votes_widj.setText('')
        self.poll_thank_you.setText('')

        
# ----------- ..... ------------ PAGES ----------- ..... ------------ #


    def __show_login__(self): # PAGE 1

        self.go_home.hide()
        self.sign_out.hide()
        self.pages.setCurrentIndex(0)


    def __show_captcha__(self): # PAGE 2

        self.captcha_input.setText("")
        self.pages.setCurrentIndex(1)
        self.__generate_captcha__()
    

    def __show_main__(self): # PAGE 3

        self.go_home.show()
        self.sign_out.show()
        self.last_vote = 0
        self.__reset_viewpoll__()
        self.pages.setCurrentIndex(2)

    
    def __show_account__(self): # PAGE 4

        self.accountalertbox.resize(0, 0)
        self.pages.setCurrentIndex(3)


    def __show_viewpoll__(self): # PAGE 5

        for x in range(len(self.dp_options)):
            self.dp_options[x].setAutoExclusive(False)
            self.dp_options[x].setChecked(False)
            self.dp_options[x].setAutoExclusive(True)

        self.__get_rand_poll__()
        self.pages.setCurrentIndex(4)


    def __show_createpoll__(self): # PAGE 6

        self.curr_num_options = 2 # every poll must have at least 2 options.
        self.__reset_createpoll__()
        self.__option_tree__()
        self.pages.setCurrentIndex(5)

    
    def __show_success__(self): # PAGE 7

        self.pages.setCurrentIndex(6)


    def __show_user_polls__(self): # PAGE 8

        self.__get_user_polls__()
        if len(self.user_poll_list) == 0:
            self.__account_alert__("You have no polls to display!")
        else:
            self.pages.setCurrentIndex(7)


# ----------- ..... ------------ REGISTRATION ----------- ..... ------------ #


    def __process_signup__(self):

        username = self.username_input.text()
        password = self.password_input.text()

        if " " in username or username == "" or " " in password or password == "":
            self.__alert__("Invalid username or password. Please try again.")
            self.username_input.setText("")
            self.password_input.setText("")

        elif self.__sniff__(username) is not True or self.__sniff__(password) is not True:
            self.__alert__("Suspicious input detected! Try again.")
            self.username_input.setText("")
            self.password_input.setText("")

        elif query_get("get_user", [fr'"{username}"'], cursor) is True:
            self.__alert__("Username already in use. Try again.")
            self.username_input.setText("")
            self.password_input.setText("")

        else:
            self.__send_register__(username, password)


    def __send_register__(self, u, p):

        user_instance = query_get("get_max_userid", None, cursor)[0]
        uid = user_instance[0] + 1
        self.current_user = User(u, p)
        self.current_user.uid = uid
        self.__show_captcha__()


    def __generate_captcha__(self): # approved

        self.captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        self.captcha_box.setText(self.captcha_text)


    def __verify_captcha__(self):

        self.captcha_response = self.captcha_input.text()

        if self.captcha_response == self.captcha_box.text():
            query_post("add_user", self.current_user.structure, cursor)
            self.captcha_input.setText("")
            self.__include_user__()
            self.__show_main__()

        else:
            self.password_input.setText("")
            self.__show_login__() # on failure go back to login/register
            self.__alert__("Mismatching captcha response. Please try again.")


    def __alert__(self, alert_text):

        self.alert.setText(f"{alert_text}")
        self.alertbox.resize(341, 51)
        

    def __close_alert__(self):

        self.alert.setText("")
        self.alertbox.resize(0, 0)


# ----------- ..... ------------ LOGIN/LOGOUT ----------- ..... ------------ #


    def __login__(self): # GOOD
        
        username = self.username_input.text()
        password = self.password_input.text()
        user = query_get("get_user", [fr'"{username}"'], cursor)

        if user == []:
            self.__alert__("Invalid username password combo. Please try again.")
        
        else:
            temp_tuple = user[0]

            if hash_match(password, temp_tuple[2]):
                self.current_user = User(username, password)
                self.current_user.uid = temp_tuple[0]
                self.__include_user__()
                self.__show_main__()

            else:
                self.__alert__("Invalid username password combo. Please try again.")


    # post username to pages where it's used
    def __include_user__(self): 

        self.welcome_msg.setText(f"Welcome {self.current_user.username}!")
        self.user_intro.setText(f"{self.current_user.username}")


    def __signout__(self): 

        self.current_user = None
        self.password_input.setText("")
        self.__close_alert__()
        self.__show_login__()


# ----------- ..... ------------ RESET ----------- ..... ------------ #


    def __reset_viewpoll__(self):

        for vote in self.dp_option_vote_list:
            vote.setText("")

        for x in range(len(self.dp_options)):
            self.dp_options[x].setStyleSheet("background-color: transparent;")
            self.dp_op_colors[x].setStyleSheet("background-color: transparent;")

        self.poll_votes_widj.setText("")
        self.poll_thank_you.setText("")

    
    def __reset_createpoll__(self):
        
        self.poll_prompt_input.setText("")
        self.option_one.setText("")
        self.option_two.setText("")
        self.option_three.setText("")
        self.option_four.setText("")
        self.option_five.setText("")
        self.option_three.resize(0, 0)
        self.option_four.resize(0, 0)
        self.option_five.resize(0, 0)      
        self.rm_op_three.resize(0, 0)
        self.rm_op_four.resize(0, 0)
        self.rm_op_five.resize(0, 0)

    
    def __reset_votes__(self):

        all_votes = query_get("get_all_votes", [self.current_user.uid], cursor)
        if all_votes != []:
            for vote in all_votes:
                query_post("rm_vote", [vote[1], vote[2], vote[0]], cursor)
            self.__show_success__()
        else:
            self.__account_alert__("You don't have any votes to remove!")


# ----------- ..... ------------ CREATE POLL ----------- ..... ------------ #

        
    def __add_poll_option__(self):
        
        self.curr_num_options += 1
        self.__option_tree__()


    def __remove_poll_option__(self):
        
        self.curr_num_options -= 1
        self.__option_tree__()


    def __option_tree__(self): # adjust gui based on number of options

        if self.curr_num_options == 2:
            self.add_option.move(190, 220)
            self.option_three.resize(0, 0)
            self.rm_op_three.resize(0, 0)

        elif self.curr_num_options == 3:
            self.add_option.move(190, 260)
            self.option_three.resize(301, 31)
            self.rm_op_three.resize(21, 21)
            self.option_four.resize(0, 0)
            self.rm_op_four.resize(0, 0)

        elif self.curr_num_options == 4:
            self.add_option.move(190, 300)
            self.option_four.resize(301, 31)
            self.rm_op_four.resize(21, 21)
            self.option_five.resize(0, 0)
            self.rm_op_five.resize(0, 0)

        elif self.curr_num_options == 5:
            self.add_option.move(190, 340)
            self.option_five.resize(301, 31)
            self.rm_op_five.resize(21, 21)

        else:
            pass


    def __post_poll__(self): # post the created poll to DB

        index = 0

        num_options = self.curr_num_options
        option_list = self.options[0:num_options]
        new_poll = Poll(self.current_user.uid, self.poll_prompt_input.text(), option_list) # create new Poll object

        query_post("add_poll", new_poll.structure, cursor) # post the poll instance to the DB
        temptup = query_get("get_l_poll", None, cursor)[0]
        poll_id = temptup[0]

        for option in option_list:
            index += 1
            query_post("add_option", (poll_id, index, fr'"{option.text()}"'), cursor) # post the options to DB

        self.__show_success__()


# ----------- ..... ------------ VIEW POLL ----------- ..... ------------ #


    def __get_rand_poll__(self): # comments added as this code is pretty bulky
        
        index = 0
        tuple_containing_lastrow = query_get("get_l_poll", None, cursor)[0]

        self.poll_cap = tuple_containing_lastrow[0]
        self.random_poll_id = random.randint(1, self.poll_cap)

        user_votes = query_get("get_votes", [self.current_user.uid, self.random_poll_id], cursor)
        cached_voted_polls = [uservote[1] for uservote in user_votes if uservote[0] == self.current_user.uid] # get all polls a user has voted on

        while self.random_poll_id in cached_voted_polls: # don't show the user a poll they've already voted on
            self.random_poll_id = random.randint(1, self.poll_cap)

        tuple_with_random_poll = query_get("get_poll", [self.random_poll_id], cursor)[0]
        q_random_poll_ops = query_get("get_options", [self.random_poll_id], cursor)
        
        self.dp_poll_options = [option[2] for option in q_random_poll_ops] # select option content
        self.dp_option_votes = [option[3] for option in q_random_poll_ops]
        self.num_options = len(self.dp_poll_options)
        
        # tuple with random poll: 0 -> PollID .. 1 -> UserID 2 -> Content

        self.display_poll = Poll(tuple_with_random_poll[1], tuple_with_random_poll[2], self.dp_poll_options)
        self.display_poll.pid = tuple_with_random_poll[0]

        self.poll_prompt.setText(f"{self.display_poll.content}")
        
        for x in self.dp_poll_options:
            self.dp_options[index].setText(x) # fetch option text and post to screen
            index += 1

        self.__view_poll_tree__() # dynamically resize and adjust the poll-box based on number of options
    

    def __view_poll_tree__(self):

        if self.num_options == 2:

            self.dp_option_three.setVisible(False)
            self.dp_option_four.setVisible(False)
            self.dp_option_five.setVisible(False)
            self.pollbox.resize(361, 221)
            self.poll_thank_you.move(20, 180)
            self.poll_votes_widj.move(270, 180)

        if self.num_options == 3:
            self.dp_option_three.setVisible(True)
            self.dp_option_four.setVisible(False)
            self.dp_option_five.setVisible(False)
            self.pollbox.resize(361, 261)
            self.poll_thank_you.move(20, 230)
            self.poll_votes_widj.move(270, 230)

        elif self.num_options == 4: 
            self.dp_option_three.setVisible(True)
            self.dp_option_four.setVisible(True)
            self.dp_option_five.setVisible(False)
            self.pollbox.resize(361, 321)
            self.poll_thank_you.move(20, 280)
            self.poll_votes_widj.move(270, 280)

        elif self.num_options == 5:
            self.dp_option_three.setVisible(True)
            self.dp_option_four.setVisible(True)
            self.dp_option_five.setVisible(True)
            self.pollbox.resize(361, 361)
            self.poll_thank_you.move(20, 320)
            self.poll_votes_widj.move(270, 320)


# ----------- ..... ------------ VOTE ON POLL ----------- ..... ------------ #


    def __vote__(self, option: int):

        existing_vote = query_get("get_existing_vote", [self.current_user.uid, self.display_poll.pid], cursor)
        
        if existing_vote == []: # go straight to adding the new one
            self.__post_vote__(option)


        else: # first remove the existing vote, then add the new one.

            vote_tup = existing_vote[0]
            remove_vote_inst = (vote_tup[1], vote_tup[2], vote_tup[0]) # PollID .. OptionID .. UserID
            query_post("rm_vote", remove_vote_inst, cursor)

            self.dp_options[vote_tup[2] - 1].setStyleSheet("background-color: transparent;") # get rid of background for old vote
            self.dp_op_colors[vote_tup[2] - 1].setStyleSheet("background-color: transparent;") # same with the filler widj

            self.__post_vote__(option)


    def __post_vote__(self, option):

        query_post("add_vote", (self.current_user.uid, self.display_poll.pid, option), cursor)

        self.poll_thank_you.setText("Thank you!")
        total_votes = sum(self.dp_option_votes) + 1
        self.poll_votes_widj.setText(f"{total_votes}")

        for x in range(self.num_options):
            
            if x + 1 == option:
                percent = round(((self.dp_option_votes[x] + 1) / total_votes) * 100, 2)
                self.dp_option_vote_list[x].setText(f"{self.dp_option_votes[x] + 1} ({percent}%)")
                self.dp_options[x].setStyleSheet('background-color: rgb(222, 114, 92);') # darken bg of voted option
                self.dp_op_colors[x].setStyleSheet("background-color: rgb(222, 114, 92);")
            else:
                percent = round(((self.dp_option_votes[x]) / total_votes) * 100, 2)
                self.dp_option_vote_list[x].setText(f"{self.dp_option_votes[x]} ({percent}%)") # display votes and percents for other options


    def __vote_option_one__(self):
        if self.last_vote != 1:
            self.last_vote = 1
            self.__vote__(1)


    def __vote_option_two__(self):
        if self.last_vote != 2:
            self.last_vote = 2
            self.__vote__(2)


    def __vote_option_three__(self):
        if self.last_vote != 3:
            self.last_vote = 3
            self.__vote__(3)


    def __vote_option_four__(self):
        if self.last_vote != 4:
            self.last_vote = 4
            self.__vote__(4)


    def __vote_option_five__(self):
        if self.last_vote != 5:
            self.last_vote = 5
            self.__vote__(5)
        

# ----------- ..... ------------ USER POLL ----------- ..... ------------ #

    def __get_user_polls__(self):

        self.user_poll_list = []

        # PollID, UserID, Content, DatePosted
        user_polls = query_get("get_u_polls", [self.current_user.uid], cursor)

        if user_polls == []:

            self.__case_zero_polls__()

        else:
            for poll in user_polls:
                temp_poll = Poll(self.current_user.uid, poll[2], []) # create list of Poll instances belonging to User
                temp_poll.pid = poll[0]
                self.user_poll_list.append(temp_poll)
            self.__update_user_poll__() # start on first poll


    def __next_user_poll__(self):
        
        if self.user_poll_index == len(self.user_poll_list) - 1: # if at last poll, go to first poll next
            self.user_poll_index = 0
        else:
            self.user_poll_index += 1

        self.__update_user_poll__()
        

    def __prev_user_poll__(self):

        if self.user_poll_index == 0: # if at first poll, going backwards sends you to last poll
            self.user_poll_index = len(self.user_poll_list) - 1
        else:
            self.user_poll_index -= 1

        self.__update_user_poll__()

    
    def __update_user_poll__(self):

        poll = self.user_poll_list[self.user_poll_index]
        prompt = poll.content
        self.__fetch_user_poll_options__() # fetch options to insert into poll body

        self.user_poll_prompt.setText(prompt)
        self.user_poll_index_label.setText(f"({self.user_poll_index + 1})/({len(self.user_poll_list)})") # set poll index label (current / total)
        remaining_options = abs(len(self.user_poll_options) - 5)
        self.__adjust_positions_u_poll__()

        for i in range(len(self.user_poll_options)):
            
            # 4 is the last index (5th option), so starting from the ' top ' of the options, 
            # we can decrement i -> (number of unused options) times to hide the label.
            self.user_poll_option_labels[i].setText(self.user_poll_options[i])
            self.user_poll_option_vote_labels[i].setText(f"{self.user_poll_option_votes[i]}")
            top = 4 

        for i in range(remaining_options):
           
            self.user_poll_option_labels[top].setText("")
            self.user_poll_option_vote_labels[top].setText("")
            top -= 1

        self.user_poll_votes_sum.setText(f"{sum(self.user_poll_option_votes)}")


    def __adjust_positions_u_poll__(self):
    
        dim_box = [361, 311, 261, 211] # height dimensions for the poll groupbox
        pos_t_votes = [320, 270, 220, 170] # y-positions for total vote row

        if len(self.user_poll_options) == 2:
            self.userpollbox.resize(361, dim_box[3])
            self.user_poll_total_votes.move(20, pos_t_votes[3])
            self.user_poll_votes_sum.move(300, pos_t_votes[3])
            self.user_poll_index_label.move(160, 170)
            self.nextpoll.move(280, 340)
            self.prevpoll.move(140, 340)

        elif len(self.user_poll_options) == 3:
            self.userpollbox.resize(361, dim_box[2])
            self.user_poll_total_votes.move(20, pos_t_votes[2])
            self.user_poll_votes_sum.move(300, pos_t_votes[2])
            self.user_poll_index_label.move(160, 220)
            self.nextpoll.move(280, 340)
            self.prevpoll.move(140, 340)

        elif len(self.user_poll_options) == 4:
            self.userpollbox.resize(361, dim_box[1])
            self.user_poll_total_votes.move(20, pos_t_votes[1])
            self.user_poll_votes_sum.move(300, pos_t_votes[1])
            self.user_poll_index_label.move(160, 270)
            self.nextpoll.move(280, 340)
            self.prevpoll.move(140, 340)

        elif len(self.user_poll_options) == 5:
            self.userpollbox.resize(361, dim_box[0])
            self.user_poll_total_votes.move(20, pos_t_votes[0])
            self.user_poll_votes_sum.move(300, pos_t_votes[0])
            self.user_poll_index_label.move(160, 320)
            self.nextpoll.move(410, 340)
            self.prevpoll.move(-10, 340)


    def __delete_user_poll__(self):
        
        if len(self.user_poll_list) == 1:
        
            to_delete_poll = self.user_poll_list.pop(self.user_poll_index)
            query_post("rm_poll", [to_delete_poll.pid], cursor)
            self.__show_account__()
            self.__account_alert__("All polls have been deleted!") # escape screen & avoid possible index errors

        else:
            to_delete_poll = self.user_poll_list.pop(self.user_poll_index) # pop the poll from the pseudo-stack
            query_post("rm_poll", [to_delete_poll.pid], cursor)

            if self.user_poll_index == 0:
                self.__update_user_poll__() # if we're at the first poll, stay in place  
            elif self.user_poll_index == len(self.user_poll_list):
                self.__prev_user_poll__() # if we're at the end, go back a poll
            else:
                self.__next_user_poll__() # otherwise, move to the next poll upon deletion


    def __case_zero_polls__(self):
        
        self.__account_alert__("You do not have any polls.")


    def __fetch_user_poll_options__(self):

        self.user_poll_options = []
        self.user_poll_option_votes = []
        poll = self.user_poll_list[self.user_poll_index]
        pid = poll.pid
        options = query_get("get_options", [pid], cursor)

        for option in options:
            self.user_poll_options.append(option[2])
            self.user_poll_option_votes.append(option[3])
            

# ----------- ..... ------------ XTRA ACC FEATURES ----------- ..... ------------ #


    def __account_alert__(self, text: str):

        self.user_account_alert.setText(text)
        self.accountalertbox.resize(321, 41)


    def __close_account_alert__(self):

        self.user_account_alert.setText("")
        self.accountalertbox.resize(0, 0)


    def __delete_account__(self):

        user_polls = query_get("get_u_polls", [self.current_user.uid], cursor)

        if user_polls == []:
            pass
        
        else:
            for poll in user_polls:
                query_post("rm_poll", [poll[0]], cursor)

        query_post("delete_acc", [self.current_user.uid], cursor)

        self.current_user = None
        self.password_input.setText("")
        self.username_input.setText("")
        self.__alert__("Account deletion successful!")
        self.__show_login__()


# ----------- ..... ------------ MAIN ----------- ..... ------------ #


if __name__ == "__main__":

    app = QApplication(sys.argv)
    display = Gui()
    app.exec()