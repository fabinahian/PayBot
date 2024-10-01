# PayBot 💸

**PayBot** is a fun and interactive Telegram bot that manages group funds. This bot helps group members keep track of their balances and allows group admins to manage funds through commands like adding or deducting amounts. It provides fun responses to make managing funds less of a chore and more enjoyable! 🎉

## Features ✨

- **Add yourself to the system:** `/add <name>`
- **Edit your username:** `/editname <newname>`
- **Add funds (admins only):** `/addfund @username <amount>`
- **Deduct funds (admins only):** `/deductfund @username <amount>`
- **Make a payment:** `/pay <description> <amount>`
- **Check your balance:** `/showmybalance`
- **Check all balances:** `/showallbalance`

## Commands 📜

| Command              | Description                                      |
|----------------------|--------------------------------------------------|
| `/start`             | Start the bot and get a welcome message.          |
| `/help`              | List all available commands.                      |
| `/add <name>`        | Add yourself to the system.                       |
| `/editname <newname>`| Edit your username.                               |
| `/addfund @username <amount>` | Admins can add funds to a user.          |
| `/deductfund @username <amount>` | Admins can deduct funds from a user.  |
| `/pay <description> <amount>` | Make a payment and deduct from your balance. |
| `/showmybalance`     | Show your current balance.                        |
| `/showallbalance`    | Show the balances of all group members.           |

## Installation 🚀

1. Clone this repository:

   ```bash
   git clone https://github.com/<your-username>/paybot.git
