# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

import asyncio
import random
from html import escape
from pyrogram import filters, types, enums
from AloneX import app, lang
from AloneX.helpers import admin_check

TAG_STOP = []

EMOJIS = ["❤️", "🔥", "✨", "🌟", "🎵", "🎧", "🎸", "🎤", "🎶", "🎹"]

@app.on_message(filters.command(["tagall", "utagall", "all"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def tagall_hndlr(client, m: types.Message):
    chat_id = m.chat.id
    if chat_id in TAG_STOP:
        TAG_STOP.remove(chat_id)

    text = escape(m.text.split(None, 1)[1]) if len(m.command) > 1 else "Hello!"

    members = []
    async for member in client.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        members.append(member.user)

    if not members:
        return await m.reply_text("No members found to tag.")

    sent = await m.reply_text(m.lang["tagall_start"])

    try:
        for i in range(0, len(members), 5):
            if chat_id in TAG_STOP:
                break

            chunk = members[i:i + 5]
            tag_text = f"<b>{text}</b>\n\n"
            for user in chunk:
                emoji = random.choice(EMOJIS)
                tag_text += f"{emoji} {user.mention} "

            await client.send_message(chat_id, tag_text)
            await asyncio.sleep(2)

        if chat_id in TAG_STOP:
            TAG_STOP.remove(chat_id)
            await m.reply_text(m.lang["tagall_stopped"])
        else:
            await m.reply_text(m.lang["tagall_completed"])

    except Exception as e:
        await m.reply_text(f"<b>Error:</b> {e}")
    finally:
        await sent.delete()

@app.on_message(filters.command(["canceltagall", "stopall", "cancelall"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def cancel_tagall(client, m: types.Message):
    chat_id = m.chat.id
    if chat_id not in TAG_STOP:
        TAG_STOP.append(chat_id)
    await m.reply_text(m.lang["tagall_stopping"])
