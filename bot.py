import os
import openai
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


openai.api_key = 'YOUR_OPEN_AI_API_KEY_HERE'


TELEGRAM_BOT_TOKEN = 'BOT_TOKEN_HERE'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your AI assistant. Ask me anything!')

async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  
    
    
    if user_message.lower().startswith("generate image:"):
        prompt = user_message[len("generate image:"):].strip()
        
        
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"  
            )
            image_url = response['data'][0]['url']

            
            await update.message.reply_photo(photo=image_url)
        except Exception as e:
            await update.message.reply_text(f"An error occurred while generating the image: {e}")
    else:
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            ai_response = response['choices'][0]['message']['content'].strip()

            
            await update.message.reply_text(ai_response)
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")

def main():
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    
    application.run_polling()

if __name__ == '__main__':
    main()
