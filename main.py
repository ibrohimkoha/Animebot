import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from keyboard import button_callback, menu, handle_buttons
from channels import check_subscription
from handlers import (FILM_CODE_FOR_ADD_VIDEO, FILM_SEARCH_BY_TITLE, FILM_TITLE, 
                      FILM_YEAR,FILM_SEARCH_BY_GANRE, 
                      FILM_IMAGE, FILM_CODE_FOR_SEND_TO_CHANNEL,
                      FILM_GANRE, CHANNEL_ID_FOR_ADD_FORCED_CHANNEL,
                      FILM_COUNTRY, CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL,
                      FILM_TILI,CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL,POST_FOR_SEND_TO_CHANNEL,
                      FILM_CODE, FILM_CODE_FOR_SEARCH,CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL,
                      FILM_VIDEO, film_code,
                        film_country,
                          film_ganre,send_message_to_all,
                            film_image,channel_id_for_delete_forced_channel,
                              film_tili, film_code_for_send_to_channel,channel_id_for_delete_post_send_channel,
                                film_title, film_video,channel_id_for_add_post_send_channel,
                                  film_year,  film_code_for_add_video, film_code_for_search, film_search_by_ganre, film_search_by_title, channel_id_for_add_forced_channel)

def main():
    # Loglarni sozlash
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.INFO
    )

    # Bot tokeningizni kiritamiz
    application = Application.builder().token("6311604386:AAE0A3u5ClLgU2vWdyWdpUX6ttw7meOJoGI").build()
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_callback, pattern="^add_film$")  # `add_film` tugmasi bosilganda
        ],
        states={
            FILM_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_title)],
            FILM_YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_year)],
            FILM_IMAGE: [MessageHandler(filters.PHOTO, film_image)],
            FILM_GANRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_ganre)],
            FILM_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_country)],
            FILM_TILI: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_tili)],
            FILM_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_code)],
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🗄 Boshqarish$"), handle_buttons)]
    )
    conv_handler_for_video_add = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^add_video_to_film$")],
        states={
            FILM_CODE_FOR_ADD_VIDEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_code_for_add_video )],
            FILM_VIDEO: [MessageHandler(filters.VIDEO & ~filters.COMMAND, film_video )],
                },

        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🗄 Boshqarish$"), handle_buttons)]
    )
    conv_handler_for_search_video_for_code = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^search_by_code$")],
        states={
            FILM_CODE_FOR_SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_code_for_search)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🔙 Ortga$"), handle_buttons)]
    )
    conv_handler_for_search_video_by_ganre = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^search_by_ganre$")],
        states={
            FILM_SEARCH_BY_GANRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_search_by_ganre)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🔙 Ortga$"), handle_buttons)]
    )
    conv_handler_for_search_video_by_title = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^search_by_title$")],
        states={
            FILM_SEARCH_BY_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_search_by_title)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🔙 Ortga$"), handle_buttons)]
    )
    conv_handler_for_send_to_channel = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r"^📬 Post tayyorlash$"), handle_buttons)],
        states={
            FILM_CODE_FOR_SEND_TO_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, film_code_for_send_to_channel)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🔙 Ortga$"), handle_buttons)]
    )
    conv_handler_for_foced_channel_add = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^add_forced_channel$")],
        states={
            CHANNEL_ID_FOR_ADD_FORCED_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_id_for_add_forced_channel)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🗄 Boshqarish$"), handle_buttons)]
    )
    conv_handler_for_post_send_channel_add = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^add_post_send_channel$")],
        states={
            CHANNEL_ID_FOR_ADD_POST_SEND_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_id_for_add_post_send_channel)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🗄 Boshqarish$"), handle_buttons)]
    )
    conv_handler_for_foced_channel_delete = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^delete_forced_channel$")],
        states={
            CHANNEL_ID_FOR_DELETE_FORCED_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_id_for_delete_forced_channel)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🗄 Boshqarish$"), handle_buttons)]
    )
    conv_handler_for_post_send_channel_delete = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern="^delete_post_send_channel$")],
        states={
            CHANNEL_ID_FOR_DELETE_POST_SEND_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_id_for_delete_post_send_channel)]
        },
        fallbacks=[MessageHandler(filters.TEXT & filters.Regex(r"^🗄 Boshqarish$"), handle_buttons)]
    )
    conv_handler_for_post_send_all = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex(r"^📤 Habar yuborish$"), handle_buttons)],
        states={
            POST_FOR_SEND_TO_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_message_to_all)]
        },
        fallbacks=[]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(conv_handler_for_video_add)
    application.add_handler(conv_handler_for_search_video_for_code)
    application.add_handler(conv_handler_for_search_video_by_ganre)
    application.add_handler(conv_handler_for_search_video_by_title)
    application.add_handler(conv_handler_for_send_to_channel)
    application.add_handler(conv_handler_for_foced_channel_add)
    application.add_handler(conv_handler_for_foced_channel_delete)
    application.add_handler(conv_handler_for_post_send_channel_add)
    application.add_handler(conv_handler_for_post_send_channel_delete)
    application.add_handler(conv_handler_for_post_send_all)
    application.add_handler(CommandHandler("start", check_subscription))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    application.add_handler(CallbackQueryHandler(button_callback))
    # Botni polling usulida ishga tushuramiz
    application.run_polling()

if __name__ == '__main__':
    main()
