import os
import json
import requests # type: ignore
from slack_sdk import WebClient # type: ignore
from slack_sdk.errors import SlackApiError # type: ignore
class Visualization:
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
    @staticmethod
    def save_slack_credentials(channel_id:str = None, slack_token:str=None):
        """
        Saves Slack credentials (channel ID and token) to a JSON file.

        Args:
            channel_id (str, optional): The ID of the Slack channel. If not provided, the user will be prompted to enter it.
            slack_token (str, optional): The Slack token. If not provided, the user will be prompted to enter it.

        Returns:
            None: The function does not return any value.
        """
        slack_token = slack_token or input("Insert the slack_token: ")
        channel_id = channel_id or input("Insert the channel_id: ")
        dictionary = {"channel_id": channel_id, "slack_token": slack_token}
        try:
            with open('slack_credentials.json', "w") as outfile:
                json.dump(dictionary, outfile)
        except Exception as e:
            print("Error occurred while saving slack credentials:", str(e))
    @staticmethod
    def send_images_via_slack(file_path: str, channel_id: str=None, slack_token: str =None, caption: str ="This is a caption"):
        """
        Sends an image file to a specified Slack channel using the Slack API.

        Args:
            file_path (str): The path to the image file to be sent.
            channel_id (str, optional): The ID of the Slack channel to send the image to. If not provided, it will attempt to read the channel ID from a JSON file named 'slack_credentials.json'.
            slack_token (str, optional): The Slack API token. If not provided, it will attempt to read the token from the same JSON file mentioned above.
            caption (str, optional): The caption to be displayed with the image in Slack.

        Raises:
            ValueError: If 'slack_credentials.json' file is not found or the values are not valid.
            ValueError: If either `channel_id` or `slack_token` is missing.

        Returns:
            None
        """
        if channel_id is None and slack_token is None:
            if os.path.exists('slack_credentials.json'):
                try:
                    with open('slack_credentials.json', 'r') as openfile:
                        json_object = json.load(openfile)
                    channel_id = json_object.get("channel_id")
                    slack_token = json_object.get("slack_token")
                except ValueError:
                    print("Please use the function 'save_slack_credentials'")
            else:
                raise ValueError("Please provide the channel_id and the slack_token or use the function 'save_slack_credentials'.")
        if channel_id is None or slack_token is None:
            raise ValueError("channel_id and slack_token are required parameters")
        client = WebClient(token=slack_token)
        try:
            response = client.files_upload(
                channels=channel_id,
                file=file_path,
                title=caption
            )
            if response["ok"]:
                print("The photo was sent.")
            else:
                for key, value in response.items():
                    print(f"{key.capitalize()}: {value}")
        except SlackApiError as e:
            print(f"Error uploading file: {e.response['error']}")
    @staticmethod
    def help_slack_bot():
        """
        Provides a list of resources to help users create and configure a Slack bot.
        """
        print('''
            1. Creating a slack_bot (read the first paragraph): https://medium.com/applied-data-science/how-to-build-you-own-slack-bot-714283fd16e5
            2. Getting the channel_id (read method 1): https://www.process.st/how-to/find-slack-channel-id/ 
            ''')