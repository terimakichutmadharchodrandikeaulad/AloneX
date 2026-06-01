# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

from pyrogram import filters, types
from AloneX import app, db, lang
from AloneX.helpers import utils

@app.on_message(filters.command(["addpremium", "rmpremium"]) & filters.user(app.owner))
@lang.language()
async def _premium_manage(client, m: types.Message):
    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang["user_not_found"])

    clone = await db.get_clone(user.id)
    if not clone:
        return await m.reply_text(m.lang["premium_no_clone"].format(user.mention))

    if m.command[0] == "addpremium":
        if clone.get("is_premium"):
            return await m.reply_text(m.lang["premium_already"].format(user.mention))

        await db.update_clone_settings(user.id, is_premium=True)
        await m.reply_text(m.lang["premium_added"].format(user.mention))
    else:
        if not clone.get("is_premium"):
            return await m.reply_text(m.lang["premium_not"].format(user.mention))

        await db.update_clone_settings(user.id, is_premium=False)
        await m.reply_text(m.lang["premium_removed"].format(user.mention))

@app.on_message(filters.command("premiumlist") & filters.user(app.owner))
@lang.language()
async def _premium_list(client, m: types.Message):
    sent = await m.reply_text(m.lang["premium_fetching"])
    premium_users = await db.get_premium_users()

    if not premium_users:
        return await sent.edit_text(m.lang["premium_none"])

    txt = m.lang["premium_list"]
    for clone in premium_users:
        try:
            user = await client.get_users(clone["owner_id"])
            txt += f"\n- {user.mention} (<code>{clone['owner_id']}</code>)"
        except:
            txt += f"\n- <code>{clone['owner_id']}</code>"

    await sent.edit_text(txt)
