# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

import os
import sys
import platform
import psutil
from pyrogram import filters, types, __version__
from pytgcalls import __version__ as pytgver
from AloneX import app, db, lang, config, userbot
from AloneX.helpers import buttons

@app.on_message(filters.command("supreme") & app.sudoers)
@lang.language()
async def supreme_panel(client, m: types.Message):
    await m.reply_text(
        text=m.lang["supreme_panel_text"],
        reply_markup=buttons.supreme_markup(m.lang)
    )

@app.on_callback_query(filters.regex("supreme_panel") & app.sudoers)
@lang.language()
async def supreme_panel_cb(client, query: types.CallbackQuery):
    await query.edit_message_text(
        text=query.lang["supreme_panel_text"],
        reply_markup=buttons.supreme_markup(query.lang)
    )

@app.on_callback_query(filters.regex("supreme_stats") & app.sudoers)
@lang.language()
async def supreme_stats_cb(client, query: types.CallbackQuery):
    process = psutil.Process(os.getpid())
    storage = psutil.disk_usage("/")

    stats_text = query.lang["stats_user"].format(
        client.name,
        len(userbot.clients),
        config.AUTO_LEAVE,
        len(db.blacklisted),
        len(client.bl_users),
        len(client.sudoers),
        len(await db.get_chats()),
        len(await db.get_users()),
    )

    from AloneX.plugins import all_modules
    stats_text += query.lang["stats_sudo"].format(
        len(all_modules),
        platform.system(),
        f"{process.memory_info().rss / 1024**2:.2f}",
        round(psutil.virtual_memory().total / (1024.0**3)),
        process.cpu_percent(interval=1.0),
        psutil.cpu_count(logical=False),
        f"{storage.used / (1024.0**3):.2f}",
        f"{storage.total / (1024.0**3):.2f}",
        sys.version.split()[0],
        __version__,
        pytgver,
    )

    await query.edit_message_text(
        text=query.lang["supreme_stats_title"] + stats_text,
        reply_markup=buttons.supreme_stats_markup()
    )

@app.on_callback_query(filters.regex("activevc_panel") & app.sudoers)
@lang.language()
async def activevc_panel_cb(client, query: types.CallbackQuery):
    from AloneX.helpers import Queue
    queue = Queue()
    if not db.active_calls:
        return await query.answer(query.lang["vc_empty"], show_alert=True)

    text = query.lang["vc_list"]
    for i, chat in enumerate(db.active_calls):
        playing = queue.get_current(chat)
        if playing:
            text += f"\n{i+1}. <code>{chat}</code>\n    ➜ {playing.title[:25]}"
        else:
             text += f"\n{i+1}. <code>{chat}</code>"

    await query.edit_message_text(
        text=text,
        reply_markup=buttons.supreme_stats_markup()
    )

@app.on_callback_query(filters.regex("sudolist_panel") & app.sudoers)
@lang.language()
async def sudolist_panel_cb(client, query: types.CallbackQuery):
    sudoers = await db.get_sudoers()
    text = query.lang["sudo_users"]
    for user_id in sudoers:
        try:
            user = (await client.get_users(user_id)).mention
            text += f"\n- {user} (<code>{user_id}</code>)"
        except:
            text += f"\n- <code>{user_id}</code>"

    await query.edit_message_text(
        text=text,
        reply_markup=buttons.supreme_stats_markup()
    )

@app.on_callback_query(filters.regex("broadcast_panel") & app.sudoers)
@lang.language()
async def broadcast_panel_cb(client, query: types.CallbackQuery):
    await query.edit_message_text(
        text=query.lang["broadcast_panel_title"],
        reply_markup=buttons.supreme_stats_markup()
    )

@app.on_callback_query(filters.regex("restart_bot") & app.sudoers)
@lang.language()
async def restart_bot_cb(client, query: types.CallbackQuery):
    await query.answer(query.lang["restart_done"], show_alert=True)
    os.execl(sys.executable, sys.executable, *sys.argv)
