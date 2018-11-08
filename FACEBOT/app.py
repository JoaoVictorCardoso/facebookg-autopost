import threading
import time

from facebook import GroupAuto
from Tkinter import *

class Threader(threading.Thread):
    def __init__(
        self,
        username,
        password,
        timeout,
        post,
        *args,
        **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.username = username
        self.password = password
        self.timeout = timeout
        self.post = post
        self.start()
    
    def run(self):
        try:
            groups = fb.get_groups()
            fb.post(groups,
                    self.post,
                    int(self.timeout),
                    debug=True)
        except Exception:
            fb.login(self.username.strip(),
                     self.password.strip())

            groups = fb.get_groups()

            fb.post(groups,
                    self.post,
                    int(self.timeout),
                    debug=True)
        
        fb.browser.quit()

class MainApplication(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.configure(
            background="#3B5998"
        )

        self.master.resizable(False, False)

        self.textareaLabel = Label(
            master,
            text="What to post?",
            background="#3B5998",
            foreground="white",
            bd=3,
        )

        self.textarea = Text(
            master,
            width=30,
            bd=3,
            height=10
        )

        self.username = Text(
            master,
            width=30,
            bd=3,
            height=1,

        )

        self.password = Entry(
            master,
            width=30,
            bd=3,
            show="*"

        )

        self.timeout = Text(
            master,
            width=30,
            bd=3,
            height=1,

        )

        self.usernameLabel = Label(
            master,
            text="Username",
            background="#3B5998",
            foreground="white",
        )

        self.passwordLabel = Label(
            master,
            text="Password",
            background="#3B5998",
            foreground="white",
        )

        self.timeoutLabel = Label(
            master,
            text="Interval",
            background="#3B5998",
            foreground="white",
        )

        self.post_btn = Button(
            master,
            text="POST",
            command=self.post,
            background="#3B5998",
            foreground="white",
            bd=3,
            width=15,
        )

        self.exit_btn = Button(
            master,
            text="EXIT",
            command=self.quit,
            background="#3B5998",
            foreground="white",
            bd=3,
            width=15,
        )

        self.donate_btn = Button(
            master,
            text="Support @ Paypal",
            command=self.quit,
            background="#3B5998",
            foreground="white",
            bd=3,
            width=15
        )

        Label(text="me@menudo.space").grid(
            row=1,
            column=1,
            padx=6,
            pady=6
        )

        self.usernameLabel.grid(
            row=2,
            column=1
        )
        self.username.grid(
            row=2,
            column=2,
            padx=9,
            pady=9
        )
        self.passwordLabel.grid(
            row=3,
            column=1
        )
        self.password.grid(
            row=3,
            column=2,
            padx=9,
            pady=9
        )
        self.timeoutLabel.grid(
            row=4,
            column=1
        )
        self.timeout.grid(
            row=4,
            column=2,
            padx=9,
            pady=9
        )
        self.textareaLabel.grid(
            row=6,
            column=1
        )
        self.textarea.grid(
            row=6,
            column=2
        )

        self.post_btn.grid(
            row=7,
            column=1,
            padx=9,
            pady=9
        )
        self.donate_btn.grid(
            row=8,
            column=1,
            padx=9,
            pady=9
        )
        self.exit_btn.grid(
            row=9,
            column=1,
            padx=9,
            pady=9
        )

    def post(self):
        post = self.textarea.get('1.0', END)
        username = self.username.get('1.0', END)
        password = self.password.get()
        timeout = self.timeout.get('1.0', END)
        if len(post) <= 1\
                or len(username) <= 1\
                or len(password) <= 1\
                or len(timeout) <= 1:
            print("""Please fill all the fields.""")
            return False

        Threader(
            username,
            password,
            timeout,
            post
        )

if __name__ == "__main__":
    fb = GroupAuto()
    MainApplicationFrame = MainApplication()
    MainApplicationFrame.mainloop()
