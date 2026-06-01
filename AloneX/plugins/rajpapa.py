# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

from pyrogram import filters, types
from AloneX import app, lang

@app.on_message(filters.command("rajpapa") & ~app.bl_users)
@lang.language()
async def rajpapa_hndlr(client, m: types.Message):
    commands_text = """
<b><u>๏ 𝐀ʟʟ 𝐂ᴏᴍᴍᴀɴᴅs 𝐋ɪsᴛ ๏</u></b>

<b><u>๏ 𝐀ᴅᴍɪɴ 𝐂ᴏᴍᴍᴀɴᴅs :</u></b>
• /pause : 𝐏ᴀᴜsᴇ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ.
• /resume : 𝐑ᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.
• /skip : 𝐒ᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ.
• /stop : 𝐒ᴛᴏᴘ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ.
• /seek [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : 𝐒ᴇᴇᴋ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ.
• /seekback [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : 𝐒ᴇᴇᴋ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ʙᴀᴄᴋᴡᴀʀᴅ.
• /reload : 𝐑ᴇʟᴏᴀᴅs ᴛʜᴇ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ.

<b><u>๏ 𝐏ʟᴀʏ 𝐂ᴏᴍᴍᴀɴᴅs :</u></b>
• /play [sᴏɴɢ ɴᴀᴍᴇ/ʏᴛ ᴜʀʟ/ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ] : 𝐏ʟᴀʏ ᴀᴜᴅɪᴏ.
• /vplay [sᴏɴɢ ɴᴀᴍᴇ/ʏᴛ ᴜʀʟ/ʀᴇᴘʟʏ ᴛᴏ ᴠɪᴅᴇᴏ] : 𝐏ʟᴀʏ ᴠɪᴅᴇᴏ.
• /playforce : 𝐅ᴏʀᴄᴇ ᴘʟᴀʏ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ.
• /vplayforce : 𝐅ᴏʀᴄᴇ ᴘʟᴀʏ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴠɪᴅᴇᴏ sᴏɴɢ.

<b><u>๏ 𝐀ᴜᴛʜ 𝐂ᴏᴍᴍᴀɴᴅs :</u></b>
• /auth : 𝐀ᴜᴛʜᴏʀɪᴢᴇ ᴀ ᴜsᴇʀ.
• /unauth : 𝐔ɴᴀᴜᴛʜᴏʀɪᴢᴇ ᴀ ᴜsᴇʀ.

<b><u>๏ 𝐌ɪsᴄ 𝐂ᴏᴍᴍᴀɴᴅs :</u></b>
• /ping : 𝐂ʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ's ᴘɪɴɢ.
• /stats : 𝐂ʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛ's sᴛᴀᴛs.
• /sudolist : 𝐒ʜᴏᴡ ᴛʜᴇ ʟɪsᴛ ᴏғ sᴜᴅᴏᴇʀs.
• /queue : 𝐒ʜᴏᴡ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛʟʏ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs.
• /rajpapa : 𝐒ʜᴏᴡ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅs ʟɪsᴛ.

<b><u>๏ 𝐂ʟᴏɴᴇ 𝐂ᴏᴍᴍᴀɴᴅs :</u></b>
• /clone : 𝐂ʀᴇᴀᴛᴇ ᴏʀ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ.
"""
    await m.reply_text(commands_text)
