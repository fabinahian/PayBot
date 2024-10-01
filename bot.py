from telegram import Update
from telegram.ext import Application, CommandHandler
import config
import database

DEBUG = True

def debug_message(message):
    if DEBUG:
        print(f"[DEBUG]: {message}")

async def user_is_admin(update: Update):
    user_id = update.effective_user.id
    chat_admins = await update.effective_chat.get_administrators()
    for admin in chat_admins:
        if admin.user.id == user_id:
            return True
    return False

async def start(update: Update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    await context.bot.send_message(chat_id=chat_id, text=f"Welcome {user.first_name}! Type /help to see what I can do 😎")

async def help_command(update: Update, context):
    chat_id = update.effective_chat.id
    help_text = (
        "Here are all the cool things I can do:\n"
        "/add 'name' - Add yourself to the system!\n"
        "/editname 'newname' - Edit your name\n"
        "/addfund @username 'amount' - Admins can add funds\n"
        "/deductfund @username 'amount' - Admins can deduct funds\n"
        "/pay 'description' 'amount' - Make a payment\n"
        "/showmybalance - Show your balance\n"
        "/showallbalance - Show all balances\n"
        "/reset - Admins can reset the bot data\n"
    )
    await context.bot.send_message(chat_id=chat_id, text=help_text)

async def reset(update: Update, context):
    if not await user_is_admin(update):
        await update.message.reply_text("Only admins can reset the bot data!")
        return
    database.reset_all_users()
    await update.message.reply_text("The bot has been reset! All users removed. 🎉")

async def add_user(update: Update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = context.args[0].strip()

    if database.add_user(user_id, username):
        await context.bot.send_message(chat_id=chat_id, text=f"User {username} added! 🎉")
    else:
        await context.bot.send_message(chat_id=chat_id, text="You are already in the database! 😎")

async def add_fund(update: Update, context):
    if not await user_is_admin(update):
        await update.message.reply_text("Nice try, but only admins can add funds! 😎")
        return
    try:
        partial_name = context.args[0].strip()
        amount = float(context.args[1])
        if amount <= 0:
            await update.message.reply_text("Amount must be positive.")
            return
        possible_users = database.get_users_by_prefix(partial_name)

        if len(possible_users) == 1:
            user_id = possible_users[0][2]
            database.add_fund(user_id, amount)
            new_balance = database.get_balance(user_id)
            await update.message.reply_text(
                f"🎉 Woohoo! Added {amount:.2f} to {possible_users[0][0]}'s balance! 💰\n"
                f"Updated balance for {possible_users[0][0]}: {new_balance:.2f} 💸"
            )
        elif len(possible_users) > 1:
            user_list = "\n".join([f"{name}" for name, _, _ in possible_users])
            await update.message.reply_text(f"Multiple matches found, please be more specific:\n{user_list} 🤔")
        else:
            await update.message.reply_text(f"Oops! No users found with the name '{partial_name}' 😅.")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid username and amount. 😅")

async def deduct_fund(update: Update, context):
    if not await user_is_admin(update):
        await update.message.reply_text("Only admins can deduct funds! 😤")
        return
    try:
        target_username = context.args[0].strip()
        amount = float(context.args[1])
        if amount <= 0:
            await update.message.reply_text("Amount must be positive.")
            return
        user_id = database.get_user_id_by_username(target_username)
        if user_id:
            database.deduct_fund(user_id, amount)
            await update.message.reply_text(f"Deducted {amount:.2f} from {target_username}'s balance! 💰")
        else:
            await update.message.reply_text("User not found!")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a username and valid amount.")

async def pay(update: Update, context):
    user_id = update.effective_user.id
    try:
        description = context.args[0]
        amount = float(context.args[1])
        if amount <= 0:
            await update.message.reply_text("Amount must be positive.")
            return
        database.deduct_fund(user_id, amount)
        new_balance = database.get_balance(user_id)
        await update.message.reply_text(
            f"🛍️ Payment for {description} of {amount:.2f} made! 💸\n"
            f"Your new balance is {new_balance:.2f}. Time to save up! 💰"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("Oops! Please provide a valid description and positive amount. 🤔")

async def show_my_balance(update: Update, context):
    user_id = update.effective_user.id
    balance = database.get_balance(user_id)
    if balance is not None:
        await update.message.reply_text(f"Your balance is {balance:.2f} 🤑")
    else:
        await update.message.reply_text("You are not in the system yet!")

async def show_all_balance(update: Update, context):
    balances = database.get_all_balances()
    if balances:
        balance_list = "\n".join([f"{name}: {balance:.2f}" for name, balance, _ in balances])
        await update.message.reply_text(f"All balances:\n{balance_list}")
    else:
        await update.message.reply_text("No users found in this group.")

def main():
    application = Application.builder().token(config.TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_user))
    application.add_handler(CommandHandler("addfund", add_fund))
    application.add_handler(CommandHandler("deductfund", deduct_fund))
    application.add_handler(CommandHandler("pay", pay))
    application.add_handler(CommandHandler("showmybalance", show_my_balance))
    application.add_handler(CommandHandler("showallbalance", show_all_balance))
    application.add_handler(CommandHandler("reset", reset))

    application.run_polling()

if __name__ == "__main__":
    main()
