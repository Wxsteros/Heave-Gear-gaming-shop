import customtkinter
import tkinter
import os
from PIL import Image
customtkinter.set_appearance_mode("dark")

app=customtkinter.CTk()
app.title("Game gear")

app.attributes("-topmost", True)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
bg_image = (r"D:\python porgramming\project\JPG\register.png")
img = customtkinter.CTkImage(light_image=Image.open(bg_image),
                   dark_image=Image.open(bg_image),size=(screen_width, screen_height)) 
label =customtkinter.CTkLabel(app, image=img) 
label = customtkinter.CTkLabel(app, image=img, text="")
label.pack(fill="both", expand=True)

#หัว CREATE AN ACCOUNT
CREATE_AN_ACCOUNT = customtkinter.CTkLabel(master=app,text='CREATE AN ACCOUNT',text_color="#FFFFFF",fg_color="#3f3f3f",font=("Arial", 31.5))
CREATE_AN_ACCOUNT.place(relx=0.6428, rely=0.2526)

#กรอก Gmail
Gmail_text = customtkinter.CTkLabel(master=app, text='Gmail', text_color="#FFFFFF",fg_color="#3f3f3f", font=("Arial", 20))
Gmail_text.place(relx=0.695, rely=0.34, anchor=tkinter.CENTER)
Gmail_Entry=customtkinter.CTkEntry(master=app,width=230,height=30,fg_color="#ffffff",font=("Arial", 20),text_color="#000000")
Gmail_Entry.place(relx=0.751, rely=0.39, anchor=tkinter.CENTER)

#กรอก Username
Username_text = customtkinter.CTkLabel(master=app, text='Username', text_color="#FFFFFF",fg_color="#3f3f3f", font=("Arial", 20))
Username_text.place(relx=0.707, rely=0.43, anchor=tkinter.CENTER)
Username_Entry=customtkinter.CTkEntry(master=app,width=230,height=30,fg_color="#ffffff",font=("Arial", 20),text_color="#000000")
Username_Entry.place(relx=0.751, rely=0.48, anchor=tkinter.CENTER)


#กรอก password
password_text=customtkinter.CTkLabel(master=app,text='password',text_color="#FFFFFF",fg_color="#3f3f3f",font=("Arial", 20))
password_text.place(relx=0.707, rely=0.52, anchor=tkinter.CENTER)
password_Entry=customtkinter.CTkEntry(master=app,width=230,height=30,fg_color="#ffffff",font=("Arial", 20),text_color="#000000")
password_Entry.place(relx=0.751, rely=0.57, anchor=tkinter.CENTER)

# รูปปุ่มตา password
openeye_image_path = (r'D:\python porgramming\project\JPG\open eye 1.png')
closeeye_image_path = (r'D:\python porgramming\project\JPG\Close eyes 1.png')
openeye_image = customtkinter.CTkImage(light_image=Image.open(openeye_image_path),
                                       dark_image=Image.open(openeye_image_path), size=(27, 18))
closeeye_image = customtkinter.CTkImage(light_image=Image.open(closeeye_image_path),
                                        dark_image=Image.open(closeeye_image_path), size=(27, 18))
# ฟังก์ชั่น ปุ่มเปิดปิดตา  password
show_password = False
def openandclose_password():
    global show_password #บอก Python ว่าใช้ตัวแปร show_password ที่ประกาศไว้นอกฟังก์ชัน ไม่ใช่สร้างใหม่
    show_password = not show_password
    if show_password:
        password_Entry.configure(show="")
        button_eye_password.configure(image=closeeye_image)
    else:
        password_Entry.configure(show="*")
        button_eye_password.configure(image=openeye_image)
password_Entry.configure(show="*")
button_eye_password = customtkinter.CTkButton(master=app, image=openeye_image, text="", width=25, height=18, fg_color="#ffffff"
                                     ,command=openandclose_password)
button_eye_password.place(relx=0.84, rely=0.57, anchor=tkinter.CENTER)

#กรอก confirm password
confirm_password_text=customtkinter.CTkLabel(master=app,text='confirm password',text_color="#FFFFFF",fg_color="#3f3f3f",font=("Arial", 20))
confirm_password_text.place(relx=0.729, rely=0.61, anchor=tkinter.CENTER)
confirm_password_Entry=customtkinter.CTkEntry(master=app,width=230,height=30,fg_color="#ffffff",font=("Arial", 20),text_color="#000000")
confirm_password_Entry.place(relx=0.751, rely=0.66, anchor=tkinter.CENTER)

# ฟังก์ชั่น ปุ่มเปิดปิดตา confirm password
show_confirm_password = False
def open_and_close_confirm_password():
    global show_confirm_password
    show_confirm_password = not show_confirm_password
    if show_confirm_password:
        confirm_password_Entry.configure(show="")
        button_eye_confirm.configure(image=closeeye_image)
    else:
        confirm_password_Entry.configure(show="*")
        button_eye_confirm.configure(image=openeye_image)

button_eye_confirm = customtkinter.CTkButton(master=app, image=openeye_image, text="",
                                             width=25, height=18, fg_color="#ffffff",
                                             command=open_and_close_confirm_password)
button_eye_confirm.place(relx=0.84, rely=0.66, anchor=tkinter.CENTER)

#ปุ่ม signup
button_signup = customtkinter.CTkButton(master=app, text='Sign Up', width=220, height=50,font=("Arial", 20),
    fg_color="#00B7FF", border_width=2,text_color="white")
button_signup.place(relx=0.746, rely=0.77, anchor=tkinter.CENTER)

#ข้อความ don't have an account
dont_have_ac_text=customtkinter.CTkLabel(master=app,text="don't have an account",text_color="#FF0000",fg_color="#3f3f3f",font=("Arial", 12))
dont_have_ac_text.place(relx=0.715, rely=0.83, anchor=tkinter.CENTER)

def manu_login():
    app.destroy()         
    if os.path.exists(r'D:\python porgramming\project\Manu loginproject.py'):
        os.system(f'python "{r'D:\python porgramming\project\Manu loginproject.py'}"')  # เปิดหน้า login.py
#กลับไปหน้า Manu login
button_login = customtkinter.CTkButton(master=app, text='login',font=("Arial", 12),width=15, height=10,
    text_color="#00B7FF",fg_color="#3f3f3f",command=manu_login)
button_login.place(relx=0.770, rely=0.8345, anchor=tkinter.CENTER)


app.mainloop()