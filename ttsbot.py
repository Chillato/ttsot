from pyrogram import *
from pyrogram.types import *
from gtts import *
import os

api_id = 8 # enter your api id (my.telegram.org)
api_hash = "" # enter your api hash (my.telegram.org)
ttstoken = "" # enter your bot's token

ttsbot = Client('tts|session', api_id, api_hash, bot_token=ttstoken)

verfychannel = "" # enter your channel username without @
username = "" # enter the token bot without @

startmsg = """
hello I'm ttsbot your bot that creates audio in en
""" # enter message start message
startbuttons = InlineKeyboardButton([
    [InlineKeyboardButton("➕add me to a group➕", url=f"http://telegram.me/{username}?startgroup=start")],
    [InlineKeyboardButton("🆘 Support 🆘", url="https://t.me/developeritchat")]
])
verifybuttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("📂 Channel 📂", url=f"https://t.me/{verfychannel}")],
    [InlineKeyboardButton("✅ Done ✅ ", "done")]
])
verufymsg = """
you are not subscribed to the channel enter to use me
""" # enter message verifychannel

@ttsbot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    try:
        await client.get_chat_member(verfychannel, message.from_user.id)
        await client.send_message(message.chat.id, startmsg, reply_markup=startbuttons)
    except:
        await client.send_message(message.chat.id, verufymsg, reply_markup=verifybuttons)

@ttsbot.on_message(filters.command("tts"))
async def tts(client, message):
    audio = message.text.split(" ", 1)
    if audio.__len__() == 2:
        tts = gTTS(text=audio[1], lang=f"en")
        tts.save("tts.ogg")
        await client.send_voice(message.chat.id, "tts.ogg")
        os.remove("tts.ogg")
    else:
        await message.reply("**❌ERROR: specifies text**")


@ttsbot.on_callback_query()
async def buttons(client, query):
    if query.data == "done":
        try:
            await client.get_chat_member(verfychannel, query.from_user.id)
            await query.message.delete()
            await client.send_message(query.message.chat.id, startmsg, reply_markup=startbuttons)
        except:
            await query.answer("subscribe to the channel!", show_alert=True)

ttsbot.run()
