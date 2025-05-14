import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot Token from environment variable (set in Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# CZKK contract addresses
CZKK_CONTRACT_BSC = "0xd5defcb306d93d4cd5dd59e66c8d4dc3b74ef096"
CZKK_CONTRACT_ETH = "0x5dBbD676f70cF9Aac23b25A28e841239fa8d2685"

# Dexscreener pool URLs
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex/pairs/bsc"
PAIRS = {
    "usdt": f"{DEXSCREENER_API}/0x06313b57eac23e0c005a76f81972175c7e8f42ef",
    "btc": f"{DEXSCREENER_API}/0x3458ae2d9409f138a879fca6ff59cb0d397769bb",
    "bnb": f"{DEXSCREENER_API}/0x862c173c27cbe6a29ec495f4a2cba4fe21da9689",
}

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch price from Dexscreener
def get_price_from_dexscreener(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data["pair"]["priceUsd"])
    except Exception as e:
        logger.error(f"Error fetching price from {url}: {e}")
        return None

# Command Handlers
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price_from_dexscreener(PAIRS["btc"])
    if price:
        await update.message.reply_text(f"BTCB/CZKK: ${price:.2f} USD")
    else:
        await update.message.reply_text("Unable to fetch BTC/CZKK rate.")

async def usdt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price_from_dexscreener(PAIRS["usdt"])
    if price:
        await update.message.reply_text(f"USDT/CZKK: ${price:.4f} USD")
    else:
        await update.message.reply_text("Unable to fetch USDT/CZKK rate.")

async def bnb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price_from_dexscreener(PAIRS["bnb"])
    if price:
        await update.message.reply_text(f"WBNB/CZKK: ${price:.4f} USD")
    else:
        await update.message.reply_text("Unable to fetch WBNB/CZKK rate.")

async def czkk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        f"CZKK Contract Addresses:\n\n"
        f"🔗 BSC: `{CZKK_CONTRACT_BSC}`\n"
        f"🔗 Ethereum: `{CZKK_CONTRACT_ETH}`"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# Main Bot App
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler(["btc", "BTC"], btc))
    app.add_handler(CommandHandler(["usdt", "USDT"], usdt))
    app.add_handler(CommandHandler(["bnb", "BNB"], bnb))
    app.add_handler(CommandHandler(["czkk", "CZKK"], czkk))

    print("Bot is running...")
    await app.run_polling()

# Entry Point
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
