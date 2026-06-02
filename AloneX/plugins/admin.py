# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

from pyrogram import filters, types
from AloneX import app, db, lang
from AloneX.helpers import admin_check, utils

@app.on_message(filters.command(["ban", "unban", "mute", "unmute", "warn", "unwarn"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def admin_cmds(client, m: types.Message):
    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang["user_not_found"])

    if user.id == client.id:
        return await m.reply_text(m.lang["admin_self_action"])

    chat_id = m.chat.id
    cmd = m.command[0]

    if cmd == "ban":
        try:
            await client.ban_chat_member(chat_id, user.id)
            await m.reply_text(m.lang["ban_success"].format(user.mention))
        except Exception as e:
            await m.reply_text(f"<b>Error:</b> {e}")

    elif cmd == "unban":
        try:
            await client.unban_chat_member(chat_id, user.id)
            await m.reply_text(m.lang["unban_success"].format(user.mention))
        except Exception as e:
            await m.reply_text(f"<b>Error:</b> {e}")

    elif cmd == "mute":
        try:
            await client.restrict_chat_member(chat_id, user.id, types.ChatPermissions())
            await m.reply_text(m.lang["mute_success"].format(user.mention))
        except Exception as e:
            await m.reply_text(f"<b>Error:</b> {e}")

    elif cmd == "unmute":
        try:
            await client.restrict_chat_member(chat_id, user.id, m.chat.permissions)
            await m.reply_text(m.lang["unmute_success"].format(user.mention))
        except Exception as e:
            await m.reply_text(f"<b>Error:</b> {e}")

    elif cmd == "warn":
        warns = await db.get_warns(chat_id, user.id) + 1
        if warns >= 3:
            try:
                await client.ban_chat_member(chat_id, user.id)
                await db.rm_warns(chat_id, user.id)
                await m.reply_text(m.lang["warn_max"].format(user.mention))
            except Exception as e:
                await m.reply_text(f"<b>Error while banning:</b> {e}")
        else:
            await db.set_warns(chat_id, user.id, warns)
            await m.reply_text(m.lang["warn_success"].format(user.mention, warns))

    elif cmd == "unwarn":
        await db.rm_warns(chat_id, user.id)
        await m.reply_text(m.lang["unwarn_success"].format(user.mention))
