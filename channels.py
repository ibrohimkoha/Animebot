from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from telegram.constants import ChatMemberStatus
from db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Channelforforced, Movie, UserBot
from keyboard import menu

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    not_subscribed_channels = []

    async with get_session() as session:
        # Foydalanuvchini tekshiramiz
        existing_user = await session.execute(select(UserBot).where(UserBot.telegram_chat_id == user_id))
        existing_user = existing_user.scalar_one_or_none()

        # Agar foydalanuvchi bazada bo‘lmasa, uni qo‘shamiz
        if not existing_user:
            new_user = UserBot(telegram_chat_id=user_id)
            session.add(new_user)
            await session.commit()

        # Majburiy kanallarni tekshiramiz
        channels = await session.execute(select(Channelforforced))
        channels = channels.scalars().all()  # Obyektlarning ro‘yxatini olamiz
        for channel in channels:
            chat_member = await context.bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
            if chat_member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                not_subscribed_channels.append(channel.channel_id)

    if not_subscribed_channels:
        buttons = []
        for channel_id in not_subscribed_channels:
            chat = await context.bot.get_chat(channel_id)  # Kanal haqida info olish
            channel_username = chat.username  # Agar username bo'lsa, olamiz
            if channel_username:
                channel_url = f"https://t.me/{channel_username}"  # Agar username bor bo‘lsa, to‘g‘ri link
            else:
                channel_url = f"https://t.me/+{str(channel_id)[4:]}"  # Agar username yo‘q bo‘lsa, "join link"
            buttons.append([InlineKeyboardButton(f"Obuna bo'lish", url=channel_url)])
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text("❌ Iltimos, barcha kanallarga obuna bo‘ling! Va qayta /start bosing!", reply_markup=reply_markup)
    else:
        args = context.args
        if args:
            movie_id = int(args[0])
            async with get_session() as session:
                movie = await session.execute(select(Movie).where(Movie.code == movie_id))
                movie = movie.scalar_one_or_none()
                await update.message.reply_photo(photo=movie.image,
    caption=f"🎬 Nomi: {movie.title} \n"
            f"🌍 Davlati: {movie.country} \n"
            f"🔊 Tili: {movie.tili} \n"
            f"📆 Yili: {movie.year} \n"
            f"🎞 Janri: {movie.ganre}")           
                if not movie.film:
                    await update.message.reply_text(f"{movie.title} filmi hali qo'shilmagan")
                else:
                    await update.message.reply_video(video=movie.film, caption=f"{movie.title} filmi")
        else:
            await menu(update, context)  # Menulga qaytaydigan fayllarni yuboramiz