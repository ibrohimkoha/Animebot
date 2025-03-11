from sqlalchemy import select
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, 
    ConversationHandler, CallbackContext
)
from db import get_session
from models import Admins, Movie,  ChannelforBot, Channelforforced, UserBot
from db import bot_username
from telegram.error import TelegramError, Forbidden, BadRequest
FILM_TITLE, FILM_YEAR, FILM_IMAGE, FILM_GANRE, FILM_COUNTRY,FILM_TILI, FILM_CODE = range(7)
FILM_CODE_FOR_ADD_VIDEO, FILM_VIDEO  = range(2) 
FILM_CODE_FOR_SEARCH = 1
FILM_SEARCH_BY_GANRE = 1
FILM_SEARCH_BY_TITLE = 1
FILM_CODE_FOR_SEND_TO_CHANNEL = 1
CHANNEL_ID_FOR_ADD_FORCED_CHANNEL = 1
CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL = 1
CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL = 1 
CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL = 1 
POST_FOR_SEND_TO_CHANNEL = 1
async def film_title(update: Update, context: CallbackContext):
    if len(update.message.text) > 100:
        await update.message.reply_text("Film nomi 99 simvolda ola bilmaydi!")
        return FILM_TITLE
    context.user_data["film_title"] = update.message.text  # Film nomini saqlaymiz
    reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📅 Film chiqarilgan yilini kiriting:", reply_markup=reply_markup)
    return FILM_YEAR

async def film_year(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.from_user.id
    if text == "🗄 Boshqarish":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]       
            
            if is_admin:
                reply_markup = ReplyKeyboardMarkup(admin_keyboard)
                await update.message.reply_text("⬅️ Admin paneliga qaytdik!", reply_markup=reply_markup)
                return ConversationHandler.END
            else:
                await update.message.reply_text("❌ Siz admin emassiz! Xatolik yuzaga kelgan bo'lsa /start bosing!")
                return ConversationHandler.END
    try:
        film_year_int = int(update.message.text)
        if not 1900 <= film_year_int <= 2100 :
            await update.message.reply_text("1900-yilning kiritilgan va 2100-yilning kiritilgan son qiymat bilan kiriting!")
            return FILM_YEAR
        context.user_data["film_year"] =  film_year_int
        reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
        "🖼 Film uchun rasm yuboring:", reply_markup=reply_markup)
        return FILM_IMAGE  
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return FILM_YEAR
    
    
async def film_image(update: Update, context: CallbackContext):
    """Faqat rasm yuborilganda file_id ni saqlaydi, aks holda xatolik chiqaradi"""
    if not update.message.photo:  # Agar rasm yuborilmagan bo'lsa
        await update.message.reply_text("❌ Iltimos, faqat rasm yuboring!")
        return  # Funksiyani yakunlaymiz, hech narsa saqlamaymiz

    # Agar rasm yuborilgan bo'lsa, file_id ni saqlaymiz
    context.user_data["film_image"] = update.message.photo[-1].file_id  
    reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📌 Filmning janrini kiriting:", reply_markup=reply_markup)
    return FILM_GANRE   

async def film_ganre(update: Update, context: CallbackContext):
    if len(update.message.text) > 50:
        await update.message.reply_text("Janrning uzunlug'i 49 simvol ga teng bo'lishi kerak!")
        return FILM_GANRE  # Funksiyani yakunlaymiz, hech narsa saqlamaymiz
    context.user_data["film_ganre"] = update.message.text  # Filmning janrini saqlaymiz
    reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("🌎 Filmning davlatini kiriting:", reply_markup=reply_markup)
    return FILM_COUNTRY

async def film_country(update: Update, context: CallbackContext):
    if len(update.message.text) > 40:
        await update.message.reply_text("Muvofaqqiyot bosqichining uzunlug'i 39 simvol ga teng bo'lishi kerak!")
        return FILM_COUNTRY  # Funksiyani yakunlaymiz, hech narsa saqlamaymiz
    context.user_data["film_country"] = update.message.text  # Filmning muvofaqqiyot bosqichini saqlaymiz
    reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("🌎 Filmning tili kiriting:", reply_markup=reply_markup)
    return FILM_TILI

async def film_tili(update: Update, context: CallbackContext):
    if len(update.message.text) > 30:
        await update.message.reply_text("Filmning tili 29 simvolga ola bilmaydi!")
        return FILM_TILI  # Funksiyani yakunlaymiz, hech narsa saqlamaymiz
    context.user_data["film_tili"] = update.message.text  # Filmning tili saqlaymiz
    reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("🖥 Filmning kodini kiriting:", reply_markup=reply_markup)
    return FILM_CODE

async def film_code(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.from_user.id
    if text == "🗄 Boshqarish":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).where(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]       
            
            if is_admin:
                reply_markup = ReplyKeyboardMarkup(admin_keyboard)
                await update.message.reply_text("⬅️ Admin paneliga qaytdik!", reply_markup=reply_markup)
                return ConversationHandler.END
            else:
                await update.message.reply_text("❌ Siz admin emassiz! Xatolik yuzaga kelgan bo'lsa /start bosing!")
                return ConversationHandler.END
    try:
        film_code_int = int(update.message.text)
        if not 1 <= film_code_int <= 10000 :
            await update.message.reply_text("Son qiymati juda kotta")
            return FILM_YEAR
        async with get_session() as session:
            exist_film_code = await session.execute(select(Movie).where(Movie.code == film_code_int))
            exist_film_code = exist_film_code.scalar_one_or_none()
            if exist_film_code:
                await update.message.reply_text("Bu kodli film mavjud!")
                return FILM_CODE
            film = Movie(
                title=context.user_data["film_title"],
                year=context.user_data["film_year"],
                image=context.user_data["film_image"],
                ganre=context.user_data["film_ganre"],
                country=context.user_data["film_country"],
                tili=context.user_data["film_tili"],
                code=film_code_int
            )
            session.add(film)
            await session.commit()
            admin_keyboard = [
                ["📊 Statistikalar", "📤 Habar yuborish"],
                ["📬 Post tayyorlash"],
                ["🎥 Filmlarni sozlash"],
            
                ["📢 Kanallar"],
                ["📋 Adminlar"],
                ["🔙 Ortga"]
            ]
            reply_markup = ReplyKeyboardMarkup(admin_keyboard, resize_keyboard=True)
            await update.message.reply_text(f"✅ Filmingiz qo'shildi!, uning kodi {film_code_int}", reply_markup=reply_markup)
            return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return FILM_CODE

async def film_code_for_add_video(update: Update, context: CallbackContext):
    try:
        film_code_int = int(update.message.text)
        async with get_session() as session:
            exist_film_code = await session.execute(select(Movie).where(Movie.code == film_code_int))
            exist_film_code = exist_film_code.scalar_one_or_none()
            if not exist_film_code:
                await update.message.reply_text("Bu kodli film mavjud emas!")
                return FILM_CODE_FOR_ADD_VIDEO
            context.user_data["film_code_for_add_video"] = film_code_int
            reply_markup = ReplyKeyboardMarkup([["🗄 Boshqarish"]], one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Video yuboring yuboring:", reply_markup=reply_markup)
            return FILM_VIDEO
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return FILM_CODE_FOR_ADD_VIDEO


async def film_video(update: Update, context: CallbackContext):
    film_code = context.user_data.get("film_code_for_add_video")  
    if not film_code:
        await update.message.reply_text("❌ Film kodi yo‘q! Avval film kodini yuboring.")
        return  

    async with get_session() as session:
        result = await session.execute(select(Movie).where(Movie.code == film_code))
        film = result.scalar_one_or_none()  
        if not film:
            await update.message.reply_text("❌ Bu kodga tegishli film topilmadi!")
            return  

        film.film = update.message.video.file_id  
        session.add(film)
        await session.commit()  
        admin_keyboard = [
                ["📊 Statistikalar", "📤 Habar yuborish"],
                ["📬 Post tayyorlash"],
                ["🎥 Filmlarni sozlash"],
            
                ["📢 Kanallar"],
                ["📋 Adminlar"],
                ["🔙 Ortga"]
            ]
        reply_markup = ReplyKeyboardMarkup(admin_keyboard, resize_keyboard=True)
        await update.message.reply_text("✅ Film videosi saqlandi!", reply_markup=reply_markup)
        return ConversationHandler.END
    

async def film_code_for_search(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text
    if text == "🔙 Ortga":
        async with get_session() as session:
            is_admin = await session.execute(select(Admins).filter(Admins.telegram_chat_id == user_id))
            is_admin = is_admin.scalar_one_or_none()
            if is_admin:
                keyboard_for_admin = [
        ["🔍Film izlash"],
        ["💵 Reklama va Homiylik"],
        ["🗄 Boshqarish"]
    ]           
                reply_markup = ReplyKeyboardMarkup(keyboard_for_admin, resize_keyboard=True)
                await update.message.reply_text("Kerakli bo‘limni tanlang:", reply_markup=reply_markup)
                return ConversationHandler.END
                
            keyboard_for_user = [
        ["🔍Film izlash"],
        ["💵 Reklama va Homiylik"]
    ]   
            reply_markup = ReplyKeyboardMarkup(keyboard_for_user, resize_keyboard=True)
            await update.message.reply_text("Kerakli bo‘limni tanlang:", reply_markup=reply_markup)
            return ConversationHandler.END
    try:
        film_code_int = int(update.message.text)
        async with get_session() as session:
            exist_film = await session.execute(select(Movie).where(Movie.code == film_code_int))
            exist_film = exist_film.scalar_one_or_none()
            if not exist_film:
                await update.message.reply_text("Bu kodli film mavjud emas!")
                return FILM_CODE_FOR_SEARCH
            inline_keyboard = [
            [InlineKeyboardButton("🎥 Filmni tomosha qilish", callback_data=f"film_{exist_film.code}")]]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await update.message.reply_photo(
    photo=exist_film.image,
    caption=f"🎬 Nomi: {exist_film.title} \n"
            f"🌍 Davlati: {exist_film.country} \n"
            f"🔊 Tili: {exist_film.tili} \n"
            f"📆 Yili: {exist_film.year} \n"
            f"🎞 Janri: {exist_film.ganre}",
    reply_markup=reply_markup
)
            
            return ConversationHandler.END 
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return FILM_CODE_FOR_SEARCH
    

async def film_search_by_ganre(update: Update, context: CallbackContext):
    ganre = update.message.text.strip() 
    async with get_session() as session:
        exist_films = await session.execute(
            select(Movie).where(Movie.ganre.ilike(f"%{ganre}%")).limit(10)  # 🔹 Qisman va katta-kichik harfga befarq qidirish
        )
        exist_films = exist_films.scalars().all()
        if not exist_films:
            await update.message.reply_text("Bu janrda film topilmadi!")
            return FILM_SEARCH_BY_GANRE
        inline_keyboard = [
            [InlineKeyboardButton(f"{count+1}. {film.title}", callback_data=f"film_{film.code}")
              ] for count, film in enumerate(exist_films)
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(f"⬇️ Qidiruv natijalari:", reply_markup=reply_markup)
        return ConversationHandler.END
    

async def film_search_by_title(update: Update, context: CallbackContext):
    title = update.message.text.strip() 
    async with get_session() as session:
        exist_films = await session.execute(
            select(Movie).where(Movie.title.ilike(f"%{title}%")).limit(10)  # 🔹 Qisman va katta-kichik harfga befarq qidirish
        )
        exist_films = exist_films.scalars().all()
        if not exist_films:
            await update.message.reply_text("Bu nomdagi film topilmadi!")
            return FILM_SEARCH_BY_TITLE
        inline_keyboard = [
            [InlineKeyboardButton(f"{count+1}. {film.title}", callback_data=f"film_{film.code}")
              ] for count, film in enumerate(exist_films)
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(f"⬇️ Qidiruv natijalari:", reply_markup=reply_markup)
        return ConversationHandler.END
    
async def film_code_for_send_to_channel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text
    if text == "🔙 Ortga":  # Admin panel tugmasi bosilganda
        admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]
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
    try:
        film_code_int = int(update.message.text)
        async with get_session() as session:
            exist_film = await session.execute(select(Movie).where(Movie.code == film_code_int))
            exist_film = exist_film.scalar_one_or_none()
            if not exist_film:
                await update.message.reply_text("Bu kodli film mavjud emas!")
                return FILM_CODE_FOR_SEND_TO_CHANNEL
            channels = await session.execute(select(ChannelforBot))
            channels = channels.scalars().all()
            inline_keyboard = []
            inline_keyboard.append([InlineKeyboardButton("🔹Tomosha qilish🔹", url=f"https://t.me/{bot_username}?start={exist_film.code}")])
            not_connected_channels = []
            for channel in channels:
                try:
                    chat = await context.bot.get_chat(channel.channel_id)
                    inline_keyboard.append([
            InlineKeyboardButton(f"{chat.username}", callback_data=f"send_to_channel_{chat.id}_{exist_film.code}")
        ])
                except TelegramError:
                    not_connected_channels.append(channel.channel_id)
                    continue  # Xato bo'lsa, ushbu kanaldan o'tib ketamiz
            if not_connected_channels:
                 await update.message.reply_text( "⚠ Quyidagi kanallarga bot ulanmagan:\n" + "\n".join(map(str, not_connected_channels)))
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await update.message.reply_photo(photo=exist_film.image, caption=f"🎬 Nomi: {exist_film.title} \n"
            f"🌍 Davlati: {exist_film.country} \n"
            f"🔊 Tili: {exist_film.tili} \n"
            f"📆 Yili: {exist_film.year} \n"
            f"🎞 Janri: {exist_film.ganre}", reply_markup=reply_markup) 
            return ConversationHandler.END          
            

    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return FILM_CODE_FOR_SEND_TO_CHANNEL
    
async def channel_id_for_add_forced_channel(update: Update, context: CallbackContext):
    admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]
    channel_id = update.message.text
    if channel_id == "🗄 Boshqarish":
        reply_markup = ReplyKeyboardMarkup(admin_keyboard)
        await update.message.reply_text("🔧 Admin paneliga xush kelibsiz!", reply_markup=reply_markup)
        return ConversationHandler.END
    if not channel_id.startswith("-100"):
        await update.message.reply_text("❌ Noto‘g‘ri kanal ID !")
        return CHANNEL_ID_FOR_ADD_FORCED_CHANNEL
    try:
        channel_id = int(channel_id)
        async with get_session() as session:
            existed_channel = await session.execute(select(Channelforforced).where(Channelforforced.channel_id == channel_id))
            existed_channel = existed_channel.scalar_one_or_none()
            if existed_channel:
                await update.message.reply_text("❌ Bu kanal qo'shilgan ")
                return CHANNEL_ID_FOR_ADD_FORCED_CHANNEL
            try:
                chat = await context.bot.get_chat(channel_id)
                channel = Channelforforced(channel_id=channel_id)
                session.add(channel)
                await session.commit()
                reply_markup = ReplyKeyboardMarkup(admin_keyboard)
                await update.message.reply_text(f"✅ kanal qo'shildi", reply_markup=reply_markup)
                return ConversationHandler.END
            except Forbidden:
                channel = Channelforforced(channel_id=channel_id)
                session.add(channel)
                await session.commit()
                reply_markup = ReplyKeyboardMarkup(admin_keyboard)
                await update.message.reply_text(f"✅ kanal qo'shildi, ushbu kanalga bot ulanmagan", reply_markup=reply_markup)
                return ConversationHandler.END
            except BadRequest:
                await update.message.reply_text("❌ Noto‘g‘ri kanal ID!")
                return CHANNEL_ID_FOR_ADD_FORCED_CHANNEL
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return CHANNEL_ID_FOR_ADD_FORCED_CHANNEL

async def channel_id_for_add_post_send_channel(update: Update, context: CallbackContext):
    admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]
    channel_id = update.message.text
    if channel_id == "🗄 Boshqarish":
        reply_markup = ReplyKeyboardMarkup(admin_keyboard)
        await update.message.reply_text("🔧 Admin paneliga xush kelibsiz!", reply_markup=reply_markup)
        return ConversationHandler.END
    if not channel_id.startswith("-100"):
        await update.message.reply_text("❌ Noto‘g‘ri kanal ID !")
        return CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL
    try:
        channel_id = int(channel_id)
        async with get_session() as session:
            existed_channel = await session.execute(select(ChannelforBot).where(ChannelforBot.channel_id == channel_id))
            existed_channel = existed_channel.scalar_one_or_none()
            if existed_channel:
                await update.message.reply_text("❌ Bu kanal qo'shilgan ")
                return CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL
            try:
                chat = await context.bot.get_chat(channel_id)
                channel = Channelforforced(channel_id=channel_id)
                session.add(channel)
                await session.commit()
                reply_markup = ReplyKeyboardMarkup(admin_keyboard)
                await update.message.reply_text(f"✅ kanal qo'shildi", reply_markup=reply_markup)
                return ConversationHandler.END
            except Forbidden:
                channel = Channelforforced(channel_id=channel_id)
                session.add(channel)
                await session.commit()
                reply_markup = ReplyKeyboardMarkup(admin_keyboard)
                await update.message.reply_text(f"✅ kanal qo'shildi, ushbu kanalga bot ulanmagan", reply_markup=reply_markup)
                return ConversationHandler.END
            except BadRequest:
                await update.message.reply_text("❌ Noto‘g‘ri kanal ID!")
                return CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL

        
async def channel_id_for_delete_forced_channel(update: Update, context: CallbackContext):
    admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]
    channel_id = update.message.text
    if channel_id == "🗄 Boshqarish":
        reply_markup = ReplyKeyboardMarkup(admin_keyboard)
        await update.message.reply_text("🔧 Admin paneliga xush kelibsiz!", reply_markup=reply_markup)
        return ConversationHandler.END
    if not channel_id.startswith("-100"):
        await update.message.reply_text("❌ Noto‘g‘ri kanal ID !")
        return CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL
    try:
        channel_id = int(channel_id)
        async with get_session() as session:
            existed_channel = await session.execute(select(Channelforforced).where(Channelforforced.channel_id == channel_id))
            existed_channel = existed_channel.scalar_one_or_none()
            if not existed_channel:
                await update.message.reply_text("❌ Bu kanal mavjud emas ")
                return CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL
            session.delete(existed_channel)
            await session.commit()
            reply_markup = ReplyKeyboardMarkup(admin_keyboard)
            await update.message.reply_text(f"✅ {channel_id} o'chirildi", reply_markup=reply_markup)
            return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Son qiymati bilan kiriting iltimos!")
        return CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL
    
async def channel_id_for_delete_post_send_channel(update: Update, context: CallbackContext):
    admin_keyboard = [
        ["📊 Statistikalar","📤 Habar yuborish"],
        ["📬 Post tayyorlash"],
        ["🎥 Filmlarni sozlash"],
    
        ["📢 Kanallar"],
        ["📋 Adminlar"],
        ["🔙 Ortga"]
    ]
    channel_id = update.message.text
    if channel_id == "🗄 Boshqarish":
        reply_markup = ReplyKeyboardMarkup(admin_keyboard)
        await update.message.reply_text("🔧 Admin paneliga xush kelibsiz!", reply_markup=reply_markup)
        return ConversationHandler.END
    if not channel_id.startswith("-100"):
        await update.message.reply_text("❌ Noto‘g‘ri kanal ID !")
        return CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL
    try:
        channel_id = int(channel_id)
        async with get_session() as session:
            existed_channel = await session.execute(select(ChannelforBot).where(ChannelforBot.channel_id == channel_id))
            existed_channel = existed_channel.scalar_one_or_none()
            if not existed_channel:
                await update.message.reply_text("❌ Bu kanal mavjud emas ")
                return CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL
            session.delete(existed_channel)
            await session.commit()
            reply_markup = ReplyKeyboardMarkup(admin_keyboard)
            await update.message.reply_text(f"✅ {channel_id} o'chirildi", reply_markup=reply_markup)
            return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("❌ Noto‘g‘ri kanal ID!")
        return CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL
    

async def send_message_to_all(update: Update, context: CallbackContext):
    """Rasm, video yoki oddiy xabarni barcha foydalanuvchilarga yuboradi"""
    message = update.message

    async with get_session() as session:
        users = await session.execute(select(UserBot))
        users = users.scalars().all()
        users = [user.telegram_chat_id for user in users]

    count = 0
    for user_id in users:
        try:
            if message.photo:
                # Agar xabar rasm bo'lsa
                photo = message.photo[-1].file_id
                caption = message.caption or "📷 Rasm"
                await context.bot.send_photo(chat_id=user_id, photo=photo, caption=caption)

            elif message.video:
                # Agar xabar video bo'lsa
                video = message.video.file_id
                caption = message.caption or "🎥 Video"
                await context.bot.send_video(chat_id=user_id, video=video, caption=caption)

            elif message.text:
                # Agar oddiy matn bo'lsa
                await context.bot.send_message(chat_id=user_id, text=message.text)

            count += 1

        except Exception:
            continue

    await update.message.reply_text(f"✅ {count} ta foydalanuvchiga xabar yuborildi!")
    return ConversationHandler.END