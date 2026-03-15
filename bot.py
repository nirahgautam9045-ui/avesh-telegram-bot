import telebot
import random
import os
import razorpay
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
USED_PAYMENTS_FILE = "used_payments.txt"

# ===== BOT TOKEN =====
TOKEN = "8785022594:AAGrjrL0C2sWpqBlev6ZGPsYf0zsR0ZeWko"
bot = telebot.TeleBot(TOKEN)

# ===== RAZORPAY SETUP =====
RAZORPAY_KEY_ID = "rzp_live_SMK2ziBeJXerJe"  # <-- apna live id
RAZORPAY_KEY_SECRET = "5ajcfr3IPL3Jm60hMmgHCsQh"  # <-- apna live secret
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# ===== DATABASES =====
captcha_db = {}
users_db = {}
captcha_attempts = {}

# ===== FOLDERS =====
QR_FOLDER = "qrcodes"  # QR images folder
KEY_FOLDER = "keys"    # Keys folder

# ===== STEP 2: PAYMENT HANDLER =====
def handle_payment(call, amount):
    user_id = call.from_user.id

    # Mapping amount → QR file (tumhare names ke hisaab se)
    qr_mapping = {
         50: "qr_50.png",
         75: "qr_75.png",
         80: "qr_80.png",
         90: "qr_90.png",
        100: "qr_100.png",
        120: "qr_120.png",
        125: "qr_125.png",
        160: "qr_160.png",
        175: "qr_175.png",
        180: "qr_180.png",
        200: "qr_200.png",
        240: "qr_240.png",
        260: "qr_260.png",
        250: "qr_250.png",
        280: "qr_280.png",
        300: "qr_300.png",
        320: "qr_320.png",
        325: "qr_325.png",
        450: "qr_450.png",
        500: "qr_500.png",
        550: "qr_550.png",
        600: "qr_600.png",
        650: "qr_650.png",
        700: "qr_700.png",
        750: "qr_750.png",
        800: "qr_800.png",
        850: "qr_850.png",
        900: "qr_900.png",
       1000: "qr_1000.png",
       1050: "qr_1050.png",
       1200: "qr_1200.png",
       1700: "qr_1700.png",
       2000: "qr_2000.png"
    }

    qr_file = qr_mapping.get(amount)
    if not qr_file:
        bot.send_message(user_id, f"❌ QR file mapping not found for {amount} INR")
        return

    qr_path = os.path.join(QR_FOLDER, qr_file)

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("✅ I have paid", callback_data=f"paid_{amount}"))
    markup.row(InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel"))

    if os.path.exists(qr_path):
        bot.send_photo(user_id, open(qr_path, "rb"), caption=f"💰 Amount: {amount} INR\nPay using this QR.")
        bot.send_message(user_id, "Click below after payment:", reply_markup=markup)
    else:
        bot.send_message(user_id, f"❌ QR file not found at {qr_path}!")

# ===== STEP 2: PAYMENT VERIFICATION & KEY DELIVERY =====
USED_PAYMENTS_FILE = "used_payments.txt"

def verify_payment_and_send_key(call, amount):
    user_id = call.from_user.id

    try:
        # Razorpay se last 10 payments fetch karo
        payments = razorpay_client.payment.fetch_all({'count': 10})['items']

        payment_found = False
        payment_id = None

        for p in payments:
            # captured payment aur exact amount match
            if p['status'] == 'captured' and int(p['amount']) == amount * 100:
                payment_id = p['id']
                payment_found = True
                break

        if not payment_found:
            bot.send_message(user_id, f"❌ Payment of {amount} INR not found.")
            return

        # ===== Check if payment already used =====
        if os.path.exists(USED_PAYMENTS_FILE):
            with open(USED_PAYMENTS_FILE, "r") as f:
                used_payments = f.read().splitlines()
        else:
            used_payments = []

        if payment_id in used_payments:
            bot.send_message(user_id, "⚠️ Payment already used. Key already delivered.")
            return

        # ===== Mapping amount → key file =====
        key_mapping = {
            250: "alpha_1.txt",
            850: "alpha_7.txt",
           1700: "alpha_30.txt",
            125: "brpc_1.txt",
            320: "brpc_10.txt",
            650: "brpc_30.txt",
             75: "driptapk_1.txt",
            300: "driptapk_7.txt",
            500: "driptapk_15.txt",
            800: "driptapk_30.txt",
            100: "driptpc_1.txt",
            320: "driptpc_7.txt",
            550: "driptpc_15.txt",
            750: "driptpc_30.txt",
             80: "driptroot_1.txt",
            325: "driptroot_7.txt",
            300: "driptroot_30.txt",
            450: "esign_30.txt",
            900: "gbox_30.txt",
            180: "fluorite_1.txt",
           1050: "fluorite_7.txt",
           2000: "fluorite_30.txt",
            450: "haxx_10.txt",
            850: "haxx_20.txt",
           1200: "haxx_30.txt",
            120: "hg_1.txt",
            280: "hg_10.txt",
            650: "hg_30.txt",
             90: "lk_1.txt",
            175: "lk_5.txt",
            260: "lk_10.txt",
            700: "lk_30.txt",
            200: "pato_3.txt",
            750: "pato_7.txt",
            600: "pato_15.txt",
           1000: "pato_30.txt",
            160: "prime_5.txt",
            300: "prime_10.txt",
             75: "brroot_1.txt",
            180: "brroot_7.txt",
            300: "brroot_15.txt",
            450: "brroot_30.txt",
             50: "stricks_1.txt",
            100: "stricks_5.txt",
            160: "stricks_10.txt",
            240: "stricks_15.txt",
            450: "stricks_30.txt",
            180: "spotify_7.txt",
            300: "spotify_15.txt",
            450: "spotify_30.txt",
            180: "spotify_60.txt"
            
            
        }

        key_file = key_mapping.get(amount)
        if not key_file:
            bot.send_message(user_id, f"❌ Key mapping not found for {amount} INR")
            return

        file_path = os.path.join(KEY_FOLDER, key_file)
        if not os.path.exists(file_path):
            bot.send_message(user_id, "❌ Key file not found.")
            return

        with open(file_path, "r") as f:
            keys = f.readlines()

        if len(keys) == 0:
            bot.send_message(user_id, "⚠️ Keys out of stock.")
            return

        # ===== Send key to user =====
        key = keys[0].strip()
        bot.send_message(user_id, f"✅ Payment Verified\n\n🔑 Your Key:\n`{key}`", parse_mode="Markdown")

        # Remove delivered key from file
        keys.pop(0)
        with open(file_path, "w") as f:
            f.writelines(keys)

        # Mark payment ID as used
        with open(USED_PAYMENTS_FILE, "a") as f:
            f.write(payment_id + "\n")

    except Exception as e:
        bot.send_message(user_id, f"⚠️ Error: {str(e)}")

# ===== MENU =====
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.row(
        telebot.types.InlineKeyboardButton("🛑 Account", callback_data="account"),
        telebot.types.InlineKeyboardButton("🛒 Buy Panel", callback_data="buy_panel")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("🌎 Global Buy Panel", callback_data="global_buy")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("❓ Help", callback_data="help"),
        telebot.types.InlineKeyboardButton("🗝️ Key History", callback_data="key_history")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("📽️ Tutorial", callback_data="tutorial")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("💰 Deposit", callback_data="deposit")
    )

    return markup

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):

    captcha = random.randint(100000, 999999)
    captcha_db[message.chat.id] = captcha

    bot.send_message(
        message.chat.id,
        f"🤖 Captcha Verification\n\n👉 {captcha}"
    )

# ===== CAPTCHA =====
@bot.message_handler(func=lambda msg: msg.chat.id in captcha_db)
def captcha_check(message):

    user_id = message.chat.id
    user_text = message.text.strip()  # removes spaces

    if user_text.isdigit() and int(user_text) == captcha_db[user_id]:

        del captcha_db[user_id]
        captcha_attempts.pop(user_id, None)

        users_db.setdefault(user_id, {"balance":0,"orders":0})

        bot.send_message(
            user_id,
            "✅ Captcha Verified!\n\n👋 Welcome!\nSelect option below:",
            reply_markup=main_menu()
        )

    else:

        captcha_attempts[user_id] = captcha_attempts.get(user_id, 0) + 1

        if captcha_attempts[user_id] >= 3:

            new_captcha = random.randint(100000, 999999)
            captcha_db[user_id] = new_captcha
            captcha_attempts[user_id] = 0

            bot.send_message(
                user_id,
                f"❌ 3 Wrong Attempts!\n\n🔄 New Captcha:\n👉 {new_captcha}"
            )

        else:

            bot.send_message(
                user_id,
                f"❌ Wrong Captcha!\nAttempts Left: {3 - captcha_attempts[user_id]}"
            )
# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    bot.answer_callback_query(call.id)

    if call.data == "account":

        user_id = call.message.chat.id
        user = users_db.get(user_id, {"balance":0,"orders":0})

        now = datetime.now()

        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%I:%M %p")

        bot.edit_message_text(
            f"👤 {call.from_user.first_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 User ID: {user_id}\n"
            f"💰 Balance: {user['balance']:.2f} INR\n"
            f"📦 Orders: {user['orders']}\n"
            f"📅 Date: {date}\n"
            f"⏰ Time: {time}\n"
            f"━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )

    elif call.data == "buy_panel":

        markup = telebot.types.InlineKeyboardMarkup()

        products = [
            ("🪪 Alpha Regedit", "alpha"),
            ("💻 Br Mode Pc", "br_pc"),
            ("📱 Dript Apk Mode", "dript_apk"),
            ("🖥️ Dript Pc Exe", "dript_pc"),
            ("🔥 Dript Root", "dript_root"),
            ("🧾 Esign Cert", "esign"),
            ("🌐 GBOX CERT", "gbox"),
            ("❄️ Fluorite iOS", "fluorite"),
            ("⚡ Haxx Pro", "haxx"),
            ("🧬 Hg Cheat", "hg"),
            ("⭐ LK Team Root", "lk"),
            ("💥 Pato Team", "pato"),
            ("🌟 Prime Apk", "prime"),
            ("🔒 Br Mode Root", "br_root"),
            ("🧪 Stricks BR Mode", "stricks"),
            ("🎵 Spotify Root", "spotify")
        ]

        for i in range(0, len(products), 2):
            row = []

            row.append(
                telebot.types.InlineKeyboardButton(products[i][0], callback_data=products[i][1])
            )

            if i+1 < len(products):
                row.append(
                    telebot.types.InlineKeyboardButton(products[i+1][0], callback_data=products[i+1][1])
                )

            markup.row(*row)

        markup.row(
            telebot.types.InlineKeyboardButton(
            "📥 All Files Download",
            url="https://t.me/+fOIPDX5ae1A1NTRl"
        )
        )
        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Menu", callback_data="back")
        )

        bot.edit_message_text(
            "🛒 Select Your Product",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "alpha":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 250 INR", callback_data="alpha_1"),
            telebot.types.InlineKeyboardButton("7 Day - 850 INR", callback_data="alpha_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 1700 INR", callback_data="alpha_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🪪 Alpha Regedit iOS\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    
    elif call.data == "br_pc":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 125 INR", callback_data="brpc_1"),
            telebot.types.InlineKeyboardButton("10 Day - 320 INR", callback_data="brpc_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 650 INR", callback_data="brpc_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Menu", callback_data="buy_panel")
        )


        bot.edit_message_text(
            "💻 Br Mods PC\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package from the list below:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "dript_apk":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="driptapk_1"),
            telebot.types.InlineKeyboardButton("7 Day - 300 INR", callback_data="driptapk_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 500 INR", callback_data="driptapk_15"),
            telebot.types.InlineKeyboardButton("30 Day - 800 INR", callback_data="driptapk_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "📱 Dript Apk Mode\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "dript_pc":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 100 INR", callback_data="driptpc_1"),
            telebot.types.InlineKeyboardButton("7 Day - 320 INR", callback_data="driptpc_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 550 INR", callback_data="driptpc_15"),
            telebot.types.InlineKeyboardButton("30 Day - 750 INR", callback_data="driptpc_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🖥️ Dript PC EXE\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "dript_root":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 80 INR", callback_data="driptroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 325 INR", callback_data="driptroot_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 300 INR", callback_data="driptroot_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🔥 Dript Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "esign":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Month - 450 INR", callback_data="esign_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🧾 Esign Cert\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "gbox":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Month - 900 INR", callback_data="gbox_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🌐 GBOX CERT\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "fluorite":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 180 INR", callback_data="fluorite_1"),
            telebot.types.InlineKeyboardButton("7 Day - 1050 INR", callback_data="fluorite_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 2000 INR", callback_data="fluorite_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "❄️ Fluorite iOS\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "haxx":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 450 INR", callback_data="haxx_10"),
            telebot.types.InlineKeyboardButton("20 Day - 850 INR", callback_data="haxx_20")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 1200 INR", callback_data="haxx_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🔥 Haxx Pro\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "hg":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 120 INR", callback_data="hg_1"),
            telebot.types.InlineKeyboardButton("10 Day - 280 INR", callback_data="hg_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 650 INR", callback_data="hg_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🧬 Hg Cheat\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "lk":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 90 INR", callback_data="lk_1"),
            telebot.types.InlineKeyboardButton("5 Day - 175 INR", callback_data="lk_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 260 INR", callback_data="lk_10"),
            telebot.types.InlineKeyboardButton("30 Day - 700 INR", callback_data="lk_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "⭐ LK Team Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "pato":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("3 Day - 200 INR", callback_data="pato_3"),
            telebot.types.InlineKeyboardButton("7 Day - 750 INR", callback_data="pato_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 600 INR", callback_data="pato_15"),
            telebot.types.InlineKeyboardButton("30 Day - 1000 INR", callback_data="pato_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "💥 Pato Team Apk + Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "prime":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("5 Day - 160 INR", callback_data="prime_5"),
            telebot.types.InlineKeyboardButton("10 Day - 300 INR", callback_data="prime_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🌟 Prime Apk\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "br_root":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="brroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="brroot_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 300 INR", callback_data="brroot_15"),
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="brroot_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🔒 Br Mode Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "stricks":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 50 INR", callback_data="stricks_1"),
            telebot.types.InlineKeyboardButton("5 Day - 100 INR", callback_data="stricks_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 160 INR", callback_data="stricks_10"),
            telebot.types.InlineKeyboardButton("15 Day - 240 INR", callback_data="stricks_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="stricks_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🧪 Stricks BR Mode\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    elif call.data == "spotify":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="spotify_7"),
            telebot.types.InlineKeyboardButton("15 Day - 300 INR", callback_data="spotify_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="spotify_30"),
            telebot.types.InlineKeyboardButton("60 Day - 750 INR", callback_data="spotify_60")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🎵 Spotify Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    # ===== BUY PANEL PAYMENT HANDLER =====

    elif call.data == "alpha_1":
        handle_payment(call, 250)

    elif call.data == "alpha_7":
        handle_payment(call, 850)

    elif call.data == "alpha_30":
        handle_payment(call, 1700)


    elif call.data == "brpc_1":
        handle_payment(call, 125)

    elif call.data == "brpc_10":
        handle_payment(call, 320)

    elif call.data == "brpc_30":
        handle_payment(call, 650)


    elif call.data == "driptapk_1":
        handle_payment(call, 75)

    elif call.data == "driptapk_7":
        handle_payment(call, 300)

    elif call.data == "driptapk_15":
        handle_payment(call, 500)

    elif call.data == "driptapk_30":
        handle_payment(call, 800)


    elif call.data == "driptpc_1":
        handle_payment(call, 100)

    elif call.data == "driptpc_7":
        handle_payment(call, 320)

    elif call.data == "driptpc_15":
        handle_payment(call, 550)

    elif call.data == "driptpc_30":
        handle_payment(call, 750)


    elif call.data == "driptroot_1":
        handle_payment(call, 80)

    elif call.data == "driptroot_7":
        handle_payment(call, 325)

    elif call.data == "driptroot_30":
        handle_payment(call, 300)


    elif call.data == "esign_30":
        handle_payment(call, 450)


    elif call.data == "gbox_30":
        handle_payment(call, 900)


    elif call.data == "fluorite_1":
        handle_payment(call, 180)

    elif call.data == "fluorite_7":
        handle_payment(call, 1050)

    elif call.data == "fluorite_30":
        handle_payment(call, 2000)


    elif call.data == "haxx_10":
        handle_payment(call, 450)

    elif call.data == "haxx_20":
        handle_payment(call, 850)

    elif call.data == "haxx_30":
        handle_payment(call, 1200)

    elif call.data == "hg_1":
        handle_payment(call, 120)

    elif call.data == "hg_10":
        handle_payment(call, 280)

    elif call.data == "hg_30":
        handle_payment(call, 650)


    elif call.data == "lk_1":
        handle_payment(call, 90)

    elif call.data == "lk_5":
        handle_payment(call, 175)

    elif call.data == "lk_10":
        handle_payment(call, 260)

    elif call.data == "lk_30":
        handle_payment(call, 700)


    elif call.data == "pato_3":
        handle_payment(call, 200)

    elif call.data == "pato_7":
        handle_payment(call, 750)

    elif call.data == "pato_15":
        handle_payment(call, 600)

    elif call.data == "pato_30":
        handle_payment(call, 1000)


    elif call.data == "prime_5":
        handle_payment(call, 160)

    elif call.data == "prime_10":
        handle_payment(call, 300)


    elif call.data == "brroot_1":
        handle_payment(call, 75)

    elif call.data == "brroot_7":
        handle_payment(call, 180)

    elif call.data == "brroot_15":
        handle_payment(call, 300)

    elif call.data == "brroot_30":
        handle_payment(call, 450)


    elif call.data == "stricks_1":
        handle_payment(call, 50)

    elif call.data == "stricks_5":
        handle_payment(call, 100)

    elif call.data == "stricks_10":
        handle_payment(call, 160)

    elif call.data == "stricks_15":
        handle_payment(call, 240)

    elif call.data == "stricks_30":
        handle_payment(call, 450)


    elif call.data == "spotify_7":
        handle_payment(call, 180)

    elif call.data == "spotify_15":
        handle_payment(call, 300)

    elif call.data == "spotify_30":
        handle_payment(call, 450)

    elif call.data == "spotify_60":
        handle_payment(call, 750)


# ===== I HAVE PAID BUTTON =====

    elif call.data.startswith("paid_"):
        amount = int(call.data.split("_")[1])
        verify_payment_and_send_key(call, amount)

    # ===== GLOBAL BUY PANEL =====

    elif call.data == "global_buy":

        markup = telebot.types.InlineKeyboardMarkup()

        buttons = [
            ("🪪 Alpha Regedit iOS", "g_alpha"),
            ("💻 Br Mode Pc", "g_br_pc"),
            ("🔒 Br Mode Root", "g_br_root"),
            ("📱 Dript Apk Mode", "g_dript_apk"),
            ("🖥️ Dript Client Pc", "g_dript_pc"),
            ("🔥 Dript Client Root", "g_dript_root"),
            ("🧾 Esign Cert iOS", "g_esign"),
            ("🌐 GBOX CERT IOS", "g_gbox"),
            ("❄️ Flourties iOS", "g_fluorite"),
            ("⚡ Haxx-cker Pro", "g_haxx"),
            ("🧬 Hg Cheat Apk", "g_hg"),
            ("⭐ Lk Team Root + Pc", "g_lk"),
            ("💥 Pato Team Apk", "g_pato"),
            ("🌟 Prime Apk Mode", "g_prime"),
            ("🧪 Strike BR Mode", "g_strike"),
            ("🎵 Spotify Root", "g_spotify")
        ]

        for i in range(0, len(buttons), 2):
            row = []

            row.append(
                telebot.types.InlineKeyboardButton(
                buttons[i][0], callback_data=buttons[i][1]
            )
        )

            if i + 1 < len(buttons):
                row.append(
                    telebot.types.InlineKeyboardButton(
                    buttons[i+1][0], callback_data=buttons[i+1][1]
                )
        )

            markup.row(*row)   # ✅ LOOP के अंदर

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Menu", callback_data="back")
        )

        bot.edit_message_text(
            "🌎 Global Buy Panel\nSelect Product:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # ===== GLOBAL PRODUCTS =====

    elif call.data == "g_alpha":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 250 INR", callback_data="g_alpha_1"),
            telebot.types.InlineKeyboardButton("7 Day - 10 INR", callback_data="g_alpha_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_alpha_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Alpha Regedit iOS\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_br_pc":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 140 INR", callback_data="g_brpc_1"),
            telebot.types.InlineKeyboardButton("10 Day - 330 INR", callback_data="g_brpc_10")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_brpc_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Br Mode Pc\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_br_root":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="g_brroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="g_brroot_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 320 INR", callback_data="g_brroot_15"),
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="g_brroot_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Br Mode Root\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_dript_apk":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="g_driptapk_1"),
            telebot.types.InlineKeyboardButton("7 Day - 300 INR", callback_data="g_driptapk_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 500 INR", callback_data="g_driptapk_15"),
            telebot.types.InlineKeyboardButton("30 Day - 800 INR", callback_data="g_driptapk_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Dript Apk Mode\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_dript_pc":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 110 INR", callback_data="g_driptpc_1"),
            telebot.types.InlineKeyboardButton("7 Day - 320 INR", callback_data="g_driptpc_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 600 INR", callback_data="g_driptpc_15"),
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_driptpc_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Dript Client Pc\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_dript_root":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 80 INR", callback_data="g_driptroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 340 INR", callback_data="g_driptroot_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 700 INR", callback_data="g_driptroot_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Dript Client Root\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_esign":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Buy Certificate - 450 INR", callback_data="g_esign_30"))
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Esign Cert iOS\nChoose option:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_gbox":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Buy Certificate - 10 INR", callback_data="g_gbox_30"))
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 GBOX CERT IOS\nChoose option:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_fluorite":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 10 INR", callback_data="g_fluorite_1"),
            telebot.types.InlineKeyboardButton("7 Day - 10 INR", callback_data="g_fluorite_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_fluorite_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Flourties iOS\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_haxx":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 450 INR", callback_data="g_haxx_10"),
            telebot.types.InlineKeyboardButton("20 Day - 10 INR", callback_data="g_haxx_20")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_haxx_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Haxx-cker Pro\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_hg":
        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 120 INR", callback_data="g_hg_1"),
            telebot.types.InlineKeyboardButton("10 Day - 250 INR", callback_data="g_hg_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_hg_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🌎 Hg Cheat Apk\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_lk":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 90 INR", callback_data="g_lk_1"),
            telebot.types.InlineKeyboardButton("5 Day - 175 INR", callback_data="g_lk_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 10 INR", callback_data="g_lk_10"),
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_lk_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "⭐ LK Team Root + PC\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_pato":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("3 Day - 200 INR", callback_data="g_pato_3"),
            telebot.types.InlineKeyboardButton("7 Day - 350 INR", callback_data="g_pato_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_pato_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "💥 Pato Team Apk\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_prime":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="g_prime_1"),
            telebot.types.InlineKeyboardButton("7 Day - 330 INR", callback_data="g_prime_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 500 INR", callback_data="g_prime_15"),
            telebot.types.InlineKeyboardButton("30 Day - 800 INR", callback_data="g_prime_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🌟 Prime Apk Mode\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_strike":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 55 INR", callback_data="g_strike_1"),
            telebot.types.InlineKeyboardButton("5 Day - 100 INR", callback_data="g_strike_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 10 INR", callback_data="g_strike_10"),
            telebot.types.InlineKeyboardButton("15 Day - 10 INR", callback_data="g_strike_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_strike_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🧪 Strike BR Mode\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_spotify":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="g_spotify_7"),
            telebot.types.InlineKeyboardButton("15 Day - 10 INR", callback_data="g_spotify_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="g_spotify_30"),
            telebot.types.InlineKeyboardButton("60 Day - 10 INR", callback_data="g_spotify_60")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🎵 Spotify Root\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "help":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton(
            "💬 Contact Support",
            url="https://t.me/avesh_thakur"
        )
    )

        markup.row(
            telebot.types.InlineKeyboardButton(
            "🔙 Back To Menu",
            callback_data="back"
        )
    )

        bot.edit_message_text(
            "❓ Help Section\n\n"
            "👉 Click button below to contact support.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "deposit":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton(
            "💬 Contact Support for Deposit",
            url="https://t.me/avesh_thakur"
        )
    )

        markup.row(
            telebot.types.InlineKeyboardButton(
            "🔙 Back To Menu",
            callback_data="back"
        )
    )

        bot.edit_message_text(
            "💰 Deposit Section\n\n"
            "👉 Please contact support for deposit details.\n"
            "👉 Our team will guide you.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "back":

        bot.edit_message_text(
            "👋 Welcome!\nSelect option below:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )
print("Bot started...")
bot.infinity_polling()
