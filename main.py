#-----WINDOW

log_in_window = Toplevel(main_window)
log_in_window.title("authorization")
log_in_window.geometry('270x150')


#-----INPUT
label_login = Label(log_in_window, text="Login:")
label_login.grid(column=0, row=0)

input_text_box_login = Entry(log_in_window, justify=CENTER)
input_text_box_login.grid(column=1, row=0)


#----LOG
log_text_box = scrolledtext.ScrolledText(log_in_window, width=30, height=2)
log_text_box.grid(column=0, columnspan=2, row=4, rowspan=1, sticky=S + W + E)


#-BUTTON

_button = Button(main_window, text="", command=)
_button.grid(column=0, row=0)