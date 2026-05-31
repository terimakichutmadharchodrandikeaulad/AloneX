# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

import asyncio
from pyrogram import Client, filters, types, enums
from pyrogram.errors import TokenInvalid, FloodWait

from AloneX import app, db, lang, logger, config
from AloneX.helpers import buttons

CLONE_BOTS = {}

@app.on_callback_query(filters.regex("clone_bot"))
@lang.language()
async def clone_bot_menu(_, query: types.CallbackQuery):
    await query.edit_message_caption(
        caption="<blockquote><b>𝐖єℓᴄσᴍє 𝐓σ 𝐓нє 𝐂ℓσиє 𝐒уѕтєм!</b>\n\n<b>𝐘συ ᴄᴀи ᴄℓσиє тнιѕ вσт тσ уσυʀ σωи тσкєи ᴀиᴅ υѕє ιт αѕ уσυʀ σωи вσт.</b></blockquote>",
        reply_markup=buttons.clone_markup(query.lang),
    )

@app.on_callback_query(filters.regex("create_clone"))
@lang.language()
async def create_clone_cb(_, query: types.CallbackQuery):
    clone = await db.get_clone(query.from_user.id)
    if clone:
        return await query.answer("𝐘συ αℓʀєαᴅу нανє α ᴄℓσиєᴅ вσт!", show_alert=True)

    msg = await query.message.chat.ask(
        "<b>𝐒єиᴅ уσυʀ вσт тσкєи тнαт уσυ ɢєт ғʀσм @BotFather</b>",
        filters=filters.text & filters.user(query.from_user.id)
    )
    bot_token = msg.text

    wait = await query.message.reply_text("<b>𝐂нєᴄкιиɢ уσυʀ тσкєи...</b>")
    try:
        from AloneX.core.bot import Bot
        clone_bot = Bot(bot_token=bot_token)
        await clone_bot.start()

        await db.add_clone(query.from_user.id, bot_token)
        CLONE_BOTS[query.from_user.id] = clone_bot

        await wait.edit_text(f"<b>✅ 𝐂ℓσиєᴅ 𝐒υᴄᴄєѕѕғυℓℓу!</b>\n\n<b>𝐘συʀ вσт: @{clone_bot.me.username}</b>")
    except TokenInvalid:
        await wait.edit_text("<b>❌ 𝐈иναℓιᴅ вσт тσкєи!</b>")
    except Exception as e:
        await wait.edit_text(f"<b>❌ 𝐄ʀʀσʀ: {e}</b>")

@app.on_callback_query(filters.regex("manage_clone"))
@lang.language()
async def manage_clone_cb(_, query: types.CallbackQuery):
    clone = await db.get_clone(query.from_user.id)
    if not clone:
        return await query.answer("𝐘συ ᴅσи'т нανє αиу ᴄℓσиєᴅ вσт!", show_alert=True)

    is_premium = clone.get("is_premium", False)
    await query.edit_message_caption(
        caption=f"<blockquote><b>𝐌αиαɢє 𝐘συʀ 𝐂ℓσиє</b>\n\n<b>𝐒тαтυѕ: {clone.get('status')}</b>\n<b>𝐏ʀєᴍɪυᴍ: {'✅' if is_premium else '❌'}</b></blockquote>",
        reply_markup=buttons.clone_manage_markup(query.lang, is_premium),
    )

@app.on_callback_query(filters.regex("delete_clone"))
@lang.language()
async def delete_clone_cb(_, query: types.CallbackQuery):
    clone = await db.get_clone(query.from_user.id)
    if not clone:
        return await query.answer("𝐍σ ᴄℓσиє ғσυиᴅ!", show_alert=True)

    await db.rm_clone(query.from_user.id)
    if query.from_user.id in CLONE_BOTS:
        try:
            await CLONE_BOTS[query.from_user.id].stop()
            del CLONE_BOTS[query.from_user.id]
        except:
            pass

    await query.answer("𝐂ℓσиє ᴅєℓєтєᴅ!", show_alert=True)
    await clone_bot_menu(_, query)

@app.on_callback_query(filters.regex(r"edit_clone_(channel|assistant)"))
@lang.language()
async def edit_clone_settings_cb(_, query: types.CallbackQuery):
    owner_id = query.from_user.id
    clone = await db.get_clone(owner_id)
    if not clone or not clone.get("is_premium"):
        return await query.answer("𝐏ʀєᴍɪυᴍ ʀєǫυιʀєᴅ тσ єᴅιт тнιѕ ѕєттιиɢ!", show_alert=True)

    setting_type = query.data.split("_")[-1]

    if setting_type == "channel":
        msg = await query.message.chat.ask(
            "<b>𝐒єиᴅ тнє иєω υᴘᴅαтє ᴄнαииєℓ ℓιик (є.ɢ. https://t.me/vertexxtg)</b>",
            filters=filters.text & filters.user(owner_id)
        )
        await db.update_clone_settings(owner_id, update_channel=msg.text)
        await query.answer("𝐔ᴘᴅαтє ᴄнαииєℓ υᴘᴅαтєᴅ!", show_alert=True)
    else:
        msg = await query.message.chat.ask(
            "<b>𝐒єиᴅ тнє αѕѕιѕтαит ɪᴅ (1, 2, σʀ 3)</b>",
            filters=filters.text & filters.user(owner_id)
        )
        try:
            assistant_id = int(msg.text)
            if assistant_id not in [1, 2, 3]:
                raise ValueError
            await db.update_clone_settings(owner_id, assistant_id=assistant_id)
            await query.answer("𝐀ѕѕιѕтαит υᴘᴅαтєᴅ!", show_alert=True)
        except ValueError:
            await query.message.reply_text("<b>❌ 𝐈иναℓιᴅ αѕѕιѕтαит ɪᴅ!</b>")

    await manage_clone_cb(_, query)

@app.on_callback_query(filters.regex("clone_premium"))
@lang.language()
async def clone_premium_cb(_, query: types.CallbackQuery):
    await query.edit_message_caption(
        caption="<blockquote><b>💎 𝐂ℓσиє 𝐏ʀєᴍɪυᴍ</b>\n\n<b>𝐔иℓσᴄк єᴅιтιиɢ υᴘᴅαтє ᴄнαииєℓ αиᴅ αѕѕιѕтαит єᴅιтѕ.</b>\n\n<b>𝐂σитαᴄт @ForRealAlone тσ ɢєт ᴘʀєᴍɪυᴍ αᴄᴄєѕѕ.</b></blockquote>",
        reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("𝐁αᴄк", callback_data="manage_clone")]])
    )

@app.on_message(filters.command("clone_broadcast") & filters.private)
async def clone_broadcast(_, message: types.Message):
    owner_id = message.from_user.id
    clone = await db.get_clone(owner_id)
    if not clone:
        return

    if not message.reply_to_message:
        return await message.reply_text("<b>𝐑єᴘℓу тσ α ᴍєѕѕαɢє тσ вʀσαᴅᴄαѕт ιи уσυʀ ᴄℓσиє.</b>")

    clone_bot = CLONE_BOTS.get(owner_id)
    if not clone_bot:
        return await message.reply_text("<b>❌ 𝐂ℓσиє вσт ιѕ иσт ʀυииιиɢ!</b>")

    sent_msg = await message.reply_text("<b>𝐁ʀσαᴅᴄαѕтιиɢ...</b>")
    count = 0
    async for dialog in clone_bot.get_dialogs():
        try:
            await message.reply_to_message.copy(dialog.chat.id)
            count += 1
            await asyncio.sleep(0.1)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except:
            continue

    await sent_msg.edit_text(f"<b>✅ 𝐁ʀσαᴅᴄαѕт ᴄσᴍᴘℓєтєᴅ! 𝐒єит тσ {count} ᴄнαтѕ.</b>")

async def start_clones():
    clones = await db.get_clones()
    from AloneX.core.bot import Bot
    for clone in clones:
        try:
            clone_bot = Bot(bot_token=clone["bot_token"])
            await clone_bot.start()
            CLONE_BOTS[clone["owner_id"]] = clone_bot
            logger.info(f"Started clone for {clone['owner_id']}")
        except Exception as e:
            logger.error(f"Failed to start clone for {clone['owner_id']}: {e}")
