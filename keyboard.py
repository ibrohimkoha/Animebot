from sqlalchemy import select, func
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                         ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import CommandHandler, MessageHandler, filters, Application, ContextTypes
from telegram import Update
from db import get_session, bot_username
from models import Admins, Channelforforced, Movie, UserBot, ChannelforBot
from telegram.constants import ChatMemberStatus
from handlers import (FILM_CODE_FOR_SEARCH,CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL,
                       FILM_SEARCH_BY_GANRE,CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL,
                         FILM_SEARCH_BY_TITLE, CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL,
                           FILM_TITLE, CHANNEL_ID_FOR_ADD_FORCED_CHANNEL,
                             FILM_CODE_FOR_ADD_VIDEO,
                               FILM_CODE_FOR_SEND_TO_CHANNEL, POST_FOR_SEND_TO_CHANNEL)
from telegram.ext import ConversationHandler
from sqlalchemy import cast, BigInteger
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    keyboard_for_user = [
        ["🔍Film izlash"]
    ]
    keyboard_for_admin = [
        ["🔍Film izlash"],
        ["🗄 Boshqarish"]
    ]

    async with get_session() as session:
        is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
        is_admin = is_admin.scalar_one_or_none()
        if is_admin:
            reply_markup = ReplyKeyboardMarkup(keyboard_for_admin, resize_keyboard=True)
        else:
            reply_markup = ReplyKeyboardMarkup(keyboard_for_user, resize_keyboard=True)
    
    await update.message.reply_text("Kerakli bo‘limni tanlang:", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text  # Foydalanuvchining bosgan tugmasini olamiz
    user_id = update.message.from_user.id
    not_subscribed_channels = []
    # Admin panel keyboard
    admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]
    inline_keyboard_for_back = [
            [InlineKeyboardButton("🔙 Ortga", callback_data="back_to_admin_panel")]]
    if text == "🔍Film izlash":
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
                    buttons.append([InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=channel_url)])
                reply_markup = InlineKeyboardMarkup(buttons)
                await update.message.reply_text("❌ Iltimos, barcha kanallarga obuna bo‘ling! Va qayta /start bosing!", reply_markup=reply_markup)
        else:
            inline_keyboard = [
            [InlineKeyboardButton("🎫 Filmni nomi orqali qidirish", callback_data="search_by_title")],
            [InlineKeyboardButton("⏰ So'nggi yuklanganlar", callback_data="search_by_last_added")],
            [InlineKeyboardButton("🎭 Janri orqali qidirish", callback_data="search_by_ganre")],
            [InlineKeyboardButton("🔑 Kodi orqali qidirish", callback_data="search_by_code")],
            [InlineKeyboardButton("🔙 Ortga", callback_data="back")]
        ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await update.message.reply_text("🔍Qidiruv tipini tanlang :", reply_markup=reply_markup)
    
    elif text == "🗄 Boshqarish":  # Admin panel tugmasi bosilganda
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()

            if is_admin:  # Faqat adminlar uchun
                reply_markup = ReplyKeyboardMarkup(admin_keyboard, resize_keyboard=True)
                await update.message.reply_text("🔧 Admin paneliga xush kelibsiz!", reply_markup=reply_markup)
                return ConversationHandler.END 
            else:
                await update.message.reply_text("❌ Siz admin emassiz!")
                return ConversationHandler.END 
    elif text == "📊 Statistikalar":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            if is_admin:
                user_count = await session.execute(select(func.count()).select_from(UserBot))
                user_count = user_count.scalar_one_or_none()
                reply_markup = InlineKeyboardMarkup(inline_keyboard_for_back)
                await update.message.reply_text(f"👥 Foydalanuvchilar: {user_count} ta", reply_markup=reply_markup)
    elif text == "🎥 Filmlarni sozlash":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()

            if is_admin:  # Faqat adminlar uchun
                inline_keyboard = [
            [InlineKeyboardButton("➕ Filmlar qo'shish ", callback_data="add_film")],
            [InlineKeyboardButton("📥 Filmga video qo'shish ", callback_data="add_video_to_film")],
            [InlineKeyboardButton("📝 Filmni tahrirlash", callback_data="edit_film")],
            [InlineKeyboardButton("🔙 Ortga", callback_data="back_to_admin_panel")]
        ]
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                await update.message.reply_text("Quyidagilardan birini tanlang:", reply_markup=reply_markup)
            else:
                await update.message.reply_text("❌ Siz admin emassiz!")
    elif text == "📢 Kanallar":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            if is_admin:  # Faqat adminlar uchun
                inline_keyboard = [
                    [InlineKeyboardButton("🔐 Majburiy kanallarni sozlash", callback_data="forced_channel_settings")],
                    [InlineKeyboardButton("📮 Post yuborish uchun kanallarni sozlash", callback_data="post_send_channel_settings")],
                    [InlineKeyboardButton("🔙 Ortga", callback_data="back_to_admin_panel")]
                ]
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                await update.message.reply_text("Quyidagilardan birini tanlang:", reply_markup=reply_markup)
    elif text == "📬 Post tayyorlash":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            if is_admin:  # Faqat adminlar uchun
                reply_markup = ReplyKeyboardMarkup([["🔙 Ortga"]], one_time_keyboard=True, resize_keyboard=True)
                await update.message.reply_text("🔑 Iltimos, film kodini kiriting:", reply_markup=reply_markup)
                return FILM_CODE_FOR_SEND_TO_CHANNEL
            else:
                await update.message.reply_text("❌ Siz admin emassiz!")
    elif text == "📤 Habar yuborish":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            if is_admin:  # Faqat adminlar uchun
                
                await update.message.reply_text("✍️ Iltimos, habaringizni yuboring")
                return POST_FOR_SEND_TO_CHANNEL
            else:
                await update.message.reply_text("❌ Siz admin emassiz!")

    elif text == "📋 Adminlar":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            if is_admin:  # Faqat adminlar uchun
                admins = await session.execute(select(Admins))
                admins = admins.scalars()
                admins_list = "\n".join([f"{admin.telegram_chat_id}" for admin in admins])
                await update.message.reply_text(f"Adminlar:\n{admins_list}")
            else:
                await update.message.reply_text("❌ Siz admin emassiz!")
    elif text == "🔙 Ortga":
        await menu(update, context)  # Asosiy menyuga qaytarish
    
    else:
        await update.message.reply_text("❌ Noma’lum buyruq!")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    if query.data.startswith("send_"): 
        data = query.data.split("_")  # ["send", "to", "channel", "{chat.id}", "{film.code}"]
        channel_id = data[3]  # Kanal IDsi
        film_code = data[4] 
        channel_id = int(channel_id)
        print(type(channel_id))
        async with get_session() as session:
            film_code = int(film_code)
            movie = await session.execute(select(Movie).where(Movie.code  == film_code))
            movie = movie.scalar_one_or_none()
            if not movie:
                await query.message.delete()
                await query.message.reply_text("❌ Film topilmadi!")
                return
            channel = await session.execute(select(ChannelforBot).where(ChannelforBot.channel_id == cast(channel_id, BigInteger)))
            channel = channel.scalar_one_or_none()
            if not channel:
                await query.message.delete()
                await query.message.reply_text("❌ Kanal topilmadi!")
                return
            inline_keyboard = [
                [InlineKeyboardButton("🔹Tomosha qilish🔹", url=f"https://t.me/{bot_username}?start={movie.code}")]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await context.bot.send_photo(chat_id=channel.channel_id,photo=movie.image, caption=f"🎬 Nomi: {movie.title} \n"
            f"🌍 Davlati: {movie.country} \n"
            f"🔊 Tili: {movie.tili} \n"
            f"📆 Yili: {movie.year} \n"
            f"🎞 Janri: {movie.ganre}", reply_markup=reply_markup) 
    if query.data.startswith("film_"):
        film_code = query.data.split("_")[1]
        async with get_session() as session:
            film_code = int(film_code)
            movie = await session.execute(select(Movie).where(Movie.code  == film_code))
            movie = movie.scalar_one_or_none()
            if film_code == movie.code:
                    await query.message.delete()
                    await query.message.reply_photo(photo=movie.image,
    caption=f"🎬 Nomi: {movie.title} \n"
            f"🌍 Davlati: {movie.country} \n"
            f"🔊 Tili: {movie.tili} \n"
            f"📆 Yili: {movie.year} \n"
            f"🎞 Janri: {movie.ganre}"
)           
                    if not movie.film:
                        await query.message.reply_text(f"{movie.title} filmi hali qo'shilmagan")
                    await query.message.reply_video(video=movie.film, caption=f"{movie.title} filmi")
    user_id = query.from_user.id
    async with get_session() as session:
        is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
        is_admin = is_admin.scalar_one_or_none()

        if query.data == 'back_to_admin_panel':
            try:
                await query.message.delete()
            except:
                pass  
            if is_admin:
                admin_keyboard = [
                ["📊 Statistikalar", "📤 Habar yuborish"],
                ["📬 Post tayyorlash"],
                ["🎥 Filmlarni sozlash"],
                
                ["📢 Kanallar"],
                ["📋 Adminlar"],
                ["🔙 Ortga"]
            ]
                reply_markup = ReplyKeyboardMarkup(admin_keyboard, resize_keyboard=True)
                await query.message.reply_text("🔧 Admin paneliga qaytdik!", reply_markup=reply_markup)
    if query.data == "add_film":
        try:
            await query.message.delete()
        except:
            pass 
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("📌 Iltimos, film nomini kiriting:", reply_markup=reply_markup)
        return FILM_TITLE
    elif query.data == "add_video_to_film":
        try:
            await query.message.delete()
        except:
            pass 
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("📌 Iltimos, film kodini kiriting:", reply_markup=reply_markup)
        return FILM_CODE_FOR_ADD_VIDEO
    elif query.data == "search_by_last_added":
        async with get_session() as session:
            movies = await session.execute(select(Movie).order_by(Movie.id.desc()).limit(10))
            movies = movies.scalars().all()
            if not movies:
                await query.message.edit_text("☹️ Filmlar topilmadi!")
                return
            buttons = []
            for count, movie in enumerate(movies, start=1):
                buttons.append([InlineKeyboardButton(f"{count} {movie.title}", callback_data=f"film_{movie.code}")])
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text("⬇️ So'nggi yuklangan filmlar:", reply_markup=reply_markup)
    elif query.data == "search_by_code":
        try:
            await query.message.delete()
        except:
            pass 
        reply_markup = ReplyKeyboardMarkup([["🔙 Ortga"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("🔑 Iltimos, film kodini kiriting:", reply_markup=reply_markup)
        return FILM_CODE_FOR_SEARCH
    elif query.data == "search_by_ganre":
        try:
            await query.message.delete()
        except:
            pass 
        reply_markup = ReplyKeyboardMarkup([["🔙 Ortga"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("🎭 Iltimos, film janr kiriting:", reply_markup=reply_markup)
        return FILM_SEARCH_BY_GANRE
    elif query.data == "search_by_title":
        try:
            await query.message.delete()
        except:
            pass 
        reply_markup = ReplyKeyboardMarkup([["🔙 Ortga"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("🎫 Iltimos, film nomini kiriting:", reply_markup=reply_markup)
        return FILM_SEARCH_BY_TITLE
    
    elif query.data == "forced_channel_settings":
        inline_keyboard = [
            [InlineKeyboardButton("➕ Qo'shish", callback_data="add_forced_channel")],
            [InlineKeyboardButton("🗑 O'chirish", callback_data="delete_forced_channel")],
            [InlineKeyboardButton("📔 Ro'yhat", callback_data="list_forced_channel")],
            [InlineKeyboardButton("🔙 Ortga", callback_data="back_to_channel_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.message.edit_text("Majburiy obunalarni sozlash bo'limidasiz:", reply_markup=reply_markup)
    elif query.data == "post_send_channel_settings":
        
        inline_keyboard = [
            [InlineKeyboardButton("➕ Qo'shish", callback_data="add_post_send_channel")],
            [InlineKeyboardButton("🗑 O'chirish", callback_data="delete_post_send_channel")],
            [InlineKeyboardButton("📔 Ro'yhat", callback_data="list_post_send_channel")],
            [InlineKeyboardButton("🔙 Ortga", callback_data="back_to_channel_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.message.edit_text("Majburiy obunalarni sozlash bo'limidasiz:", reply_markup=reply_markup)
    elif query.data == "back_to_channel_settings":
        try:
            await query.message.delete()
        except:
            pass 
        inline_keyboard = [
                    [InlineKeyboardButton("🔐 Majburiy kanallarni sozlash", callback_data="forced_channel_settings")],
                    [InlineKeyboardButton("📮 Post yuborish uchun kanallarni sozlash", callback_data="post_send_channel_settings")],
                    [InlineKeyboardButton("🔙 Ortga", callback_data="back_to_admin_panel")]
                ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.message.reply_text("Quyidagilardan birini tanlang:", reply_markup=reply_markup)

    elif query.data == "add_forced_channel":
        try:
            await query.message.delete()
        except:
            pass
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("📌 Iltimos, qo'shmoqchi kanal idisi ni kiriting:", reply_markup=reply_markup)
        return CHANNEL_ID_FOR_ADD_FORCED_CHANNEL
    elif query.data == "add_post_send_channel":
        try:
            await query.message.delete()
        except:
            pass
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text("📌 Iltimos, qo'shmoqchi kanal idisi ni kiriting:", reply_markup=reply_markup)
        return CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL
    elif query.data == "delete_forced_channel":
        try:
            await query.message.delete()
        except:
            pass
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        async with get_session() as session:
            forced_channels = await session.execute(select(Channelforforced))
            forced_channels = forced_channels.scalars().all()
            channel_ids = "\n".join(f"📌 {channel.channel_id}" for channel in forced_channels)
            await query.message.reply_text(f"📌 Iltimos, quyidagi kanallardan birini tanlang:\n\n{channel_ids}", reply_markup=reply_markup)
            return CHANNEL_ID_FOR_ADD_FORCED_CHANNEL
    elif query.data == "delete_post_send_channel":
        try:
            await query.message.delete()
        except:
            pass
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        async with get_session() as session:
            forced_channels = await session.execute(select(ChannelforBot))
            forced_channels = forced_channels.scalars().all()
            channel_ids = "\n".join(f"📌 {channel.channel_id}" for channel in forced_channels)
            await query.message.reply_text(f"📌 Iltimos, quyidagi kanallardan birini tanlang:\n\n{channel_ids}", reply_markup=reply_markup)
        return CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL
    elif query.data == "list_forced_channel":
        async with get_session() as session:
            forced_channels = await session.execute(select(Channelforforced))
            forced_channels = forced_channels.scalars().all()
            if not forced_channels:
                await query.message.edit_text("😐 Majburiy kanallar topilmadi!")
                return
            channel_ids = "\n".join(f"📌 {channel.channel_id}" for channel in forced_channels)
            await query.message.edit_text(f"📌 Majburiy kanallar:\n\n{channel_ids}", reply_markup=None)
    elif query.data == "list_post_send_channel":
            async with get_session() as session:
                forced_channels = await session.execute(select(ChannelforBot))
                forced_channels = forced_channels.scalars().all()
                if not forced_channels:
                    await query.message.edit_text("😐 Post yuborish kanallar topilmadi!")
                    return
                channel_ids = "\n".join(f"📌 {channel.channel_id}" for channel in forced_channels)
                await query.message.edit_text(f"📌 Post yuborish kanallar:\n\n{channel_ids}", reply_markup=None)

    elif query.data == "back":
        await query.message.edit_text("🔙 Ortga qaytdik!", reply_markup=None)

