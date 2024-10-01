# PayBot 💸

**PayBot** is a fun and interactive Telegram bot that manages group funds. This bot helps group members keep track of their balances and allows group admins to manage funds through simple commands like adding or deducting amounts. With PayBot, managing group funds becomes less of a chore and more enjoyable with fun responses! 🎉

## Features ✨

- **Add yourself to the system:** `/add <name>`
- **Edit your username:** `/editname <newname>`
- **Add funds (admins only):** `/addfund @username <amount>`
- **Deduct funds (admins only):** `/deductfund @username <amount>`
- **Make a payment:** `/pay <description> <amount>`
- **Check your balance:** `/showmybalance`
- **Check all balances:** `/showallbalance`

## Commands 📜

| Command                             | Description                                          |
|-------------------------------------|------------------------------------------------------|
| `/start`                            | Start the bot and get a welcome message.             |
| `/help`                             | List all available commands.                         |
| `/add <name>`                       | Add yourself to the system.                          |
| `/editname <newname>`               | Edit your username.                                  |
| `/addfund @username <amount>`       | Admins can add funds to a user.                      |
| `/deductfund @username <amount>`    | Admins can deduct funds from a user.                 |
| `/pay <description> <amount>`       | Make a payment and deduct it from your balance.      |
| `/showmybalance`                    | Show your current balance.                           |
| `/showallbalance`                   | Show the balances of all group members.              |

## Installation 🚀

### Step 1: Clone the Repository

```bash
git clone https://github.com/fabinahian/PayBot.git
```

### Step 2: Navigate to the Project Directory

```bash
cd PayBot
```

### Step 3: Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables

```bash
BOT_TOKEN=your-telegram-bot-token
```

### Step 6: Run the Bot

```bash
python bot.py
```


Feel free to fork this project, submit issues, and make pull requests. Contributions are always welcome!

