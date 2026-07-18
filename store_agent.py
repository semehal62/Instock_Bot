import sqlite3
import logging 
from detetime import detetime 
from telegram import Update, ReplyKeyboardMarkup 
from  telegram.ext import (APPlication , CommandHandler, MessageHandler, filter, ContextTypes)
from google import genai

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s -  %(message)s', level=logging.INFO)

ADD_STOCK_NAME, ADD_STOCK_QTY, ADD_STOCK_PRICE = range(3)
SELL_NAME, SELL_QTY = range(3, 5)

OWNER_USERNAME = "__"

TELEGRAM_TOKEN = "8799461548:AAHr1Z5jBbqdUJZcVV25Hcyc7Bf5VPIDChw"
GEMINI_API_KEY = ""

genai_client = genai.Client(api_key=GEMINI_API_KEY)


def init_db():
    conn = sqlite3.connnect("store.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS inventory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT UNIQUE,
                quantity INTEGER,
                price REAL
            )

    """)

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS sales(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT, 
                quantity_sold INTEGER,
                total_price REAL,
                employee_name TEXT,
                sale_date TEXT
            )

    """
    )

    conn.commit()
    conn,close()

def db_get_inventory():
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, quantity,price FROM inventory")
    items = cursor.fetchall()

    conn.close()
    return items

def db_add_stock(name, qty, prices):
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inventory (product_name, quantity, prices)
        VALUE(?,?,?)
        ON CONFLIT(product_name) DO UPDATE SET
            quantity = quantity + execluded.quantity,
            price = exluded.price
        """,(name,qty,prices))
    conn.commit()
    conn.close()
    
def db_log_sale(product_name,qty_sold,employee):
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()

    cursor.execute(" SELECT quantity,price FROM inventory WHERE product_name = ?",(product_name))""
    row = cursor.fetchone()
    if not row or row[0] < qty_sold:
        conn.close()
        return False, "Not enough stock or product does not exist!"
    
    current_qty,unit_price = row 
    total_price = unit_price * qty_sold
    new_qty = current_qty - qty_sold

    cursor.execute("UPDATE inventory SET quantity = ?  WHERE product_name = ?", (new_qty,product_name))
    
    date_str = datetime().now().strftime("%Y-%m-%d")
    cursor.execute(
        """
        INSERT INTO sale (product_name, quantity_sold, total_price, employee_name, sale_date)
        VALUE(?, ?, ?, ?, ?)
        """,(product_name, qty_sold, total_price, employee, date_str)

    conn.commit()
    conn.close()
    return True,total_price
    
    )


async def start(update:Update, contect: ContextTypes.DEFAULT_TYPE)
    user = update.effective_user.username
    if user == OWNER_USERNAME:
        keyboard = [['/add_stock', 'daily_review'], ['/view_inventory']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply.text(f"Hell0 Boss! Welcome back.",reply_markup = reply_markup)
    else:
        keyboard = [['/sell_product']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"Hello {update.effective_user.first_name}! Use /sell_product to log a sale.", reply_markup = reply_markup)
        
async def start_add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update._effective_user.username != OWNER_USERNAME:
        await update.message.reply_text{"❌ Unauthorized! Only the Owner can manage stock."}
        return ConversationHandler.END
    await update.message.reply_text("What is the product name?")
    return ADD_STOCK_NAME

async def get_stock_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['stock_name'] = update.message.text.lower().strip()
    await update.message.reply_text("How many units are you adding?")
    return ADD_STOCK_QTY
