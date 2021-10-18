#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from telethon import events
from telethon.sync import TelegramClient
from os import remove
from bot.plugins.downloader import *
from bot.messages import *
from pyromod import listen
from asyncio import TimeoutError
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, User
from pyrogram.errors import UserNotParticipant
from info import AUTH_CHANNEL

#Force Subscribe

    @Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**Please Join the Channel and click 'Try Again' to use this Bot!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("⭕ 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊𝐒 ⭕", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return

##########################################

'''Login as a Bot'''
bot = TelegramClient('URL_Uploader', api_id, api_hash).start(bot_token = bot_token)


''''Defining Some Handlers for Bot'''
#Start Handler
@bot.on(events.NewMessage(pattern = r'/start$'))
async def start_handler(event):
    await event.respond(start_msg, parse_mode = 'html')

#Help Handler
@bot.on(events.NewMessage(pattern = r'/help$'))
async def help_handler(event):
    await event.respond(help_msg, parse_mode = 'html')

@bot.on(events.NewMessage)
async def upload_handler(event):

    message_info = event.message

    if str(type(message_info.entities[0])) == "<class 'telethon.tl.types.MessageEntityUrl'>":
        if task() == "Running":
            await event.respond(task_ongoing, parse_mode = 'html')
        else:
            url = message_info.text
            downloader = await Downloader.start(event, url, bot)
            filename = downloader.filename

            if filename:    #Sending file to user
                msg = downloader.n_msg
                message = event.message
                userid = event.sender_id
                try:
                    await bot.send_file(userid , file = filename, reply_to = message)
                except Exception as e:
                    await bot.delete_messages(None, msg)
                    await bot.send_message(userid, unsuccessful_upload, reply_to = message)
                    print(line_number(), e)
                else:
                    await bot.delete_messages(None, msg)
                finally:
                    remove(filename)
            task("No Task")
    return None


'''Bot is Started to run all time'''
print('Bot is Started!')
bot.start()
bot.run_until_disconnected()