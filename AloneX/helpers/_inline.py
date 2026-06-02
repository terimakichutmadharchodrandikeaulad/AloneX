# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic

import inspect
from pyrogram import types
try:
    from pyrogram.enums import ButtonStyle
except ImportError:
    class ButtonStyle:
        PRIMARY = SUCCESS = DANGER = DEFAULT = None

from AloneX import config

class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self._ikb = types.InlineKeyboardButton
        self._ikb_sig = inspect.signature(self._ikb.__init__)

    def ikb(self, *args, **kwargs):
        if "style" in kwargs and "style" not in self._ikb_sig.parameters:
            kwargs.pop("style")
        return self._ikb(*args, **kwargs)

    def start_key(self, lang: dict, username: str, private: bool = False) -> types.InlineKeyboardMarkup:
        rows = [
            [
                self.ikb(text=lang["add_me"], url=f"https://t.me/{username}?startgroup=true", style=ButtonStyle.SUCCESS),
            ],
            [
                self.ikb(text=lang["help"], callback_data="help_menu", style=ButtonStyle.PRIMARY),
            ],
            [
                self.ikb(text=lang["channel"], url=config.SUPPORT_CHANNEL, style=ButtonStyle.SUCCESS),
                self.ikb(text=lang["support"], url=config.SUPPORT_CHAT, style=ButtonStyle.SUCCESS),
            ],
        ]
        if private:
            rows += [
                [
                    self.ikb(text=lang["aloneowner"], user_id=config.OWNER_ID, style=ButtonStyle.DANGER),
                    self.ikb(text=lang.get("clone", "˹ 𝐂ʟσиє ˼"), callback_data="clone_bot", style=ButtonStyle.DANGER)
                ]
            ]
        else:
            rows += [[self.ikb(text=lang["language"], callback_data="language")]]
        return self.ikm(rows)

    def help_markup(self, lang: dict, back: bool = False) -> types.InlineKeyboardMarkup:
        if back:
            return self.ikm([[self.ikb(text=lang["back"], callback_data="help back")]])
        keyboard = [
            [
                self.ikb(text=lang["help_0"], callback_data="help_item admins"),
                self.ikb(text=lang["help_1"], callback_data="help_item auth"),
                self.ikb(text=lang["help_2"], callback_data="help_item blist"),
            ],
            [
                self.ikb(text=lang["help_3"], callback_data="help_item lang"),
                self.ikb(text=lang["help_4"], callback_data="help_item ping"),
                self.ikb(text=lang["help_5"], callback_data="help_item play"),
            ],
            [
                self.ikb(text=lang["help_6"], callback_data="help_item queue"),
                self.ikb(text=lang["help_7"], callback_data="help_item stats"),
                self.ikb(text=lang["help_8"], callback_data="help_item sudo"),
            ],
            [
                self.ikb(text=lang["back"], callback_data="start_menu"),
                self.ikb(text=lang["close"], callback_data="close"),
            ],
        ]
        return self.ikm(keyboard)

    def settings_markup(self, lang: dict, admin_only: bool, cmd_delete: bool, _language: str, chat_id: int) -> types.InlineKeyboardMarkup:
        keyboard = [
            [
                self.ikb(text=lang["play_mode"], callback_data=f"settings play_mode {chat_id}"),
                self.ikb(text="✅" if admin_only else "❌", callback_data=f"settings play_mode {chat_id}"),
            ],
            [
                self.ikb(text=lang["cmd_delete"], callback_data=f"settings cmd_delete {chat_id}"),
                self.ikb(text="✅" if cmd_delete else "❌", callback_data=f"settings cmd_delete {chat_id}"),
            ],
            [
                self.ikb(text=lang["language"], callback_data=f"settings language {chat_id}"),
                self.ikb(text=_language, callback_data=f"settings language {chat_id}"),
            ],
            [
                self.ikb(text=lang["close"], callback_data="close"),
            ],
        ]
        return self.ikm(keyboard)

    def clone_markup(self, lang: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="𝐂ʀєᴀᴛє 𝐂ℓσиє", callback_data="create_clone"),
                ],
                [
                    self.ikb(text="𝐌ᴀиᴀɢє 𝐂ℓσиє", callback_data="manage_clone"),
                ],
                [
                    self.ikb(text=lang["back"], callback_data="start_menu"),
                ]
            ]
        )

    def queue_markup(self, chat_id: int, status: str, is_playing: bool) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=status, callback_data=f"controls status {chat_id}"),
                ],
                [
                    self.ikb(
                        text="▷" if not is_playing else "II",
                        callback_data=f"controls {'resume' if not is_playing else 'pause'} {chat_id} q",
                        style=ButtonStyle.SUCCESS
                    ),
                    self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}", style=ButtonStyle.DANGER),
                    self.ikb(text="▢", callback_data=f"controls stop {chat_id}", style=ButtonStyle.DANGER),
                ],
                [
                    self.ikb(text="⌯ 𝐂ʟσsє ⌯", callback_data="close", style=ButtonStyle.DANGER),
                ]
            ]
        )

    def lang_markup(self, current: str) -> types.InlineKeyboardMarkup:
        from AloneX.core.lang import lang_codes
        kb = []
        for code, name in lang_codes.items():
            kb.append(
                self.ikb(
                    text=f"{'✅ ' if current == code else ''}{name}",
                    callback_data=f"lang_change {code}"
                )
            )

        rows = [kb[i:i + 3] for i in range(0, len(kb), 3)]
        rows.append([self.ikb(text="⌯ 𝐂ʟσsє ⌯", callback_data="close", style=ButtonStyle.DANGER)])
        return self.ikm(rows)

    def cancel_dl(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=text, callback_data="cancel_dl", style=ButtonStyle.DANGER),
                ]
            ]
        )

    def clone_manage_markup(self, lang: dict, is_premium: bool) -> types.InlineKeyboardMarkup:
        keyboard = [
            [
                self.ikb(text="𝐔ᴘᴅᴧᴛє 𝐂ʜᴧииєʟ", callback_data="edit_clone_channel"),
                self.ikb(text="𝐔ᴘᴅᴧᴛє 𝐀ssɪsᴛᴧиᴛ", callback_data="edit_clone_assistant"),
            ] if is_premium else [
                self.ikb(text="𝐆єᴛ 𝐏ʀєᴍɪυᴍ", callback_data="clone_premium"),
            ],
            [
                self.ikb(text="𝐃єℓєᴛє 𝐂ℓσиє", callback_data="delete_clone"),
            ],
            [
                self.ikb(text=lang["back"], callback_data="clone_bot"),
            ]
        ]
        return self.ikm(keyboard)

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
        lang: dict = None,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append(
                [self.ikb(text=status, callback_data=f"controls status {chat_id}")]
            )
        elif timer:
            keyboard.append(
                [self.ikb(text=timer, callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY)]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(text="▷", callback_data=f"controls resume {chat_id}", style=ButtonStyle.SUCCESS),
                    self.ikb(text="II", callback_data=f"controls pause {chat_id}", style=ButtonStyle.SUCCESS),
                    self.ikb(text="⥁", callback_data=f"controls replay {chat_id}", style=ButtonStyle.PRIMARY),
                    self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}", style=ButtonStyle.DANGER),
                    self.ikb(text="▢", callback_data=f"controls stop {chat_id}", style=ButtonStyle.DANGER),
                ]
            )
            keyboard.append(
                [
                    self.ikb(text=lang["channel"] if lang else "˹ 𝐔ᴘᴅᴧᴛєs ˼", url=config.SUPPORT_CHANNEL, style=ButtonStyle.SUCCESS),
                ]
            )
        return self.ikm(keyboard)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="❐", copy_text=link),
                    self.ikb(text="Youtube", url=link),
                ],
            ]
        )

    def play_queued(self, chat_id: int, file_id: str, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=text, callback_data=f"controls force {chat_id} {file_id}", style=ButtonStyle.SUCCESS),
                    self.ikb(text="⌯ 𝐂ʟσsє ⌯", callback_data="close", style=ButtonStyle.DANGER),
                ]
            ]
        )

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=text, url=config.SUPPORT_CHAT, style=ButtonStyle.SUCCESS),
                ]
            ]
        )
