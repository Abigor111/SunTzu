import json

import requests
@staticmethod
def save_telegram_credentials(bot_token: str =None, chat_id: str=None):
    """
    Save the Telegram credentials to a JSON file.

    Args:
        bot_token (str, optional): The bot token. If not provided, the user will be prompted to enter it.
        chat_id (str, optional): The chat ID. If not provided, the user will be prompted to enter it.
        filename (str, optional): The name of the JSON file to save the credentials. Defaults to "telegram_credentials.json".
    """
    bot_token = bot_token or input("Insert the bot_token: ")
    chat_id = chat_id or input("Insert the chat id: ")
    dictionary = {"chat_id": chat_id, "bot_token": bot_token}
    try:
        with open('telegram_credentials.json', "w") as outfile:
            json.dump(dictionary, outfile)
    except Exception as e:
        print("Error occurred while saving telegram credentials:", str(e))
@staticmethod
def send_images_via_telegram(file_path: str, chat_id: str=None, bot_token: str =None, caption: str ="This is a caption"):
    """
    Sends an image via Telegram using the provided file path, chat ID, bot token, and caption.

    Args:
        file_path (str): The path to the image file.
        chat_id (str, optional): The ID of the chat to send the image to. If not provided, it will be retrieved from the 'telegram_credentials.json' file. Defaults to None.
        bot_token (str, optional): The token of the Telegram bot. If not provided, it will be retrieved from the 'telegram_credentials.json' file. Defaults to None.
        caption (str, optional): The caption for the image. Defaults to "This is a caption".

    Raises:
        ValueError: If chat_id and bot_token are not provided and the 'telegram_credentials.json' file does not exist.
        ValueError: If chat_id or bot_token is not provided.

    Returns:
        None
    """
    if chat_id is None and bot_token is None:
        if os.path.exists('telegram_credentials.json'):
            try:
                with open('telegram_credentials.json', 'r') as openfile:
                    json_object = json.load(openfile)
                chat_id = json_object.get("chat_id")
                bot_token = json_object.get("bot_token")
            except ValueError:
                print("Please use the function 'save_telegram_credentials'")
        else:
            raise ValueError("Please provide the chat_id and the bot_token or use the function 'save_telegram_credentials'.")
    if chat_id is None or bot_token is None:
        raise ValueError("chat_id and bot_token are required parameters")
    base_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(file_path, 'rb') as my_file:
        parameters = {
            "chat_id": chat_id,
            "caption": caption
        }
        files = {   
            "photo": my_file
        }
        try:
            resp = requests.post(base_url, data=parameters, files=files)
            status_code = resp.status_code
            if status_code == 200:
                print("The photo was sent.")
            else:
                resp_json = resp.json()
                print("Sent","-", resp_json.get("ok"))
                del resp_json["ok"]
                for key, values in resp_json.items():
                    print(key.capitalize(), "-", values)
        except requests.exceptions.RequestException as e:
            print("An error occurred during the request:", str(e))
@staticmethod
def help_telegram_bot():
    """
    Provides information on how to use a Telegram bot.
    """
    print('''
    1. How to create a bot: https://www.directual.com/lesson-library/how-to-create-a-telegram-bot
    2. Adding the bot to a group: https://botifi.me/en/help/telegram-adding-bot-to-channel-or-group/
    3. Getting the bot_token: https://botifi.me/en/help/telegram-existed-bot/
    4. Getting the chat_id of a group: https://www.wikihow.com/Know-Chat-ID-on-Telegram-on-Android
    5. Possible errors: https://core.telegram.org/api/errors
    ''')