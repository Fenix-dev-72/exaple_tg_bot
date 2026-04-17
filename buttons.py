from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_inline_buttons(buttons:list, callback:str, size:list=[1], repeat:bool=False):
    ikb=InlineKeyboardBuilder()
    for btn in buttons:
        ikb.add(InlineKeyboardButton(text=btn,callback_data=callback+"_"+btn))
    ikb.adjust(*size,repeat=repeat)
    return ikb.as_markup(resize_keyboard=True)

def create_reply_buttons(buttons:list,size:list=[1], repeat:bool=False,resize_keyboard=False):
    rkb=ReplyKeyboardBuilder()
    for btn in buttons:
        rkb.add(KeyboardButton(text=btn))
    rkb.adjust(*size,repeat=repeat)
    return rkb.as_markup(resize_keyboard=resize_keyboard)