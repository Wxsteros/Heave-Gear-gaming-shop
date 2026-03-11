import customtkinter
import tkinter
import os
from PIL import Image
import bcrypt
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('blue')


app = customtkinter.CTk()
app.title("Game gear")
app.attributes("-topmost", True)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

bg_image = (r"D:\python porgramming\project\JPG\Welcom to Heven gear gaming shop.png")
img = customtkinter.CTkImage(light_image=Image.open(bg_image),
                   dark_image=Image.open(bg_image),size=(screen_width, screen_height)) 
label =customtkinter.CTkLabel(app, image=img) 
label = customtkinter.CTkLabel(app, image=img, text="")
label.pack(fill="both", expand=True)

#หัว User login
username_login = customtkinter.CTkLabel(master=app,text='User Login',text_color="#FFFFFF",fg_color="#3f3f3f",font=("Arial", 31.5))
username_login.place(relx=0.698, rely=0.25)

#กรอก Username
username_text = customtkinter.CTkLabel(master=app, text='username', text_color="#FFFFFF",fg_color="#3f3f3f", font=("Arial", 20))
username_text.place(relx=0.695, rely=0.34, anchor=tkinter.CENTER)
username_Entry=customtkinter.CTkEntry(master=app,width=230,height=30,fg_color="#ffffff",font=("Arial", 20),text_color="#000000")
username_Entry.place(relx=0.74, rely=0.39, anchor=tkinter.CENTER)

#กรอก password
password_text=customtkinter.CTkLabel(master=app,text='password',text_color="#FFFFFF",fg_color="#3f3f3f",font=("Arial", 20))
password_text.place(relx=0.695, rely=0.43, anchor=tkinter.CENTER)
password_Entry=customtkinter.CTkEntry(master=app,width=230,height=30,fg_color="#ffffff",font=("Arial", 20),text_color="#000000")
password_Entry.place(relx=0.74, rely=0.48, anchor=tkinter.CENTER)

# เพิ่มปุ่มแสดง/ซ่อนรหัสผ่าน
openeye_image_path = (r'D:\python porgramming\project\JPG\open eye 1.png')
closeeye_image_path = (r'D:\python porgramming\project\JPG\Close eyes 1.png')
openeye_image = customtkinter.CTkImage(light_image=Image.open(openeye_image_path),
                                       dark_image=Image.open(openeye_image_path), size=(27, 18))
closeeye_image = customtkinter.CTkImage(light_image=Image.open(closeeye_image_path),
                                        dark_image=Image.open(closeeye_image_path), size=(27, 18))

show_password = False
def openandclose_password():
    global show_password #บอก Python ว่าใช้ตัวแปร show_password ที่ประกาศไว้นอกฟังก์ชัน ไม่ใช่สร้างใหม่
    show_password = not show_password
    if show_password:
        password_Entry.configure(show="")
        button_eye.configure(image=closeeye_image)
    else:
        password_Entry.configure(show="*")
        button_eye.configure(image=openeye_image)
password_Entry.configure(show="*")
button_eye = customtkinter.CTkButton(master=app, image=openeye_image, text="", width=25, height=18, fg_color="#ffffff"
                                     ,command=openandclose_password)
button_eye.place(relx=0.83, rely=0.48, anchor=tkinter.CENTER)

#ปุ่ม forgot password
button_forgotpassword=customtkinter.CTkButton(master=app,text='forgot password ?',text_color="#D80606",
                                                fg_color="#3f3f3f",width=15, height=10,font=("Arial", 12))
button_forgotpassword.place(relx=0.78, rely=0.514, anchor=tkinter.CENTER)

#ปุ่ม login
button_login = customtkinter.CTkButton(master=app, text='login', width=220, height=50,font=("Arial", 20),
    fg_color="#00B7FF", border_width=2,
    text_color="white")
button_login.place(relx=0.74, rely=0.58, anchor=tkinter.CENTER)

def manu_register():
    app.destroy()         
    if os.path.exists(r'D:\python porgramming\project\Registerproject.py'):
        os.system(f'python "{r'D:\python porgramming\project\Registerproject.py'}"')
#ปุ่ม Register
button_register = customtkinter.CTkButton(master=app, text='register', width=220, height=50,font=("Arial", 20),
    fg_color="#00B7FF", border_width=2,text_color="white",command=manu_register)
button_register.place(relx=0.74, rely=0.67, anchor=tkinter.CENTER)

app.mainloop()