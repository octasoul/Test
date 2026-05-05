import os
import io
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from rembg import remove
from PIL import Image

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ.get("BOT_TOKEN")  # Set this in your hosting env vars


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to BG Remover Bot!\n\n"
        "📸 Just send me any photo and I'll remove the background instantly — for FREE!\n\n"
        "✅ Supports: people, objects, products, logos\n"
        "⚡ Powered by rembg (runs 100% locally, no data sent to any API)"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *How to use:*\n\n"
        "1. Send a photo (as photo or as file/document)\n"
        "2. Wait a few seconds ⏳\n"
        "3. Get your image with transparent background! 🎉\n\n"
        "_Tip: Send as document for best quality_",
        parse_mode="Markdown"
    )


async def remove_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle both photo messages and document (file) uploads."""
    msg = await update.message.reply_text("⏳ Processing your image, please wait...")

    try:
        # Get file — prefer document for full quality, fallback to photo
        if update.message.document:
            file = await update.message.document.get_file()
        elif update.message.photo:
            file = await update.message.photo[-1].get_file()  # Highest resolution
        else:
            await msg.edit_text("❌ Please send a valid image.")
            return

        # Download image into memory
        img_bytes = await file.download_as_bytearray()
        input_image = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        # Remove background
        output_bytes = remove(img_bytes)
        output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

        # Save as PNG (supports transparency)
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        await msg.delete()
        await update.message.reply_document(
            document=output_buffer,
            filename="removed_bg.png",
            caption="✅ Background removed! Sent as PNG with transparency."
        )

    except Exception as e:
        logging.error(f"Error: {e}")
        await msg.edit_text(
            "❌ Something went wrong. Please try again with a different image.\n"
            f"Error: {str(e)}"
        )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, remove_background))

    print("🤖 Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
