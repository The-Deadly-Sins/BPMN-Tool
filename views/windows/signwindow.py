from tkinter import *
from resources.colors import *
from views.effects.color_transition import ColorTransition
from views.effects.move_transition import MoveTransition
from views.factories.iconbuttonfactory import MainButton, SecondaryButton, DangerButton
from views.components.textbox import TextBox
from views.windows.abstract.window import Window
from helpers.translator import translate
from models.entities.Container import Container
from models.entities.Entities import User, SparePwd
from views.windows.modals.messagemodal import MessageModal
from views.windows.profilewindow import ProfileWindow
from views.windows.homewindow import HomeWindow
from datetime import datetime, timedelta
from helpers.stringhelper import generate_code, camel_case
from helpers.sendemail import send_email
import re

class SignWindow(Window):

    def __init__(self, root):
        super().__init__(root, 'BPMN Tool')

        self.design()

    def design(self):
        # lay out the container frames
        self.frm_in = Frame(self, bg=background, width=self.DEFAULT_WIDTH/2, padx=100)
        self.frm_in.pack(side=RIGHT, expand=1, fill=BOTH)
        self.frm_up = Frame(self, bg=background, width=self.DEFAULT_WIDTH/2, padx=100)
        self.frm_up.pack(side=LEFT, expand=1, fill=BOTH)
        self.frm_in.pack_propagate(0)
        self.frm_up.pack_propagate(0)
        # design the sign in side
        self.lbl_title_signin = Label(self.frm_in, text=translate('Sign in'), fg=teal, bg=background, font='-size 32 -weight bold')
        self.lbl_title_signin.pack(side=TOP, pady=(150, 50))
        signin_config = [
            { 'name': 'txt_in_username', 'label': translate('Username:'), 'icon': 'account.png' },
            { 'name': 'txt_in_password', 'label': translate('Password:'), 'icon': 'key.png' }
        ]
        # put the form in place
        for config in signin_config:
            Label(self.frm_in, text=config.get('label'), font='-size 11 -weight bold', fg=black, bg=background).pack(side=TOP, anchor=N+W, pady=(0, 5))
            tb = TextBox(self.frm_in, 'resources/icons/ui/' + config.get('icon'))
            tb.pack(side=TOP, fill=X, anchor=N+W, pady=(0, 10))
            if config.get('name') == 'txt_in_password': tb.entry.config(show='*')
            setattr(self, config.get('name'), tb)
        # buttons
        frm_in_btns = Frame(self.frm_in, bg=background)
        frm_in_btns.pack(side=TOP, fill=X, pady=(5, 0))
        self.btn_signin = MainButton(frm_in_btns, translate('Sign In'), 'login.png', self.btn_signin_click, 8)
        self.btn_signin.pack(side=LEFT)
        self.btn_viewpwd = SecondaryButton(frm_in_btns, translate('View Password'), 'eye.png', self.btn_viewpassword_click, 8)
        self.btn_viewpwd.pack(side=RIGHT)
        # divider
        frm_in_divider = Frame(self.frm_in, bg=border)
        frm_in_divider.pack(side=TOP, fill=X, pady=(100, 5))
        # extra options frame
        frm_in_xtra = Frame(self.frm_in, bg=background)
        frm_in_xtra.pack(side=TOP, fill=X)
        self.lbl_signup = Label(frm_in_xtra, fg=teal, font='-size 9', text=translate('Sign up'), bg=background)
        self.lbl_signup.pack(side=RIGHT)
        self.lbl_signup.bind('<Button-1>', self.lbl_signup_click)
        self.lbl_forgotpwd = Label(frm_in_xtra, fg=black, font='-size 9 -underline 1', text=translate('Forgot your password?'), bg=background)
        self.lbl_forgotpwd.pack(side=LEFT)
        self.lbl_forgotpwd.bind('<Button-1>', self.lbl_forgotpwd_click)
        # designing the sign up side
        self.up_congig = {
            translate('Step 1: Authentication Settings'): [
                { 'name': 'txt_email', 'label': translate('Email:'), 'icon': 'mail.png' },
                { 'name': 'txt_up_pwd', 'label': translate('Password:'), 'icon': 'key.png' },
                { 'name': 'txt_confirm', 'label': translate('Confirm Password:'), 'icon': 'key.png' }
            ],
            translate('Step 2: Identity Information'): [
                { 'name': 'txt_up_username', 'label': translate('Username:'), 'icon': 'account.png' },
                { 'name': 'txt_firstname', 'label': translate('First Name:'), 'icon': 'account.png' },
                { 'name': 'txt_lastname', 'label': translate('Last Name:'), 'icon': 'account.png' }
            ],
            translate('Step 3: Personal Information'): [
                { 'name': 'txt_gender', 'label': translate('Gender:'), 'icon': 'wc.png' },
                { 'name': 'txt_company', 'label': translate('Company:'), 'icon': 'business.png' }
            ]
        }
        # preparations
        self.current = 0
        self.steptitles = []
        self.checkpoints = []
        self.forms = []
        # sign up header
        self.lbl_title_signup = Label(self.frm_up, text=translate('Sign Up'), fg=teal, bg=background, font='-size 32 -weight bold')
        self.lbl_title_signup.pack(side=TOP, pady=(100, 30))
        # step label
        self.lbl_step = Label(self.frm_up, text='Step X: Description', fg=black, bg=background, font='-size 12')
        self.lbl_step.pack(side=TOP)
        # map frame
        self.frm_map = Frame(self.frm_up, bg=background)
        self.frm_map.pack(side=TOP, fill=X, pady=(5, 0))
        for s in self.up_congig.keys():
            frm_cp = Frame(self.frm_map, highlightthickness=1, highlightbackground=teal, height=15, bg=white)
            frm_cp.pack(side=LEFT, fill=X, expand=1, padx=(0, 4 if list(self.up_congig.keys()).index(s) != len(self.up_congig.keys()) else 0))
            self.checkpoints.append(frm_cp)
        # forms container
        self.frm_frmcontainer = Frame(self.frm_up, bg=background)
        self.frm_frmcontainer.pack(side=TOP, fill=X, pady=(30, 0))
        for s in self.up_congig.keys():
            tb_config = self.up_congig.get(s)
            frm_form = Frame(self.frm_frmcontainer, bg=background)
            for i in tb_config:
                Label(frm_form, text=i.get('label'), font='-size 11 -weight bold', fg=black, bg=background).pack(side=TOP, anchor=N+W, pady=(0, 5))
                tb = TextBox(frm_form, 'resources/icons/ui/' + i.get('icon'))
                tb.pack(side=TOP, fill=X, anchor=N+W, pady=(0, 10))
                if i.get('name') in ['txt_up_pwd', 'txt_confirm']: tb.entry.config(show='*')
                setattr(self, i.get('name'), tb)
            # save those entities
            self.steptitles.append(s)
            self.forms.append(frm_form)
        # extra sign up options
        frm_in_xtra = Frame(self.frm_up, bg=background)
        frm_in_xtra.pack(side=BOTTOM, fill=X, pady=(5, 75))
        self.lbl_signin = Label(frm_in_xtra, fg=teal, font='-size 9', text=translate('Sign in'), bg=background)
        self.lbl_signin.pack(side=RIGHT)
        self.lbl_signin.bind('<Button-1>', self.lbl_signin_click)
        # divider
        frm_in_divider = Frame(self.frm_up, bg=border)
        frm_in_divider.pack(side=BOTTOM, fill=X)
        # buttons
        frm_up_btns = Frame(self.frm_up, bg=background)
        frm_up_btns.pack(side=BOTTOM, fill=X, pady=(0, 60))
        self.btn_prev = DangerButton(frm_up_btns, translate('Go Back'), 'revert_history.png', self.btn_prev_click, 8)
        self.btn_prev.pack(side=LEFT)
        self.btn_next = SecondaryButton(frm_up_btns, translate('Next Step'), 'yes.png', self.btn_next_click, 8)
        self.btn_next.pack(side=RIGHT)
        # display the first step
        self.move_to(self.current)
        # creating the veil
        self.frm_veil = Frame(self, bg=teal)
        self.frm_veil.place(x=0, y=0, relwidth=0.5, relheight=1)
        # make it a non-resizable window
        self.resizable(0, 0)

    def move_to(self, index: int):
        # event corrector
        def correct(idx):
            return [
                lambda c: self.checkpoints[idx].config(bg=c),
                lambda: self.checkpoints[idx]['bg']
            ]
        # change the label's text
        self.lbl_step.config(text=self.steptitles[index])
        # show the corresponding form container
        for frm in self.forms: frm.pack_forget()
        self.forms[index].pack(side=TOP, fill=X)
        # change checkpoint indicators
        for cp in self.checkpoints: cp.config(bg=white, highlightthickness=1)
        self.checkpoints[index].config(bg=white, highlightthickness=2)
        for i in [x for x in range(index)]:
            # reset the border width
            self.checkpoints[i].config(highlightthickness=1)
            # animate the color
            ColorTransition(correct(i)[0], correct(i)[1], teal)
 
    # BOOKMARK: Sign In Logic
    def btn_signin_click(self, event):
        if getattr(self, 'txt_in_username').get_text() == '' or getattr(self, 'txt_in_password').get_text() == '': MessageModal(self,title='Error',message=f'Please enter your username and password to login!',messageType='info')
        else:
            user = Container.filter(User, User.userName == getattr(self, 'txt_in_username').get_text()).first()
            if user == None: MessageModal(self,title='Error',message=f'This username doesn\'t exist!',messageType='error')
            else:
                if user.password != getattr(self, 'txt_in_password').get_text():
                    sparepwd = Container.filter(SparePwd, SparePwd.userId == user.id).order_by(SparePwd.expirationDate.desc()).first()
                    if sparepwd != None and sparepwd.verificationCode == getattr(self, 'txt_in_password').get_text():
                        if sparepwd.expirationDate < datetime.now():
                            MessageModal(self,title='Expired code',message=f'This verification code has expired!',messageType='error')
                        else:
                            window = ProfileWindow(self.master, user=user)
                            self.windowManager.run(window)
                            MessageModal(self,title='Change password',message=f'Please change your password!',messageType='info')
                    else:
                        MessageModal(self,title='Wrong password',message=f'Wrong password, please try again or request a verification code!',messageType='error')
                else: 
                    self.windowManager.run(HomeWindow(self.master, user= user))

    # BOOKMARK: View Password Logic
    def btn_viewpassword_click(self, event):
        getattr(self, 'txt_in_password').entry.config(show= '' if getattr(self, 'txt_in_password').entry.cget('show') == '*' else '*')
        self.btn_viewpwd.label['text'] = translate('View Password') if getattr(self, 'txt_in_password').entry.cget('show') == '*' else translate('Hide Password')

    # BOOKMARK: Sign Up Next
    def btn_signup_next(self, event):
        validated_fields = self.validate_step()
        if self.current+1 == 3 and validated_fields == 2:
            if Container.filter(User, User.userName == getattr(self, 'txt_up_username').get_text()).first() != None: 
                MessageModal(self,title='UserName taken',message=f'{getattr(self, "txt_up_username").get_text()} is already taken\nplease pick another userName!',messageType='error')
            else:
                atts = {}
                Container.save(User(email=self.txt_email.get_text(), userName=self.txt_up_username.get_text(), firstName=self.txt_firstname.get_text(), lastName=self.txt_lastname.get_text(), password=self.txt_up_pwd.get_text(), company=self.txt_company.get_text(), gender=self.txt_gender.get_text()))
                self.empty_all()
                MessageModal(self,title='Success',message='Account created !\nFeel free to Login and good luck with your work!',messageType='info')
                MoveTransition(self.frm_veil_set_x, self.frm_veil_get_x, 0, 2.5)
        else:
            return validated_fields

    # Empty all the textboxes
    def empty_all(self):
        for form in self.up_congig.keys():
            for row in self.up_congig[form]:
                getattr(self, row['name']).entry.delete(0,END)
 

    # BOOKMARK: Go to Sign Up Form
    def lbl_signup_click(self, event):
        MoveTransition(self.frm_veil_set_x, self.frm_veil_get_x, self.winfo_width()/2, 2.5)

    # BOOKMARK: Forgotten password
    def lbl_forgotpwd_click(self, event):
        if getattr(self, 'txt_in_username').get_text() == '': MessageModal(self,title='Error',message=f'Please enter your username to recieve an email containing the verification code!',messageType='info')
        else:
            user = Container.filter(User, User.userName == getattr(self, 'txt_in_username').get_text()).first()
            if user == None: MessageModal(self,title='Error',message=f'This username doesn\'t exist!',messageType='error')
            else:
                sparepwd = Container.filter(SparePwd, SparePwd.userId == user.id).first()
                if sparepwd == None or sparepwd.expirationDate < datetime.now(): 
                    sparepwd = SparePwd(user= user, expirationDate= datetime.now() + timedelta(days=1), verificationCode= generate_code())
                    Container.save(sparepwd)
                
                MessageModal(self,title='Success',message='A verification code has been sent to your email!',messageType='info')
                send_email(user, sparepwd.verificationCode)

    # BOOKMARK: Go to Sign In Form
    def lbl_signin_click(self, event):
        MoveTransition(self.frm_veil_set_x, self.frm_veil_get_x, 0, 2.5)

    # BOOKMARK: Next step
    def btn_next_click(self, event):
        # check if the form is validated 
        if self.btn_signup_next(event) == 3:
            # display corresponding form
            if self.current + 1 < len(self.forms):
                self.current += 1
                self.move_to(self.current)
            # change label's text
            self.btn_next_step_config()

    # BOOKMARK: Prev (Go back)
    def btn_prev_click(self, event): 
        # display corresponding form
        if self.current - 1 >= 0:
            self.current -= 1
            self.move_to(self.current)
        # change label's text
        self.btn_next_step_config()
    
    # 
    def btn_next_step_config(self):
        self.btn_next.label.config(text=(translate('Sign Up') if self.current == len(self.forms) - 1 else translate('Next Step')))

    # Veil Properties
    def frm_veil_set_x(self, x):
        self.frm_veil.place_configure(x=x)

    def frm_veil_get_x(self):
        return self.frm_veil.winfo_x()

    def validate_step(self):
        valid_fields = 0
        try:
            for i in self.up_congig[self.steptitles[self.current]]:
                if getattr(self,i.get('name')).get_text() == '' and i.get('name') not in ['txt_confirm']: 
                    raise Exception(camel_case(i.get("label")),f'{i.get("label")} Cannot be null!')

                elif i.get('name') in ['txt_firstname','txt_lastname'] and not re.fullmatch('[A-Za-z]{2,15}( [A-Za-z]{2,15})?', getattr(self,i.get('name')).get_text()):
                    raise Exception(camel_case(i.get("label")),f'\n1.Can contain 2 words with 1 space in between\n2.Must be between 2 - 15 alphabets each')
                        
                elif i.get('name') in ['txt_up_username','txt_up_pwd'] and not re.fullmatch('^[a-zA-Z0-9_.-]+$', getattr(self,i.get('name')).get_text()):
                    raise Exception(camel_case(i.get("label")),f'can only be alphanumeric and contain (. _ -)')
                        
                elif i.get('name') == 'txt_email' and not re.fullmatch('[^@]+@[^@]+\.[^@]+', getattr(self,i.get('name')).get_text()):
                    raise Exception(camel_case(i.get("label")),f'Please enter a valid email!\nEX: emailName@email.com')
                        
                elif i.get('name') == 'txt_company' and getattr(self,i.get('name')).get_text() != '' and not re.fullmatch('^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$', getattr(self,i.get('name')).get_text()):
                    raise Exception(camel_case(i.get("label")),f'\n1. Must be between 4 - 20 characters\n2. It should not contain any special characters')
                        
                elif i.get('name') == 'txt_gender' and getattr(self,i.get('name')).get_text() != '' and getattr(self,i.get('name')).get_text().lower() not in ['female','male']:
                    raise Exception(camel_case(i.get("label")),f'Gender must be either male or female!')
                        
                elif i.get('name') == 'txt_confirm' and getattr(self,i.get('name')).get_text() != getattr(self,'txt_up_pwd').get_text():
                    raise Exception('Password confirmation',f'Password doesn\'t match.\nPlease confirm your password!')

                valid_fields += 1

        except Exception as ex:
            MessageModal(self,title=f'{ex.args[0]} Error',message=ex.args[1],messageType='error')
        finally:
            return valid_fields

