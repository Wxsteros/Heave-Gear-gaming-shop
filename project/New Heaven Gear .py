import os, webbrowser #ใช้สำหรับจัดการไฟล์ โฟลเดอร์ในเครื่อง 
from pathlib import Path
import re #ใช้สำหรับ ตรวจสอบ ข้อความ
import sqlite3 # ใช้เชื่อมต่อและจัดการฐานข้อมูล
from datetime import datetime #ใช้ดึงเวลา/วันที่ปัจจุบัน และแปลงรูปแบบเวลา
from pathlib import Path #ใช้จัดการ path ไฟล์
from typing import Optional #ใช้กำหนด type ว่า value
import tkinter.filedialog as fd #เอาไว้เปิด dialog ให้ user เลือกไฟล์จาก Windows
# ========== UI / Widgets ==========
import customtkinter 
from CTkMessagebox import CTkMessagebox #ใช้ popup แจ้งเตือน/ถาม/แจ้ง error 
# ========== Images ==========
from PIL import Image, ImageDraw, ImageOps #สำหรับเปิด, ตัดขอบ, วาด, 
# ========== PDF (ReportLab) ==========
from reportlab.pdfgen import canvas #ใช้สร้าง PDF และวาด text/เส้น/รูปลง PDF
from reportlab.lib.pagesizes import A4 #กำหนดขนาดหน้ากระดาษ PDF เป็น A4
from reportlab.lib.units import mm #ใช้กำหนดหน่วยเป็นมิลลิเมตรใน PDF
from reportlab.lib import colors #กำหนดสีที่จะใช้ใน PDF
from reportlab.lib.utils import ImageReader #ใช้แปลงรูปให้สามารถนำไปวางใน PDF ได้
from reportlab.pdfbase import pdfmetrics #ใช้จัดการ font ใน PDF
from reportlab.pdfbase.ttfonts import TTFont #ใช้โหลด font .ttf ของเราเองเข้า PDF

# ======== CONFIG ร้าน / โลโก้ / ฟอนต์ไทย ========
STORE_NAME   = "Heaven Gear Gaming Shop"
STORE_ADDR   = "Heaven Gear Gaming Shop สาขา Complex ศูนย์อาหารและบริการ 1 ตำบลศิลา อำเภอเมืองขอนแก่น ขอนแก่น 40000"
STORE_PHONE  = "099-369-0768"
STORE_EMAIL  = "Kittikon.k@kkumail.com"
VAT_RATE     = 0.07
LOGO_PATH    = r"D:\python porgramming\project\JPG\logo1 .png"  

# ====== ฟอนต์ไทยสำหรับ PDF (ต้องมีไฟล์ .ttf) ======
PDF_FONT = "THSarabunNew"
REPORTLAB_OK = True

#ฟังก์ชั่นนี้ใช้สำหรับ โหลด font TH Sarabun เข้าไปให้ reportlab ใช้เวลาสร้าง PDF เพื่อให้ไฟล์ PDF ของเราแสดงภาษาไทยได้ถูกต้อง ไม่เพี้ยน ไม่เป็นสี่เหลี่ยม
def _init_pdf_font():
    global REPORTLAB_OK, PDF_FONT
    try:
        base = os.path.dirname(r"D:\python porgramming\project\fonts")  
        font_path = os.path.join(base, "fonts", "THSarabunNew.ttf")
        print("[CHECK FONT EXISTS?] =>", os.path.exists(font_path), font_path)
        pdfmetrics.registerFont(TTFont(PDF_FONT, font_path))
        REPORTLAB_OK = True
        print("[PDF FONT] OK")
    except Exception as e:
        REPORTLAB_OK = False
        print("PDF font init error =>", e)
_init_pdf_font()
# ================================================

#ธีมของapp
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

# ================== DATABASE ==================
DB_PATH = "Heaven gear shop.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def setup_user_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (                  
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            gmail TEXT NOT NULL,
            fullname TEXT,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            path TEXT
        );
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL CHECK(price >= 0),
            stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
            category TEXT NOT NULL,
            image_path TEXT,
            description TEXT
        );        
            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'PENDING',
            total INTEGER NOT NULL DEFAULT 0,
            address_snapshot TEXT,
            cancel_reason TEXT,
            path_slip TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
            CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            unit_price INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            image_path TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        );            
    """)
    try:
        cur.execute("ALTER TABLE users ADD COLUMN fullname TEXT")
    except sqlite3.OperationalError:
        # ถ้ามีอยู่แล้วจะขึ้น 'duplicate column name' — ปล่อยผ่าน
        pass
    conn.commit()
    conn.close()

#ฟังก์ชันนี้ทำหน้าที่ บันทึกข้อมูลสมาชิกใหม่ลงตาราง users
def register_user(fullname,Username, Password, role="user", Gmail=None, Address=None, Phone=None):
    conn = connect_db()
    try:
        conn.execute("INSERT INTO users (fullname,username, password, role, gmail, address, phone) VALUES (?, ?, ?, ?, ?, ?)",(Username, Password, role, Gmail, Address, Phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# ฟังก์ชันนี้ใช้ตรวจสอบว่า username และ gmail ที่ user ใส่มา ตรงกัน หรือไม่
# ถ้าตรง ใช้ในระบบ “ลืมรหัสผ่าน” ได้
def verify_user_email(username: str, gmail: str) -> int | None:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND gmail=?", (username, gmail))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# ฟังก์ชันนี้ใช้เปลี่ยน password ของ user 
def update_user_password(user_id: int, new_password: str) -> bool:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
    conn.commit()
    ok = cur.rowcount > 0
    conn.close()
    return ok

# ฟังก์ชันนี้คือ ตรวจสอบการเข้าสู่ระบบ (Login)
# ถ้ารหัสผ่านถูก → ส่ง id กับ role กลับไป
def login_user(username, password):
    conn = connect_db()
    try:
        row = conn.execute("SELECT id, password, role FROM users WHERE username=?", (username,)).fetchone()
        if not row:
            return None
        uid, stored_pw, role = row
        if password == stored_pw:   
            return (uid, role)
        return None
    finally:
        conn.close()

 #สร้าง admin เริ่มต้น 
def seed_admin_user():
    conn = connect_db()
    cur = conn.cursor()
    check = cur.execute("SELECT id FROM users WHERE role='admin' LIMIT 1").fetchone()
    if not check:
        register_user("admin", "admin123", 
                    role="admin",Gmail="admin@example.com",
                    Address="HQ",Phone="0000000000")  #  admin login = admin / admin123
    conn.close()
setup_user_table()

#ฟังก์ชั่นนี้ไว้ช่วยให้ database รุ่นเก่า สามารถรองรับ features ใหม่ของโปรเจคได้ โดยไม่ต้องลบทิ้งแล้วสร้างใหม่.
def ensure_order_schema():
    conn = connect_db()
    cur = conn.cursor()
    # ===== orders =====
    #เปิด DB และอ่านคอลัมน์ที่มีอยู่ใน orders
    #ถ้าขาด column ไหน → เพิ่ม column นั้นเข้าไปทันทีด้วย
    cur.execute("PRAGMA table_info(orders)")
    ocols = {c[1] for c in cur.fetchall()}

    if "status" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'PENDING'")
    if "total" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN total INTEGER NOT NULL DEFAULT 0")
    if "address_snapshot" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN address_snapshot TEXT")
    if "cancel_reason" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN cancel_reason TEXT")
    if "path_slip" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN path_slip TEXT")

    # --- คอลัมน์ใหม่ที่ต้องใช้กับใบเสร็จ/การชำระเงิน ---
    if "shipping_fee" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN shipping_fee INTEGER NOT NULL DEFAULT 0")
    if "txn_id" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN txn_id TEXT")
    if "paid_date" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN paid_date DATETIME")
    if "issue_date" not in ocols:
        cur.execute("ALTER TABLE orders ADD COLUMN issue_date DATETIME")

    # ===== sales_log (ใช้ใน Approve_Order_and_Log) =====
    #สร้างตาราง sales_log  เพื่อบันทึกสถิติการขาย
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            qty INTEGER NOT NULL,
            unit_price INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            confirmed_at DATETIME NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

# add สินค้าใหม่เข้าตาราง product
def Create_Product(Name, Price, Stock, Category, Image_Path, Description):
    conn = connect_db()
    try:
        conn.execute("""INSERT INTO products (name, price, stock, category, image_path, description)VALUES (?, ?, ?, ?, ?, ?)"""
                     ,(Name, int(Price), int(Stock), Category, Image_Path, Description))
        conn.commit()
        return True
    except Exception as e:
        print("Create_Product error:", e)
        return False
    finally:
        conn.close()

# แก้ไขข้อมูลสินค้าในตาราง product
def Update_Product(Product_ID, Name, Price, Stock, Category, Image_Path, Description):
    conn = connect_db()
    try:
        conn.execute("""UPDATE products SET 
                     name=?, price=?, stock=?, category=?, image_path=?, description=?
                     WHERE id=?
                     """
                     ,(Name, int(Price), int(Stock), Category, Image_Path, Description, int(Product_ID)))
        conn.commit()
        return conn.total_changes > 0
    except Exception as e:
        print("Update_Product error:", e)
        return False
    finally:
        conn.close()
# ลบข้อมูลสินค้าในตาราง product
def Delete_Product(Product_ID):
    conn = connect_db()
    try:
        conn.execute("DELETE FROM products WHERE id=?", (int(Product_ID),))
        conn.commit()
        return conn.total_changes > 0
    except Exception as e:
        print("Delete_Product error:", e)
        return False
    finally:
        conn.close()

#ฟังก์ชันนี้ใช้สำหรับ ดึงรายการสินค้าจากฐานข้อมูล products เอาไว้ใช้ seach หาสินค้า
def Fetch_Products(Keyword=None):
    conn = connect_db()
    try:
        if Keyword:
            KW = f"%{Keyword.strip()}%"
            rows = conn.execute("""
                SELECT id, name, price, stock, category, image_path, description
                FROM products
                WHERE name LIKE ? OR category LIKE ?
                COLLATE NOCASE
                ORDER BY id DESC
            """, (KW, KW)).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, name, price, stock, category, image_path, description
                FROM products
                ORDER BY id DESC
            """).fetchall()

        return rows
    finally:
        conn.close()

#  ของหมวดหมู่ทั้งหมดที่มีในตาราง products (เรียง A→Z) ในหน้า seach
def Fetch_Categories():
    conn = connect_db()
    try:
        rows = conn.execute("SELECT DISTINCT category FROM products ORDER BY category COLLATE NOCASE").fetchall()
        return [r[0] for r in rows if r and r[0]]
    finally:
        conn.close()

# ฟังก์ชันนี้ใช้ ดึงสินค้าแบบเลือกตามหมวดหมู่
def Fetch_Products_By_Category(category):
    conn = connect_db()
    try:
        if category == "All":
            sql = """SELECT id, name, price, stock, category, image_path, description
                     FROM products ORDER BY id DESC"""
            return conn.execute(sql).fetchall()
        else:
            sql = """SELECT id, name, price, stock, category, image_path, description
                     FROM products WHERE category = ? ORDER BY id DESC"""
            return conn.execute(sql, (category,)).fetchall()
    finally:
        conn.close()

# คืนค่ารายละเอียดสินค้าโดยใช้รหัสสินค้า ไว้สำหรับเวลาเราจะดูสินค้า 1 ชิ้นแบบเจาะจง เช่นตอนกดปุ่ม edit product ใน admin
def Fetch_Product_By_ID(pid: int):
    conn = connect_db()
    try:
        row = conn.execute(
            """SELECT id, name, price, stock, category, image_path, description
               FROM products WHERE id = ?""",
            (int(pid),)
        ).fetchone()
        return row  # -> (id, name, price, stock, category, image_path, description) or None
    finally:
        conn.close()

#ดึงข้อมูลผู้ใช้ 1 คนจากตาราง users โดยค้นจาก id
#ใช้เวลาจะโชว์ profile user หรือโหลดข้อมูลก่อนแก้ไข
def Fetch_User_By_ID(uid: int):
    conn = connect_db()
    try:
        cur = conn.cursor()
        row = cur.execute(
            "SELECT id, username, role, gmail, fullname, address, phone FROM users WHERE id=?",
            (int(uid),)
        ).fetchone()
        return row
    finally:
        conn.close()

#อัปเดตข้อมูลติดต่อของผู้ใช้ (gmail, address, phone) ตาม user_id
#ใช้เมื่อ user แก้ไขข้อมูลส่วนตัวในหน้า Profile
def Update_User_Contacts(uid: int, gmail: str, address: str, phone: str, fullname: str):
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET gmail=?, address=?, phone=?, fullname=? WHERE id=?",
            (gmail, address, phone, fullname, int(uid))
        )
        conn.commit()
        # อย่าใช้ total_changes เป็นเงื่อนไขตัดสิน (จะเป็น 0 หากค่าที่ส่งมาเท่าเดิมเป๊ะ)
        return True
    finally:
        conn.close()

#ฟังก์ชันเปลี่ยนรหัสผ่าน ของหน้า profile page
def Update_User_Password(uid: int, old_pw: str, new_pw: str):
    conn = connect_db()
    try:
        row = conn.execute("SELECT password FROM users WHERE id=?", (int(uid),)).fetchone()
        if not row:
            return (False, "บัญชีผู้ใช้ไม่พบ")
        if row[0] != old_pw:
            return (False, "รหัสผ่านเดิมไม่ถูกต้อง")
        if len(new_pw) < 8:
            return (False, "รหัสผ่านใหม่ต้องอย่างน้อย 8 ตัว")
        if not re.search(r"[A-Za-z]",new_pw) or not re.search(r"\d",new_pw ):
            return (False, "รหัสผ่านใหม่ต้องอย่างน้อย 1 ตัวอักษร และ 1 ตัวเลข")
        conn.execute("UPDATE users SET password=? WHERE id=?", (new_pw, int(uid)))
        conn.commit()
        return (True, "เปลี่ยนรหัสผ่านสำเร็จ")
    finally:
        conn.close()
                
def _ensure_users_path_column(cur: sqlite3.Cursor) -> None:
    # ตรวจสอบว่าตาราง users มีคอลัมน์ path แล้วหรือยัง ถ้าไม่มีก็เพิ่มให้
    cur.execute("PRAGMA table_info(users);")
    cols = [c[1] for c in cur.fetchall()]
    if "path" not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN path TEXT;")

#ฟังก์ชันนี้เอาไว้ อัปเดตรูปโปรไฟล์ของ user ใช้ตอน user เปลี่ยนรูป profile ในหน้าโปรไฟล์ 
def Update_User_Avatar(user_id: int, path: str) -> bool:
    if not path:
        return False
    try:
        abs_path = os.path.abspath(path)
        conn = connect_db()
        cur = conn.cursor()
        # กันกรณีฐานข้อมูลเก่ายังไม่มีคอลัมน์ path
        _ensure_users_path_column(cur)
        cur.execute("UPDATE users SET path = ? WHERE id = ?", (abs_path, user_id))
        conn.commit()
        # rowcount = 0 หมายถึงไม่พบ user_id
        return cur.rowcount > 0
    except Exception as e:
        # log ตามต้องการ เช่น print(e) หรือเขียนลงไฟล์
        return False
    finally:
        try:
            conn.close()
        except Exception:
            pass
#ฟังก์ชันนี้ใช้ ดึง path ของรูปโปรไฟล์ของ user จาก database ใช้ตอนเปิดหน้า profile เพื่อนำ path ไปเปิดแสดงผลในหน้าโปรไฟล์
def Fetch_User_Avatar_Path(user_id: int) -> Optional[str]:
    try:
        conn = connect_db()
        cur = conn.cursor()
        # กันกรณีฐานข้อมูลเก่ายังไม่มีคอลัมน์ path
        _ensure_users_path_column(cur)
        cur.execute("SELECT path FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        avatar_path = row[0]
        if not avatar_path:
            return None
        # แปลงเป็น absolute เผื่อมีการย้าย working dir
        return os.path.abspath(avatar_path)
    except Exception as e:
        # log ตามต้องการ
        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass

# === NEW: Order DB helpers ===
#ใช้สำหรับ สร้างออเดอร์ใหม่ แล้วบันทึกลงตาราง orders
def Create_Order(user_id:int, total:int, address_snapshot:str=None, path_slip:str=None,
                 status:str="PENDING", shipping_fee:int=0):
    conn = connect_db()
    try:
        ensure_order_schema()  # กันไว้ก่อน เผื่อ DB เก่ายังไม่มีคอลัมน์ใหม่
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (user_id, total, address_snapshot, path_slip, status, shipping_fee)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, int(total), address_snapshot, path_slip, status, int(shipping_fee)))
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        print("Create_Order error:", e)
        return None
    finally:
        conn.close()

ensure_order_schema() 
#ฟังก์ชันนี้ใช้เพื่อ อัปเดต path รูปสลิปการโอนเงินของ order นั้นๆ ตอน user upload slip → จะเอา path ไปเก็บไว้ใน column path_slip ของ order
def Update_Order_Slip(order_id: int, slip_path: str):
    conn = connect_db()
    try:
        conn.execute("UPDATE orders SET path_slip=? WHERE id=?", (slip_path, int(order_id)))
        conn.commit()
        return True
    finally:
        conn.close()

#ฟังก์ชันนี้ใช้ เปลี่ยนสถานะของออเดอร์
def Update_Order_Status(order_id: int, new_status: str, cancel_reason: Optional[str]=None):
    conn = connect_db()
    try:
        if new_status == "CANCELLED":
            conn.execute("UPDATE orders SET status=?, cancel_reason=? WHERE id=?", (new_status, cancel_reason, int(order_id)))
        else:
            conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, int(order_id)))
        conn.commit()
        return True
    finally:
        conn.close()

#ใช้ดึงรายการออเดอร์ของ user คนนั้นทั้งหมด เพื่อไปแสดงในหน้า "Order History" ของ user เรียงจาก order ล่าสุด → order เก่า
def Fetch_Orders_By_User(user_id: int):
    conn = connect_db()
    try:
        rows = conn.execute("""
            SELECT id, order_date, status, total, address_snapshot, path_slip, cancel_reason
            FROM orders WHERE user_id=?
            ORDER BY id DESC
        """, (int(user_id),)).fetchall()
        return rows
    finally:
        conn.close()

#ฟังก์ชันนี้ใช้ ดึงสินค้าแต่ละรายการภายในออเดอร์หนึ่งออเดอร์ แต่รองรับได้หลายรูปแบบ DB (เผื่อ DB รุ่นเก่า รุ่นใหม่)
#ใช้ตอนแสดง detail order ในหน้า Order / Admin
def Fetch_Order_Items(order_id: int):
    conn = connect_db()
    cur = conn.cursor()
    try:
        # ตรวจว่ามีคอลัมน์ product_name / unit_price หรือไม่
        cur.execute("PRAGMA table_info(order_items)")
        cols = {c[1] for c in cur.fetchall()}
        has_pname = "product_name" in cols
        has_pid   = "product_id" in cols
        has_price = "unit_price" in cols

        if has_pname and has_price:
            # เคสเก่า: เก็บชื่อกับราคาไว้ใน order_items อยู่แล้ว
            cur.execute("""
                SELECT product_name, qty, unit_price
                FROM order_items
                WHERE order_id = ?
                ORDER BY id ASC
            """, (order_id,))
            rows = cur.fetchall()
            # บังคับชนิด
            return [(str(n or ""), int(q), int(p)) for (n, q, p) in rows]

        # เคสใหม่: ใช้ product_id แล้วต้อง join products เพื่อเอาชื่อ
        # พยายามเดาราคา:
        #   1) ถ้ามี unit_price ใน order_items ใช้ค่านั้น
        #   2) ไม่มีก็ fallback ไปใช้ products.price
        if has_pid:
            if has_price:
                cur.execute("""
                    SELECT COALESCE(oi.product_name, p.name) AS name,
                           oi.qty,
                           COALESCE(oi.unit_price, p.price) AS price
                    FROM order_items oi
                    LEFT JOIN products p ON p.id = oi.product_id
                    WHERE oi.order_id = ?
                    ORDER BY oi.id ASC
                """, (order_id,))
            else:
                cur.execute("""
                    SELECT COALESCE(oi.product_name, p.name) AS name,
                           oi.qty,
                           p.price AS price
                    FROM order_items oi
                    LEFT JOIN products p ON p.id = oi.product_id
                    WHERE oi.order_id = ?
                    ORDER BY oi.id ASC
                """, (order_id,))
            rows = cur.fetchall()
            return [(str(n or ""), int(q), int(p)) for (n, q, p) in rows]

        # ถ้ายังไม่เข้าเคสไหนเลย ให้ลอง select ที่เบาที่สุด
        cur.execute("""
            SELECT product_name, qty, unit_price
            FROM order_items
            WHERE order_id = ?
            ORDER BY id ASC
        """, (order_id,))
        rows = cur.fetchall()
        return [(str(n or ""), int(q), int(p or 0)) for (n, q, p) in rows]
    finally:
        conn.close()

#เหมือนด้านบนแต่ใช้ตอนออกใบเสร็จ PDF (เอาไว้คำนวณราคาหลังหักส่วนลด)
def Fetch_Order_Items_Detail(order_id: int):
    """
    คืนลิสต์ [(name, qty, unit_price, discount_per_unit)]
    ใช้ในใบเสร็จ: ราคาต่อชิ้น (หลังหักส่วนลด) = max(unit_price - discount_per_unit, 0)
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(order_items)")
        cols = {c[1] for c in cur.fetchall()}
        has_disc = "discount_per_unit" in cols

        if has_disc:
            sql = """
                SELECT product_name, qty, unit_price, COALESCE(discount_per_unit, 0)
                FROM order_items
                WHERE order_id = ?
                ORDER BY id ASC
            """
        else:
            sql = """
                SELECT product_name, qty, unit_price, 0 AS discount_per_unit
                FROM order_items
                WHERE order_id = ?
                ORDER BY id ASC
            """
        cur.execute(sql, (order_id,))
        rows = cur.fetchall()
        return [(str(n or ""), int(q), int(p or 0), int(d or 0)) for (n, q, p, d) in rows]
    finally:
        conn.close()

#ฟังก์ชันนี้ใช้ ดึงออเดอร์ทั้งหมดในระบบ (ฝั่ง Admin) ดึง order จากหลาย user และ join กับ users เพื่อดึง username มาด้วย เรียงจาก order ใหม่สุดไป order เก่าสุด
def Fetch_All_Orders():
    conn = connect_db()
    try:
        rows = conn.execute("""
            SELECT o.id, o.order_date, u.username, o.status, o.total, o.address_snapshot, o.path_slip
            FROM orders o
            JOIN users u ON u.id = o.user_id
            ORDER BY o.id DESC
        """).fetchall()
        return rows
    finally:
        conn.close()

#
def Approve_Order_and_Log(order_id: int) -> None:
    """
    ยืนยันออเดอร์:
      - กันยืนยันซ้ำ (ถ้าเป็น CANCELLED/CONFIRMED จะ raise)
      - ดึง order_items ของออเดอร์นี้
      - ตัดสต็อกสินค้า (ไม่ต่ำกว่า 0)
      - บันทึกลง sales_log (หนึ่งแถวต่อสินค้าหนึ่งรายการ)
      - อัปเดตสถานะ orders.status = 'CONFIRMED'
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        # ตรวจสถานะปัจจุบันก่อน
        cur.execute("SELECT status FROM orders WHERE id=?", (order_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"ไม่พบออเดอร์ #{order_id}")
        status = (row[0] or "").upper()
        if status == "CONFIRMED":
            raise ValueError(f"ออเดอร์ #{order_id} ถูกยืนยันไปแล้ว")
        if status == "CANCELLED":
            raise ValueError(f"ออเดอร์ #{order_id} ถูกยกเลิกแล้ว")

        # ดึงรายการสินค้าในออเดอร์
        cur.execute("""
            SELECT product_name, qty, unit_price
            FROM order_items
            WHERE order_id=?
            ORDER BY id ASC
        """, (order_id,))
        items = cur.fetchall()

        # สำหรับแต่ละรายการ: หา product.id เพื่อตัดสต็อก + log
        for (name, qty, unit_price) in items:
            qty = int(qty); unit_price = int(unit_price)

            cur.execute("SELECT id, stock FROM products WHERE name=? LIMIT 1", (name,))
            prod = cur.fetchone()
            if prod:
                pid, stock = prod
                new_stock = max(0, int(stock) - qty)
                cur.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, pid))
            else:
                pid = 0  # กันกรณีของเก่าไม่มีในตาราง products

            cur.execute("""
                INSERT INTO sales_log
                    (order_id, product_id, product_name, qty, unit_price, total_price, confirmed_at)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now','localtime'))
            """, (order_id, pid, name, qty, unit_price, qty*unit_price))

        # ปิดท้ายด้วยการอัปเดตสถานะออเดอร์
        cur.execute("UPDATE orders SET status='CONFIRMED' WHERE id=?", (order_id,))

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def Query_Top_Selling(by: str, year: int, month: int | None = None, day: int | None = None):
    """
    คืนลิสต์ [(product_name, sum_qty, sum_revenue)]
      by: "day" | "month" | "year"
      - day   -> ต้องมี year, month, day
      - month -> ต้องมี year, month
      - year  -> ต้องมี year
    อ้างอิงเวลาจาก sales_log.confirmed_at (TEXT, strftime ได้)
    """
    by = (by or "").lower()
    y = f"{int(year):04d}"

    conn = connect_db()
    cur = conn.cursor()
    try:
        if by == "day":
            if month is None or day is None:
                raise ValueError("โหมด 'day' ต้องระบุ month และ day ด้วย")
            m = f"{int(month):02d}"
            d = f"{int(day):02d}"
            cur.execute("""
                SELECT product_name, SUM(qty) AS total_qty, SUM(total_price) AS revenue
                FROM sales_log
                WHERE strftime('%Y', confirmed_at)=? AND strftime('%m', confirmed_at)=? AND strftime('%d', confirmed_at)=?
                GROUP BY product_id, product_name
                ORDER BY total_qty DESC, revenue DESC
            """, (y, m, d))

        elif by == "month":
            if month is None:
                raise ValueError("โหมด 'month' ต้องระบุ month ด้วย")
            m = f"{int(month):02d}"
            cur.execute("""
                SELECT product_name, SUM(qty) AS total_qty, SUM(total_price) AS revenue
                FROM sales_log
                WHERE strftime('%Y', confirmed_at)=? AND strftime('%m', confirmed_at)=?
                GROUP BY product_id, product_name
                ORDER BY total_qty DESC, revenue DESC
            """, (y, m))

        else:  # year
            cur.execute("""
                SELECT product_name, SUM(qty) AS total_qty, SUM(total_price) AS revenue
                FROM sales_log
                WHERE strftime('%Y', confirmed_at)=?
                GROUP BY product_id, product_name
                ORDER BY total_qty DESC, revenue DESC
            """, (y,))

        rows = cur.fetchall()
        return rows
    finally:
        conn.close()

def Reject_Order(order_id: int, reason: str = "rejected by admin") -> bool:
    """
    ยกเลิกออเดอร์:
      - อัปเดต orders.status = 'CANCELLED'
      - บันทึกเหตุผลลง cancel_reason
      - (ไม่ restock ย้อนกลับ — ถ้าต้องการให้เติมเพิ่มภายหลัง)
    """
    conn = connect_db()
    cur = conn.cursor()
    try:
        # กันยกเลิกซ้ำ—ไม่บังคับ แต่แจ้งผลลัพธ์ให้เรียบง่าย
        cur.execute("SELECT status FROM orders WHERE id=?", (order_id,))
        row = cur.fetchone()
        if not row:
            return False
        status = (row[0] or "").upper()
        if status == "CANCELLED":
            return True  # ถือว่าสภาพสุดท้ายตรงตามต้องการแล้ว
        if status == "CONFIRMED":
            # ถ้าอยากบล็อกการยกเลิกหลัง confirm ให้ return False / raise ได้
            pass

        cur.execute(
            "UPDATE orders SET status='CANCELLED', cancel_reason=? WHERE id=?",
            (reason, order_id),
        )
        conn.commit()
        return cur.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
#ฟังก์ชันนี้เอาไว้ บันทึกข้อมูลการจ่ายเงินของออเดอร์  id / วันที่จ่าย / วันที่ออกใบเสร็จ
def Set_Order_Payment_Info(order_id: int, txn_id: str | None, paid_date: str | None, issue_date: str | None = None) -> bool:
    """
    paid_date / issue_date ควรเป็นรูปแบบ 'YYYY-MM-DD' หรือ 'YYYY-MM-DD HH:MM:SS'
    """
    conn = connect_db()
    try:
        conn.execute("""
            UPDATE orders
               SET txn_id = ?,
                   paid_date = ?,
                   issue_date = COALESCE(?, issue_date)
             WHERE id = ?
        """, (txn_id, paid_date, issue_date, int(order_id)))
        conn.commit()
        return conn.total_changes > 0
    finally:
        conn.close()

seed_admin_user()

#class HeavenGear คือหน้าต่างหลักของโปรแกรมทั้งหมด และเป็นตัวจัดการระบบสลับหน้า UI ภายในแอป Heaven Gear Shop
class HeavenGear(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game Gear")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.cart = CartModel()
        self.current_user_id = None
        self.current_user_role = "guest"
        
        # Screen dimensions
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Create container for switching pages
        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #เมื่อเปิดโปรแกรมขึ้นมา มันจะสร้างทุกหน้าเอาไว้ล่วงหน้า Login, Register, Admin, Cart, Profile, Payment, Order page 
        #แล้วเก็บไว้ในตัวแปร frames จากนั้นเวลาจะสลับหน้าใดหน้าใด จะเรียกฟังก์ชัน show_frame() เพื่อดึงหน้าเป้าหมายขึ้นมาแสดง
        for F in (main_menu, LoginPage, RegisterPage, AdminPage,CartPage, SearchPage,ProfilePage,PaymentPage,Order_Page):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(main_menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()   
        if hasattr(frame, "on_show"):
            frame.on_show()

# ---------- Cart Model ----------
#class CartModel คือตัวจัดการข้อมูลตะกร้าสินค้าในโปรแกรมทั้งหมด
class CartModel:
    def __init__(self):
        # {"id": int, "name": str, "price": int, "qty": int, "image": str, "selected": bool, "max_stock": Optional[int]}
        self.items = []
        self._next_id = 1

    @staticmethod
    #แปลง string ราคาให้เป็นตัวเลข
    def parse_price(s: str) -> int:
        return int(''.join(ch for ch in str(s) if ch.isdigit()))

    @staticmethod
    #จัดรูปแบบตัวเลขให้มี comma
    def fmt_price(n: int) -> str:
        return f"{n:,}"
    #เพิ่มสินค้าเข้า cart 
    #ถ้ามีสินค้าแบบเดียวกันในตะกร้าอยู่แล้ว → เพิ่มจำนวนแทนและไม่ให้จำนวนเกิน max_stock 
    def add_item(self, name: str, price_any, image_path: str, qty: int = 1, max_stock: int | None = None):
        price = price_any if isinstance(price_any, int) else self.parse_price(price_any)
        for it in self.items:
            if it["name"] == name and it["image"] == image_path and it["price"] == price:
                # อัปเดต max_stock ให้แคบสุด (กันข้อมูลเก่ากว้างกว่า)
                if max_stock is not None:
                    it["max_stock"] = max_stock if it.get("max_stock") is None else min(it["max_stock"], max_stock)
                # บวกจำนวนแล้ว “คงที่ไม่ให้เกินสต็อก”
                limit = it.get("max_stock")
                if limit is not None:
                    it["qty"] = min(limit, it["qty"] + qty)
                else:
                    it["qty"] += qty
                return it["id"]
        item = {
            "id": self._next_id,
            "name": name,
            "price": price,
            "qty": max(1, min(qty, max_stock)) if isinstance(max_stock, int) else max(1, qty),
            "image": image_path,
            "selected": True,
            "max_stock": max_stock if isinstance(max_stock, int) else None
        }
        self.items.append(item)
        self._next_id += 1
        return item["id"]
    
    #ลบสินค้า 1 ชิ้นออกจาก cart ตาม id
    def remove(self, item_id: int):
        self.items = [it for it in self.items if it["id"] != item_id]

    #ตั้งจำนวนสินค้าเป็นจำนวนใหม่ แต่ถ้ามี max_stock ก็จะไม่ให้เกิน
    def set_qty(self, item_id: int, qty: int):
        for it in self.items:
            if it["id"] == item_id:
                if it.get("max_stock") is not None:
                    it["qty"] = max(1, min(qty, it["max_stock"]))
                else:
                    it["qty"] = max(1, qty)
                break

    #เพิ่ม/ลดจำนวนสินค้า (ใช้ตอนกดปุ่ม + / -)
    def add_qty(self, item_id: int, delta: int):
        for it in self.items:
            if it["id"] == item_id:
                newq = it["qty"] + delta
                if it.get("max_stock") is not None:
                    it["qty"] = max(1, min(newq, it["max_stock"]))
                else:
                    it["qty"] = max(1, newq)
                break

    #กำหนดว่าสินค้านี้ “เลือกไว้คิดเงิน” หรือไม่ (True/False)
    def set_selected(self, item_id: int, selected: bool):
        for it in self.items:
            if it["id"] == item_id:
                it["selected"] = selected
                break

    #คำนวณราคารวมของสินค้าชิ้นเดียว            
    def line_total(self, item_id: int) -> int:
        for it in self.items:
            if it["id"] == item_id:
                return it["price"] * it["qty"]
        return 0

    #เลือกสินค้าทุกชิ้นในตะกร้า หรือเอาทุกชิ้นออก
    def select_all(self, selected: bool):
        for it in self.items:
            it["selected"] = selected

    #คำนวณ “ยอดรวมทั้งหมด” ของสินค้าที่ถูกเลือกอยู่
    def total_selected(self) -> int:
        return sum(it["price"] * it["qty"] for it in self.items if it["selected"])

    #เช็คว่าสินค้าทั้งหมดในตะกร้าถูกเลือกทั้งหมดหรือไม่
    def all_selected(self) -> bool:
        return len(self.items) > 0 and all(it["selected"] for it in self.items)

#====== widgest Show promotion in Main Menu ======
class ImageCarousel(customtkinter.CTkFrame):
    def __init__(self, parent, image_paths=None, width=1200, height=450,interval_ms=18000, autoplay=True, fit_mode="cover"):
        super().__init__(parent, width=width, height=height)
        self.IMG_WIDTH, self.IMG_HEIGHT = width, height
        self.interval_ms, self.autoplay = interval_ms, autoplay
        self.fit_mode = fit_mode  # "cover" | "contain" | "fill"
        self._pil_images, self._ctk_image, self.index, self.after_id = [], None, 0, None

        self.image_label = customtkinter.CTkLabel(self, text="", width=self.IMG_WIDTH, height=self.IMG_HEIGHT)
        self.image_label.pack(fill="both", expand=True)
        self.set_images(image_paths or [])

    def set_images(self, paths):
        self._stop_timer()
        self._pil_images = [Image.open(p).convert("RGBA") for p in paths]
        self.index = 0
        self._render_current()
        if self.autoplay and len(self._pil_images) > 1: self._schedule_next()

    def next(self):
        if not self._pil_images: return
        self.index = (self.index + 1) % len(self._pil_images)
        self._render_current(True)

    def _schedule_next(self):
        self._stop_timer()
        if self.autoplay and len(self._pil_images) > 1:
            self.after_id = self.after(self.interval_ms, self.next)

    def _stop_timer(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def _render_current(self, reset_timer=False):
        if not self._pil_images:
            self.image_label.configure(text="(ไม่มีรูปภาพ)", image=None)
            return
        pil_original = self._pil_images[self.index]
        self._ctk_image = customtkinter.CTkImage(light_image=pil_original, dark_image=pil_original,size=(self.IMG_WIDTH, self.IMG_HEIGHT))
        self.image_label.configure(image=self._ctk_image, text="")
        if reset_timer and self.autoplay: self._schedule_next()

# ====== Product Card Widget ========
class ProductCard(customtkinter.CTkFrame):
    def __init__(self, parent, product_id, name, price, stock, category, image_path, description, on_add=None):
        # ขนาดคงที่
        super().__init__(parent, fg_color="white", corner_radius=15, width=238, height=320)
        self.grid_propagate(False)  # >>> เพิ่มบรรทัดนี้ เพื่อให้ width/height บังคับใช้
        self.product_id = product_id
        self.on_add = on_add
        # รูปภาพสินค้า
        self.thumb_img = self._make_image(image_path, (90, 90))
        # layout ภายใน
        self.grid_columnconfigure(0, weight=1)
        # ให้แถว 4 เป็นสเปเซอร์ (ดันปุ่มไปก้นการ์ด)
        self.grid_rowconfigure(4, weight=1)
        
        self.img_label = customtkinter.CTkLabel(self, image=self.thumb_img, text="")
        self.img_label.grid(row=0, column=0, padx=10, pady=(12, 6), sticky="n")

        self.name_label = customtkinter.CTkLabel(self, text=name,text_color="#111111", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.name_label.grid(row=1, column=0, padx=10, pady=(0, 4))

        self.price_label = customtkinter.CTkLabel(self, text=f"{CartModel.fmt_price(price)} ฿",text_color="#444444", font=customtkinter.CTkFont(size=13))
        self.price_label.grid(row=2, column=0, padx=10, pady=(0, 2))

        self.stock_label = customtkinter.CTkLabel(self, text=f"Stock: {stock}",text_color="#777777", font=customtkinter.CTkFont(size=12))
        self.stock_label.grid(row=3, column=0, padx=10, pady=(0, 8))

        self.Add_button = customtkinter.CTkButton(self, text="หยิบใส่ตะกร้า", width=120, height=28,hover_color="false", text_color="#FFFFFF", corner_radius=8
                                                  ,command=self._on_add_clicked)
        
        self.Add_button.grid(row=4, column=0, padx=10, pady=(0, 12))

        # คลิกการ์ด/รูป/ข้อความ เพื่อเปิดรายละเอียด
        self.configure(cursor="hand2")
        self.bind("<Button-1>", self._open_detail_dialog)
        for w in (self.img_label, self.name_label, self.price_label, self.stock_label):
            w.bind("<Button-1>", self._open_detail_dialog)

    def _make_image(self,path: str, size=(72, 72)):
        try:
            if path and os.path.exists(path):
                im = Image.open(path).convert("RGBA")
            else:
                raise FileNotFoundError
        except Exception:
            im = Image.new("RGBA", size, (230, 230, 230, 255))  # placeholder เทา
        return customtkinter.CTkImage(im, size=size)

    def _on_add_clicked(self):
        if self.on_add:
            self.on_add()
        else:
            CTkMessagebox(title="Info", message="ยังไม่ได้กำหนด on_add", icon="info")

    def _open_detail_dialog(self, *_):
        data = Fetch_Product_By_ID(self.product_id)
        if not data:
            CTkMessagebox(title="ไม่พบสินค้า", message="ไม่พบสินค้านี้ในฐานข้อมูล", icon="warning")
            return

        pid, name, price, stock, category, img_path, desc = data

        self.Top = customtkinter.CTkToplevel(self)
        top = self.Top
        top.title(name)
        top.geometry("1200x600")
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        top.attributes("-topmost", True)
        top._after_ids = set()

        def drop_topmost():
            if top.winfo_exists():
                try:
                    top.attributes("-topmost", False)
                except Exception:
                    pass
        job = top.after(100, drop_topmost)
        top._after_ids.add(job)

        def on_close():
            if hasattr(top, "_after_ids"):
                for aid in list(top._after_ids):
                    try:
                        top.after_cancel(aid)
                    except Exception:
                        pass
                top._after_ids.clear()
            try:
                top.destroy()
            except Exception:
                pass
        top.protocol("WM_DELETE_WINDOW", on_close)

        # ===== ใช้เลย์เอาต์ชุดเดียว =====
        Frame_Body = customtkinter.CTkFrame(top, fg_color="#FFFFFF", corner_radius=16)
        Frame_Body.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        Frame_Body.grid_columnconfigure(0, weight=0)
        Frame_Body.grid_columnconfigure(1, weight=1)
        Frame_Body.grid_rowconfigure(0, weight=1)

        big_img = self._make_image(img_path, (300, 300))
        Img_Label = customtkinter.CTkLabel(Frame_Body, image=big_img, text="")
        Img_Label.image = big_img
        Img_Label.grid(row=0, column=0, padx=16, pady=16, sticky="n")

        Frame_Info = customtkinter.CTkFrame(Frame_Body, fg_color="transparent")
        Frame_Info.grid(row=0, column=1, padx=12, pady=16, sticky="nsew")
        Frame_Info.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(Frame_Info, text=name, text_color="#000000",
                                font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))

        customtkinter.CTkLabel(Frame_Info, text=f"หมวดหมู่: {category}", text_color="#666666",
                                font=customtkinter.CTkFont(size=13)).grid(row=1, column=0, sticky="w")

        customtkinter.CTkLabel(Frame_Info, text=f"ราคา {CartModel.fmt_price(price)} ฿", text_color="#000000",
                                font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=2, column=0, sticky="w", pady=(8, 4))

        Desc_Box = customtkinter.CTkTextbox(Frame_Info, height=220, width=450, wrap="word")
        Desc_Box.insert("1.0", desc or "-")
        Desc_Box.configure(state="disabled")
        Desc_Box.grid(row=3, column=0, sticky="nsew", pady=(8, 8))
        Frame_Info.grid_rowconfigure(3, weight=1)  # ให้กล่องคำอธิบายยืดได้

        Action_Row = customtkinter.CTkFrame(Frame_Info, fg_color="transparent")
        Action_Row.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        # จัดคอลัมน์: 0=ปรับจำนวน | 1=spacer(ยืด) | 2=หยิบใส่ตะกร้า | 3=ปิด
        Action_Row.grid_columnconfigure(0, weight=0)
        Action_Row.grid_columnconfigure(1, weight=1)  # spacer
        Action_Row.grid_columnconfigure(2, weight=0)
        Action_Row.grid_columnconfigure(3, weight=0)

        # กล่องปรับจำนวน (ซ้าย)
        qty_frame = customtkinter.CTkFrame(Action_Row, fg_color="transparent")
        qty_frame.grid(row=0, column=0, sticky="w")
        qty_var = customtkinter.IntVar(value=1)
        def decrease_qty():
            if qty_var.get() > 1:
                qty_var.set(qty_var.get() - 1)

        def increase_qty():
            if qty_var.get() < int(stock):
                qty_var.set(qty_var.get() + 1)

        customtkinter.CTkButton(qty_frame, text="-", width=36, height=30,fg_color="#E0E0E0", text_color="#000000", hover_color="#CCCCCC",command=decrease_qty).pack(side="left", padx=(0, 4))

        customtkinter.CTkLabel(qty_frame, textvariable=qty_var, width=40, height=28,
                                fg_color="#FFFFFF", text_color="#000000", corner_radius=8).pack(side="left")

        customtkinter.CTkButton(qty_frame, text="+", width=36, height=30,fg_color="#E0E0E0", text_color="#000000", hover_color="#CCCCCC",command=increase_qty).pack(side="left", padx=(4, 0))

        # ปุ่มขวา: หยิบใส่ตะกร้า + ปิด
        def add_to_cart_with_qty():
            if self.on_add:
                qty = qty_var.get()
                self.on_add(qty)
                CTkMessagebox(title="เพิ่มลงตะกร้า", message=f"เพิ่ม {name} x{qty} แล้ว", icon="check")
                on_close()

        btn_add = customtkinter.CTkButton(Action_Row, text="หยิบใส่ตะกร้า", width=120, height=32,command=add_to_cart_with_qty)
        btn_add.grid(row=0, column=2, sticky="e", padx=(0, 8))

        btn_close = customtkinter.CTkButton(Action_Row, text="ปิด", width=90, height=32,fg_color="#EEEEEE", text_color="#111111",hover="false",command=on_close)
        btn_close.grid(row=0, column=3, sticky="e")
      
# ====== Main Menu Page ========
class main_menu(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------- โครงร่างหลัก ----------
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)

        # =================== Header ===================
        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", bg_color="#bebebe",corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="ew")
        self.Hight_frame.grid_propagate(False)

        for c in range(6):
            self.Hight_frame.grid_columnconfigure(c, weight=0)
            self.Hight_frame.grid_columnconfigure(2, weight=1)

        # Logo
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        self.button_logo = customtkinter.CTkButton(self.Hight_frame, image=self.logo, text="",width=48, height=35, fg_color="#ffffff",hover_color="#e0e0e0"
                                                   , corner_radius=12,command=lambda: [controller.show_frame(main_menu), self.show_products("All")])
        self.button_logo.grid(row=0, column=0, padx=(16, 8), pady=22, sticky="w")

        # ช่องค้นหา
        spacer = customtkinter.CTkLabel(self.Hight_frame, text="", width=10, fg_color="#ffffff")
        spacer.grid(row=0, column=1, padx=6)

        self.searchbox = customtkinter.CTkEntry(self.Hight_frame, placeholder_text="Search",width=300, height=30, fg_color="#ffffff",bg_color="#ffffff", border_width=2
                                                ,border_color="#000000", corner_radius=15)
        self.searchbox.grid(row=0, column=2, padx=4, pady=22, sticky="e")

        self.search_image = r"D:\python porgramming\project\JPG\Screenshot 2025-09-25 103736.png"
        self.search_button_img = customtkinter.CTkImage(Image.open(self.search_image), size=(20, 20))
        self.search_button = customtkinter.CTkButton(self.Hight_frame, image=self.search_button_img, text="",width=36, height=30
                                                     , fg_color="#ffffff",hover_color="#e0e0e0", corner_radius=12,command=self.go_search)
        self.search_button.grid(row=0, column=3, padx=5, pady=20, sticky="e")

        # Cart
        self.cart_image_path = r"D:\python porgramming\project\JPG\Screenshot 2025-09-25 110705.png"
        self.cart_image = customtkinter.CTkImage(Image.open(self.cart_image_path), size=(24, 24))
        self.cart_button = customtkinter.CTkButton(self.Hight_frame, image=self.cart_image, text="",width=36, height=30, fg_color="#ffffff"
                                                   ,hover_color="#e0e0e0", corner_radius=12,command=lambda: controller.show_frame(CartPage))
        self.cart_button.grid(row=0, column=4, padx=6, pady=22, sticky="e")

        # ปุ่มควบคุม User (ตอนแรกเป็น Sign In)
        self.btn_user_control = customtkinter.CTkButton(self.Hight_frame,text="Sign In",width=36, height=30,fg_color="#00B7FF", hover_color="#0096D6"
                                                        ,text_color="#000000",corner_radius=16,command=lambda: self.controller.show_frame(LoginPage))
        self.btn_user_control.grid(row=0, column=5, padx=(6, 16), pady=22, sticky="e")

        self.user_menu = None
        self.update_header()

        # =================== Low Fame ===================
        self.Low_frame = customtkinter.CTkScrollableFrame(self, fg_color="#e0e0e0",bg_color="#e0e0e0", corner_radius=0)
        self.Low_frame.grid(row=1, column=0, sticky="nsew")
        self.Low_frame._parent_canvas.configure(bg="#f3f3f3", highlightthickness=0)
        
        # ปรับสี scrollbar
        if hasattr(self.Low_frame, "_scrollbar"):self.Low_frame._scrollbar.configure(fg_color="#e0e0e0")

        # สไลด์โชว์
        image_paths = [r"D:\python porgramming\project\Promote\welcome.png" ,r"D:\python porgramming\project\Promote\Future_Noir.png"] 
        carousel = ImageCarousel(self.Low_frame, image_paths=image_paths, interval_ms=2500, autoplay=True)
        carousel.pack(padx=16, pady=16)

        # ===== ปุ่มหมวดหมู่ =====
        self.category_frame = customtkinter.CTkFrame(self.Low_frame, fg_color="transparent")
        self.category_frame.pack(pady=20)

        BTN_W, BTN_H = 120, 120
        ICON_SIZE = (48, 48)

        # Monitor
        self.morniter_image = r"D:\python porgramming\project\JPG\Mornitor icon.jpg"
        self.morniter_img = customtkinter.CTkImage(Image.open(self.morniter_image), size=ICON_SIZE)
        self.morniter_button = customtkinter.CTkButton(self.category_frame, image=self.morniter_img, text="Monitor",width=BTN_W, height=BTN_H
                                                       ,fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000"
                                                       ,compound="top",command=lambda: self.show_products("Monitor"))
        self.morniter_button.pack(side="left", padx=20)

        # Keyboard
        self.Keyboard_image = r"D:\python porgramming\project\JPG\Keyboard icon.jpg"
        self.Keyboard_img = customtkinter.CTkImage(Image.open(self.Keyboard_image), size=ICON_SIZE)
        self.Keyboard_button = customtkinter.CTkButton(self.category_frame, image=self.Keyboard_img, text="Keyboard",width=BTN_W, height=BTN_H
                                                       ,fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000",compound="top"
                                                       ,command=lambda: self.show_products("Keyboard"))
        self.Keyboard_button.pack(side="left", padx=20)

        # Mouse
        self.Mouse_image = r"D:\python porgramming\project\JPG\Mouse icon.jpg"
        self.Mouse_img = customtkinter.CTkImage(Image.open(self.Mouse_image), size=ICON_SIZE)
        self.Mouse_button = customtkinter.CTkButton(self.category_frame, image=self.Mouse_img, text="Mouse",width=BTN_W, height=BTN_H
                                                    ,fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000",compound="top"
                                                    ,command=lambda: self.show_products("Mouse"))
        self.Mouse_button.pack(side="left", padx=20)

        # Mousepad
        self.Mousepad_image = r"D:\python porgramming\project\JPG\Mouse pad icon.jpg"
        self.Mousepad_img = customtkinter.CTkImage(Image.open(self.Mousepad_image), size=ICON_SIZE)
        self.Mousepad_button = customtkinter.CTkButton(self.category_frame, image=self.Mousepad_img, text="Mousepad",width=BTN_W, height=BTN_H
                                                       ,fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000", compound="top"
                                                       ,command=lambda: self.show_products("Mousepad"))
        self.Mousepad_button.pack(side="left", padx=20)

        # Headphone
        self.Headphone_image = r"D:\python porgramming\project\JPG\Head phone icon.webp"
        self.Headphone_img = customtkinter.CTkImage(Image.open(self.Headphone_image), size=ICON_SIZE)
        self.Headphone_button = customtkinter.CTkButton(self.category_frame, image=self.Headphone_img, text="Headphone",width=BTN_W, height=BTN_H
                                                        , fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000", compound="top"
                                                        , command=lambda: self.show_products("Headphone"))
        self.Headphone_button.pack(side="left", padx=20)

        # Microphone
        self.Microphone_image = r"D:\python porgramming\project\JPG\microphon icon.jpg"
        self.Microphone_img = customtkinter.CTkImage(Image.open(self.Microphone_image), size=ICON_SIZE)
        self.Microphone_button = customtkinter.CTkButton(self.category_frame, image=self.Microphone_img, text="Microphone",width=BTN_W, height=BTN_H
                                                         ,fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000", compound="top"
                                                         ,command=lambda: self.show_products("Microphone"))
        self.Microphone_button.pack(side="left", padx=20)

        # Controller
        self.Controller_image = r"D:\python porgramming\project\JPG\Controller.webp"
        self.Controller_img = customtkinter.CTkImage(Image.open(self.Controller_image), size=ICON_SIZE)
        self.Controller_button = customtkinter.CTkButton(self.category_frame, image=self.Controller_img, text="Controller",width=BTN_W, height=BTN_H
                                                        , fg_color="white", hover_color="#f0f0f0",corner_radius=40, text_color="#000000", compound="top"
                                                        , command=lambda: self.show_products("Controller"))
        self.Controller_button.pack(side="left", padx=20)

        self.section_container = customtkinter.CTkFrame(self.Low_frame, fg_color="transparent")
        self.section_container.pack(fill="x", padx=16, pady=(10, 24))

        # ======= SECTION สินค้า (มีฉากหลัง) =======
        # เฟรมฉากหลัง
        self.products_bg = customtkinter.CTkFrame(self.section_container, fg_color="#f3f3f3",corner_radius=18, height=260)
        self.products_bg.pack(fill="x", padx=50)
        self.products_bg.pack_propagate(False)

        self.show_products("All")

    # =================== ไอคอนโปรไฟล์ (สำรอง) + cache ===================
        self.default_profile_icon_path = r"D:\python porgramming\project\JPG\247319.png"  # ใช้เป็นรูปสำรอง
        self._profile_ctkimg_cache = None  
    def go_search(self):
        kw = self.searchbox.get().strip()
        # สลับหน้าไป SearchPage แล้วส่งคำค้นเริ่มต้น
        sp = self.controller.frames[SearchPage]
        self.controller.show_frame(SearchPage)
        sp.update_header()
        sp.set_boot_keyword(kw)
    
    # =================== เมธอดอัปเดตเฮดเดอร์ ===================
    def update_header(self):
        role = getattr(self.controller, "current_user_role", "guest")
        uid  = getattr(self.controller, "current_user_id", None)

        if role == "guest" or uid is None:
            self.btn_user_control.configure(text="Sign In", image=None,fg_color="#00B7FF", hover_color="#0096D6", text_color="#000000",
                                            command=lambda: self.controller.show_frame(LoginPage))
        else:
            self.btn_user_control.configure(text="Menu", image=None,fg_color="#00B7FF", hover_color="#0096D6"
                                            , text_color="#000000", command=self.open_user_menu)
            
        
    def open_user_menu(self):
        if self.user_menu is not None and self.user_menu.winfo_exists():
            self.user_menu.destroy()
            self.user_menu = None
            return

        menu = customtkinter.CTkToplevel(self)
        self.user_menu = menu
        menu.overrideredirect(True)
        menu.attributes("-topmost", True)
        menu._after_ids = set()

        bx = self.btn_user_control.winfo_rootx()
        by = self.btn_user_control.winfo_rooty()
        bw = self.btn_user_control.winfo_width()
        bh = self.btn_user_control.winfo_height()

        # --- เช็คสิทธิ์ผู้ใช้ ---
        role = getattr(self.controller, "current_user_role", "guest")
        is_admin = (str(role).lower() == "admin")

        # ปรับความสูงเมนูอัตโนมัติ (มีปุ่มแอดมินก็สูงขึ้น)
        base_h = 240
        extra_h = 44 if is_admin else 0
        mw, mh = 190, base_h + extra_h

        menu.geometry(f"{mw}x{mh}+{bx + bw - mw}+{by + bh + 6}")

        container = customtkinter.CTkFrame(menu, fg_color="#FFFFFF",
                                        corner_radius=14, border_color="#E5E7EB", border_width=1)
        container.pack(padx=8, pady=8, fill="both", expand=True)

        uid = getattr(self.controller, "current_user_id", None)
        u = Fetch_User_By_ID(uid) if uid is not None else None
        uname = (u[1] if u else "User")
        if len(uname) > 14:
            uname = uname[:12] + "…"

        header_box = customtkinter.CTkFrame(container, fg_color="#F5F6F7", corner_radius=10)
        header_box.pack(fill="x", padx=12, pady=(12,8))

        customtkinter.CTkLabel(
            header_box, text=uname,
            font=customtkinter.CTkFont(size=15, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w", padx=10, pady=(8,4))

        # ====== ปุ่มเฉพาะแอดมิน ======
        if is_admin:
            def open_admin():
                self.close_user_menu_safe()
                self.controller.show_frame(AdminPage)
                # ถ้าต้องการให้รีเฟรชทันที (ไม่บังคับ)
                # page = self.controller.frames[AdminPage]
                # page.on_show()

            customtkinter.CTkButton(container, text="Admin Page", width=140, height=36,fg_color="#EAF7EA", hover_color="#D8F0D8", text_color="#0B6B0B",
                                    corner_radius=10, command=open_admin).pack(padx=12, pady=(6, 6))

        # ===== ปุ่มเมนูเดิม =====
        def open_profile():
            self.close_user_menu_safe()
            self.controller.show_frame(ProfilePage)

        def open_myorder():
            self.close_user_menu_safe()
            self.controller.show_frame(Order_Page)

        def logout_user():
            self.controller.current_user_role = "guest"
            self.controller.current_user_id = None
            CTkMessagebox(title="Logged out", message="คุณได้ออกจากระบบแล้ว", icon="info")
            self.close_user_menu_safe()
            self.update_header()

        customtkinter.CTkButton(container, text="Profile", width=140, height=36,fg_color="#EEF6FF", hover_color="#D6EBFF", text_color="#0863C5",
                                corner_radius=10, command=open_profile).pack(padx=12, pady=(6, 6))

        customtkinter.CTkButton(container, text="My Order", width=140, height=36,fg_color="#FFF8E7", hover_color="#FFEDC2", text_color="#D17D00",
                                corner_radius=10, command=open_myorder).pack(padx=12, pady=(6, 6))

        customtkinter.CTkButton(container, text="Sign Out", width=140, height=36,fg_color="#FFF3F3", hover_color="#FFE3E3", text_color="#C81E1E",
                                corner_radius=10, command=logout_user).pack(padx=12, pady=(6, 12))

        def focus_out(_):
            def delayed_check():
                if not menu.winfo_exists():
                    return
                try:
                    if menu.focus_displayof() is None:
                        self.close_user_menu_safe()
                except Exception:
                    self.close_user_menu_safe()
            job = menu.after(50, delayed_check)
            menu._after_ids.add(job)
        menu.bind("<FocusOut>", focus_out)

    # =================== เมธอดปิดเมนูผู้ใช้แบบปลอดภัย ===================
    def close_user_menu_safe(self):
        menu = getattr(self, "user_menu", None)  # <<< เปลี่ยนชื่อให้ตรง
        if not menu or not menu.winfo_exists():
            self.user_menu = None
            return
        if hasattr(menu, "_after_ids"):
            for aid in list(menu._after_ids):
                try:
                    menu.after_cancel(aid)
                except Exception:
                    pass
            menu._after_ids.clear()
        try:
            menu.destroy()
        except Exception:
            pass
        self.user_menu = None
    # =================== เมธอดสลับสินค้า ===================
    def show_products(self, category: str):
    # 1) ไฮไลต์ปุ่ม
        for cat, btn in getattr(self, "category_buttons", {}).items():
            btn.configure(fg_color="#e7f3ff" if cat == category else "white")

        # 2) ล้างการ์ดเก่า
        for child in self.products_bg.winfo_children():
            child.destroy()

        # 3) ดึงข้อมูลจาก DB
        rows = Fetch_Products_By_Category(category)  # -> (id, name, price, stock, category, image_path, description)

        # 4) วางการ์ดสินค้า
        max_cols = 5
        for i, (pid, name, price, stock, cat, img_path, desc) in enumerate(rows):
            def make_on_add(n=name, p=price, img=img_path, stk=stock):
                def _add(qty=1):
                    self.controller.cart.add_item(n, int(p), img or "", qty, max_stock=int(stk))
                return _add
            
            card = ProductCard(self.products_bg,
                                product_id=pid,
                                name=name,
                                price=price,
                                stock=stock,
                                category=cat,
                                image_path=img_path,
                                description=desc,
                                on_add=make_on_add()
                                )
            r, c = divmod(i, max_cols)
            card.grid(row=r, column=c + 1, padx=20, pady=20, sticky="n")
        # 5) ปรับความสูงฉากหลัง
        rows_count = len(rows)
        lines = (rows_count + max_cols - 1) // max_cols if rows_count else 1
        new_height = max(24 + lines * (250 + 20) + 24, 260)
        self.products_bg.configure(height=new_height)     

# ====== Cart Page ========
class CartPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header/Layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="ew")
        self.Hight_frame.grid_propagate(False)
        for i in range(6):
            self.Hight_frame.grid_columnconfigure(i, weight=0)
        self.Hight_frame.grid_columnconfigure(2, weight=1)

        # โลโก้กลับหน้าหลัก
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        self.logo_button=customtkinter.CTkButton(self.Hight_frame, image=self.logo, text="", width=48, height=35,
                                fg_color="#ffffff", hover_color="#e0e0e0", corner_radius=12,
                                command=lambda: self.controller.show_frame(main_menu))
        self.logo_button.grid(row=0, column=0, padx=(16, 8), pady=22, sticky="w")

        # รายการสินค้า
        self.cart_frame = customtkinter.CTkScrollableFrame(self, fg_color="#ffffff", corner_radius=30, width=900, height=550)
        self.cart_frame.grid(row=1, column=0, padx=24, pady=12, sticky="nsew")
        self.cart_frame.grid_columnconfigure(0, weight=1)

        # แถบล่าง
        self.footer = customtkinter.CTkFrame(self, fg_color="#e9f3ff", corner_radius=20, height=70)
        self.footer.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="ew")
        self.footer.grid_propagate(False)
        self.footer.grid_columnconfigure(0, weight=0)
        self.footer.grid_columnconfigure(1, weight=1)
        self.footer.grid_columnconfigure(2, weight=0)

        self.chk_all = customtkinter.CTkCheckBox(self.footer, text="เลือกทั้งหมด", command=self.on_toggle_all)
        self.chk_all.grid(row=0, column=0, padx=16, pady=16)

        self.total_lbl = customtkinter.CTkLabel(self.footer, text="รวม   0",font=customtkinter.CTkFont(size=16, weight="bold"))
        self.total_lbl.grid(row=0, column=1, padx=16, sticky="e")

        self.order_btn = customtkinter.CTkButton(self.footer, text="สั่งสินค้า", width=120, height=36, corner_radius=12,command=lambda: self.controller.show_frame(PaymentPage))
        self.order_btn.grid(row=0, column=2, padx=16)

        # วาดครั้งแรก
        self.render_cart()

    # เรียกเมื่อถูกยกหน้าแสดง
    def on_show(self):
        self.render_cart()

    # ---------- UI helpers ----------
    def clear_cart_ui(self):
        for w in self.cart_frame.winfo_children():
            w.destroy()

    def render_cart(self):
        self.clear_cart_ui()
        app_cart = self.controller.cart
        for it in app_cart.items:
            self._create_row(it)
        self.refresh_footer()
    
    #========== box สินค้าในตะกร้า ============
    def _create_row(self, it):
        # แถวสินค้า
        row = customtkinter.CTkFrame(self.cart_frame, fg_color="#f2f2f2", corner_radius=16)
        row.pack(fill="x", padx=20, pady=10)

        # layout ใหม่: 0=chk, 1=img, 2=name(ยืดได้), 3=กลุ่มขวาทั้งชุด
        for c in range(4):
            row.grid_columnconfigure(c, weight=0)
        row.grid_columnconfigure(2, weight=1)  # ให้ชื่อสินค้ายืด ดันกลุ่มขวาไปชิดขวา

        # checkbox
        chk = customtkinter.CTkCheckBox(row, text="", command=lambda i=it["id"]: self.on_item_check(i))
        chk.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        chk.select() if it["selected"] else chk.deselect()

        # รูปสินค้า
        try:
            img = customtkinter.CTkImage(Image.open(it["image"]), size=(80, 80))
        except Exception:
            img = None
        img_product = customtkinter.CTkLabel(row, image=img, text="")
        img_product.grid(row=0, column=1, padx=10, pady=10)

        # ชื่อสินค้า (อยู่คอลัมน์ที่ยืดได้)
        name_product = customtkinter.CTkLabel(row, text=it["name"], font=customtkinter.CTkFont(size=15, weight="bold"))
        name_product.grid(row=0, column=2, padx=10, sticky="w")

        # ---------- กลุ่มฝั่งขวาทั้งชุด ----------
        right_box = customtkinter.CTkFrame(row, fg_color="transparent")
        right_box.grid(row=0, column=3, padx=6, pady=8, sticky="e")  # ชิดขวาจริง ๆ

        # ราคา/ชิ้น 
        price = customtkinter.CTkLabel(right_box, text=f" ฿{CartModel.fmt_price(it['price'])} / ชิ้น ")
        price.pack(side="left", padx=8)

        # กล่องจำนวน
        box = customtkinter.CTkFrame(right_box, fg_color="#dddddd", corner_radius=10)
        box.pack(side="left", padx=8)

        #ปุ่มเพิ่มจำสินค้า
        button_minus_qulity = customtkinter.CTkButton(box, text="-", width=28, height=24, corner_radius=8,command=lambda i=it["id"]: self.on_qty_delta(i, -1))
        button_minus_qulity.grid(row=0, column=0, padx=2, pady=2)

        #จำนวนสินค้า
        qty_var = customtkinter.StringVar(value=str(it["qty"]))
        qty_entry = customtkinter.CTkEntry(box, width=40, height=24, textvariable=qty_var, justify="center")
        qty_entry.grid(row=0, column=1, padx=2, pady=2)

        #ปุ่มลดจำนวนสินค้า
        button_add_qulity = customtkinter.CTkButton(box, text="+", width=28, height=24, corner_radius=8,command=lambda i=it["id"]: self.on_qty_delta(i, +1))
        button_add_qulity.grid(row=0, column=2, padx=2, pady=2)

        # รวมต่อรายการ
        line_total_lbl = customtkinter.CTkLabel(right_box,text=f" ฿{CartModel.fmt_price(self.controller.cart.line_total(it['id']))}")
        line_total_lbl.pack(side="left", padx=8)

        # ปุ่มลบ
        button_delet_product = customtkinter.CTkButton(right_box, text="ลบ", fg_color="#ffffff", hover_color="#ffeeee", text_color="#D80606"
                                                        ,width=46, command=lambda i=it["id"], r=row: self.on_delete(i, r))
        button_delet_product.pack(side="left", padx=8)

        # อัปเดตเมื่อแก้จำนวนในช่อง
        def on_qty_entry_change(*_):
            try:
                q = int(qty_var.get())
            except ValueError:
                q = it["qty"]

            # สั่งให้โมเดล clamp ตามกติกา max_stock
            self.controller.cart.set_qty(it["id"], q)

            # อ่านค่าจริงที่ถูก clamp แล้วมาอัปเดตจอ
            real = next(i for i in self.controller.cart.items if i["id"] == it["id"])["qty"]
            qty_var.set(str(real))
            line_total_lbl.configure(text=f" ฿{CartModel.fmt_price(self.controller.cart.line_total(it['id']))}")
            self.refresh_footer()

            # ถ้าผู้ใช้กรอกเกินสต็อก ให้แจ้งเตือนครั้งเดียวแบบสุภาพ
            limit = it.get("max_stock")
            if limit is not None and q > limit:
                CTkMessagebox(title="แจ้งเตือน", message=f"จำนวนสูงสุด {limit} ชิ้น (ตามสต็อก)", icon="warning")

        qty_var.trace_add("write", lambda *_: on_qty_entry_change())
        
    # ---------- Actions ----------
    def on_qty_delta(self, item_id: int, delta: int):
        self.controller.cart.add_qty(item_id, delta)
        self.render_cart()

    def on_delete(self, item_id: int, row_widget):
        self.controller.cart.remove(item_id)
        row_widget.destroy()
        self.refresh_footer()

    def on_item_check(self, item_id: int):
        for it in self.controller.cart.items:
            if it["id"] == item_id:
                self.controller.cart.set_selected(item_id, not it["selected"])
                break
        self.refresh_footer()

    def on_toggle_all(self):
        want = not self.controller.cart.all_selected()
        self.controller.cart.select_all(want)
        self.render_cart()

    def refresh_footer(self):
        total = self.controller.cart.total_selected()
        self.total_lbl.configure(text=f"รวม   {CartModel.fmt_price(total)}")
        self.chk_all.select() if self.controller.cart.all_selected() else self.chk_all.deselect()
        self.order_btn.configure(state=("normal" if total > 0 else "disabled"))

#======= payment Page =======
class PaymentPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.slip_path = None

        # Header
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="ew")
        self.Hight_frame.grid_propagate(False)
        for i in range(4):
            self.Hight_frame.grid_columnconfigure(i, weight=0)
        self.Hight_frame.grid_columnconfigure(1, weight=1)

        # โลโก้
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        customtkinter.CTkButton(self.Hight_frame, image=self.logo, text="", width=48, height=35,
            fg_color="#ffffff", hover_color="#e0e0e0", corner_radius=12,
            command=lambda: self.controller.show_frame(main_menu)).grid(row=0, column=0, padx=(16,8), pady=22, sticky="w")

        customtkinter.CTkLabel(self.Hight_frame, text="Payment", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=0, column=1, sticky="w")

        # เนื้อหา: ซ้าย/ขวา
        content = customtkinter.CTkFrame(self, fg_color="#d8d8d8",corner_radius=14)
        content.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=2)  # left
        content.grid_columnconfigure(1, weight=1)  # right

        # ---------- ซ้าย: ที่อยู่ + ใบเสร็จ ----------
        left = customtkinter.CTkFrame(content, fg_color="#ffffff", corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        left.grid_columnconfigure(0, weight=1)

        # ที่อยู่ผู้สั่ง
        self.addr_box = customtkinter.CTkFrame(left, fg_color="#f2f6ff", corner_radius=12)
        self.addr_box.grid(row=0, column=0, padx=16, pady=16, sticky="ew")
        self.addr_title = customtkinter.CTkLabel(self.addr_box, text="ที่อยู่จัดส่ง", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.addr_title.grid(row=0, column=0, sticky="w", padx=12, pady=(10,2))
        self.addr_label = customtkinter.CTkLabel(self.addr_box, text="", justify="left")
        self.addr_label.grid(row=1, column=0, sticky="w", padx=12, pady=(0,10))

        # ใบเสร็จรายการ
        self.receipt = customtkinter.CTkScrollableFrame(left, fg_color="#ffffff", corner_radius=12, height=360)
        self.receipt.grid(row=1, column=0, padx=16, pady=(0,16), sticky="nsew")
        self.receipt.grid_columnconfigure(0, weight=1)

        self.receipt_table = customtkinter.CTkFrame(self.receipt, fg_color="#ffffff")
        self.receipt_table.pack(fill="x", padx=8, pady=(8, 4))

        # กำหนดน้ำหนักคอลัมน์ของตาราง (ชื่อ:กว้าง, ที่เหลือ:ตัวเลข)
        for c, w in enumerate((3, 1, 1, 1)):
            self.receipt_table.grid_columnconfigure(c, weight=w)

        def _build_receipt_header():
            hdr = customtkinter.CTkFrame(self.receipt_table, fg_color="#f0f0f0", corner_radius=8)
            hdr.grid(row=0, column=0, columnspan=4, sticky="ew", padx=0, pady=(0, 6))
            hdr.grid_columnconfigure(0, weight=3)
            hdr.grid_columnconfigure(1, weight=1)
            hdr.grid_columnconfigure(2, weight=1)
            hdr.grid_columnconfigure(3, weight=1)

            customtkinter.CTkLabel(hdr, text="สินค้า").grid(row=0, column=0, padx=12, pady=8, sticky="w")
            customtkinter.CTkLabel(hdr, text="จำนวน").grid(row=0, column=1, padx=12, pady=8, sticky="e")
            customtkinter.CTkLabel(hdr, text="ราคา/ชิ้น").grid(row=0, column=2, padx=12, pady=8, sticky="e")
            customtkinter.CTkLabel(hdr, text="รวม").grid(row=0, column=3, padx=12, pady=8, sticky="e")

        self._build_receipt_header = _build_receipt_header

        # รวมเงิน + ปุ่มยืนยันชำระ
        bottom_row = customtkinter.CTkFrame(left, fg_color="transparent")
        bottom_row.grid(row=2, column=0, padx=16, pady=(0,16), sticky="ew")
        bottom_row.grid_columnconfigure(0, weight=1)   # text left
        bottom_row.grid_columnconfigure(1, weight=0)   # number right

        self.subtotal_label_text = customtkinter.CTkLabel(bottom_row, text="Subtotal :")
        self.subtotal_label_text.grid(row=0, column=0, sticky="w", pady=2)

        self.subtotal_label_val = customtkinter.CTkLabel(bottom_row, text="0 ฿")
        self.subtotal_label_val.grid(row=0, column=1, sticky="e", pady=2)

        self.vat_label_text = customtkinter.CTkLabel(bottom_row, text="VAT 7% :")
        self.vat_label_text.grid(row=1, column=0, sticky="w", pady=2)

        self.vat_label_val = customtkinter.CTkLabel(bottom_row, text="0 ฿")
        self.vat_label_val.grid(row=1, column=1, sticky="e", pady=2)

        self.total_label_text = customtkinter.CTkLabel(bottom_row, text="รวมทั้งหมด :", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.total_label_text.grid(row=2, column=0, sticky="w", pady=(4,6))

        self.total_label_val = customtkinter.CTkLabel(bottom_row, text="0 ฿", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.total_label_val.grid(row=2, column=1, sticky="e", pady=(4,6))

        self.btn_confirm = customtkinter.CTkButton(bottom_row, text="ยืนยันการชำระเงิน", command=self._confirm_payment)
        self.btn_confirm.grid(row=3, column=1, sticky="e", pady=(8,0))
        # ---------- ขวา: QR + อัปโหลดสลิป ----------
        right = customtkinter.CTkScrollableFrame(content, fg_color="#ffffff", corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        right.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(right, text="สแกนเพื่อชำระ (QR)", font=customtkinter.CTkFont(size=15, weight="bold")).grid(row=0, column=0, padx=16, pady=(16,6), sticky="w")

        qr_placeholder = customtkinter.CTkFrame(right, fg_color="#ffffff", corner_radius=12)
        qr_placeholder.grid(row=1, column=0, padx=16, pady=(0,12), sticky="nsew")

        try:
            image_qr = r"D:\python porgramming\project\JPG\qr_heaven.jpg"  # ✅ ไม่มีช่องว่าง
            qr_img = customtkinter.CTkImage(light_image=Image.open(image_qr),dark_image=Image.open(image_qr),size=(350, 350))

            qr_label = customtkinter.CTkLabel(qr_placeholder, image=qr_img, text="")
            qr_label.image = qr_img
            qr_label.pack(expand=True, padx=10, pady=10)
        
        except Exception as e:
            customtkinter.CTkLabel(qr_placeholder,text="ไม่พบ QR Code\nกรุณาตรวจสอบ path",text_color="red").pack(expand=True, pady=20)
            print("QR Load Error:", e)

        # อัปโหลดสลิป
        up = customtkinter.CTkFrame(right, fg_color="#f9fafb", corner_radius=12)
        up.grid(row=2, column=0, padx=16, pady=(0,16), sticky="ew")
        customtkinter.CTkLabel(up, text="อัปโหลดสลิปการโอน", font=customtkinter.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=12, pady=(12,6), sticky="w")
        self.slip_preview = customtkinter.CTkLabel(up, text="(ยังไม่เลือกไฟล์)")
        self.slip_preview.grid(row=1, column=0, padx=12, pady=(0,8), sticky="w")
        
        # --- กล่องตัวอย่างสลิป ---
        self.slip_holder = customtkinter.CTkFrame(up, fg_color="#ffffff", corner_radius=10)
        self.slip_holder.grid(row=1, column=0, padx=12, pady=(0,8), sticky="ew")
        self.slip_img_label = customtkinter.CTkLabel(self.slip_holder, text="(ยังไม่เลือกไฟล์)", height=220, anchor="center")
        self.slip_img_label.pack(fill="both", expand=True, padx=8, pady=8)

        # ชื่อไฟล์สลิป
        self.slip_name = customtkinter.CTkLabel(up, text="", text_color="#666666")
        self.slip_name.grid(row=2, column=0, padx=12, pady=(0,8), sticky="w")

        # ตัวแปรอ้างอิงรูป ป้องกัน GC
        self._slip_ctkimg = None
        customtkinter.CTkButton(up, text="เลือกไฟล์สลิป", command=self._pick_slip).grid(row=2, column=0, padx=12, pady=(0,12), sticky="w")

    def on_show(self):
        # ----- โหลดที่อยู่ผู้ใช้ -----
        uid = getattr(self.controller, "current_user_id", None)
        if uid is None:
            CTkMessagebox(title="ต้องเข้าสู่ระบบ", message="โปรดเข้าสู่ระบบก่อนชำระเงิน", icon="warning")
            self.controller.show_frame(LoginPage)
            return

        u = Fetch_User_By_ID(uid)
        if not u:
            CTkMessagebox(title="ข้อผิดพลาด", message="ไม่พบข้อมูลผู้ใช้", icon="cancel")
            self.controller.show_frame(main_menu)
            return
        uid_db, username, role, gmail, fullname, address, phone = u
        display_name = fullname or username
        self.addr_label.configure(text=f"{display_name}\n{address}\nโทร: {phone}\nอีเมล: {gmail}")

        # ----- สลิป (คงไว้ถ้ามี / รีเซ็ตถ้าไม่มี) -----
        if getattr(self, "slip_path", None):
            self._render_slip_preview(self.slip_path)
        else:
            self.slip_img_label.configure(image=None, text="(ยังไม่เลือกไฟล์)")
            self.slip_name.configure(text="")

        # ===== วาดใบเสร็จ =====
        # เคลียร์เฉพาะแถวในตาราง แล้วยกหัวตารางขึ้นใหม่
        for w in self.receipt_table.winfo_children():
            w.destroy()
        self._build_receipt_header()

        # ดึงรายการจากตะกร้า (fallback: ถ้าไม่มี selected ให้แสดงทั้งตะกร้า)
        cart_items = getattr(self.controller, "cart", None).items if hasattr(self.controller, "cart") else []
        selected = [it for it in cart_items if it.get("selected")]
        items = selected or cart_items

        # ลบ label "ไม่มีสินค้า..." เดิม (ถ้ามี)
        if hasattr(self, "_empty_lbl") and self._empty_lbl and self._empty_lbl.winfo_exists():
            self._empty_lbl.destroy()

        if not items:
            self._empty_lbl = customtkinter.CTkLabel(self.receipt, text="ไม่มีสินค้าในใบเสร็จ", text_color="#666")
            self._empty_lbl.pack(pady=12)
        else:
            r = 1
            for it in items:
                name = str(it.get("name", ""))
                qty  = int(it.get("qty", 0))
                unit = int(it.get("price", 0))
                sub  = qty * unit

                customtkinter.CTkLabel(self.receipt_table, text=name)\
                    .grid(row=r, column=0, padx=12, pady=6, sticky="w")
                customtkinter.CTkLabel(self.receipt_table, text=str(qty))\
                    .grid(row=r, column=1, padx=12, pady=6, sticky="e")
                customtkinter.CTkLabel(self.receipt_table, text=f"฿{CartModel.fmt_price(unit)}")\
                    .grid(row=r, column=2, padx=12, pady=6, sticky="e")
                customtkinter.CTkLabel(self.receipt_table, text=f"฿{CartModel.fmt_price(sub)}")\
                    .grid(row=r, column=3, padx=12, pady=6, sticky="e")
                r += 1

        # ===== คิดเงินจาก "items" ที่แสดงจริง =====
        subtotal = sum(int(it.get("price", 0)) * int(it.get("qty", 0)) for it in items)
        vat = int(round(subtotal * 0.07))
        grand = subtotal + vat

        self.subtotal_label_val.configure(text=f"฿{CartModel.fmt_price(subtotal)}")
        self.vat_label_val.configure(text=f"฿{CartModel.fmt_price(vat)}")
        self.total_label_val.configure(text=f"฿{CartModel.fmt_price(grand)}")

        # เก็บค่าไว้ใช้ต่อ
        self._last_subtotal = subtotal
        self._last_vat = vat
        self._last_grand = grand

    def _pick_slip(self):
        f = fd.askopenfilename(title="เลือกสลิปโอนเงิน",
            filetypes=[("Images","*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.gif"), ("All files","*.*")])
        if f:
            self.slip_path = f
            base = os.path.basename(f)
            # อัปเดตชื่อไฟล์และพรีวิวรูป
            self.slip_name.configure(text=f"เลือกแล้ว: {base}")
            self._render_slip_preview(f)

    def _render_slip_preview(self, path: str, max_size=(360, 360)):
        try:
            img = Image.open(path)
            # แก้ปัญหารูปหมุนจาก EXIF (รูปจากมือถือ)
            try:
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            # ย่อโดยรักษาสัดส่วนให้พอดีกล่อง
            img.thumbnail(max_size, Image.LANCZOS)

            # สร้าง CTkImage (ต้องเก็บอ้างอิงไว้กัน GC)
            self._slip_ctkimg = customtkinter.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.slip_img_label.configure(image=self._slip_ctkimg, text="")
        except Exception as e:
            # แสดงข้อความแทน ถ้าพรีวิวไม่ได้
            self._slip_ctkimg = None
            self.slip_img_label.configure(image=None, text="แสดงตัวอย่างสลิปไม่ได้\nกรุณาลองไฟล์อื่น", text_color="red")
            print("Slip preview error:", e)

    def _confirm_payment(self):
        """บันทึกออเดอร์จากสินค้าที่เลือกในตะกร้า + คิด VAT แล้วบันทึกยอดรวมสุดท้าย (orders + order_items)"""
        # 1) ตรวจสิทธิ์
        uid = getattr(self.controller, "current_user_id", None)
        if uid is None:
            CTkMessagebox(title="ต้องเข้าสู่ระบบ", message="โปรดเข้าสู่ระบบก่อนชำระเงิน", icon="warning")
            self.controller.show_frame(LoginPage)
            return

        # 2) สินค้าที่เลือก
        items = [it for it in self.controller.cart.items if it.get("selected")]
        if not items:
            CTkMessagebox(title="ยังไม่มีสินค้า", message="กรุณาเลือกสินค้าในตะกร้าก่อน", icon="warning")
            return

        # 2.5) ✅ เช็คสลิปต้องมีไฟล์จริงก่อนชำระ
        if not getattr(self, "slip_path", None) or not os.path.isfile(self.slip_path):
            CTkMessagebox(title="ยังไม่มีสลิป", message="กรุณาอัปโหลดสลิปก่อนยืนยันการชำระเงิน", icon="warning")
            return

        # 3) คำนวณยอด
        subtotal = self.controller.cart.total_selected()
        vat = int(round(subtotal * 0.07))
        grand = subtotal + vat
        self._last_subtotal = subtotal
        self._last_vat = vat
        self._last_grand = grand

        # 4) สแน็ปช็อตที่อยู่
        u = Fetch_User_By_ID(uid)
        if not u:
            CTkMessagebox(title="ข้อผิดพลาด", message="ไม่พบข้อมูลผู้ใช้", icon="cancel")
            return
        _id, username, role, gmail, fullname, address, phone = u
        display_name = fullname or username
        addr_snapshot = f"{display_name}\n{address}\nโทร: {phone}\nอีเมล: {gmail}"
        
        # 5) สถานะออเดอร์ (มีสลิปแล้วถือว่า PAID)
        status = "PAID"

        # 6) บันทึกออเดอร์ + รายการสินค้า (ใช้ทรานแซกชันเดียว)
        conn = None
        try:
            conn = connect_db() 
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO orders (user_id, total, status, address_snapshot, path_slip, order_date)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (uid, grand, status, addr_snapshot, self.slip_path))
            order_id = cur.lastrowid

            # แทรกรายการสินค้าลง order_items
            for it in items:
                name = str(it.get("name", ""))
                qty  = int(it.get("qty", 0))
                unit = int(it.get("price", 0))
                cur.execute("""
                    INSERT INTO order_items (order_id, product_name, qty, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, name, qty, unit))

            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            CTkMessagebox(title="ออกออเดอร์ไม่สำเร็จ", message=str(e), icon="cancel")
            return
        finally:
            if conn:
                conn.close()

        # 7) เคลียร์เฉพาะสินค้าที่เลือกออกจากตะกร้า + รีเซ็ตสลิป
        self.controller.cart.items = [it for it in self.controller.cart.items if not it.get("selected")]
        self.slip_path = None
        self.slip_img_label.configure(image=None, text="(ยังไม่เลือกไฟล์)")
        self.slip_name.configure(text="")

        # 8) แจ้งผลและพาไปหน้า My Order (ฝั่งผู้ใช้)
        msg = f"บันทึกออเดอร์ #{order_id} แล้ว\nยอดสุทธิ (รวม VAT 7%): ฿{CartModel.fmt_price(grand)}\nรอตรวจสลิปโดยแอดมิน"
        CTkMessagebox(title="สำเร็จ", message=msg, icon="check")
        self.controller.show_frame(Order_Page)

        
#======= Order Page ========
class Order_Page(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.Selected_Order_ID = None

        # Layout หลัก
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="ew")
        self.Hight_frame.grid_propagate(False)
        for i in range(3):
            self.Hight_frame.grid_columnconfigure(i, weight=0)
        self.Hight_frame.grid_columnconfigure(1, weight=1)

        # โลโก้กลับหน้าหลัก
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        try:
            self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        except Exception:
            self.logo = None
        customtkinter.CTkButton(self.Hight_frame, image=self.logo, text="", width=48, height=35,
                                fg_color="#ffffff", hover_color="#e0e0e0", corner_radius=12,
                                command=lambda: self.controller.show_frame(main_menu)
                                ).grid(row=0, column=0, padx=(16,8), pady=22, sticky="w")
        customtkinter.CTkLabel(self.Hight_frame, text="My Orders",
                               font=customtkinter.CTkFont(size=20, weight="bold")
                               ).grid(row=0, column=1, sticky="w")

        # Content ซ้าย/ขวา
        self.Content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.Content.grid(row=1, column=0, sticky="nsew")
        self.Content.grid_rowconfigure(0, weight=1)
        self.Content.grid_columnconfigure(0, weight=1)
        self.Content.grid_columnconfigure(1, weight=1)

        self.list_frame = customtkinter.CTkScrollableFrame(self.Content, fg_color="#ffffff", corner_radius=14)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=(16,8), pady=(8,16))
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.detail_frame = customtkinter.CTkScrollableFrame(self.Content, fg_color="#ffffff", corner_radius=14)
        self.detail_frame.grid(row=0, column=1, sticky="nsew", padx=(8,16), pady=(8,16))
        self.detail_frame.grid_columnconfigure(0, weight=1)

    # ---------- เข้าหน้านี้ ----------
    def on_show(self):
        uid = getattr(self.controller, "current_user_id", None)
        if uid is None:
            CTkMessagebox(title="ต้องเข้าสู่ระบบ", message="โปรดเข้าสู่ระบบก่อน", icon="warning")
            self.controller.show_frame(LoginPage)
            return
        self._refresh_lists()

    # ---------- โหลดลิสต์ซ้าย ----------
    def _refresh_lists(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for w in self.detail_frame.winfo_children():
            w.destroy()

        uid = self.controller.current_user_id
        rows = Fetch_Orders_By_User(uid)
        if not rows:
            customtkinter.CTkLabel(self.list_frame, text="ยังไม่มีออเดอร์", text_color="#666").pack(pady=20)
            return

        # วาด card ลิสต์
        for (oid, odate, status, total, addr, slip, cancel_reason) in rows:
            card = customtkinter.CTkFrame(self.list_frame, fg_color="#f7f9fc", corner_radius=12)
            card.pack(fill="x", padx=12, pady=8)
            head = customtkinter.CTkFrame(card, fg_color="transparent")
            head.pack(fill="x", padx=10, pady=(8,2))
            customtkinter.CTkLabel(head, text=f"#{oid} | {odate} | ฿{CartModel.fmt_price(total)}",
                                    font=customtkinter.CTkFont(size=13, weight="bold")).pack(side="left")
            st = (status or "").upper().strip()
            bg, fg = self._status_colors(st)
            customtkinter.CTkLabel(head, text=st, text_color=fg, fg_color=bg, corner_radius=8, padx=8, pady=2).pack(side="right")
            if addr:
                short_addr = addr if len(addr) <= 140 else addr[:140] + "..."
                customtkinter.CTkLabel(card, text=short_addr, justify="left", text_color="#555"
                                       ).pack(anchor="w", padx=10, pady=(0,10))
            def _open(_oid=oid): self._render_detail(_oid)
            card.bind("<Button-1>", lambda e, x=oid: _open(x))
            for ch in card.winfo_children():
                ch.bind("<Button-1>", lambda e, x=oid: _open(x))

        # auto select ใบล่าสุด
        self.Selected_Order_ID = rows[0][0]
        self._render_detail(self.Selected_Order_ID)

    # ---------- สีสถานะ ----------
    @staticmethod
    def _status_colors(status: str):
        s = (status or "").upper()
        if s == "CONFIRMED":
            return "#E8F5E9", "#1B5E20"  # เขียวอ่อน / เขียวเข้ม
        if s == "CANCELLED":
            return "#FFEBEE", "#B71C1C"  # แดงอ่อน / แดงเข้ม
        return "#FFF8E1", "#E65100"      # PENDING/PAID: ส้ม

    # ---------- รายละเอียดออเดอร์ขวา ----------
    def _render_detail(self, order_id: int):
        self.Selected_Order_ID = order_id
        for w in self.detail_frame.winfo_children():
            w.destroy()

        conn = connect_db(); cur = conn.cursor()
        head = cur.execute("""
            SELECT o.id, o.order_date, u.fullname, o.status, o.address_snapshot, o.path_slip, o.total
            FROM orders o
            LEFT JOIN users u ON u.id = o.user_id
            WHERE o.id=?
        """, (order_id,)).fetchone()
        conn.close()

        if not head:
            customtkinter.CTkLabel(self.detail_frame, text="ไม่พบออเดอร์", text_color="#b00").pack(pady=20)
            return

        oid, odate, uname, status, addr_snap, slip, header_total = head
        status_norm = (status or "").upper().strip()

        # หัวเรื่อง + badge
        top = customtkinter.CTkFrame(self.detail_frame, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(16,6))
        customtkinter.CTkLabel(top, text=f"Order #{oid} | {odate} | by {uname}",
                               font=customtkinter.CTkFont(size=16, weight="bold")).pack(side="left")
        bg, fg = self._status_colors(status_norm)
        customtkinter.CTkLabel(top, text=status_norm, text_color=fg, fg_color=bg,
                               corner_radius=8, padx=8, pady=2).pack(side="right")

        # ที่อยู่
        if addr_snap:
            box = customtkinter.CTkFrame(self.detail_frame, fg_color="#f7f9fc", corner_radius=10)
            box.pack(fill="x", padx=16, pady=(6,10))
            customtkinter.CTkLabel(box, text=addr_snap, justify="left").pack(anchor="w", padx=12, pady=8)

        # สลิป
        if slip:
            try:
                im = customtkinter.CTkImage(Image.open(slip), size=(360, 360))
                img_lbl = customtkinter.CTkLabel(self.detail_frame, image=im, text="")
                img_lbl.image = im
                img_lbl.pack(padx=16, pady=(0, 10))
                def _zoom():
                    t = customtkinter.CTkToplevel(self); t.title(f"Slip #{oid}")
                    imi = customtkinter.CTkImage(Image.open(slip), size=(640, 640))
                    l = customtkinter.CTkLabel(t, image=imi, text=""); l.image = imi; l.pack(padx=12, pady=12)
                img_lbl.bind("<Button-1>", lambda e: _zoom())
            except Exception:
                customtkinter.CTkLabel(self.detail_frame, text="(เปิดสลิปไม่ได้)").pack()

        # รายการสินค้า
        items = []
        try:
            items = Fetch_Order_Items(order_id)  # -> [(name, qty, unit_price), ...]
        except Exception as e:
            CTkMessagebox(title="Order items error", message=str(e), icon="cancel")

        tbl = customtkinter.CTkFrame(self.detail_frame, fg_color="#ffffff", corner_radius=10)
        tbl.pack(fill="x", padx=16, pady=(6, 6))
        for c, w in enumerate((3,1,1,1)):
            tbl.grid_columnconfigure(c, weight=w)

        hdr = customtkinter.CTkFrame(tbl, fg_color="#f0f0f0", corner_radius=8)
        hdr.grid(row=0, column=0, columnspan=4, sticky="ew")
        for c,w in enumerate((3,1,1,1)):
            hdr.grid_columnconfigure(c, weight=w)
        customtkinter.CTkLabel(hdr, text="สินค้า").grid(row=0, column=0, padx=12, pady=6, sticky="w")
        customtkinter.CTkLabel(hdr, text="จำนวน").grid(row=0, column=1, padx=12, pady=6, sticky="e")
        customtkinter.CTkLabel(hdr, text="ราคา/ชิ้น").grid(row=0, column=2, padx=12, pady=6, sticky="e")
        customtkinter.CTkLabel(hdr, text="รวม").grid(row=0, column=3, padx=12, pady=6, sticky="e")

        r = 1
        subtotal = 0
        for (name, qty, unit_price) in items:
            qty = int(qty); unit_price = int(unit_price)
            line_total = qty * unit_price
            subtotal += line_total
            customtkinter.CTkLabel(tbl, text=str(name)).grid(row=r, column=0, padx=12, pady=6, sticky="w")
            customtkinter.CTkLabel(tbl, text=str(qty)).grid(row=r, column=1, padx=12, pady=6, sticky="e")
            customtkinter.CTkLabel(tbl, text=f"฿{CartModel.fmt_price(unit_price)}").grid(row=r, column=2, padx=12, pady=6, sticky="e")
            customtkinter.CTkLabel(tbl, text=f"฿{CartModel.fmt_price(line_total)}").grid(row=r, column=3, padx=12, pady=6, sticky="e")
            r += 1

        vat = int(round(subtotal * VAT_RATE))
        shipping = 0  # : ถ้ามีค่าขนส่งให้ดึงจาก DB
        grand = subtotal + shipping + vat

        summary = customtkinter.CTkFrame(self.detail_frame, fg_color="transparent")
        summary.pack(fill="x", padx=16, pady=(4, 8))
        summary.grid_columnconfigure(0, weight=1)
        summary.grid_columnconfigure(1, weight=0)
        customtkinter.CTkLabel(summary, text="Subtotal :").grid(row=0, column=0, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(subtotal)}").grid(row=0, column=1, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text="Shipping :").grid(row=1, column=0, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(shipping)}").grid(row=1, column=1, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text="VAT 7% :").grid(row=2, column=0, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(vat)}").grid(row=2, column=1, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text="รวมทั้งหมด :", font=customtkinter.CTkFont(weight="bold")).grid(row=3, column=0, sticky="e", padx=8, pady=(4,6))
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(grand)}", font=customtkinter.CTkFont(weight="bold")).grid(row=3, column=1, sticky="e", padx=8, pady=(4,6))

        # ปุ่มด้านล่าง
        btns = customtkinter.CTkFrame(self.detail_frame, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 12))
        if status_norm == "CONFIRMED":
            customtkinter.CTkButton(btns, text="Download ใบเสร็จ (PDF)",fg_color="#eef6ff", text_color="#0b57d0",
                                    command=lambda: self._download_receipt_pdf(oid)).pack(side="right", padx=6)
        else:
            customtkinter.CTkLabel(btns, text="(จะดาวน์โหลดได้เมื่อแอดมินยืนยันออเดอร์แล้ว)", text_color="#777"
                                   ).pack(side="right", padx=6)

        if status_norm in ("PAID", "PENDING"):
            customtkinter.CTkButton(btns, text="ยกเลิกออเดอร์",fg_color="#ffefef", text_color="#b00000",
                                    command=lambda: self._cancel_order(oid)).pack(side="right", padx=6)

    # ---------- ยกเลิก ----------
    def _cancel_order(self, oid: int):
        ans = CTkMessagebox(title="ยกเลิกออเดอร์", message="ยืนยันการยกเลิกหรือไม่?", icon="warning",
                            option_1="No", option_2="Yes").get()
        if ans == "Yes":
            Update_Order_Status(oid, "CANCELLED", cancel_reason="cancel by user")
            CTkMessagebox(title="ยกเลิกแล้ว", message=f"ยกเลิก Order #{oid} เรียบร้อย", icon="check")
            self._refresh_lists()

    # ---------- สร้าง PDF ----------
    def _download_receipt_pdf(self, oid: int):
        if not REPORTLAB_OK:
            CTkMessagebox(title="ต้องติดตั้งฟอนต์/ไลบรารี",
                        message="โปรดติดตั้ง reportlab และฟอนต์ไทย THSarabunNew",
                        icon="warning")
            return

        # ตรวจสถานะซ้ำ (กันเลี่ยง UI)
        conn = connect_db(); cur = conn.cursor()
        row = cur.execute("SELECT status FROM orders WHERE id=?", (oid,)).fetchone()
        conn.close()
        if not row:
            CTkMessagebox(title="ผิดพลาด", message="ไม่พบออเดอร์", icon="cancel"); return
        if (row[0] or "").upper() != "CONFIRMED":
            CTkMessagebox(title="ยังไม่สามารถดาวน์โหลดได้",
                        message="ออเดอร์ยังไม่ถูกยืนยันจากแอดมิน", icon="warning"); return

        path = fd.asksaveasfilename(title="บันทึกใบเสร็จเป็น PDF",
                                    defaultextension=".pdf",
                                    filetypes=[("PDF", "*.pdf")],
                                    initialfile=f"receipt_order_{oid}.pdf")
        if not path:
            return

        try:
            self._export_order_pdf(oid, path)
            CTkMessagebox(title="สำเร็จ", message="บันทึกไฟล์ PDF เรียบร้อย", icon="check")

            # ===== เปิดไฟล์อัตโนมัติ =====
            try:
                # บน Windows จะเปิดด้วยโปรแกรม default ของ .pdf (อาจเป็น Edge/Chrome/Adobe)
                os.startfile(path)
            except Exception:
                # ถ้า startfile ใช้ไม่ได้ ให้เปิดในเบราว์เซอร์ผ่าน file://
                url = Path(path).resolve().as_uri()
                webbrowser.open_new_tab(url)

        except Exception as e:
            CTkMessagebox(title="ผิดพลาด", message=str(e), icon="cancel")


    # ---------- วาด PDF ตามแบบตัวอย่าง ----------
    def _export_order_pdf(self, order_id: int, out_path: str):
        # ===== DB =====
        conn = connect_db(); cur = conn.cursor()
        head = cur.execute("""
            SELECT o.id, o.order_date, u.fullname, u.gmail, u.address, u.phone,
                o.status, o.address_snapshot
            FROM orders o
            JOIN users u ON u.id = o.user_id
            WHERE o.id=?
        """, (order_id,)).fetchone()
        conn.close()
        if not head: raise RuntimeError("ไม่พบออเดอร์")

        oid, odate, ufullname, ugmail, uaddr, uphone, status, addr_snap = head
        if (status or "").upper() != "CONFIRMED":
            raise PermissionError("ดาวน์โหลดใบเสร็จได้เมื่อออเดอร์ถูกยืนยันแล้ว (CONFIRMED)")

        
        items = Fetch_Order_Items_Detail(order_id)

        # ===== คำนวณ =====
        rows = []
        subtotal = 0
        for i, (name, qty, unit_price, disc_unit) in enumerate(items, start=1):
            eff_unit = max(int(unit_price) - int(disc_unit or 0), 0)
            line_total = eff_unit * int(qty)
            subtotal += line_total
            rows.append((i, str(name), int(qty), eff_unit, line_total))
        vat = int(round(subtotal * 0.07))
        grand = subtotal + vat

        # ที่อยู่ (หลายบรรทัดได้ แต่ “ไม่ขีดเส้นใต้”)
        ship_addr = (addr_snap or uaddr or "").replace("\r", "")
        ship_lines = [ln.strip() for ln in ship_addr.split("\n") if ln.strip()]

        # ===== PDF =====
        c = canvas.Canvas(out_path, pagesize=A4)
        W, H = A4
        L, R, T, B = 15*mm, 15*mm, H-15*mm, 15*mm
        y = T

        def setfont(sz=10): c.setFont(PDF_FONT, sz)
        def txt(s, x, y, sz=10, align="left"):
            setfont(sz)
            if align == "left": c.drawString(x, y, s)
            elif align == "right": c.drawRightString(x, y, s)
            else: c.drawCentredString(x, y, s)

        # Header กล่องโค้ง
        header_h = 32*mm
        c.roundRect(L, y-header_h, W-L-R, header_h, 6, stroke=1, fill=0)
        if LOGO_PATH and os.path.exists(LOGO_PATH):
            try:
                c.drawImage(ImageReader(LOGO_PATH), L+4*mm, y-24*mm, 22*mm, 18*mm,
                            preserveAspectRatio=True, mask='auto')
            except Exception: pass
        rx = L + (W-L-R) - 4*mm
        ty = y - 6*mm
        txt("ใบเสร็จรับเงิน", rx, ty, 12, "right");            ty -= 5*mm
        txt("Heaven Gear Gaming Shop", rx, ty, 11, "right");     ty -= 4.2*mm
        txt("ที่อยู่ เลขที่ 123 หมู่ 16 ถนนมิตรภาพ ต.ในเมือง อ.เมืองขอนแก่น", rx, ty, 9, "right"); ty -= 4.2*mm
        txt("จังหวัดขอนแก่น 40000", rx, ty, 9, "right");        ty -= 4.2*mm
        txt("เบอร์ติดต่อ 099-369-0768", rx, ty, 9, "right");    ty -= 4.2*mm
        txt("อีเมล Kittikon.k@kkumail.com", rx, ty, 9, "right")
        y -= (header_h + 6*mm)

        # ===== META: “ไม่มีเส้นใต้” ตามที่ขอ =====
        line_gap = 5*mm
        def meta(label, value, gap=line_gap):
            nonlocal y
            txt(f"{label}  {value or ''}", L, y, 10, "left")
            y -= gap

        meta("หมายเลขคำสั่งซื้อ", oid)
        meta("วันที่สั่งซื้อ", odate)
        meta("ชื่อลูกค้า", ufullname)
        meta("อีเมล", ugmail)
        meta("เบอร์โทร", uphone)
        meta("ที่อยู่สำหรับจัดส่ง", uaddr)

        # ===== ตารางสินค้า =====
        col_w = [15*mm, 95*mm, 20*mm, 20*mm, 30*mm]
        row_h = 8*mm
        table_header = [["ลำดับ","รายการสินค้า","จำนวน","ราคาต่อชิ้น","รวม"]]

        def draw_table_block(data):
            nonlocal y
            # กรอบ
            total_h = row_h * len(data)
            c.rect(L, y-total_h, sum(col_w), total_h, stroke=1, fill=0)
            # เส้นแนวนอน
            yy = y
            for _ in data[1:]:
                yy -= row_h; c.line(L, yy, L+sum(col_w), yy)
            # เส้นแนวตั้ง
            xx = L
            for w in col_w[:-1]:
                xx += w; c.line(xx, y, xx, y-total_h)
            # ข้อความ (เลขชิดขวา)
            ty = y - row_h + 3
            for row in data:
                for i, cell in enumerate(row):
                    if i in (0,2,3,4):
                        txt(str(cell), L + sum(col_w[:i+1]) - 4, ty, 10, "right")
                    else:
                        txt(str(cell), L + sum(col_w[:i]) + 3, ty, 10, "left")
                ty -= row_h
            y -= total_h

        # หัวตาราง
        draw_table_block(table_header)

        def new_page():
            nonlocal y
            c.showPage(); y = T
            txt("ใบเสร็จรับเงิน", L, y, 11, "left"); y -= 8*mm
            draw_table_block(table_header)

        bottom_limit = B + 65*mm
        for seq, name, qty, eff_unit, line_total in rows:
            if y - row_h < bottom_limit: new_page()
            draw_table_block([[str(seq), name, str(qty),
                            f"{CartModel.fmt_price(eff_unit)} บาท",
                            f"{CartModel.fmt_price(line_total)} บาท"]])

        # ===== สรุปยอด (ไม่วาดเส้นซ้ำ) =====
        y -= 4*mm
        sum_col_w = [40*mm, 30*mm]
        X = W - R - sum(sum_col_w)
        sum_rows = [ ("ยอดรวมสินค้า",            f"{CartModel.fmt_price(subtotal)} บาท"),
                     ("ภาษีมูลค่าเพิ่ม 7% (VAT)", f"{CartModel.fmt_price(vat)} บาท"),
                     ("ยอดชำระรวม",               f"{CartModel.fmt_price(grand)} บาท"),
                   ]
        total_h = 8.5*mm * len(sum_rows)
        # กรอบเดียว + เส้นคั่นแนวนอน + เส้นตั้งตรงกลาง
        c.rect(X, y-total_h, sum(sum_col_w), total_h, stroke=1, fill=0)
        c.line(X + sum_col_w[0], y, X + sum_col_w[0], y-total_h)
        ty = y - 8.5*mm + 3
        for idx, (label, val) in enumerate(sum_rows):
            txt(label, X+3, ty, 10, "left")
            txt(val,   X+sum(sum_col_w)-4, ty, 10, "right")
            if idx < len(sum_rows)-1:
                c.line(X, ty-3, X+sum(sum_col_w), ty-3)
            ty -= 8.5*mm
        y -= (total_h + 12*mm)

        # ===== วิธีชำระเงิน / วันที่ยืนยัน / ชำระเงินแล้ว =====
        txt("วิธีชำระเงิน  QR PromptPay", L, y, 10, "left"); y -= 6*mm
        txt(f"วันที่ยืนยันการสั่งซื้อ {odate}", L, y, 10, "left"); y -= 6*mm
        txt("ชำระเงินแล้ว", L, y, 10, "left"); y -= 6*mm

        note = "หมายเหตุ ใบเสร็จนี้เป็นหลักฐานการซื้อขายอุปกรณ์คอมพิวเตอร์จากร้าน Heaven Gear Gaming Shop กรุณาเก็บใบเสร็จเพื่อการเคลม/ประกันสินค้า"
        txt(note, L, y, 9, "left")

        c.showPage(); c.save()

# ====== Profile Page ========
class ProfilePage(customtkinter.CTkFrame):  # โปรไฟล์แบบซ้าย/ขวา 1:2
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.mode = "VIEW"          # VIEW / EDIT
        self._avatar_ctk = None     # cache รูป

        # ---------- โครงร่างหลัก ----------
        self.grid_rowconfigure(0, weight=0)   # Header
        self.grid_rowconfigure(1, weight=1)   # Content
        self.grid_columnconfigure(0, weight=1)

        # =================== Header ===================
        header = customtkinter.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=72)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        for c in range(3):
            header.grid_columnconfigure(c, weight=0)
        header.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(header, text="My Profile",font=customtkinter.CTkFont(size=22, weight="bold")
                                ).grid(row=0, column=0, padx=18, pady=18, sticky="w")

        customtkinter.CTkButton(header, text="Back to Home",command=lambda: self.controller.show_frame(main_menu)
                                ).grid(row=0, column=2, padx=16, pady=18, sticky="e")

        # =================== Content (ซ้าย/ขวา 1:2) ===================
        content = customtkinter.CTkFrame(self, fg_color="#f7f9fc")
        content.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 16))
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)  # ซ้าย (1 ส่วน)
        content.grid_columnconfigure(1, weight=3)  # ขวา (2 ส่วน)

        # ---------- Sidebar (ซ้าย) ----------
        self.sidebar = customtkinter.CTkFrame(content, fg_color="#ffffff", corner_radius=14)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(12, 8), pady=12)
        self.sidebar.grid_columnconfigure(0, weight=1)

        # รูปโปรไฟล์
        self.avatar_label = customtkinter.CTkLabel(self.sidebar, text="")
        self.avatar_label.grid(row=0, column=0, padx=16, pady=(16, 8))

        # ชื่อผู้ใช้ใต้รูป
        self.lbl_username_title = customtkinter.CTkLabel(self.sidebar, text="", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.lbl_username_title.grid(row=1, column=0, padx=12, pady=(0, 16))

        # ปุ่ม: Edit Profile (เปลี่ยนรูป)
        customtkinter.CTkButton(self.sidebar, text="Edit Profile ", fg_color="#111827",
                                command=self._choose_avatar).grid(row=2, column=0, padx=16, pady=(4, 8), sticky="ew")

        # ปุ่ม: View / Edit / Sign out
        customtkinter.CTkButton(self.sidebar, text="View", command=lambda: self._switch_mode("VIEW")
                                ).grid(row=3, column=0, padx=16, pady=6, sticky="ew")

        customtkinter.CTkButton(self.sidebar, text="Edit", fg_color="#00B7FF", text_color="#000000",command=lambda: self._switch_mode("EDIT")
                                ).grid(row=4, column=0, padx=16, pady=6, sticky="ew")

        customtkinter.CTkLabel(self.sidebar, text="",height=290).grid(row=5, column=0, sticky="nsew")

        customtkinter.CTkButton(self.sidebar, text="Sign out", fg_color="#ef4444",command=self._sign_out
                                ).grid(row=6, column=0, padx=16, pady=(6, 16), sticky="sew")

        # ---------- Main Area (ขวา) ----------
        self.main_area = customtkinter.CTkFrame(content, fg_color="#ffffff", corner_radius=14)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=(8, 12), pady=12)
        self.main_area.grid_columnconfigure(0, weight=1)

        # ====== VIEW (อ่านอย่างเดียว) ======
        self.view_frame = customtkinter.CTkFrame(self.main_area, fg_color="transparent")
        self.view_frame.grid_columnconfigure(1, weight=1)

        self.lbl_fullname_v = customtkinter.CTkLabel(self.view_frame, text="")
        self.lbl_username_v = customtkinter.CTkLabel(self.view_frame, text="")
        self.lbl_gmail_v    = customtkinter.CTkLabel(self.view_frame, text="")
        self.lbl_address_v  = customtkinter.CTkLabel(self.view_frame, text="")
        self.lbl_phone_v    = customtkinter.CTkLabel(self.view_frame, text="")

        def row_v(r, name, widget):
            customtkinter.CTkLabel(self.view_frame, text=name, text_color="#6b7280").grid(row=r, column=0, padx=16, pady=10, sticky="w")
            widget.grid(row=r, column=1, padx=16, pady=10, sticky="w")

        row_v(0, "Fullname", self.lbl_fullname_v)
        row_v(1, "Username", self.lbl_username_v)
        row_v(2, "Gmail",    self.lbl_gmail_v)
        row_v(3, "Address",  self.lbl_address_v)
        row_v(4, "Phone",    self.lbl_phone_v)

        # ====== EDIT (แก้ไขข้อมูล) ======
        self.edit_frame = customtkinter.CTkFrame(self.main_area, fg_color="transparent")
        self.edit_frame.grid_columnconfigure(1, weight=1)

        self.ent_fullname = customtkinter.CTkEntry(self.edit_frame, placeholder_text="fullname")
        self.ent_gmail    = customtkinter.CTkEntry(self.edit_frame, placeholder_text="Gmail")
        self.ent_address  = customtkinter.CTkEntry(self.edit_frame, placeholder_text="Address")
        self.ent_phone    = customtkinter.CTkEntry(self.edit_frame, placeholder_text="Phone")

        def row_e(r, name, widget):
            customtkinter.CTkLabel(self.edit_frame, text=name, text_color="#6b7280").grid(
                row=r, column=0, padx=16, pady=10, sticky="w")
            widget.grid(row=r, column=1, padx=16, pady=10, sticky="ew")

        row_e(0, "fullname",self.ent_fullname )
        row_e(1, "Gmail",   self.ent_gmail)
        row_e(2, "Address", self.ent_address)
        row_e(3, "Phone",   self.ent_phone)

        sep = customtkinter.CTkLabel(self.edit_frame, text="— เปลี่ยนรหัสผ่าน (ถ้าต้องการ) —", text_color="#9ca3af")
        sep.grid(row=4, column=0, columnspan=2, pady=(8, 0))

        self.ent_oldpw = customtkinter.CTkEntry(self.edit_frame, placeholder_text="Old password", show="*")
        self.ent_newpw = customtkinter.CTkEntry(self.edit_frame, placeholder_text="New password (≥ 8)", show="*")
        row_e(5, "Old password", self.ent_oldpw)
        row_e(6, "New password", self.ent_newpw)

        btn_bar = customtkinter.CTkFrame(self.edit_frame, fg_color="transparent")
        btn_bar.grid(row=7, column=0, columnspan=2, sticky="e", padx=16, pady=(8, 16))
        customtkinter.CTkButton(btn_bar, text="ยกเลิก", fg_color="#eeeeee", text_color="#111111",
                                command=lambda: self._switch_mode("VIEW")).pack(side="right", padx=6)
        customtkinter.CTkButton(btn_bar, text="บันทึก", fg_color="#00B7FF", text_color="#000000",
                                command=self._save_changes).pack(side="right", padx=6)

        # เริ่มต้นที่ VIEW
        self.view_frame.pack(fill="both", expand=True, padx=12, pady=12)

    # =================== Lifecycle ===================
    def on_show(self):
        if getattr(self.controller, "current_user_id", None) is None:
            CTkMessagebox(title="กรุณาเข้าสู่ระบบ", message="ต้องเข้าสู่ระบบเพื่อดูโปรไฟล์", icon="warning")
            self.controller.show_frame(LoginPage)
            return
        self._reload_view()
        self._load_avatar()

    # =================== Actions ===================
    def _switch_mode(self, mode):
        self.mode = mode
        for w in (self.view_frame, self.edit_frame):
            w.pack_forget()
        if mode == "VIEW":
            self.view_frame.pack(fill="both", expand=True, padx=12, pady=12)
        else:
            # เติมค่าปัจจุบันลงฟอร์ม
            uid = self.controller.current_user_id
            data = Fetch_User_By_ID(uid)
            if data:
                _id, username, role, gmail,fullname, address, phone = data
                self.ent_fullname.delete(0, "end"); self.ent_fullname.insert(0, fullname or "")
                self.ent_gmail.delete(0, "end");   self.ent_gmail.insert(0, gmail or "")
                self.ent_address.delete(0, "end"); self.ent_address.insert(0, address or "")
                self.ent_phone.delete(0, "end");   self.ent_phone.insert(0, phone or "")
                self.ent_oldpw.delete(0, "end");   self.ent_newpw.delete(0, "end")
            self.edit_frame.pack(fill="both", expand=True, padx=12, pady=12)

    def _reload_view(self):
        uid = getattr(self.controller, "current_user_id", None)
        if uid is None:
            return
        data = Fetch_User_By_ID(uid)
        if not data:
            CTkMessagebox(title="Error", message="ไม่พบข้อมูลผู้ใช้", icon="cancel")
            return
        _id, username, role, gmail, fullname, address, phone = data

        self.lbl_fullname_v.configure(text=fullname or "-")   # << เพิ่มบรรทัดนี้
        self.lbl_username_v.configure(text=username or "-")
        self.lbl_gmail_v.configure(text=gmail or "-")
        self.lbl_address_v.configure(text=address or "-")
        self.lbl_phone_v.configure(text=phone or "-")
        self.lbl_username_title.configure(text=fullname or username or "User")  # ใต้ใน sidebar
        self._switch_mode("VIEW")

    def _save_changes(self):
        uid = getattr(self.controller, "current_user_id", None)
        if uid is None:
            return

        fullname = " ".join(self.ent_fullname.get().split()).strip()
        gmail   = self.ent_gmail.get().strip()
        address = self.ent_address.get().strip()
        phone   = self.ent_phone.get().strip()

        if not gmail or "@" not in gmail:
            CTkMessagebox(title="Validation", message="กรุณากรอก Gmail ให้ถูกต้อง", icon="warning"); return
        if not address:
            CTkMessagebox(title="Validation", message="กรุณากรอก Address", icon="warning"); return
        if not phone:
            CTkMessagebox(title="Validation", message="กรุณากรอก Phone", icon="warning"); return

        ok = Update_User_Contacts(uid, gmail, address, phone, fullname)
        if not ok:
            CTkMessagebox(title="Error", message="บันทึกข้อมูลติดต่อไม่สำเร็จ", icon="cancel"); return

        old_pw = self.ent_oldpw.get().strip()
        new_pw = self.ent_newpw.get().strip()
        if old_pw or new_pw:
            success, msg = Update_User_Password(uid, old_pw, new_pw)
            if not success:
                CTkMessagebox(title="เปลี่ยนรหัสผ่าน", message=msg, icon="warning")
            else:
                CTkMessagebox(title="สำเร็จ", message="บันทึกข้อมูลและเปลี่ยนรหัสผ่านเรียบร้อย", icon="check")
        else:
            CTkMessagebox(title="สำเร็จ", message="บันทึกข้อมูลเรียบร้อย", icon="check")

        self._reload_view()

    # =================== Avatar ===================
    def _choose_avatar(self):
        try:
            import tkinter.filedialog as fd
            from PIL import Image
        except Exception:
            CTkMessagebox(title="Error", message="ต้องติดตั้ง Pillow และเปิดใช้งาน filedialog", icon="cancel")
            return

        fpath = fd.askopenfilename(title="เลือกภาพโปรไฟล์",
                                   filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if not fpath:
            return
        uid = getattr(self.controller, "current_user_id", None)
        if uid is None:
            return
        
        # ฟังก์ชันบันทึก avatar ใน DB ให้ใช้
        saved = True
        if "Update_User_Avatar" in globals():
            try:
                saved = Update_User_Avatar(uid, fpath)
            except Exception:
                saved = False
        if not saved:
            CTkMessagebox(title="Warning", message="บันทึกเส้นทางรูปไม่สำเร็จ แต่จะแสดงรูปชั่วคราว", icon="warning")
        # โหลดรูปมาแสดง
        self._load_avatar(fpath)

    def _load_avatar(self, override_path=None):
        try:
            from PIL import Image, ImageDraw
        except Exception:
            return

        uid = getattr(self.controller, "current_user_id", None)
        avatar_path = None

        if override_path:
            avatar_path = override_path
        else:
            # ถ้า DB รองรับการเก็บ path
            if "Fetch_User_Avatar_Path" in globals():
                avatar_path = Fetch_User_Avatar_Path(uid)

        try:
            img = Image.open(avatar_path) if avatar_path else Image.new("RGB", (240, 240), "#d1d5db")
        except Exception:
            img = Image.new("RGB", (240, 240), "#d1d5db")

        # ---  Crop ให้เป็นวงกลม ---
        img = img.convert("RGB")
        img = img.resize((150, 150))  # สามารถเปลี่ยนขนาดได้
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
        img.putalpha(mask)

        # convert เป็น CTkImage
        self._avatar_ctk = customtkinter.CTkImage(light_image=img, size=(150, 150))
        self.avatar_label.configure(image=self._avatar_ctk, text="")

    # =================== Sign out ===================
    def _sign_out(self):
        # ถ้า controller มีเมธอด sign_out ให้ใช้เลย ไม่มีก็ fallback
        if hasattr(self.controller, "sign_out") and callable(self.controller.sign_out):
            self.controller.sign_out()
        else:
            self.controller.current_user_id = None
        CTkMessagebox(title="Signed out", message="ออกจากระบบเรียบร้อย", icon="check")
        self.controller.show_frame(LoginPage)

# =================== Search Page ===================
class SearchPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------- โครงร่าง ----------
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1)

        # =================== Header ===================
        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", bg_color="#bebebe",corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="ew")
        self.Hight_frame.grid_propagate(False)
        for c in range(7):
            self.Hight_frame.grid_columnconfigure(c, weight=0)
        self.Hight_frame.grid_columnconfigure(2, weight=1)

        # โลโก้กลับหน้าแรก
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        self.button_logo = customtkinter.CTkButton(self.Hight_frame, image=self.logo, text="",width=48, height=35, fg_color="#ffffff",
                                                   hover_color="#e0e0e0", corner_radius=12,command=lambda: self.controller.show_frame(main_menu))
        self.button_logo.grid(row=0, column=0, padx=(16, 8), pady=22, sticky="w")

        # ช่องค้นหา (คำค้น)
        self.searchbox = customtkinter.CTkEntry(self.Hight_frame, placeholder_text="ค้นหาชื่อ/หมวดหมู่",width=320, height=30, fg_color="#ffffff",
                                                bg_color="#ffffff", border_width=2,border_color="#000000", corner_radius=15)
        self.searchbox.grid(row=0, column=2, padx=6, pady=22, sticky="e")
        self.searchbox.bind("<Return>", lambda e: self.do_search())

        # ปุ่มค้นหา
        self.search_button = customtkinter.CTkButton(self.Hight_frame, text="ค้นหา",width=80, height=30, fg_color="#ffffff",
                                                     hover_color="#e0e0e0", text_color="#000000",corner_radius=12, command=self.do_search)
        self.search_button.grid(row=0, column=3, padx=(6, 8), pady=22, sticky="e")

        # ปุ่มตะกร้า
        self.cart_image_path = r"D:\python porgramming\project\JPG\Screenshot 2025-09-25 110705.png"
        self.cart_image = customtkinter.CTkImage(Image.open(self.cart_image_path), size=(24, 24))
        self.cart_button = customtkinter.CTkButton(self.Hight_frame, image=self.cart_image, text="",width=36, height=30, fg_color="#ffffff",
                                                   hover_color="#e0e0e0", corner_radius=12,command=lambda: self.controller.show_frame(CartPage))
        self.cart_button.grid(row=0, column=4, padx=6, pady=22, sticky="e")

        # ปุ่มผู้ใช้/โปรไฟล์ (แบบง่าย ไม่ใช้เมนูป๊อปอัปซ้ำ)
        self.account_btn = customtkinter.CTkButton(self.Hight_frame, text="Sign In",width=80, height=30, fg_color="#00B7FF",
                                                   hover_color="#0096D6", text_color="#000000",corner_radius=16,
                                                   command=lambda: self.controller.show_frame(LoginPage))
        self.account_btn.grid(row=0, column=5, padx=(6, 16), pady=22, sticky="e")

        # อัปเดตหัวถ้าล็อกอินแล้ว
        self.update_header()

        # =================== Content ===================
        container = customtkinter.CTkFrame(self, fg_color="#e0e0e0", corner_radius=0)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)

        # แถบฟิลเตอร์ (หมวดหมู่/ช่วงราคา/เรียง)
        self.filter_bar = customtkinter.CTkFrame(container, fg_color="#f3f3f3", corner_radius=14)
        self.filter_bar.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        for i in range(10):
            self.filter_bar.grid_columnconfigure(i, weight=0)
        self.filter_bar.grid_columnconfigure(9, weight=1)

        # หมวดหมู่
        cats = ["All"] + Fetch_Categories()
        self.cat_var = customtkinter.StringVar(value="All")
        customtkinter.CTkLabel(self.filter_bar, text="หมวดหมู่").grid(row=0, column=0, padx=(12, 6), pady=10, sticky="w")
        self.cat_menu = customtkinter.CTkOptionMenu(self.filter_bar, values=cats, variable=self.cat_var,command=lambda *_: self.do_search())
        self.cat_menu.grid(row=0, column=1, padx=(0, 12), pady=10, sticky="w")

        # ราคา
        customtkinter.CTkLabel(self.filter_bar, text="ราคา").grid(row=0, column=2, padx=(12, 6), pady=10, sticky="w")
        self.min_price = customtkinter.CTkEntry(self.filter_bar, placeholder_text="ต่ำสุด", width=90)
        self.max_price = customtkinter.CTkEntry(self.filter_bar, placeholder_text="สูงสุด", width=90)
        self.min_price.grid(row=0, column=3, padx=(0, 6), pady=10)
        self.max_price.grid(row=0, column=4, padx=(0, 12), pady=10)

        # เรียงลำดับ
        customtkinter.CTkLabel(self.filter_bar, text="เรียง").grid(row=0, column=5, padx=(12, 6), pady=10, sticky="w")
        self.sort_var = customtkinter.StringVar(value="ใหม่ล่าสุด")
        self.sort_menu = customtkinter.CTkOptionMenu(self.filter_bar,values=["ใหม่ล่าสุด", "ราคาต่ำ→สูง", "ราคาสูง→ต่ำ", "ชื่อ A→Z"],
                                                     variable=self.sort_var, command=lambda *_: self.do_search())
        self.sort_menu.grid(row=0, column=6, padx=(0, 12), pady=10)

        self.apply_btn = customtkinter.CTkButton(self.filter_bar, text="Apply", width=80,command=self.do_search)
        self.apply_btn.grid(row=0, column=7, padx=(0, 12), pady=10)

        # พื้นที่ผลลัพธ์
        self.results_bg = customtkinter.CTkFrame(container, fg_color="#f3f3f3", corner_radius=18, height=260)
        self.results_bg.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self.results_bg.grid_propagate(False)
        self.results_bg.grid_columnconfigure(0, weight=1)
        self.results_bg.grid_rowconfigure(0, weight=1)

        self.results = customtkinter.CTkScrollableFrame(self.results_bg, fg_color="#f3f3f3", corner_radius=18)
        self.results.grid(row=0, column=0, sticky="nsew")
        self.results.grid_columnconfigure(0, weight=1)

        # สถานะคำค้นล่าสุด (ใช้ตอนมาจากหน้า Home)
        self._boot_keyword = None

    def update_header(self):
        role = getattr(self.controller, "current_user_role", "guest")
        if role == "guest":
            self.account_btn.configure(text="Sign In", fg_color="#00B7FF",hover_color="#0096D6", text_color="#000000",
                                       command=lambda: self.controller.show_frame(LoginPage))
        else:
            self.account_btn.configure(text="Account", fg_color="#FFFFFF",hover_color="#EFEFEF", text_color="#111111",
                                       command=lambda: self.controller.show_frame(ProfilePage))

    # เรียกจากหน้าอื่นเพื่อวางคำค้นตั้งต้น
    def set_boot_keyword(self, kw: str):
        self._boot_keyword = (kw or "").strip()
        self.searchbox.delete(0, "end")
        if self._boot_keyword:
            self.searchbox.insert(0, self._boot_keyword)
        self.do_search()

    def _clear_results(self):
        for w in self.results.winfo_children():
            w.destroy()

    def _sorted_filtered(self, rows):
        # rows: [(id,name,price,stock,category,image_path,description), ...]
        # กรองด้วยราคา
        def parse_int(s):
            try:
                return int(str(s).strip())
            except Exception:
                return None

        mn = parse_int(self.min_price.get())
        mx = parse_int(self.max_price.get())

        out = []
        for r in rows:
            pid, name, price, stock, cat, img, desc = r
            if mn is not None and price < mn:
                continue
            if mx is not None and price > mx:
                continue
            out.append(r)

        # เรียง
        key = self.sort_var.get()
        if key == "ราคาต่ำ→สูง":
            out.sort(key=lambda x: (x[2], -x[0]))              # price asc, then id desc
        elif key == "ราคาสูง→ต่ำ":
            out.sort(key=lambda x: (-x[2], -x[0]))             # price desc
        elif key == "ชื่อ A→Z":
            out.sort(key=lambda x: (str(x[1]).lower(), -x[0])) # name asc
        else:  # ใหม่ล่าสุด
            out.sort(key=lambda x: -x[0])                      # id desc (ล่าสุดก่อน)
        return out

    def do_search(self):
        kw = self.searchbox.get().strip()
        cat = self.cat_var.get().strip()
        
        # ดึงจากฐานข้อมูล
        if cat == "All":
            base_rows = Fetch_Products(kw) if kw else Fetch_Products()
        else:
            # ถ้าเลือกหมวดหมู่ จะใช้ WHERE category = ? ก่อน แล้วค่อยกรองชื่อด้วย kw
            base_rows = Fetch_Products_By_Category(cat)
            if kw:
                k = kw.lower()
                base_rows = [r for r in base_rows if (k in str(r[1]).lower() or k in str(r[4]).lower())]

        rows = self._sorted_filtered(base_rows)
        self.searchbox.delete(0, "end")
        # แสดงผล
        self._clear_results()
        if not rows:
            customtkinter.CTkLabel(self.results, text="ไม่พบผลลัพธ์", text_color="#444444",
                                   font=customtkinter.CTkFont(size=14)).pack(pady=20)
            self.results_bg.configure(height=260)
            return

        max_cols = 6
        # สร้างคอนเทนเนอร์กริดสวย ๆ
        grid_wrap = customtkinter.CTkFrame(self.results, fg_color="#f3f3f3")
        grid_wrap.pack(padx=8, pady=12, fill="x")
        for c in range(max_cols):
            grid_wrap.grid_columnconfigure(c, weight=1)

        for i, (pid, name, price, stock, cat, img_path, desc) in enumerate(rows):
            def make_on_add(n=name, p=price, img=img_path, stk=stock):
                def _add(qty=1):
                    self.controller.cart.add_item(n, int(p), img or "", qty, max_stock=int(stk))
                return _add

            card = ProductCard(grid_wrap,
                               product_id=pid,
                               name=name,
                               price=price,
                               stock=stock,
                               category=cat,
                               image_path=img_path,
                               description=desc,
                               on_add=make_on_add())
            r, c = divmod(i, max_cols)
            card.grid(row=r, column=c, padx=12, pady=12, sticky="n")

        lines = (len(rows) + max_cols - 1) // max_cols
        new_h = max(24 + lines * (320 + 24) + 24, 260)  # ปรับตามความสูงการ์ด
        self.results_bg.configure(height=new_h)

# ====== Login page ========
class LoginPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------- Layout ----------
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # =================== Header ===================
        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", bg_color="transparent",
                                                  corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="nsew")
        self.Hight_frame.grid_propagate(False)
        for H in range(6):
            self.Hight_frame.grid_columnconfigure(H, weight=0)
            self.Hight_frame.grid_columnconfigure(2, weight=1)

        # Logo
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        self.button_logo = customtkinter.CTkButton(self.Hight_frame, image=self.logo, text="", width=48,
                                                   height=35, fg_color="#ffffff", hover_color="#e0e0e0",
                                                   corner_radius=12,
                                                   command=lambda: controller.show_frame(main_menu))
        self.button_logo.grid(row=0, column=0, padx=(16, 8), pady=22, sticky="w")

        # =================== Content ===================
        self.Low_frame = customtkinter.CTkFrame(self, fg_color="#e0e0e0", bg_color="transparent",
                                                corner_radius=0)
        self.Low_frame.grid(row=1, column=0, sticky="nsew")
        for L in range(3):
            self.Low_frame.grid_columnconfigure(L, weight=1)

        # Promotion carousel
        image_paths = [r"D:\python porgramming\project\Promote\login_1.png",r"D:\python porgramming\project\Promote\login_2.png"]
        carousel = ImageCarousel(self.Low_frame, image_paths=image_paths, interval_ms=2500,
                                 autoplay=True, width=900, height=650)
        carousel.grid(row=0, column=0, padx=40, pady=40)

        # login frame
        self.loginframe = customtkinter.CTkFrame(self.Low_frame, width=450, height=650,
                                                 fg_color="white", corner_radius=30)
        self.loginframe.grid(row=0, column=2, padx=40, pady=40)

        # ✅ เรียกหน้า Login view
        self._build_login_view()

    # =====================================================================================
    def _clear_loginframe(self):
        for w in self.loginframe.winfo_children():
            w.destroy()
    # =====================================================================================
    
    def _build_login_view(self):
        # ล้างของเดิมออกก่อนสร้างหน้า Login ใหม่
        self._clear_loginframe()

        # ---------- logo (ในกรอบ login ขวา) ----------
        self.logo_image = (r"D:\python porgramming\project\JPG\logo1 .png")
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(self.logo_image),
                                                 dark_image=Image.open(self.logo_image),size=(156, 110))
        self.logo_label = customtkinter.CTkLabel(self.loginframe, image=self.logo_image,text="", fg_color="#ffffff")
        self.logo_label.place(relx=0.5, rely=0.15, anchor="center")

        # ---------- หัวข้อ Sign In ----------
        self.Sign_In = customtkinter.CTkLabel(self.loginframe, text='Sign In',text_color="#000000", fg_color="#ffffff", bg_color="#ffffff",
                                              font=("Arial", 31.5))
        self.Sign_In.place(relx=0.39, rely=0.25)

        # ---------- Username ----------
        self.Username_Entry = customtkinter.CTkEntry(self.loginframe, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 14),
                                                     text_color="#000000", bg_color="#ffffff", placeholder_text="Username")
        self.Username_Entry.place(relx=0.52, rely=0.425, anchor='center')

        # ---------- Password ----------
        self.Password_Entry = customtkinter.CTkEntry(self.loginframe, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 14),text_color="#000000"
                                                     , bg_color="#ffffff", placeholder_text="Password", show="*")
        self.Password_Entry.place(relx=0.52, rely=0.525, anchor='center')

        # ---------- ปุ่มแสดง/ซ่อนรหัสผ่าน ----------
        self.openeye_image_path = r'D:\python porgramming\project\JPG\open eye 1.png'
        self.closeeye_image_path = r'D:\python porgramming\project\JPG\Close eyes 1.png'
        self.openeye_image = customtkinter.CTkImage(light_image=Image.open(self.openeye_image_path),
                                                    dark_image=Image.open(self.openeye_image_path), size=(20, 15))
        self.closeeye_image = customtkinter.CTkImage(light_image=Image.open(self.closeeye_image_path),
                                                     dark_image=Image.open(self.closeeye_image_path), size=(20, 15))
        self.show_password = False

        def openandclose_password():
            self.show_password = not self.show_password
            if self.show_password:
                self.Password_Entry.configure(show="")
                self.button_eye.configure(image=self.closeeye_image)
            else:
                self.Password_Entry.configure(show="*")
                self.button_eye.configure(image=self.openeye_image)

        self.button_eye = customtkinter.CTkButton(self.loginframe, image=self.openeye_image, text="", width=22, height=15,fg_color="#ffffff"
                                                  , command=openandclose_password, bg_color="#ffffff",hover="false", corner_radius=30)
        self.button_eye.place(relx=0.73, rely=0.523, anchor='center')

        # ---------- ปุ่ม forgot password (ชี้ไปหน้ารีเซ็ต) ----------
        self.button_forgotpassword = customtkinter.CTkButton(self.loginframe, text='forgot password ?', text_color="#D80606",fg_color="#ffffff", width=15, height=10
                                                             , font=("Arial", 12),bg_color="#ffffff", hover="false", command=self._build_reset_view)
        self.button_forgotpassword.place(relx=0.67, rely=0.563, anchor='center')

        # ---------- ฟังก์ชันล็อกอิน ----------
        def connect_database():
            Username = self.Username_Entry.get().strip()
            Password = self.Password_Entry.get().strip()
            if Username == '' or Password == '':
                CTkMessagebox(title="Error", message="All Fields Are Required", icon="cancel")
                return
            elif len(Password) < 8:
                CTkMessagebox(title="Error", message="Password requires a minimum of 8 characters", icon="cancel")
                return
            elif len(Username) < 5:
                CTkMessagebox(title="Error", message="Username requires a minimum of 5 characters", icon="cancel")
                return
            elif not re.search(r"[A-Za-z]", Password) or not re.search(r"\d", Password):
                CTkMessagebox(title="Error", message="Password must include at least 1 letter and 1 number", icon="cancel")
                return
            

            result = login_user(Username, Password)
            if result is None:
                CTkMessagebox(title="Error", message="Invalid username or password", icon="cancel")
                return

            self.Username_Entry.delete(0, "end")
            self.Password_Entry.delete(0, "end")

            user_id, role = result
            self.controller.current_user_id = user_id
            self.controller.current_user_role = role
            CTkMessagebox(title="Success", message=f"Login successful ({role})", icon="check")
            self.controller.frames[main_menu].update_header()
            if role == "admin":
                self.controller.show_frame(AdminPage)
            else:
                self.controller.frames[main_menu].update_header()
                self.controller.show_frame(main_menu)

        # ---------- ปุ่ม SIGN IN ----------
        self.button_SIGN_IN = customtkinter.CTkButton(self.loginframe, text='SIGN IN', width=220, height=50, font=("Arial", 20),fg_color="#00B7FF"
                                                      , corner_radius=32, bg_color="#ffffff",text_color="#000000", command=connect_database)
        self.button_SIGN_IN.place(relx=0.5, rely=0.66, anchor='center')

        # ---------- ปุ่ม SIGN UP ----------
        self.button_SIGN_UP = customtkinter.CTkButton(self.loginframe, text='SIGN UP', width=220, height=50, font=("Arial", 20),fg_color="#00B7FF"
                                                    , bg_color="#ffffff", corner_radius=32, text_color="#000000"
                                                    , command=lambda: self.controller.show_frame(RegisterPage))
        self.button_SIGN_UP.place(relx=0.5, rely=0.75, anchor='center')

    # =====================================================================================
    # ฟังก์ชันเคลียและสร้างหน้า reset password
    def _build_reset_view(self):
        self._clear_loginframe()

        # ---------- logo (ในกรอบ login ขวา) ----------
        logo_path = r"D:\python porgramming\project\JPG\logo1 .png"
        self.login_logo_img = customtkinter.CTkImage(Image.open(logo_path), size=(156, 110))
        self.logo_label = customtkinter.CTkLabel(master=self.loginframe, image=self.login_logo_img,
                                                 text="", fg_color="#ffffff")
        self.logo_label.place(relx=0.5, rely=0.15, anchor="center")

        # ---------- หัวข้อ Reset Password ----------
        Reset_Password = customtkinter.CTkLabel(self.loginframe, text="Reset Password",font=("Arial", 28), text_color="black")
        Reset_Password.place(relx=0.5, rely=0.27, anchor="center")

        # ======= ช่อง Username / Gmail =======
        self.reset_username = customtkinter.CTkEntry(self.loginframe, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 14),text_color="#000000"
                                                     , bg_color="#ffffff", placeholder_text="Username")
        self.reset_username.place(relx=0.5, rely=0.34, anchor="center")

        self.reset_gmail = customtkinter.CTkEntry(self.loginframe, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 14), text_color="#000000"
                                                  , bg_color="#ffffff", placeholder_text="Registered Gmail")
        self.reset_gmail.place(relx=0.5, rely=0.42, anchor="center")

        # ป้ายสถานะตรวจสอบ
        self.verify_status = customtkinter.CTkLabel(self.loginframe, text="", text_color="#444444")
        self.verify_status.place(relx=0.5, rely=0.47, anchor="center")

        # ======= ช่องใส่รหัสผ่านใหม่ (เริ่มต้นปิดไว้) =======
        self.reset_pw = customtkinter.CTkEntry(self.loginframe, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 14),text_color="#000000", bg_color="#ffffff"
                                                , placeholder_text="New Password",show="*", state="disabled")
        self.reset_pw.place(relx=0.5, rely=0.62, anchor="center")

        self.reset_pw2 = customtkinter.CTkEntry(self.loginframe, width=250, height=30, fg_color="#FFFFFF", font=("Arial",14),text_color="#000000", bg_color="#ffffff"
                                                , placeholder_text="Confirm Password",show="*", state="disabled")
        self.reset_pw2.place(relx=0.5, rely=0.68, anchor="center")

        # ======= โหลดรูปตา =======
        eye_open_path = r'D:\python porgramming\project\JPG\open eye 1.png'
        eye_close_path = r'D:\python porgramming\project\JPG\Close eyes 1.png'
        self.eye_open_img_reset = customtkinter.CTkImage(Image.open(eye_open_path), size=(20, 15))
        self.eye_close_img_reset = customtkinter.CTkImage(Image.open(eye_close_path), size=(20, 15))

        # state โชว์/ซ่อน สำหรับสองช่อง
        self._show_pw_1 = False
        self._show_pw_2 = False

        # ======= ปุ่มตา Show/Hide สำหรับแต่ละช่อง =======
        def toggle_pw_1():
            # ไม่สลับถ้ายังเป็นโหมดฮินต์
            if getattr(self.reset_pw, "_is_hint", False):
                return
            self._show_pw_1 = not self._show_pw_1
            self.reset_pw.configure(show="" if self._show_pw_1 else "*")
            self.eye_btn_pw.configure(image=self.eye_close_img_reset if self._show_pw_1 else self.eye_open_img_reset)

        def toggle_pw_2():
            if getattr(self.reset_pw2, "_is_hint", False):
                return
            self._show_pw_2 = not self._show_pw_2
            self.reset_pw2.configure(show="" if self._show_pw_2 else "*")
            self.eye_btn_pw2.configure(image=self.eye_close_img_reset if self._show_pw_2 else self.eye_open_img_reset)

        self.eye_btn_pw = customtkinter.CTkButton(self.loginframe, image=self.eye_open_img_reset, text="", width=22, height=15,fg_color="#ffffff"
                                                  , bg_color="#ffffff", hover="false", corner_radius=30, command=toggle_pw_1, state="disabled")
        self.eye_btn_pw.place(relx=0.71, rely=0.62, anchor="center")

        self.eye_btn_pw2 = customtkinter.CTkButton(self.loginframe, image=self.eye_open_img_reset, text="", width=22, height=15,fg_color="#ffffff"
                                                    ,bg_color="#ffffff", hover="false", corner_radius=30,command=toggle_pw_2, state="disabled")
        self.eye_btn_pw2.place(relx=0.71, rely=0.68, anchor="center")

        # ===== Helper: ใส่/จัดการฮินต์ใน CTkEntry =====
        def _set_hint(entry, msg):
            entry._hint_msg = msg
            entry._is_hint = True
            entry.configure(show="")                 # ให้เห็นข้อความฮินต์ชัดๆ
            entry.configure(text_color="#777777")    # สีเทาอ่อน
            entry.delete(0, "end")
            entry.insert(0, msg)

        def _clear_hint_if_needed(entry):
            if getattr(entry, "_is_hint", False):
                entry.delete(0, "end")
                entry.configure(text_color="#000000")
                entry._is_hint = False
                # ถ้าเป็นช่องรหัส ให้กลับไปซ่อนตาม state ปัจจุบัน
                if entry is self.reset_pw:
                    entry.configure(show="" if self._show_pw_1 else "*")
                elif entry is self.reset_pw2:
                    entry.configure(show="" if self._show_pw_2 else "*")

        def _restore_hint_if_empty(entry):
            if not entry.get().strip() and hasattr(entry, "_hint_msg") and entry._hint_msg:
                _set_hint(entry, entry._hint_msg)

        # bind focus-in/out ให้ 2 ช่องรหัส
        self.reset_pw.bind("<FocusIn>",  lambda e: _clear_hint_if_needed(self.reset_pw))
        self.reset_pw.bind("<FocusOut>", lambda e: _restore_hint_if_empty(self.reset_pw))
        self.reset_pw2.bind("<FocusIn>",  lambda e: _clear_hint_if_needed(self.reset_pw2))
        self.reset_pw2.bind("<FocusOut>", lambda e: _restore_hint_if_empty(self.reset_pw2))

        # ======= ปุ่มตรวจสอบ Username + Gmail =======
        def verify_user():
            u = self.reset_username.get().strip()
            g = self.reset_gmail.get().strip()
            if not u or not g:
                self.verify_status.configure(text="กรุณากรอก Username และ Gmail", text_color="#D80606")
                return
            elif "@" not in g:
                CTkMessagebox(title="Error", message="Gmail must contain '@'", icon="cancel")
                return

            uid = verify_user_email(u, g)
            if uid:
                self._verified_uid = uid
                self.verify_status.configure(text="✅ ยืนยันตัวตนสำเร็จ", text_color="#0a8f19")

                # เปิดช่อง + ปุ่ม
                self.reset_pw.configure(state="normal")
                self.reset_pw2.configure(state="normal")
                self.button_confirm.configure(state="normal")
                self.eye_btn_pw.configure(state="normal")
                self.eye_btn_pw2.configure(state="normal")

                # ใส่ข้อความขึ้นในช่องรหัส (ข้อความจริง ไม่ใช่ placeholder)
                _set_hint(self.reset_pw,  " New Password ")
                _set_hint(self.reset_pw2, " Confrim Password ")
            else:
                self._verified_uid = None
                self.verify_status.configure(text="❌ ไม่พบ Username หรือ Gmail", text_color="#D80606")

                # ปิดกลับ และล้างค่าช่อง/ฮินต์
                for ent in (self.reset_pw, self.reset_pw2):
                    ent.configure(state="disabled", show="")
                    ent.delete(0, "end")
                    ent._is_hint = False
                    ent._hint_msg = ""
                self.button_confirm.configure(state="disabled")
                self.eye_btn_pw.configure(state="disabled")
                self.eye_btn_pw2.configure(state="disabled")

        Chack_Button = customtkinter.CTkButton(self.loginframe, text="Verify", font=("Arial", 17), text_color="black", width=170, height=40,
                                               fg_color="#00B7FF", hover_color="#e6e6e6", corner_radius=32, command=verify_user)
        Chack_Button.place(relx=0.5, rely=0.53, anchor="center")

        # ======= ปุ่มยืนยัน Reset (เปิดหลังตรวจสอบ) =======
        def do_reset():
            if not getattr(self, "_verified_uid", None):
                CTkMessagebox(title="Error", message="กรุณากดปุ่ม 'ตรวจสอบ' ก่อน", icon="cancel")
                return

            # เคลียร์ฮินต์ถ้ามี เพื่อให้ไม่ถือเป็นค่ารหัส
            _clear_hint_if_needed(self.reset_pw)
            _clear_hint_if_needed(self.reset_pw2)

            p1 = self.reset_pw.get().strip()
            p2 = self.reset_pw2.get().strip()
            if not p1 or not p2:
                CTkMessagebox(title="Error", message="กรุณากรอกรหัสผ่านใหม่ให้ครบ", icon="cancel"); return
            if p1 != p2:
                CTkMessagebox(title="Error", message="รหัสผ่านไม่ตรงกัน", icon="cancel"); return
            if len(p1) < 8:
                CTkMessagebox(title="Error", message="รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร", icon="cancel"); return

            if update_user_password(self._verified_uid, p1):
                CTkMessagebox(title="Success", message="อัปเดตรหัสผ่านสำเร็จแล้ว", icon="check")
                self._build_login_view()
            else:
                CTkMessagebox(title="Error", message="อัปเดตไม่สำเร็จ", icon="cancel")

        self.button_confirm = customtkinter.CTkButton(self.loginframe, text="Confirm Reset", width=170, height=40, font=("Arial", 17),fg_color="#00B7FF"
                                                      , bg_color="#ffffff", corner_radius=32, text_color="#000000",command=do_reset, state="disabled")
        self.button_confirm.place(relx=0.5, rely=0.78, anchor="center")

        # ======= ปุ่มกลับไปหน้า Login =======
        Back_Button = customtkinter.CTkButton(self.loginframe, text="Back", font=("Arial", 14), fg_color="#F3F3F3", bg_color="#ffffff"
                                              ,corner_radius=32, text_color="#000000", hover_color="#ebebeb", width=60,command=self._build_login_view)
        Back_Button.place(relx=0.1, rely=0.96, anchor="center")
   
# ====== Register page ========
class RegisterPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ---------- โครงร่างหลักแบบ Responsive ด้วย grid ----------
        self.grid_rowconfigure(0, weight=0)  # Header สูงคงที่
        self.grid_rowconfigure(1, weight=1)  # Content ขยายเต็มที่
        self.grid_columnconfigure(0, weight=1)
        # =================== Header ===================
        self.Hight_frame = customtkinter.CTkFrame(master=self, fg_color="#ffffff", bg_color="transparent",corner_radius=0, height=80)
        self.Hight_frame.grid(row=0, column=0, sticky="nsew")
        self.Hight_frame.grid_propagate(False)  
        # จัดคอลัมน์ภายใน Header (โลโก้ | เว้น | เว้น | เว้น | ค้นหา  |ปุ่มค้นหา )
        for H in range(6):
            self.Hight_frame.grid_columnconfigure(H, weight=0)
            self.Hight_frame.grid_columnconfigure(2, weight=1)  

        self.Low_frame = customtkinter.CTkFrame(master=self, fg_color="#e0e0e0", bg_color="transparent", corner_radius=0)
        self.Low_frame.grid(row=2, column=0, sticky="nsew")
        for L in range(2):
            self.Low_frame.grid_columnconfigure(L,weight=0)
            self.Low_frame.grid_columnconfigure(2,weight=2)

        # Logo
        self.logo_image = r"D:\python porgramming\project\JPG\logo1 .png"
        self.logo = customtkinter.CTkImage(Image.open(self.logo_image), size=(48, 35))
        self.button_logo = customtkinter.CTkButton(master=self.Hight_frame, image=self.logo, text="",width=48, height=35, fg_color="#ffffff", hover_color="#e0e0e0", corner_radius=12)
        self.button_logo.grid(row=0, column=0, padx=(16, 8), pady=22, sticky="w")

        # Sign Up Frame
        self.Sign_Up_Frame=customtkinter.CTkFrame(master=self.Low_frame,fg_color="#ffffff", bg_color="transparent",corner_radius=30, width=500 , height=650)
        self.Sign_Up_Frame.grid(row=0, column=2,padx=40,pady=40)

        #หัวข้อ Sign Up
        self.Sign_Up=customtkinter.CTkLabel(master=self.Sign_Up_Frame, text='Sign Up', text_color="#000000",fg_color="#ffffff",bg_color="#ffffff", font=("Arial", 31.5))
        self.Sign_Up.place(relx=0.39, rely=0.03)

        # full name
        self.Full_Name_Entry = customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30,fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000",bg_color="#ffffff"
                                                     ,placeholder_text="Full Name")
        self.Full_Name_Entry.place(relx=0.52, rely=0.15,anchor='center')

        #  username 
        self.Username_Entry = customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30,fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000",bg_color="#ffffff"
                                                     ,placeholder_text="Username")
        self.Username_Entry.place(relx=0.52, rely=0.25,anchor='center')

        #  password 
        self.Password_Entry = customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30,fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000",bg_color="#ffffff"
                                                     ,placeholder_text="Password")
        self.Password_Entry.place(relx=0.52, rely=0.35, anchor='center')
        
        # รูป ปุ่มแสดง/ซ่อนรหัสผ่าน 
        self.openeye_image_path = (r'D:\python porgramming\project\JPG\open eye 1.png')
        self.closeeye_image_path = (r'D:\python porgramming\project\JPG\Close eyes 1.png')
        self.openeye_image = customtkinter.CTkImage(light_image=Image.open(self.openeye_image_path),dark_image=Image.open(self.openeye_image_path), size=(22, 15))
        self.closeeye_image = customtkinter.CTkImage(light_image=Image.open(self.closeeye_image_path), dark_image=Image.open(self.closeeye_image_path), size=(22, 15))

        # เปิด/ปิด ตา  Password
        self.show_password = False
        self.Password_Entry.configure(show="*")
        def openandclose_password():
            self.show_password = not self.show_password
            if self.show_password:
                self.Password_Entry.configure(show="")
                self.button_eye_password.configure(image=self.closeeye_image)
            else:
                self.Password_Entry.configure(show="*")
                self.button_eye_password.configure(image=self.openeye_image)
        self.openandclose_password = openandclose_password

        self.button_eye_password = customtkinter.CTkButton(master=self.Sign_Up_Frame, image=self.openeye_image, text="",width=25, height=18,fg_color="#ffffff",bg_color="#ffffff",hover="false"
                                                           ,command=self.openandclose_password)
        self.button_eye_password.place(relx=0.73, rely=0.35, anchor='center')

        # Confram password
        self.confirm_password_Entry = customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000", bg_color="#ffffff"
                                                             ,placeholder_text="Confram password")
        self.confirm_password_Entry.place(relx=0.52, rely=0.45, anchor='center')

        # เปิด/ปิด ตา  Confram Password
        self.show_confirm_password = False
        self.confirm_password_Entry.configure(show="*")
        def open_and_close_confirm_password():
            self.show_confirm_password = not self.show_confirm_password
            if self.show_confirm_password:
                self.confirm_password_Entry.configure(show="")
                self.button_eye_confirm.configure(image=self.closeeye_image)
            else:
                self.confirm_password_Entry.configure(show="*")
                self.button_eye_confirm.configure(image=self.openeye_image)
        self.open_and_close_confirm_password = open_and_close_confirm_password

        self.button_eye_confirm = customtkinter.CTkButton(master=self.Sign_Up_Frame, image=self.openeye_image, text="",width=25, height=18, fg_color="#ffffff",hover="false"
                                                        ,command=self.open_and_close_confirm_password)
        self.button_eye_confirm.place(relx=0.73, rely=0.45,anchor='center')

        # Gmail
        self.gmail_Entry=customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000", bg_color="#ffffff"
                                                ,placeholder_text="Gmail")
        self.gmail_Entry.place(relx=0.52, rely=0.55, anchor='center')

        #Address
        self.Address_Entry=customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000", bg_color="#ffffff"
                                                  ,placeholder_text="Address")
        self.Address_Entry.place(relx=0.52, rely=0.65, anchor='center')

        #phone Number
        self.Phone_Entry=customtkinter.CTkEntry(master=self.Sign_Up_Frame, width=250, height=30, fg_color="#FFFFFF", font=("Arial", 16), text_color="#000000", bg_color="#ffffff"
                                                ,placeholder_text="Phone Number")
        
        vcmd = (self.register(lambda P: P.isdigit() or P == ""), "%P")
        self.Phone_Entry.configure(validate="key", validatecommand=vcmd)
        self.Phone_Entry.place(relx=0.52, rely=0.75, anchor='center')

        def connect_database():
            Full_Name_input = self.Full_Name_Entry.get().strip()
            Username_input = self.Username_Entry.get().strip()
            Password_input = self.Password_Entry.get().strip()
            Confirm_input = self.confirm_password_Entry.get().strip()
            Gmail_input = self.gmail_Entry.get().strip()
            Address_input = self.Address_Entry.get().strip()
            Phone_input = self.Phone_Entry.get().strip()

            if Full_Name_input =='' or Username_input =='' or Password_input == '' or Confirm_input == '' or Gmail_input == '' or Address_input =='' or Phone_input =='':
                CTkMessagebox(title="Error", message="All Fields Are Required", icon="cancel")
                return
            elif len(Username_input) < 6 :
                CTkMessagebox(title="Error", message="Password requires a minimum of 6 characters",icon="cancel")   
                return
            elif len(Password_input) < 8:
                CTkMessagebox(title="Error", message="Password requires a minimum of 8 characters",icon="cancel")   
                return
            elif not re.search(r"[A-Za-z]", Password_input) or not re.search(r"\d", Password_input):
                CTkMessagebox(title="Error", message="Password must include at least 1 letter and 1 number", icon="cancel")
                return
            elif Password_input != Confirm_input:
                CTkMessagebox(title="Error", message="Password confirmation dose not match",icon="cancel")
                return
            elif not Phone_input.isdigit() or len(Phone_input) != 10:
                CTkMessagebox(title="Error", message="Phone must be 10 digits", icon="cancel")
                return
            elif "@" not in Gmail_input:
                CTkMessagebox(title="Error", message="Gmail must contain '@'", icon="cancel")
                return
          
            status = register_user(Full_Name_input,Username_input, Password_input, role="user",Gmail= Gmail_input,Address = Address_input, Phone=Phone_input)
            if not status:
                CTkMessagebox(title="Error", message="Username already exists", icon="cancel")
                return
            
            self.Full_Name_Entry.delete(0, "end")
            self.Username_Entry.delete(0, "end")
            self.Password_Entry.delete(0, "end")
            self.confirm_password_Entry.delete(0, "end")
            self.gmail_Entry.delete(0, "end")
            self.Address_Entry.delete(0, "end") 
            self.Phone_Entry.delete(0, "end")

            CTkMessagebox(title="Success", message="Account created. Please sign in.", icon="check")
            self.controller.show_frame(LoginPage)   
        self.button_SIGN_UP = customtkinter.CTkButton(master=self.Sign_Up_Frame,text='SIGN UP',text_color="#000000",width=220,height=50,font=("Arial", 20),fg_color="#00B7FF",bg_color="#ffffff"
                                                      ,corner_radius=32,command=connect_database)
        self.button_SIGN_UP.place(relx=0.5, rely=0.85, anchor='center')
        Alredy_have_on_account=customtkinter.CTkLabel(master=self.Sign_Up_Frame,text="Alredy have on account ")
        Alredy_have_on_account.place(relx=0.43, rely=0.93, anchor='center')
        self.button_back_to_Sign_in=customtkinter.CTkButton(master=self.Sign_Up_Frame,text="Sign in", text_color="#D80606",fg_color="#ffffff", width=15, height=10
                                                            ,font=("Arial", 12),bg_color="#ffffff",hover="false",command=lambda: self.controller.show_frame(LoginPage))
        self.button_back_to_Sign_in.place(relx=0.62, rely=0.93, anchor='center')

# ====== Admin page ========
class AdminPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.categories = ["Monitor", "Keyboard", "Mouse", "Mousepad", "Headphone", "Microphone", "Controller"]

        # ---------- ค่าตั้งต้นรูป ----------
        self.Thumb_Size = (80, 80)
        self._ThumbCache = {}
        self.Selected_Order_ID = None
        self.Order_Detail_Frame = None

        # ---------- โครงร่างหลัก ----------
        self.grid_rowconfigure(0, weight=0)   # Header
        self.grid_rowconfigure(1, weight=0)   # Controls
        self.grid_rowconfigure(2, weight=1)   # Content
        self.grid_columnconfigure(0, weight=1)

        # =================== Header ===================
        self.Hight_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=72)
        self.Hight_frame.grid(row=0, column=0, sticky="ew")
        self.Hight_frame.grid_propagate(False)
        for c in range(4):
            self.Hight_frame.grid_columnconfigure(c, weight=0)
        self.Hight_frame.grid_columnconfigure(2, weight=1)

        self.Admin_Title = customtkinter.CTkLabel(self.Hight_frame, text="Admin Dashboard",
                                                  font=customtkinter.CTkFont(size=22, weight="bold"))
        self.Admin_Title.grid(row=0, column=0, padx=16, pady=18, sticky="w")

        self.Back_Home_Button = customtkinter.CTkButton(self.Hight_frame, text="Back to Home",
                                                        command=lambda: controller.show_frame(main_menu))
        self.Back_Home_Button.grid(row=0, column=3, padx=16)

        # =================== Controls (โหมด + ค้นหา) ===================
        self.Low_frame = customtkinter.CTkFrame(self, fg_color="#f7f9fc", corner_radius=12)
        self.Low_frame.grid(row=1, column=0, padx=16, pady=(10, 8), sticky="ew")
        for c in range(4):
            self.Low_frame.grid_columnconfigure(c, weight=0)
        self.Low_frame.grid_columnconfigure(2, weight=1)

        self.Mode_Var = customtkinter.StringVar(value="ADD")
        self.Mode_Segment = customtkinter.CTkSegmentedButton(self.Low_frame,values=["ADD", "EDIT", "DELETE", "ORDER", "Sales Report"],
                                                            variable=self.Mode_Var,command=self.On_Mode_Change  )
        self.Mode_Segment.grid(row=0, column=0, padx=(12, 8), pady=10)

        self.Search_Entry = customtkinter.CTkEntry(self.Low_frame, placeholder_text="ค้นหาด้วยชื่อหรือหมวดหมู่...")
        self.Search_Entry.grid(row=0, column=2, padx=8, pady=10, sticky="ew")

        self.Search_Button = customtkinter.CTkButton(self.Low_frame, text="Search", command=self.Refresh_List)
        self.Search_Button.grid(row=0, column=3, padx=(8, 12), pady=10)

        # =================== Content ===================
        self.Content_Container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.Content_Container.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self.Content_Container.grid_rowconfigure(0, weight=1)
        self.Content_Container.grid_columnconfigure(0, weight=1)
        self.Content_Container.grid_columnconfigure(1, weight=0)

        self.Product_List_Frame  = None
        self.Product_Form_Frame  = None
        self.Order_Detail_Frame  = None
        self.Report_Frame        = None

        self._ensure_frames()
        self.Editing_Product_ID = None
        self.current_mode = None
        self.On_Mode_Change("ADD")


    # ---------- เฉพาะแอดมิน ----------
    def on_show(self):
        if getattr(self.controller, "current_user_role", "guest") != "admin":
            CTkMessagebox(title="Permission denied", message="Admins only.", icon="cancel")
            self.controller.show_frame(main_menu)

    def _ensure_frames(self):
        # ซ้าย: ลิสต์
        if self.Product_List_Frame is None or not self.Product_List_Frame.winfo_exists():
            self.Product_List_Frame = customtkinter.CTkScrollableFrame(
                self.Content_Container, fg_color="#ffffff", corner_radius=14, width=700
            )

        # ขวา: ฟอร์มสินค้า
        if self.Product_Form_Frame is None or not self.Product_Form_Frame.winfo_exists():
            self.Product_Form_Frame = customtkinter.CTkScrollableFrame(
                self.Content_Container, fg_color="#ffffff", corner_radius=14,
                width=420, height=560, label_text=""
            )
            self.Product_Form_Frame.grid_columnconfigure(0, weight=0)
            self.Product_Form_Frame.grid_columnconfigure(1, weight=1)
            self._Build_Product_Form()

        # ขวา: รายละเอียดออเดอร์
        if self.Order_Detail_Frame is None or not self.Order_Detail_Frame.winfo_exists():
            self.Order_Detail_Frame = customtkinter.CTkScrollableFrame(self.Content_Container, fg_color="#ffffff", corner_radius=14, width=520, height=560)

        # รายงาน
        if self.Report_Frame is None or not self.Report_Frame.winfo_exists():
            self.Report_Frame = customtkinter.CTkFrame(self.Content_Container,fg_color="#ffffff",corner_radius=14)

    def _hide_all_content(self):
        for w in self.Content_Container.winfo_children():
            try:
                w.grid_forget()
            except Exception:
                pass

    # ---------- ฟอร์มสินค้า ----------
    def _Build_Product_Form(self):
        if not hasattr(self, "Product_Form_Frame") or not self.Product_Form_Frame.winfo_exists():
            self.Product_Form_Frame = customtkinter.CTkScrollableFrame(
                self.Content_Container, fg_color="#ffffff", corner_radius=14,
                width=420, height=560, label_text=""
            )
            self.Product_Form_Frame.grid(row=0, column=1, sticky="nsew")
            self.Product_Form_Frame.grid_columnconfigure(0, weight=0)
            self.Product_Form_Frame.grid_columnconfigure(1, weight=1)
        else:
            for w in self.Product_Form_Frame.winfo_children():
                w.destroy()

        # ===== หัวเรื่อง =====
        self.Form_Title = customtkinter.CTkLabel(self.Product_Form_Frame, text="Product Form", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.Form_Title.grid(row=0, column=1, columnspan=2, padx=16, pady=(16, 6), sticky="w")

        # ===== Name =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Name").grid(row=1, column=0, padx=(16, 4), pady=6, sticky="w")
        self.Product_Name_Entry = customtkinter.CTkEntry(self.Product_Form_Frame)
        self.Product_Name_Entry.grid(row=1, column=1, padx=16, pady=6, sticky="ew")

        # ===== Price =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Price").grid(row=2, column=0, padx=(16, 4), pady=6, sticky="w")
        self.Price_Entry = customtkinter.CTkEntry(self.Product_Form_Frame)
        self.Price_Entry.grid(row=2, column=1, padx=16, pady=6, sticky="ew")

        # ===== Stock =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Stock").grid(row=3, column=0, padx=(16, 4), pady=6, sticky="w")
        self.Stock_Entry = customtkinter.CTkEntry(self.Product_Form_Frame)
        self.Stock_Entry.grid(row=3, column=1, padx=16, pady=6, sticky="ew")

        # ===== Category =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Category").grid(row=4, column=0, padx=(16, 4), pady=6, sticky="w")
        self.Category_Var = customtkinter.StringVar(value=self.categories[0])
        self.Category_Option = customtkinter.CTkOptionMenu(self.Product_Form_Frame, values=self.categories, variable=self.Category_Var)
        self.Category_Option.grid(row=4, column=1, padx=16, pady=6, sticky="ew")

        # ===== Image Path + Browse =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Image Path").grid(row=5, column=0, padx=(16, 4), pady=6, sticky="w")
        self.Image_Wrap = customtkinter.CTkFrame(self.Product_Form_Frame, fg_color="transparent")
        self.Image_Wrap.grid(row=5, column=1, padx=16, pady=6, sticky="ew")
        self.Image_Wrap.grid_columnconfigure(0, weight=1)

        self.Image_Path_Entry = customtkinter.CTkEntry(self.Image_Wrap)
        self.Image_Path_Entry.grid(row=0, column=0, sticky="ew")
        self.Image_Path_Entry.bind("<KeyRelease>", lambda e: self._Update_Form_Preview())

        self.Browse_Image_Button = customtkinter.CTkButton(self.Image_Wrap, text="Browse", command=self._Pick_Image)
        self.Browse_Image_Button.grid(row=0, column=1, padx=(6, 0))

        # ===== Preview =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Preview", font=customtkinter.CTkFont(size=14)).grid(row=6, column=0, padx=(16, 4), pady=(8, 0), sticky="w")
        self.Image_Preview_Frame = customtkinter.CTkFrame(self.Product_Form_Frame, fg_color="#f7f7f7", corner_radius=12)
        self.Image_Preview_Frame.grid(row=6, column=1, padx=16, pady=(8, 6), sticky="nsew")
        self.Image_Preview_Frame.grid_columnconfigure(0, weight=1)
        self.Image_Preview_Frame.grid_rowconfigure(0, weight=1)
        self.Image_Preview_Label = customtkinter.CTkLabel(self.Image_Preview_Frame, text="(no image)")
        self.Image_Preview_Label.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        # ===== Description =====
        customtkinter.CTkLabel(self.Product_Form_Frame, text="Description").grid(row=7, column=0, padx=16, pady=6, sticky="w")
        self.Description_Text = customtkinter.CTkTextbox(self.Product_Form_Frame, height=180)
        self.Description_Text.grid(row=7, column=1, padx=16, pady=6, sticky="nsew")

        # ===== Buttons =====
        self.Button_Reset = customtkinter.CTkButton(self.Product_Form_Frame, text="Reset", fg_color="#eeeeee", text_color="#000000", command=self._Clear_Form)
        self.Button_Reset.grid(row=9, column=0, padx=16, pady=12, sticky="w")

        self.Button_Save = customtkinter.CTkButton(self.Product_Form_Frame, text="Save", command=self.On_Save)
        self.Button_Save.grid(row=9, column=1, padx=16, pady=12, sticky="e")
    
    # ---------- Helper รูป ----------
    def _Get_Thumb(self, Path, Size=None):
        Size = Size or self.Thumb_Size
        key = (Path or "", Size)
        if key in self._ThumbCache:
            return self._ThumbCache[key]
        try:
            pil = Image.open(Path).convert("RGBA")
            pil.thumbnail(Size, Image.LANCZOS)
        except Exception:
            pil = Image.new("RGBA", Size, (220, 220, 220, 255))  # placeholder เทา
        img = customtkinter.CTkImage(light_image=pil, dark_image=pil, size=Size)
        self._ThumbCache[key] = img
        return img

    def _Open_Preview(self, Path):
        try:
            pil = Image.open(Path).convert("RGBA")
        except Exception:
            CTkMessagebox(title="Preview", message="ไม่พบไฟล์รูปภาพ", icon="warning")
            return
        w, h = pil.size
        scale = min(900 / max(w, 1), 700 / max(h, 1), 1.0)
        disp = pil.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        im = customtkinter.CTkImage(light_image=disp, dark_image=disp, size=(disp.width, disp.height))

        top = customtkinter.CTkToplevel(self)
        top.title("Preview")
        lab = customtkinter.CTkLabel(top, image=im, text="")
        lab.image = im
        lab.pack(padx=12, pady=12)
        top.focus_set()

    def _Pick_Image(self):
        f = fd.askopenfilename(title="เลือกไฟล์รูปภาพ",
                               filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp;*.gif")])
        if f:
            self.Image_Path_Entry.delete(0, "end")
            self.Image_Path_Entry.insert(0, f)
            self._Update_Form_Preview()

    def _Update_Form_Preview(self):
        path = self.Image_Path_Entry.get().strip()
        if not path:
            self.Image_Preview_Label.configure(text="(no image)", image=None)
            self.Image_Preview_Label.image = None
            return
        try:
            pil = Image.open(path).convert("RGBA")
            max_w, max_h = 360, 220
            scale = min(max_w / max(1, pil.width), max_h / max(1, pil.height), 1.0)
            disp = pil.resize((int(pil.width * scale), int(pil.height * scale)), Image.LANCZOS)
            im = customtkinter.CTkImage(light_image=disp, dark_image=disp, size=(disp.width, disp.height))
            self.Image_Preview_Label.configure(text="", image=im)
            self.Image_Preview_Label.image = im
        except Exception:
            self.Image_Preview_Label.configure(text="(cannot open image)", image=None)
            self.Image_Preview_Label.image = None

    # ---------- โหมด ----------
    def On_Mode_Change(self, new_mode=None, *_):
        # อัปเดตค่าโหมดจาก segmented button หากส่งมาเป็นสตริง
        if isinstance(new_mode, str):
            self.Mode_Var.set(new_mode)

        mode = self.Mode_Var.get()

        # กันรีเฟรชซ้ำๆ โดยไม่จำเป็น (ถ้าต้องการจะคอมเมนต์ทิ้งก็ได้)
        if getattr(self, "current_mode", None) == mode and \
        (self.Product_List_Frame is not None and self.Product_List_Frame.winfo_ismapped()):
            return
        self.current_mode = mode

        # รีเซ็ต layout base
        self.Content_Container.grid_columnconfigure(0, weight=1, minsize=0)
        self.Content_Container.grid_columnconfigure(1, weight=1, minsize=0)
        self.Content_Container.grid_rowconfigure(0, weight=1)

        # ซ่อนทั้งหมดก่อน
        self._hide_all_content()

        # เคลียร์ลิสต์ซ้าย และสถานะ
        for w in self.Product_List_Frame.winfo_children():
            w.destroy()
        if mode == "ORDER":
            self.Selected_Order_ID = None
        self.Editing_Product_ID = None
        self._Clear_Form()

        # ปรับปุ่ม Save ให้สื่อสารโหมด
        if hasattr(self, "Button_Save"):
            if mode == "ADD":
                self.Button_Save.configure(text="Save (Add)")
            elif mode == "EDIT":
                self.Button_Save.configure(text="Save (Update)")
            elif mode == "DELETE":
                self.Button_Save.configure(text="Confirm Delete")
            elif mode == "ORDER":
                self.Button_Save.configure(text="(Orders List)")
            elif mode == "Sales Report":
                self.Button_Save.configure(text="(Report)")

        # วางเฟรมตามโหมด
        if mode == "ORDER":
            self.Product_List_Frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
            self.Order_Detail_Frame.grid(row=0, column=1, sticky="nsew")
        elif mode == "Sales Report":
            self.Content_Container.grid_columnconfigure(0, weight=1)   # ให้กินทั้งจอ
            self.Content_Container.grid_columnconfigure(1, weight=0)   # ไม่มีฝั่งขวา
            self.Report_Frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=(0,0))
        else:
            self.Product_List_Frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
            self.Product_Form_Frame.grid(row=0, column=1, sticky="nsew")

        # เติมข้อมูลตามโหมด
        self.update_idletasks()
        self.Refresh_List()

    # ---------- รายการซ้าย ----------
    def Refresh_List(self):
        for w in self.Product_List_Frame.winfo_children():
            w.destroy()

        Mode = self.Mode_Var.get()

        # ========== โหมด ORDER: แบ่งซ้าย/ขวา ==========
        if Mode == "ORDER":
            orders = Fetch_All_Orders()
            if not orders:
                customtkinter.CTkLabel(self.Product_List_Frame, text="ยังไม่มีออเดอร์", text_color="#666").pack(pady=20)
                if self.Order_Detail_Frame and self.Order_Detail_Frame.winfo_exists():
                    for w in self.Order_Detail_Frame.winfo_children():
                        w.destroy()
                return

            for (oid, odate, uname, status, total, addr_snap, slip) in orders:
                row = customtkinter.CTkFrame(self.Product_List_Frame, fg_color="#ffffff", corner_radius=12)
                row.pack(fill="x", padx=12, pady=8)

                head = f"#{oid} | {odate} | by {uname} | {status} | ฿{CartModel.fmt_price(total)}"
                customtkinter.CTkLabel(
                    row, text=head, font=customtkinter.CTkFont(size=13, weight="bold")
                ).grid(row=0, column=0, padx=10, pady=(8, 2), sticky="w")

                customtkinter.CTkLabel(
                    row, text=(addr_snap or ""), justify="left", text_color="#555"
                ).grid(row=1, column=0, padx=10, pady=(0, 8), sticky="w")

                def _bind_row_click(widget, _oid=oid):
                    widget.bind("<Button-1>", lambda e, x=_oid: self._render_order_detail(x))

                _bind_row_click(row)
                for child in row.winfo_children():
                    _bind_row_click(child)

            # เลือกออเดอร์เดิมถ้ายังอยู่, ไม่งั้นเลือกตัวแรก
            ids = [o[0] for o in orders]
            if self.Selected_Order_ID in ids:
                self._render_order_detail(self.Selected_Order_ID)
            else:
                self.Selected_Order_ID = None
                if orders:
                    self._render_order_detail(orders[0][0])
            return

        # ========== โหมด Sales Report ==========
        if Mode == "Sales Report":
            # ซ่อนกรอบรายละเอียดออเดอร์ฝั่งขวา (ถ้ามี)

            # ให้แน่ใจว่ามี Report_Frame (ถูกสร้างใน On_Mode_Change แล้ว)
            if not hasattr(self, "Report_Frame") or not self.Report_Frame.winfo_exists():
                self.Report_Frame = customtkinter.CTkFrame(self.Content_Container, fg_color="#ffffff", corner_radius=14)

            parent = self.Report_Frame

            # รีเซ็ต layout base ของ parent ทุกครั้ง (กันหดเวลาสลับโหมดไปมา)
            parent.grid_columnconfigure(0, weight=1, minsize=0)
            parent.grid_rowconfigure(0, weight=0, minsize=0)  # แถว control
            parent.grid_rowconfigure(1, weight=1, minsize=0)  # แถวตาราง

            # เคลียร์ของเก่าใน Report_Frame
            for w in parent.winfo_children():
                w.destroy()

            # ---------- แถวควบคุม ----------
            ctrl = customtkinter.CTkFrame(parent, fg_color="#ffffff", corner_radius=12)
            ctrl.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 6))

            customtkinter.CTkLabel(ctrl, text="Sales Report", font=customtkinter.CTkFont(size=15, weight="bold")).grid(row=0, column=0, padx=12, pady=10, sticky="w")

            self.Report_Mode = getattr(self, "Report_Mode", customtkinter.StringVar(value="Daily"))
            customtkinter.CTkSegmentedButton(ctrl, values=["Daily", "Monthly", "Yearly"], variable=self.Report_Mode
            ).grid(row=0, column=1, padx=8, pady=10, sticky="w")

            import datetime
            now = datetime.datetime.now()
            years  = [str(y) for y in range(now.year - 5, now.year + 1)]
            months = [f"{m:02d}" for m in range(1, 13)]
            days   = [f"{d:02d}" for d in range(1, 32)]

            self.Year_Var  = getattr(self, "Year_Var",  customtkinter.StringVar(value=str(now.year)))
            self.Month_Var = getattr(self, "Month_Var", customtkinter.StringVar(value=f"{now.month:02d}"))
            self.Day_Var   = getattr(self, "Day_Var",   customtkinter.StringVar(value=f"{now.day:02d}"))

            customtkinter.CTkLabel(ctrl, text="Year").grid(row=1, column=0, padx=(16, 6), pady=8, sticky="w")
            customtkinter.CTkOptionMenu(ctrl, values=years, variable=self.Year_Var, width=90)\
                .grid(row=1, column=1, padx=(0, 12), pady=8, sticky="w")

            customtkinter.CTkLabel(ctrl, text="Month").grid(row=1, column=2, padx=(0, 6), pady=8, sticky="w")
            customtkinter.CTkOptionMenu(ctrl, values=months, variable=self.Month_Var, width=80)\
                .grid(row=1, column=3, padx=(0, 12), pady=8, sticky="w")

            customtkinter.CTkLabel(ctrl, text="Day").grid(row=1, column=4, padx=(0, 6), pady=8, sticky="w")
            customtkinter.CTkOptionMenu(ctrl, values=days, variable=self.Day_Var, width=80)\
                .grid(row=1, column=5, padx=(0, 12), pady=8, sticky="w")
            
            customtkinter.CTkButton(ctrl, text="Generate", command=lambda: _do_report())\
                .grid(row=1, column=6, padx=12, pady=8, sticky="w")

            # ---------- ตารางผลลัพธ์ ----------
            table = customtkinter.CTkScrollableFrame(parent, fg_color="#ffffff", corner_radius=12)
            table.grid(row=1, column=0, sticky="nsew", padx=12, pady=(6, 12))

            # คอลัมน์ของ table เดียวกันทั้งหัว/ข้อมูล/สรุป
            table.grid_columnconfigure(0, weight=3, uniform="rpt")  # สินค้า
            table.grid_columnconfigure(1, weight=1, uniform="rpt")  # จำนวนขาย
            table.grid_columnconfigure(2, weight=1, uniform="rpt")  # รายได้รวม

            # ===== Header (อยู่ใน table โดยตรงที่ row=0) =====
            customtkinter.CTkLabel(table, text="สินค้า")\
                .grid(row=0, column=0, padx=(12, 6), pady=(6, 4), sticky="w")
            customtkinter.CTkLabel(table, text="จำนวนขาย", anchor="e", justify="right")\
                .grid(row=0, column=1, padx=(6, 6),  pady=(6, 4), sticky="e")
            customtkinter.CTkLabel(table, text="รายได้รวม", anchor="e", justify="right")\
                .grid(row=0, column=2, padx=(6, 12), pady=(6, 4), sticky="e")

            def _render_table_rows(rows):
                # เคลียร์ row >= 1 (คง header แถว 0)
                for w in table.winfo_children():
                    info = w.grid_info()
                    if info and int(info.get("row", 0)) >= 1:
                        w.destroy()

                r = 1
                total_qty = 0
                total_rev = 0

                # ===== แถวข้อมูล =====
                for (name, qty, rev) in rows:
                    customtkinter.CTkLabel(table, text=name)\
                        .grid(row=r, column=0, padx=(12, 6), pady=6, sticky="w")
                    customtkinter.CTkLabel(table, text=str(qty), anchor="e", justify="right")\
                        .grid(row=r, column=1, padx=(6, 6),  pady=6, sticky="e")
                    customtkinter.CTkLabel(table, text=f"฿{CartModel.fmt_price(rev)}", anchor="e", justify="right")\
                        .grid(row=r, column=2, padx=(6, 12), pady=6, sticky="e")
                    total_qty += int(qty)
                    total_rev += int(rev)
                    r += 1

                # ===== แถวสรุป (ยังอยู่ใน table เดียวกัน) =====
                customtkinter.CTkLabel(table, text="รวมทั้งหมด",
                                    font=customtkinter.CTkFont(weight="bold"))\
                    .grid(row=r, column=0, padx=(12, 6), pady=(8, 12), sticky="w")
                customtkinter.CTkLabel(table, text=str(total_qty),
                                    font=customtkinter.CTkFont(weight="bold"), anchor="e", justify="right")\
                    .grid(row=r, column=1, padx=(6, 6),  pady=(8, 12), sticky="e")
                customtkinter.CTkLabel(table, text=f"฿{CartModel.fmt_price(total_rev)}",
                                    font=customtkinter.CTkFont(weight="bold"), anchor="e", justify="right")\
                    .grid(row=r, column=2, padx=(6, 12), pady=(8, 12), sticky="e")


            def _do_report():
                mode = self.Report_Mode.get()
                y = int(self.Year_Var.get())
                m = int(self.Month_Var.get())
                d = int(self.Day_Var.get())
                if mode == "Daily":
                    rows = Query_Top_Selling("day", y, m, d)
                elif mode == "Monthly":
                    rows = Query_Top_Selling("month", y, m, None)
                else:
                    rows = Query_Top_Selling("year", y, None, None)
                _render_table_rows(rows)
            # แสดงครั้งแรก
            _do_report()
            return

        # ========== โหมดสินค้า (ADD/EDIT/DELETE) ==========
        KW = self.Search_Entry.get().strip()
        rows = Fetch_Products(KW)
        for (PID, Name, Price, Stock, Cat, Img, Desc) in rows:
            Row_Box = customtkinter.CTkFrame(self.Product_List_Frame, fg_color="#f5f5f5", corner_radius=12)
            Row_Box.pack(fill="x", padx=12, pady=8)

            Row_Box.grid_columnconfigure(0, weight=0)
            Row_Box.grid_columnconfigure(1, weight=1)
            Row_Box.grid_columnconfigure(2, weight=0)

            Thumb = self._Get_Thumb(Img, self.Thumb_Size)
            Img_Label = customtkinter.CTkLabel(Row_Box, image=Thumb, text="")
            Img_Label.image = Thumb
            Img_Label.grid(row=0, column=0, rowspan=2, padx=(12, 8), pady=8, sticky="w")
            if Img:
                Img_Label.bind("<Button-1>", lambda e, p=Img: self._Open_Preview(p))

            header_text = f"[{PID}] {Name} | ฿{CartModel.fmt_price(Price)} | เหลือ {Stock} ชิ้น | {Cat}"
            Info_Label = customtkinter.CTkLabel(Row_Box, text=header_text, font=customtkinter.CTkFont(size=14, weight="bold"), anchor="w", justify="left")
            Info_Label.grid(row=0, column=1, padx=4, pady=(10, 2), sticky="w")

            Preview_Desc = (Desc or "").strip()
            if len(Preview_Desc) > 140:
                Preview_Desc = Preview_Desc[:140] + "..."
            Sub_Label = customtkinter.CTkLabel(Row_Box, text=Preview_Desc, anchor="w", justify="left", wraplength=560)
            Sub_Label.grid(row=1, column=1, padx=4, pady=(0, 8), sticky="w")

            Button_Area = customtkinter.CTkFrame(Row_Box, fg_color="transparent")
            Button_Area.grid(row=0, column=2, rowspan=2, padx=12, pady=8, sticky="e")

            if Mode == "EDIT":
                customtkinter.CTkButton(Button_Area, text="Edit",command=lambda d=(PID, Name, Price, Stock, Cat, Img, Desc): self._Load_For_Edit(d)).pack(padx=4, pady=4)
            elif Mode == "DELETE":
                customtkinter.CTkButton(Button_Area, text="Delete", fg_color="#fad7d7", text_color="#ffffff", hover_color="#b00000",
                    command=lambda _pid=PID: self._Confirm_Delete(_pid)).pack(padx=4, pady=4)

    def _refresh_both(self):
        cur_mode = self.Mode_Var.get()

        if hasattr(self, "Product_Form_Frame") and self.Product_Form_Frame.winfo_exists():
            for w in self.Product_Form_Frame.winfo_children():
                w.destroy()
        self._Build_Product_Form()
        self._Clear_Form()

        # ให้ตัวจัดโหมดทำงานทั้งหมด (ซ่อน/แสดง + เติมข้อมูล)
        self.On_Mode_Change(cur_mode)

    # ---------- ฟังก์ชันจัดการฟอร์ม ----------
    def _Clear_Form(self):
        self.Product_Name_Entry.delete(0, "end")
        self.Price_Entry.delete(0, "end")
        self.Stock_Entry.delete(0, "end")
        self.Category_Var.set(self.categories[0])
        self.Image_Path_Entry.delete(0, "end")
        self.Description_Text.delete("1.0", "end")
        self.Editing_Product_ID = None
        self.Image_Preview_Label.configure(text="(no image)", image=None)
        self.Image_Preview_Label.image = None

    def _Fill_Form_Template(self, data):
        _, Name, Price, Stock, Cat, Img, Desc = data
        self.Mode_Var.set("ADD")
        self.On_Mode_Change()
        self.Product_Name_Entry.delete(0, "end"); self.Product_Name_Entry.insert(0, str(Name or ""))
        self.Price_Entry.delete(0, "end"); self.Price_Entry.insert(0, str(Price or ""))
        self.Stock_Entry.delete(0, "end"); self.Stock_Entry.insert(0, str(Stock or ""))
        self.Category_Var.set(Cat if Cat in self.categories else self.categories[0])
        self.Image_Path_Entry.delete(0, "end"); self.Image_Path_Entry.insert(0, str(Img or ""))
        self.Description_Text.delete("1.0", "end"); self.Description_Text.insert("1.0", str(Desc or ""))
        self._Update_Form_Preview()

    def _Load_For_Edit(self, data):
        PID, Name, Price, Stock, Cat, Img, Desc = data
        self.Mode_Var.set("EDIT")
        self.On_Mode_Change()
        self.Editing_Product_ID = PID

        self.Product_Name_Entry.delete(0, "end"); self.Product_Name_Entry.insert(0, str(Name or ""))
        self.Price_Entry.delete(0, "end"); self.Price_Entry.insert(0, str(Price or ""))
        self.Stock_Entry.delete(0, "end"); self.Stock_Entry.insert(0, str(Stock or ""))
        self.Category_Var.set(Cat if Cat in self.categories else self.categories[0])
        self.Image_Path_Entry.delete(0, "end"); self.Image_Path_Entry.insert(0, str(Img or ""))
        self.Description_Text.delete("1.0", "end"); self.Description_Text.insert(0.0, str(Desc or ""))
        self._Update_Form_Preview()

    def _Confirm_Delete(self, pid):
        ans = CTkMessagebox(title="Confirm delete",message=f"ต้องการลบสินค้า ID {pid} ใช่หรือไม่?",icon="warning", option_1="Cancel", option_2="Delete").get()

        if ans == "Delete":
            try:
                Delete_Product(pid)
                CTkMessagebox(title="Deleted", message="ลบสินค้าเรียบร้อย", icon="check")
                if self.Editing_Product_ID == pid:
                    self._Clear_Form()
            except Exception as e:
                CTkMessagebox(title="Error", message=f"ลบไม่สำเร็จ: {e}", icon="cancel")

        self._Clear_Form()
        self.Mode_Segment.set("ADD")
        self.Mode_Var.set("ADD")
        self.On_Mode_Change()

    def On_Save(self):
        Mode = self.Mode_Var.get()
        name = self.Product_Name_Entry.get().strip()
        price_s = self.Price_Entry.get().strip()
        stock_s = self.Stock_Entry.get().strip()
        cat = self.Category_Var.get().strip()
        img = self.Image_Path_Entry.get().strip()
        desc = self.Description_Text.get("1.0", "end").strip()

        if not name:
            CTkMessagebox(title="Validation", message="กรุณากรอกชื่อสินค้า", icon="warning"); return
        try:
            price = int(price_s); assert price >= 0
        except Exception:
            CTkMessagebox(title="Validation", message="ราคาไม่ถูกต้อง", icon="warning"); return
        try:
            stock = int(stock_s); assert stock >= 0
        except Exception:
            CTkMessagebox(title="Validation", message="สต็อกไม่ถูกต้อง", icon="warning"); return
        if cat not in self.categories:
            CTkMessagebox(title="Validation", message="หมวดหมู่ไม่ถูกต้อง", icon="warning"); return

        if Mode == "ADD":
            ok = Create_Product(name, price, stock, cat, img, desc)
            if ok:
                CTkMessagebox(title="Success", message="เพิ่มสินค้าเรียบร้อย", icon="check")
                self._refresh_both()
            else:
                CTkMessagebox(title="Error", message="เพิ่มสินค้าไม่สำเร็จ", icon="cancel")

        elif Mode == "EDIT":
            if not self.Editing_Product_ID:
                CTkMessagebox(title="Warning", message="ยังไม่ได้เลือกสินค้าที่จะแก้ไข", icon="warning"); return
            ok = Update_Product(self.Editing_Product_ID, name, price, stock, cat, img, desc)
            if ok:
                CTkMessagebox(title="Success", message="อัปเดตสินค้าเรียบร้อย", icon="check")
                self._refresh_both()
            else:
                CTkMessagebox(title="Error", message="อัปเดตไม่สำเร็จ", icon="cancel")

        elif Mode == "DELETE":
            if not self.Editing_Product_ID:
                CTkMessagebox(title="Warning", message="ยังไม่ได้เลือกสินค้าที่จะลบ", icon="warning"); return
            self._Confirm_Delete(self.Editing_Product_ID)

    # ---------- ฝั่งขวา: รายละเอียดออเดอร์ ----------
    def _render_order_detail(self, order_id: int):
        self.Selected_Order_ID = order_id

        # ใช้กรอบขวาที่สร้างไว้แล้วใน On_Mode_Change
        self.Content_Container.grid_columnconfigure(1, weight=1)
        self.Content_Container.grid_rowconfigure(0, weight=1)

        # ถ้ายังไม่เคยสร้าง (เผื่อถูกเรียกก่อนสลับโหมด) ให้สร้างแบบมี height
        if self.Order_Detail_Frame is None or (not self.Order_Detail_Frame.winfo_exists()):
            self.Order_Detail_Frame = customtkinter.CTkScrollableFrame(self.Content_Container, fg_color="#ffffff", corner_radius=14, width=520, height=560)


        if not self.Order_Detail_Frame.winfo_ismapped():
            self.Order_Detail_Frame.grid(row=0, column=1, sticky="nsew")

        # เคลียร์ของเดิม
        for w in self.Order_Detail_Frame.winfo_children():
            w.destroy()

        # ---------- ดึงหัวออเดอร์ ----------
        conn = None
        try:
            conn = connect_db(); cur = conn.cursor()
            cur.execute("""
                SELECT o.id, o.order_date, u.username,
                       o.status, o.address_snapshot, o.path_slip
                FROM orders o
                LEFT JOIN users u ON u.id = o.user_id
                WHERE o.id = ?
            """, (order_id,))
            head = cur.fetchone()
        except Exception as e:
            CTkMessagebox(title="Render error", message=str(e), icon="cancel")
            return
        finally:
            if conn:
                conn.close()

        if not head:
            customtkinter.CTkLabel(self.Order_Detail_Frame, text="ไม่พบออเดอร์", text_color="#b00").pack(pady=12)
            return

        oid, odate, uname, status, addr_snap, slip = head
        uname = uname or "(unknown)"
        status_norm = (status or "").strip().upper()

        # ---------- Header ----------
        customtkinter.CTkLabel(self.Order_Detail_Frame,text=f"Order #{oid} | {odate} | by {uname}"
                               ,font=customtkinter.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))
        customtkinter.CTkLabel(self.Order_Detail_Frame, text=f"สถานะ: {status}").pack(anchor="w", padx=16)

        # ---------- Address ----------
        if addr_snap:
            box = customtkinter.CTkFrame(self.Order_Detail_Frame, fg_color="#f7f9fc", corner_radius=10)
            box.pack(fill="x", padx=16, pady=(8, 8))
            customtkinter.CTkLabel(box, text=addr_snap, justify="left").pack(anchor="w", padx=12, pady=8)

        # ---------- Slip ----------
        if slip:
            try:
                im = customtkinter.CTkImage(Image.open(slip), size=(360, 360))
                img_lbl = customtkinter.CTkLabel(self.Order_Detail_Frame, image=im, text="")
                img_lbl.image = im
                img_lbl.pack(padx=16, pady=(0, 8))
                def _zoom():
                    t = customtkinter.CTkToplevel(self); t.title(f"Slip #{oid}")
                    imi = customtkinter.CTkImage(Image.open(slip), size=(640, 640))
                    l = customtkinter.CTkLabel(t, image=imi, text=""); l.image = imi; l.pack(padx=12, pady=12)
                img_lbl.bind("<Button-1>", lambda e: _zoom())
            except Exception:
                customtkinter.CTkLabel(self.Order_Detail_Frame, text="(เปิดสลิปไม่ได้)").pack()

        # ===== ตารางสินค้า (หัว+แถว) จัดในคอนเทนเนอร์เดียวกัน เพื่อให้คอลัมน์ตรงกัน =====
        tbl = customtkinter.CTkFrame(self.Order_Detail_Frame, fg_color="#ffffff", corner_radius=10)
        tbl.pack(fill="x", padx=16, pady=(6, 6))

        try:
            items = Fetch_Order_Items(order_id)   # -> [(name, qty, unit_price), ...]
        except Exception as e:
            CTkMessagebox(title="Order items error", message=str(e), icon="cancel")
            items = []

        # คอลัมน์: ชื่อ(กว้าง) : จำนวน : ราคา/ชิ้น : รวม
        for c, w in enumerate((3, 1, 1, 1)):
            tbl.grid_columnconfigure(c, weight=w)

        # หัวตาราง (ใส่พื้นหลังอ่อน ๆ โดยครอบด้วยกล่อง)
        hdr = customtkinter.CTkFrame(tbl, fg_color="#f0f0f0", corner_radius=8)
        hdr.grid(row=0, column=0, columnspan=4, sticky="ew", padx=0, pady=(0, 4))
        for c, w in enumerate((3, 1, 1, 1)):
            hdr.grid_columnconfigure(c, weight=w)

        customtkinter.CTkLabel(hdr, text="สินค้า").grid(row=0, column=0, padx=12, pady=6, sticky="w")
        customtkinter.CTkLabel(hdr, text="จำนวน").grid(row=0, column=1, padx=12, pady=6, sticky="e")
        customtkinter.CTkLabel(hdr, text="ราคา/ชิ้น").grid(row=0, column=2, padx=12, pady=6, sticky="e")
        customtkinter.CTkLabel(hdr, text="รวม").grid(row=0, column=3, padx=12, pady=6, sticky="e")

        # แถวข้อมูล: วาง "ตรงใน tbl" (ไม่สร้าง frame ย่อยต่อแถว) เพื่อให้คอลัมน์ตรงกันเป๊ะ
        r = 1
        subtotal = 0
        if not items:
            customtkinter.CTkLabel(tbl, text="(ออเดอร์นี้ไม่มีสินค้า)", text_color="#888")\
                .grid(row=r, column=0, padx=12, pady=8, sticky="w", columnspan=4)
        else:
            for (name, qty, unit_price) in items:
                qty = int(qty); unit_price = int(unit_price)
                line_total = qty * unit_price
                subtotal += line_total

                customtkinter.CTkLabel(tbl, text=str(name))\
                    .grid(row=r, column=0, padx=12, pady=6, sticky="w")
                customtkinter.CTkLabel(tbl, text=str(qty))\
                    .grid(row=r, column=1, padx=12, pady=6, sticky="e")
                customtkinter.CTkLabel(tbl, text=f"฿{CartModel.fmt_price(unit_price)}")\
                    .grid(row=r, column=2, padx=12, pady=6, sticky="e")
                customtkinter.CTkLabel(tbl, text=f"฿{CartModel.fmt_price(line_total)}")\
                    .grid(row=r, column=3, padx=12, pady=6, sticky="e")
                r += 1

        # ===== สรุป Subtotal / VAT / รวม =====
        vat = int(round(subtotal * 0.07))
        grand = subtotal + vat

        summary = customtkinter.CTkFrame(self.Order_Detail_Frame, fg_color="transparent")
        summary.pack(fill="x", padx=16, pady=(4, 8))
        summary.grid_columnconfigure(0, weight=1)
        summary.grid_columnconfigure(1, weight=0)

        customtkinter.CTkLabel(summary, text="Subtotal :").grid(row=0, column=0, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(subtotal)}")\
            .grid(row=0, column=1, sticky="e", padx=8, pady=2)

        customtkinter.CTkLabel(summary, text="VAT 7% :").grid(row=1, column=0, sticky="e", padx=8, pady=2)
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(vat)}")\
            .grid(row=1, column=1, sticky="e", padx=8, pady=2)

        customtkinter.CTkLabel(summary, text="รวมทั้งหมด :", font=customtkinter.CTkFont(weight="bold"))\
            .grid(row=2, column=0, sticky="e", padx=8, pady=(4, 6))
        customtkinter.CTkLabel(summary, text=f"฿{CartModel.fmt_price(grand)}",
                               font=customtkinter.CTkFont(weight="bold"))\
            .grid(row=2, column=1, sticky="e", padx=8, pady=(4, 6))


        # ปุ่มยืนยัน/ปฏิเสธ
        btns = customtkinter.CTkFrame(self.Order_Detail_Frame, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 12))

        can_approve = status_norm in {"PENDING", "PAID"}
        customtkinter.CTkButton(
            btns, text="ยืนยันสลิป",
            state=("normal" if can_approve else "disabled"),
            fg_color="#e7ffe7", text_color="#126600",
            # ❗❗ แก้: ไม่ส่งพารามิเตอร์เข้าเมธอดที่ไม่รับ arg
            command=self._approve_selected_order
        ).pack(side="right", padx=6)

        customtkinter.CTkButton(
            btns, text="ปฏิเสธ",
            state=("normal" if can_approve else "disabled"),
            fg_color="#ffefef", text_color="#b00000",
            command=self._reject_selected_order
        ).pack(side="right", padx=6)

    def _approve_selected_order(self):
        if self.Selected_Order_ID is None:
            CTkMessagebox(title="แจ้งเตือน", message="ยังไม่ได้เลือกออเดอร์", icon="warning"); return
        try:
            # ✅ ตัดสต็อก + log + set CONFIRMED
            Approve_Order_and_Log(self.Selected_Order_ID)
            CTkMessagebox(title="สำเร็จ", message="ยืนยันสลิปแล้ว", icon="check")
        except Exception as e:
            CTkMessagebox(title="ผิดพลาด", message=str(e), icon="cancel")
        # รีเฟรชลิสต์ และเปิดใบเดิมให้เห็นสถานะใหม่
        self.Refresh_List()
        if self.Selected_Order_ID:
            self._render_order_detail(self.Selected_Order_ID)

    def _reject_selected_order(self):
        if self.Selected_Order_ID is None:
            CTkMessagebox(title="แจ้งเตือน", message="ยังไม่ได้เลือกออเดอร์", icon="warning"); return
        try:
            Reject_Order(self.Selected_Order_ID, reason="rejected by admin")
            CTkMessagebox(title="สำเร็จ", message="ปฏิเสธออเดอร์แล้ว", icon="check")
        except Exception as e:
            CTkMessagebox(title="ผิดพลาด", message=str(e), icon="cancel")
        self.Refresh_List()
        if self.Selected_Order_ID:
            self._render_order_detail(self.Selected_Order_ID)

    # (ถ้าจะเก็บเมธอดลบออเดอร์ไว้ในคลาส ให้ทำเป็น staticmethod จะชัดเจนกว่า)
    @staticmethod
    def Delete_Order(order_id: int) -> bool:
        conn = connect_db()
        try:
            conn.execute("DELETE FROM orders WHERE id=?", (int(order_id),))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()

if __name__ == "__main__":
    app = HeavenGear()
    app.geometry(f"{app.screen_width}x{app.screen_height}")
    app.mainloop()