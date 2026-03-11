import customtkinter
import os
from PIL import Image
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('blue')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game gear")
        self.attributes("-topmost", True)

        # ค่าหน้าจอ 
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # สร้าง container สำหรับเปลี่ยนหน้า 
        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # หน้า Login / Register / Admin_page / User_page)
        self.frames = {}
        for F in (LoginPage, RegisterPage,Admin_page,show_product_page):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #show frame หน้า login
        self.show_frame("LoginPage")

    def show_frame(self, name: str):
        self.frames[name].tkraise()
        
#===================หน้า Login====================
class LoginPage(customtkinter.CTkFrame):
    def __init__(self, master, app: App):
        super().__init__(master, fg_color="#000000")
        self.app = app
        self.bg_image = ("D:\python porgramming\project\JPG\Welcom to Heven gear gaming shop (2).png")
        self.img = customtkinter.CTkImage(light_image=Image.open(self.bg_image),dark_image=Image.open(self.bg_image),size=(self.app.screen_width, self.app.screen_height))
        self.label = customtkinter.CTkLabel(self, image=self.img, text="")
        self.label.pack(fill="both", expand=True)
        
        self.lgn_frame = customtkinter.CTkFrame(master=self, fg_color="#3f3f3f",bg_color="#000000",width=550, height=650,corner_radius=50,)
        self.lgn_frame.place(relx=0.74, rely=0.5,anchor='center')

        self.logo_image=("D:\python porgramming\project\JPG\logo1 .png")
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(self.logo_image),dark_image=Image.open(self.logo_image), size=(156, 110))
        self.logo_label = customtkinter.CTkLabel(master=self, image=self.logo_image, text="",fg_color="#3f3f3f")
        self.logo_label.place(relx=0.74, rely=0.23, anchor="center")

        #  หัวข้อ Sign In
        self.Sign_In = customtkinter.CTkLabel(master=self, text='Sign In', text_color="#FFFFFF",fg_color="#3f3f3f",bg_color="#3f3f3f", font=("Arial", 31.5))
        self.Sign_In.place(relx=0.705, rely=0.31)

        #  username 
        self.username_text = customtkinter.CTkLabel(master=self, text='username', text_color="#FFFFFF",fg_color="#3f3f3f",bg_color="#3f3f3f", font=("Arial", 20))
        self.username_text.place(relx=0.695, rely=0.4,anchor='center')
        self.username_Entry = customtkinter.CTkEntry(master=self, width=230, height=30,fg_color="#ffffff", font=("Arial", 20), text_color="#000000",bg_color="#3f3f3f")
        self.username_Entry.place(relx=0.74, rely=0.45,anchor='center')

        #  password 
        self.password_text = customtkinter.CTkLabel(master=self, text='password', text_color="#FFFFFF",fg_color="#3f3f3f",bg_color="#3f3f3f", font=("Arial", 20))
        self.password_text.place(relx=0.695, rely=0.49, anchor='center')
        self.password_Entry = customtkinter.CTkEntry(master=self, width=230, height=30,fg_color="#ffffff", font=("Arial", 20), text_color="#000000",bg_color="#3f3f3f")
        self.password_Entry.place(relx=0.74, rely=0.54, anchor='center')

        # ปุ่มแสดง/ซ่อนรหัสผ่าน 
        self.openeye_image_path = (r'D:\python porgramming\project\JPG\open eye 1.png')
        self.closeeye_image_path = (r'D:\python porgramming\project\JPG\Close eyes 1.png')
        self.openeye_image = customtkinter.CTkImage(light_image=Image.open(self.openeye_image_path),dark_image=Image.open(self.openeye_image_path), size=(27, 18))
        self.closeeye_image = customtkinter.CTkImage(light_image=Image.open(self.closeeye_image_path), dark_image=Image.open(self.closeeye_image_path), size=(27, 18))

        self.show_password = False
        self.password_Entry.configure(show="*")

        def openandclose_password():
            self.show_password = not self.show_password
            if self.show_password:
                self.password_Entry.configure(show="")
                self.button_eye.configure(image=self.closeeye_image)
            else:
                self.password_Entry.configure(show="*")
                self.button_eye.configure(image=self.openeye_image)

        self.openandclose_password = openandclose_password 
        self.button_eye = customtkinter.CTkButton(master=self, image=self.openeye_image, text="",width=25, height=18, fg_color="#ffffff",command=self.openandclose_password,bg_color="#3f3f3f")
        self.button_eye.place(relx=0.83, rely=0.54,anchor='center')

        #  ปุ่ม forgot password  
        self.button_forgotpassword = customtkinter.CTkButton(master=self, text='forgot password ?', text_color="#D80606",fg_color="#3f3f3f", width=15, height=10
                                                             ,font=("Arial", 12),bg_color="#3f3f3f")
        self.button_forgotpassword.place(relx=0.78, rely=0.574, anchor='center')

        #เข้าหน้าAdmin
        def manu_admin():
            self.app.show_frame("Admin_page")
        self.manu_admin = manu_admin

        #เข้าหน้าuser
        def show_product_page():
            self.app.show_frame("show_product_page")
        self.show_product_page= show_product_page

        #ฟังก์ชันตรวจสอบข้อมูล password กับ Username ใน Data base
        #def connect_database():
        #    if  self.password_Entry.get()==''or self.username_Entry.get()=='':
        #        CTkMessagebox(title="Error", message="Password is incorrect", icon="cancel")
        #    elif self.password_Entry!= self.confirm_password_Entry or self.username_Entry  :
        #        CTkMessagebox(title="Error",message="Username or Password is incorrect.try again.", icon="cancel")
        #  ปุ่ม login 
        self.button_SIGN_IN = customtkinter.CTkButton(master=self, text='SIGN IN', width=220, height=50, font=("Arial", 20),fg_color="#3f3f3f",hover_color="#00B7FF"
                                                       ,border_color="#FFD900",border_width=2,corner_radius=32,bg_color="#3f3f3f",text_color="white",command=self.show_product_page)#compound=connect_database
        self.button_SIGN_IN.place(relx=0.74, rely=0.66,anchor='center')

        #ฟังก์ชั่น เปลี่ยนไปหน้า Sign up
        def manu_register():
            self.app.show_frame("RegisterPage")
        self.manu_register = manu_register 

        #ปุ่ม register
        self.button_SIGN_UP = customtkinter.CTkButton(master=self,text='SIGN UP',width=220,height=50,font=("Arial", 20),fg_color="#3f3f3f",bg_color="#3f3f3f",hover_color="#00B7FF"
                                                       ,border_color="#FFD900",border_width=2,corner_radius=32,text_color="white",command=self.manu_register)
        self.button_SIGN_UP.place(relx=0.74, rely=0.75, anchor='center')

#=================หน้า Sing Up ================
class RegisterPage(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        #  พื้นหลัง 
        self.bg_image = ("D:\python porgramming\project\JPG\Register to Heven shop.png")
        self.img = customtkinter.CTkImage(light_image=Image.open(self.bg_image),dark_image=Image.open(self.bg_image)
                                          ,size=(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))
        self.label = customtkinter.CTkLabel(self, image=self.img, text="")
        self.label.pack(fill="both", expand=True)

        self.lgn_frame = customtkinter.CTkFrame(master=self, fg_color="#3f3f3f",bg_color="#000000",width=550, height=650,corner_radius=50,)
        self.lgn_frame.place(relx=0.74, rely=0.5,anchor='center')

        self.logo_image=("D:\python porgramming\project\JPG\logo1 .png")
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(self.logo_image),dark_image=Image.open(self.logo_image), size=(156, 110))
        self.logo_label = customtkinter.CTkLabel(master=self, image=self.logo_image, text="",fg_color="#3f3f3f")
        self.logo_label.place(relx=0.74, rely=0.23, anchor="center")

        #  หัวข้อ CREATE AN ACCOUNT
        self.CREATE_AN_ACCOUNT = customtkinter.CTkLabel(master=self, text='CREATE AN ACCOUNT',text_color="#FFFFFF", fg_color="#3f3f3f",bg_color="#3f3f3f",font=("Arial", 27.5))
        self.CREATE_AN_ACCOUNT.place(relx=0.645, rely=0.31)

        #  Gmail
        self.Gmail_text = customtkinter.CTkLabel(master=self, text='Gmail',text_color="#FFFFFF", fg_color="#3f3f3f",bg_color="#3f3f3f", font=("Arial", 20))
        self.Gmail_text.place(relx=0.687, rely=0.39,anchor='center')
        self.Gmail_Entry = customtkinter.CTkEntry(master=self, width=230, height=30,fg_color="#ffffff",bg_color="#3f3f3f",font=("Arial", 20),text_color="#000000")
        self.Gmail_Entry.place(relx=0.743, rely=0.44, anchor='center')

        #  Username 
        self.Username_text = customtkinter.CTkLabel(master=self, text='Username',text_color="#FFFFFF", fg_color="#3f3f3f",bg_color="#3f3f3f",font=("Arial", 20))
        self.Username_text.place(relx=0.7, rely=0.48, anchor='center')
        self.Username_Entry = customtkinter.CTkEntry(master=self, width=230, height=30,fg_color="#ffffff",bg_color="#3f3f3f",font=("Arial", 20), text_color="#000000")
        self.Username_Entry.place(relx=0.743, rely=0.53, anchor='center')

        #ฟังก์ชันตรวจสอบข้อมูล password กับ confirm password
        def connect_database():
            if self.Gmail_Entry.get()==''or self.Username_Entry.get()=='' or self.password_Entry.get()==''or self.confirm_password_Entry.get()=='':
                CTkMessagebox(title="Error", message="All Fields Are Required", icon="cancel")
            elif self.password_Entry!= self.confirm_password_Entry:
                CTkMessagebox(title="Error", message="Password confirmation dose not match", icon="cancel")
           # else:
            #    try:
            #        conn = sqlite3.connect(r"D:\python porgramming\Heaven gear gaming shop")

        #  Password 
        self.password_text = customtkinter.CTkLabel(master=self, text='Password',text_color="#FFFFFF", fg_color="#3f3f3f",bg_color="#3f3f3f",font=("Arial",20))
        self.password_text.place(relx=0.699, rely=0.57,anchor='center')
        self.password_Entry = customtkinter.CTkEntry(master=self, width=230, height=30,fg_color="#ffffff",bg_color="#3f3f3f",font=("Arial", 20), text_color="#000000",show="*")
        self.password_Entry.place(relx=0.743, rely=0.61,anchor='center')

        # รูปไอคอนตา
        self.openeye_image_path = (r'D:\python porgramming\project\JPG\open eye 1.png')
        self.closeeye_image_path = (r'D:\python porgramming\project\JPG\Close eyes 1.png')
        self.openeye_image = customtkinter.CTkImage(light_image=Image.open(self.openeye_image_path),dark_image=Image.open(self.openeye_image_path), size=(27, 18))
        self.closeeye_image = customtkinter.CTkImage(light_image=Image.open(self.closeeye_image_path),dark_image=Image.open(self.closeeye_image_path), size=(27, 18))

        # ฟังก์ชันเปิด/ปิดตา password 
        self.show_password = False
        def openandclose_password():
            self.show_password = not self.show_password
            if self.show_password:
                self.password_Entry.configure(show="")
                self.button_eye_password.configure(image=self.closeeye_image)
            else:
                self.password_Entry.configure(show="*")
                self.button_eye_password.configure(image=self.openeye_image)
        self.openandclose_password = openandclose_password

        self.button_eye_password = customtkinter.CTkButton(master=self, image=self.openeye_image, text="",width=25, height=18,fg_color="#ffffff",bg_color="#3f3f3f"
                                                           ,command=self.openandclose_password)
        self.button_eye_password.place(relx=0.834, rely=0.61, anchor='center')

        #  Confirm password 
        self.confirm_password_text = customtkinter.CTkLabel(master=self, text='Confirm password',text_color="#FFFFFF", fg_color="#3f3f3f",bg_color="#3f3f3f",font=("Arial", 20))
        self.confirm_password_text.place(relx=0.723, rely=0.66,anchor='center')
        self.confirm_password_Entry = customtkinter.CTkEntry(master=self, width=230, height=30,fg_color="#ffffff",bg_color="#3f3f3f",font=("Arial", 20), text_color="#000000", show="*")
        self.confirm_password_Entry.place(relx=0.743, rely=0.71, anchor='center')

        self.show_confirm_password = False
        def open_and_close_confirm_password():
            self.show_confirm_password = not self.show_confirm_password
            if self.show_confirm_password:
                self.confirm_password_Entry.configure(show="")
                self.button_eye_confirm.configure(image=self.closeeye_image)
            else:
                self.confirm_password_Entry.configure(show="*")
                self.button_eye_confirm.configure(image=self.openeye_image)
        self.open_and_close_confirm_password = open_and_close_confirm_password

        self.button_eye_confirm = customtkinter.CTkButton(master=self, image=self.openeye_image, text="", width=25, height=18, fg_color="#ffffff", bg_color="#3f3f3f",
                                  command=self.open_and_close_confirm_password)
        self.button_eye_confirm.place(relx=0.834, rely=0.71, anchor='center')

        #  ปุ่ม Sign Up 
        self.button_signup = customtkinter.CTkButton(master=self, text='Sign Up', width=220, height=50, font=("Arial", 20),fg_color="#3f3f3f",hover_color="#00B7FF"
                                                    ,border_color="#FFD900",border_width=2,corner_radius=32,bg_color="#3f3f3f",text_color="white",command=connect_database)
        self.button_signup.place(relx=0.74, rely=0.78,anchor='center')

        #  don't have an account 
        self.dont_have_ac_text = customtkinter.CTkLabel(master=self, text="don't have an account",text_color="#FF0000",fg_color="#3f3f3f",font=("Arial", 12),bg_color="#3f3f3f")
        self.dont_have_ac_text.place(relx=0.72, rely=0.828,anchor='center')

        # ปุ่ม login กลับหน้า Login
        def manu_login():
            self.app.show_frame("LoginPage")
        self.manu_login = manu_login
        self.button_login = customtkinter.CTkButton(master=self, text='login', font=("Arial", 12),width=15, height=10, text_color="#00B7FF", fg_color="#3f3f3f",bg_color="#3f3f3f"
                                                    ,command=self.manu_login)
        self.button_login.place(relx=0.772, rely=0.828,anchor='center')


#หน้า show product to user
class show_product_page(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="#000000")
        self.app = app

        # เฟรมขวา 
        self.right_frame = customtkinter.CTkScrollableFrame(
            master=self,fg_color="#3f3f3f",bg_color="#000000",width=1100,height=700,corner_radius=20)
        self.right_frame.place(relx=0.61, rely=0.5, anchor='center')

        # เฟรมซ้าย 
        self.left_frame = customtkinter.CTkScrollableFrame( master=self,fg_color="#3f3f3f",bg_color="#000000",width=255,height=700,corner_radius=20)
        self.left_frame.place(relx=0.12, rely=0.5, anchor='center')
        
        self.right_stack = customtkinter.CTkFrame(self, fg_color="#3f3f3f",bg_color="#3f3f3f",width=1100, height=700,corner_radius=20)
        self.right_stack.place(relx=0.61, rely=0.5, anchor='center')
        self.right_stack.grid_rowconfigure(0, weight=1)
        self.right_stack.grid_columnconfigure(0, weight=1)

        self.pages: dict[str, customtkinter.CTkScrollableFrame] = {}

        #================== หน้า Edit profile  user ================
        def Page_Editprofile() -> customtkinter.CTkScrollableFrame:
            page = customtkinter.CTkScrollableFrame(master=self.right_stack, fg_color="#3f3f3f",bg_color="#000000", corner_radius=20, width=1100, height=700)
            page.grid(row=0, column=0, sticky="nsew") # วางทับตำแหน่งเดียวกันทั้งหมด
            
            self.icon_profile_img = customtkinter.CTkImage(light_image=Image.open(r"D:\python porgramming\project\JPG\Profile.png"),
                                                            dark_image=Image.open(r"D:\python porgramming\project\JPG\Profile.png"),
                                                            size=(200,200))
            
            icon = customtkinter.CTkLabel(master=page,image=self.icon_profile_img,text="",fg_color="transparent")
            icon.pack(pady=(6, 24))

            self.MY_ACCOUNT = customtkinter.CTkLabel(master=page, text='MY ACCOUNT',text_color="#FFFFFF", fg_color="#3f3f3f",bg_color="#3f3f3f",font=("Arial", 27.5))
            self.MY_ACCOUNT.pack()

            #==================ฟอร์มแก้ไขข้อมูล==================
            form = customtkinter.CTkFrame(page, fg_color="#3f3f3f")
            form.pack(pady=12, padx=10)
            customtkinter.CTkLabel(form, text="Username", text_color="white").grid(row=0, column=0, sticky="w", pady=6, padx=5)
            customtkinter.CTkEntry(form, width=200).grid(row=0, column=2, pady=6, padx=5)

            customtkinter.CTkLabel(form, text="Password", text_color="white").grid(row=1, column=0, sticky="w", pady=6, padx=5)
            customtkinter.CTkEntry(form, width=200, show="*").grid(row=1, column=2, pady=6, padx=5)

            customtkinter.CTkLabel(form, text="Email", text_color="white").grid(row=0, column=3, sticky="w", pady=6, padx=5)
            customtkinter.CTkEntry(form, width=200).grid(row=0, column=5, pady=6, padx=5)

            customtkinter.CTkLabel(form, text="Phone number", text_color="white").grid(row=1, column=3, sticky="w", pady=6, padx=5)
            customtkinter.CTkEntry(form, width=200).grid(row=1, column=5, pady=6, padx=5)

            customtkinter.CTkLabel(form, text="Address", text_color="white").grid(row=3, column=0, sticky="w", pady=6, padx=5)
            customtkinter.CTkEntry(form, width=200).grid(row=3, column=2, pady=6, padx=5)

            customtkinter.CTkLabel(form, text="Full name", text_color="white").grid(row=3, column=3, sticky="w", pady=6, padx=5)
            customtkinter.CTkEntry(form, width=200).grid(row=3, column=5, pady=6, padx=5)

            update_button = customtkinter.CTkButton(page, text="Update", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
            update_button.pack(pady=12, padx=10)

            #show profile
            
            self.pages["profile"] = page
            return page

        self.Page_Editprofile = Page_Editprofile

    
        #==================หน้า show product================
        def Page_show_product() -> customtkinter.CTkScrollableFrame:
            page = customtkinter.CTkScrollableFrame(master=self.right_stack, fg_color="#3f3f3f", bg_color="#000000", corner_radius=20, width=1100, height=700)
            page.grid(row=0, column=0, sticky="nsew") # วางทับตำแหน่งเดียวกันทั้งหมด

            # สร้าง label SHOW PRODUCT
            self.show_product_label = customtkinter.CTkLabel(master=page, text='All Products', text_color="#FFFFFF", fg_color="#3f3f3f", bg_color="#3f3f3f", font=("Arial", 27.5))
            self.show_product_label.pack(pady=20)

            self.pages["show_product"] = page
            return page

        self.Page_show_product = Page_show_product

        def Mouse_page()-> customtkinter.CTkScrollableFrame: 
            pass
        self.Mouse = Mouse_page
        def Mouse_Pad_page()-> customtkinter.CTkScrollableFrame:
            pass
        self.Mouse_Pad = Mouse_Pad_page
        def Keybord_page()-> customtkinter.CTkScrollableFrame:
            pass
        self.Keybord = Keybord_page 
        def Mornitor_page()-> customtkinter.CTkScrollableFrame:
            pass
        self.Mornitor = Mornitor_page
        def Headphone_page()-> customtkinter.CTkScrollableFrame:
            pass
        self.Headphone = Headphone_page
        def Microphone_page()-> customtkinter.CTkScrollableFrame:
            pass  
        self.Microphone = Microphone_page  

        # เพิ่ม widget ตัวอย่างในเฟรมซ้าย
        self.logo_image=("D:\python porgramming\project\JPG\logo1 .png")
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(self.logo_image),dark_image=Image.open(self.logo_image), size=(156, 110)) 
        self.logo_label = customtkinter.CTkLabel(self.left_frame, image=self.logo_image, text="",fg_color="#3f3f3f")
        self.logo_label.pack(pady=10)

        #ปุ่ม รถเข็น
        Cart_image = customtkinter.CTkImage(light_image=Image.open(r"D:\python porgramming\project\JPG\basket.png"),
                            dark_image=Image.open(r"D:\python porgramming\project\JPG\basket.png"),
                            size=(30,30))
        Cart = customtkinter.CTkButton(self.left_frame, image=Cart_image, text="", fg_color="#3f3f3f",bg_color="#3f3f3f",text_color="white")
        Cart.pack(pady=5, padx=10, fill="x")

        # ปุ่ม Edit profile
        profile_icon = customtkinter.CTkImage(light_image=Image.open(r"D:\python porgramming\project\JPG\user-icon.png"),
                                                dark_image=Image.open(r"D:\python porgramming\project\JPG\user-icon.png"),
                                                size=(70,70))
        profile_icon_btn = customtkinter.CTkButton(self.left_frame, image=profile_icon, text="", fg_color="#3f3f3f",bg_color="#3f3f3f",text_color="white",command=self.Page_Editprofile)
        profile_icon_btn.pack(pady=5, padx=10, fill="x")

        #ปุ่มแสดงสินค้าทั้งหมด
        All_product = customtkinter.CTkButton(self.left_frame, text="All product", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16),command=self.Page_show_product)
        All_product.pack(pady=5, padx=10, fill="x")

        # ====== PRICE RANGE FILTER (เพิ่มไว้ในเฟรมซ้าย) ======
        # ค่าตั้งต้นและขอบเขต 
        self.PRICE_MIN_BOUND = 0
        self.PRICE_MAX_BOUND = 15000

        # เก็บค่าที่ผู้ใช้เลือก
        self.price_min_var = customtkinter.IntVar(value=0)
        self.price_max_var = customtkinter.IntVar(value=15000)

        price_frame = customtkinter.CTkFrame(self.left_frame, fg_color="#3f3f3f", corner_radius=12)
        price_frame.pack(pady=5,padx=10, fill="x")
        customtkinter.CTkLabel(price_frame, text="ช่วงราคา", text_color="white", font=("Arial", 14, "bold")).pack(pady=(10, 6))

        # แสดงค่าปัจจุบัน
        value_row = customtkinter.CTkFrame(price_frame, fg_color="transparent")
        value_row.pack(fill="x", padx=12)
        self.min_label = customtkinter.CTkLabel(value_row, text=f"ต่ำสุด: {self.price_min_var.get():,} บาท", text_color="white")
        self.min_label.pack(side="left")
        self.max_label = customtkinter.CTkLabel(value_row, text=f"สูงสุด: {self.price_max_var.get():,} บาท", text_color="white")
        self.max_label.pack(side="right")

        # ค่าต่ำสุด
        def on_min_change(v):
            v = int(v)
            # ห้ามเกินค่าบน
            if v > self.price_max_var.get():
                v = self.price_max_var.get()
            self.price_min_var.set(v)
            self.min_label.configure(text=f"ต่ำสุด: {v:,} บาท")

        self.min_slider = customtkinter.CTkSlider(price_frame, from_=self.PRICE_MIN_BOUND, to=self.PRICE_MAX_BOUND,number_of_steps=1000, command=on_min_change)
        self.min_slider.set(self.price_min_var.get())
        self.min_slider.pack(padx=5, pady=(5,10), fill="x")

        # ค่าสูงสุด
        def on_max_change(v):
            v = int(v)
            # ห้ามต่ำกว่าค่าล่าง
            if v < self.price_min_var.get():
                v = self.price_min_var.get()
            self.price_max_var.set(v)
            self.max_label.configure(text=f"สูงสุด: {v:,} บาท")

        self.max_slider = customtkinter.CTkSlider(price_frame, from_=self.PRICE_MIN_BOUND, to=self.PRICE_MAX_BOUND,number_of_steps=1000, command=on_max_change)
        self.max_slider.set(self.price_max_var.get())
        self.max_slider.pack(padx=5, pady=10, fill="x")

        # ปุ่ม Apply 
        apply_btn = customtkinter.CTkButton( price_frame, text="Apply", fg_color="#27dfec", text_color="white",font=("Arial", 16))
        apply_btn.pack(padx=5, pady=10, fill="x")

        # ปุ่มหมวดหมู่สินค้าประเภทเม้าส์
        Mouse = customtkinter.CTkButton(self.left_frame, text="Mouse", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
        Mouse.pack(pady=5, padx=10, fill="x")

        # ปุ่มหมวดหมู่สินค้าประเภทแผ่นรองเม้าส์
        Mouse_Pad = customtkinter.CTkButton(self.left_frame, text="Mouse Pad", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
        Mouse_Pad.pack(pady=5, padx=10, fill="x")

        # ปุ่มหมวดหมู่สินค้าประเภทคีย์บอร์ด
        Keybord = customtkinter.CTkButton(self.left_frame, text="Keyboard", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
        Keybord.pack(pady=5, padx=10, fill="x")

        # ปุ่มหมวดหมู่สินค้าประเภทจอ
        Mornitor = customtkinter.CTkButton(self.left_frame, text="Mornitor", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
        Mornitor.pack(pady=5, padx=10, fill="x")

        # ปุ่มหมวดหมู่สินค้าประเภทหูฟัง
        Headphone = customtkinter.CTkButton(self.left_frame, text="Headphone", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
        Headphone.pack(pady=5, padx=10, fill="x")

        # ปุ่มหมวดหมู่สินค้าประเภทไมโครโฟน
        Microphone = customtkinter.CTkButton(self.left_frame, text="Microphone", fg_color="#27dfec",bg_color="#3f3f3f",text_color="white",font=("Arial", 16))
        Microphone.pack(pady=5, padx=10, fill="x")
        
        # ปุ่ม logout
        Logout = customtkinter.CTkButton(self.left_frame, text="Logout", fg_color="#FF0000", bg_color="#3f3f3f", text_color="white", font=("Arial", 16), command=lambda: self.app.show_frame("LoginPage"))
        Logout.pack(pady=5, padx=10, fill="x")
                
class Admin_page(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app  

if __name__ == "__main__":
    app = App()
    # ตั้ง geometry เท่าหน้าจอเพื่อให้ภาพเต็ม (หรือจะใช้ app.state("zoomed"))
    app.geometry(f"{app.screen_width}x{app.screen_height}")
    app.mainloop() 