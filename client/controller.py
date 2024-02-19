import customtkinter as ctk
import re

from CTkMessagebox import CTkMessagebox
from copy import copy
from typing import Dict, List, Callable

import sys; sys.path.append('../')
from communication_protocol.TCPMessages import *
sys.path.append('client/')

from windows.window import Window
from windows.window_types import WindowTypes
from windows.login import LoginWindow
from windows.signup import SignUpWindow
from windows.email_verification import EmailVerificationWindow
from windows.core_app.core_app_entry import CoreAppEntryPointWindow 
from windows.add_channel import AddChannelWindow
from windows.settings import SettingWindow
from windows.search import SearchWindow
from suggestions.word_suggestion_API import WordSuggestionAPI

class Controller:

    def __init__(self, root: ctk.CTk) -> None:
        
        self.root = root

        self.user_id: int = None
        self.username: str = None
        self.firstname: str = None
        self.lastname: str = None    
        self.email: str = None
        self.password: str = None
        self.dob: datetime = None
        self.account_created: str = None    
        self.logged_in: bool = False 

        self.current_channel_id: int = None
        self.word_suggestion_API = WordSuggestionAPI()

        self.friends: List[str] = []
        self.outgoing_friend_requests: List[str] = []
        self.outgoing_msgs = []


        
        self._setup_frames()

    # //// SETUP ////

    def add_binding(self, key: str, func: Callable):
        self.root.bind(key, func)

    def _setup_frames(self) -> None:
        self.root_container = ctk.CTkFrame(self.root) 
        self.frames: Dict[str, Window] = {} 
        
        for FrameClass in (
            LoginWindow,
            SignUpWindow, 
            EmailVerificationWindow, 
            CoreAppEntryPointWindow, 
            AddChannelWindow, 
            SearchWindow, 
            SettingWindow
            ):

            frame = FrameClass(self.root_container, self)
            self.frames[FrameClass.__name__] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.login_window: LoginWindow = self.frames[WindowTypes.LoginWindow]
        self.signup_window: SignUpWindow = self.frames[WindowTypes.SignUpWindow]
        self.email_verification_window: EmailVerificationWindow = self.frames[WindowTypes.EmailVerificationWindow]
        self.core_app: CoreAppEntryPointWindow = self.frames[WindowTypes.CoreAppEntryPointWindow]
        self.add_channel_window: AddChannelWindow = self.frames[WindowTypes.AddChannelWindow]
        self.search_window: SearchWindow = self.frames[WindowTypes.SearchWindow]
        self.setting_window: SettingWindow = self.frames[WindowTypes.SettingWindow]
        self.switch_frame(WindowTypes.LoginWindow)

        self.root_container.pack(side = "top", fill = "both", expand = True)
    
        self.root_container.grid_rowconfigure(0, weight = 1)
        self.root_container.grid_columnconfigure(0, weight = 1)

    
    def switch_frame(self, frame_name: str) -> None:
        frame = self.frames[frame_name]
        frame.window_bindings()
        frame.tkraise()
        self.core_app.text_bar_frame.send_button.configure(state = "on")
    

    # //// Client ////


    def recieve_incoming_msg(self, msg: NewMessageNotif):
        #check channel id
        self.core_app.channel_frame.add_message(msg.channel_id, msg.sender_name, msg.time_sent, msg.content)

    def get_outgoing_msgs(self) -> List[TCPMessage]:
        if self.outgoing_msgs:

            msgs = copy(self.outgoing_msgs)
            self.outgoing_msgs = []
            return msgs

    # //// Messages ////

    def add_message(self, content: str) -> None:
        if self.current_channel_id:
            self.core_app.channel_frame.add_message(
                self.current_channel_id,
                self.username,
                datetime.now(),
                content)
            self.outgoing_msgs.append(
                TextMessage(self.current_channel_id, content)
            )
        else:
            CTkMessagebox(
                title = "Channel Error", 
                message= "You are not in a channel, join or create a channel to send messages.", 
                icon="cancel") 


    # //// Channels ////

    def channel_create_request(self, channel_name: str):
        self.outgoing_msgs.append(
            ChannelCreateRequest(
            channel_name=channel_name
            )
        )
    
    def add_channel(self, channel_id: int, channel_name: str):
        self.core_app.add_channel(channel_id, channel_name)
        self.core_app.channel_frame.add_user(channel_id, self.username, self.firstname, self.lastname)
        self.switch_frame(WindowTypes.CoreAppEntryPointWindow)
        
    
    def switch_channel(self, channel_id):
        self.current_channel_id = channel_id
        self.core_app.channel_frame.switch_channel(channel_id)
        users = self.core_app.channel_frame.current_channel_frame.users
        self.core_app.right_side_frame.user_list_frame.set_users(users)

    def user_join_channel_update(self, channel_id: int, username: str, firstname: str, lastname: str) -> None:
        #rerender if in focus
        self.core_app.channel_frame.add_user(channel_id, username, firstname, lastname)
        
        #If a channel frame is current being viewed
        if self.current_channel_id == channel_id:
            users = self.core_app.channel_frame.current_channel_frame.users
            self.core_app.right_side_frame.user_list_frame.set_users(users)
    

    def channel_join_request(self, channel_id: int):
        if channel_id not in self.core_app.channel_frame.channel_frames:
            self.outgoing_msgs.append(
                ChannelJoinRequest(
                channel_id=channel_id
                )
            )

    def create_channel(self, channel_id: int, channel_name: str):
        self.add_channel_window.central_frame.create_channel_frame.channel_name_entry_box.clear()
        self.add_channel_window.central_frame.join_channel_frame.channel_id_entry_box.clear()
        self.add_channel(channel_id, channel_name)


    def join_channel(self, channel_id: int, channel_name: str):
        self.add_channel_window.central_frame.create_channel_frame.channel_name_entry_box.clear()
        self.add_channel_window.central_frame.join_channel_frame.channel_id_entry_box.clear()
        self.add_channel(channel_id, channel_name)

    def leave_channel(self):

        cfs = self.core_app.channel_frame.channel_frames
        self.outgoing_msgs.append(ChannelLeave(self.current_channel_id))
        if self.current_channel_id in cfs:
            cfs.pop(self.current_channel_id)
            self.core_app.left_side_frame.remove_channel_button(self.current_channel_id)
            #if other channels exist
            if cfs.keys():
                self.switch_channel(list(cfs.keys())[0])
        
    def user_left_channel_update(self, channel_id, username):
        #Remove username of the user who left from the list stored in the channel frame
        users = self.core_app.channel_frame.current_channel_frame.users
        for user in users:
            if user[0] == username:
                users.remove(user)
        #If the channel is currently being viewed
        if channel_id == self.current_channel_id:
            #Update the user list frame with modified user list
            self.core_app.right_side_frame.user_list_frame.set_users(users)
            
    # //// Friends ////
    def send_friend_request(self, username: str, firstname: str, lastname: str) -> None:
        if username not in self.outgoing_friend_requests and username not in self.friends:
            self.outgoing_msgs.append(FriendRequest(username))            
            self.setting_window.friend_list_frame.add_decision_frame(username, firstname, lastname, "Pending")
            self.outgoing_friend_requests.append(username)
    
    def accept_friend_request(self, username: str) -> None:
        self.friends.append(username)
        self.outgoing_msgs.append(FriendRequestDecision(True, username))
        self.setting_window.friend_list_frame.update_decision_frame(username, "Remove")

    def reject_friend_request(self, username: str) -> None:
        self.outgoing_msgs.append(FriendRequestDecision(False, username))
        self.setting_window.friend_list_frame.remove_decision_frame(username)

    def friend_request_recieved(self, username: str, firstname: str, lastname: str) -> None:
        self.setting_window.friend_list_frame.add_decision_frame(username, firstname, lastname, "Accept")

    def remove_friend(self, username: str) -> None:
        self.friends.remove(username)
        self.setting_window.friend_list_frame.remove_decision_frame(username)
        self.outgoing_msgs.append(FriendRemoval(username))

    def remove_friend_notif(self, username: str) -> None:
        self.friends.remove(username)
        self.setting_window.friend_list_frame.remove_decision_frame(username)


    def friend_request_decision(self, username: str, accepted: bool) -> None:
        if accepted:
            self.friends.append(username)
            self.setting_window.friend_list_frame.update_decision_frame(username, "Remove")
        else:
            self.outgoing_friend_requests.remove(username)
            self.setting_window.friend_list_frame.remove_decision_frame(username)


    def friend_status_notif(self, username: str, firstname: str, lastname: str, decision: str) -> None:
        if decision == "Remove":
            self.friends.append(username)
        if decision == "Pending":
            self.outgoing_friend_requests.append(username)
        self.setting_window.friend_list_frame.add_decision_frame(username, firstname, lastname, decision)

    # //// Search ////
    def search_request(self, search: str) -> None:
        self.outgoing_msgs.append(
            SearchRequest(search)
        )

    def search_response(self, response_data: List) -> None:
        self.search_window.central_search_frame.results_frame.set_results(response_data)

    # //// Login ////
    def attempt_login(self, username: str, password: str) -> None:
        self.username = username
        self.core_app.username = username
        self.outgoing_msgs.append(
            LoginAttempt(
            username=username,
            password=password
            )
        )

    def login_approved(
            self,
            user_id: int, 
            username: str, 
            firstname: str, 
            lastname: str, 
            email: str, 
            dob: datetime, 
            account_created: str):
    
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.dob = dob
        self.account_created = account_created
        self.logged_in = True
        self.switch_frame(WindowTypes.CoreAppEntryPointWindow)

        self.setting_window.information_frame.create_labels(
            username, 
            firstname, 
            lastname, 
            email, 
            dob.strftime(r'%Y:%m:%d'), 
            account_created
            )

    def login_failed(self, error_decription):
        if error_decription == LoginError.USERNAME_NOT_FOUND:
            CTkMessagebox(
                title = "Login Attempt Failed", 
                message= "The username you have entered does not exist. ", 
                icon="cancel"
                )
        elif error_decription == LoginError.PASSWORD_INCORRECT:
            CTkMessagebox(
                title = "Login Attempt Failed", 
                message= "The password you have entered is incorrect. ", 
                icon="cancel"
                )

    # //// Sign up ////
    def signup_request(self) -> None:
        detail_entry_frame = self.signup_window.detail_entry_frame

        month_str = detail_entry_frame.date_entry_frame.month_option_menu.get()
        day = int(detail_entry_frame.date_entry_frame.day_entry_box.get())
        year = int(detail_entry_frame.date_entry_frame.year_entry_box.get())
        month = detail_entry_frame.date_entry_frame.MONTHS.index(month_str) + 1

        self.username = detail_entry_frame.top_entry_frame.username_entry_box.get()
        self.firstname = detail_entry_frame.top_entry_frame.firstname_entry_box.get()
        self.lastname = detail_entry_frame.top_entry_frame.lastname_entry_box.get()
        self.email = detail_entry_frame.top_entry_frame.email_entry_box.get()
        self.password = detail_entry_frame.top_entry_frame.password_entry_box.get()
        self.dob = datetime(year, month, day)
        self.account_created = "Account created: Just now"
        self.core_app.username = self.username


        #Validate email
        if not re.match(r'\S+@\S+\.[a-zA-Z]{2,}', self.email):
            CTkMessagebox(
                title = "Sign up error", 
                message= """The email you have entered has an invalid format""",
                icon="cancel"
                )
        #Validate password
        elif not re.match(r'(?=\S*[a-z])(?=\S*[A-Z])(?=\S*[0-9]).\S{8,}', self.password):
            CTkMessagebox(
                title = "Sign up error", 
                message= """Your password must be:
                - At least 8 characters
                - Contain upper case digits
                - Contain lower case digits
                - Contain numbers""",
                icon="cancel"
                )
        else:
            self.outgoing_msgs.append(
                SignUpAttempt(
                    username = self.username,
                    firstname = self.firstname,
                    lastname = self.lastname,
                    email = self.email,
                    password = self.password,
                    dob = self.dob
                )
            )
        

    def signup_response(self, success: str, error: SignUpError) -> None:
        if success:
            self.email_verification_window.set_email(self.email)
            self.switch_frame(WindowTypes.EmailVerificationWindow)
        else:
            if error == SignUpError.EMAIL_TAKEN:
                CTkMessagebox(
                    title = "Sign up error", 
                    message= "The email you have entered is already in use", 
                    icon="cancel"
                    )
            elif error == SignUpError.USERNAME_TAKEN:
                CTkMessagebox(
                    title = "Sign up error", 
                    message= "The username you have entered is already in use", 
                    icon="cancel"
                    )


    def verify_code(self, code: str) -> None: 
        self.outgoing_msgs.append(
            EmailVerificationCodeAttempt(
                code = code,
                username = self.username,
                firstname = self.firstname,
                lastname = self.lastname,
                email = self.email,
                password = self.password,
                dob = self.dob                
            )
        )

    def signup_confirmation(self, success: bool, user_id: int) -> None:
        if success:
            self.user_id = user_id
            self.switch_frame(WindowTypes.CoreAppEntryPointWindow)
            self.logged_in = True
        else:
            self.switch_frame(WindowTypes.LoginWindow)
            CTkMessagebox(title = "Sign up error", message= "The code you have entered is incorrect", icon="cancel")
        self.setting_window.information_frame.create_labels(
            self.username, 
            self.firstname,
            self.lastname, 
            self.email, 
            self.dob.strftime(r'%Y:%m:%d'), 
            self.account_created
            )

    # //// Text Suggestions ////

    def get_suggestions(self, prefix: str) -> List[str]:
        return self.word_suggestion_API.get_suggestion(prefix)

    def on_suggestion_press(self, suggestionNo):
        self.core_app.text_bar_frame.on_suggestion_press(suggestionNo=suggestionNo)
