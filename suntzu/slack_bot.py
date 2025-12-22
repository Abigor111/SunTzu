from slack_sdk import WebClient # type: ignore
from slack_sdk.errors import SlackApiError # type: ignore

import json
def save_slack_credentials(channel_id:str, slack_token:str):
    """
    Saves Slack credentials (channel ID and token) to a JSON file.

    Args:
        channel_id (str, optional): The ID of the Slack channel. If not provided, the user will be prompted to enter it.
        slack_token (str, optional): The Slack token. If not provided, the user will be prompted to enter it.

    Returns:
        None: The function does not return any value.
    """
    slack_token = slack_token
    channel_id = channel_id
    dictionary = {"channel_id": channel_id, "slack_token": slack_token}
    try:
        with open('slack_credentials.json', "w") as outfile:
            json.dump(dictionary, outfile)
    except Exception as e:
        print("Error occurred while saving slack credentials:", str(e))
def send_images_via_slack(file_path: str, caption: str ="This is a caption"):
    """
    Sends an image file to a specified Slack channel using the Slack API.

    Args:
        file_path (str): The path to the image file to be sent.
        caption (str, optional): The caption to be displayed with the image in Slack.

    Raises:
        ValueError: If 'slack_credentials.json' file is not found or the values are not valid.
        ValueError: If either `channel_id` or `slack_token` is missing.

    Returns:
        None
    """
    try:
        with open('slack_credentials.json', 'r') as openfile:
            json_object = json.load(openfile)
        channel_id = json_object.get("channel_id")
        slack_token = json_object.get("slack_token")
        if channel_id is None or slack_token is None:
            raise ValueError("channel_id and slack_token are required parameters")
    except FileNotFoundError:
        print("Please use the function 'save_slack_credentials'")
    upload_photo(file_path, slack_token, channel_id, caption)
def upload_photo(path, slack_token, channel_id, caption):
    client = WebClient(token=slack_token)
    try:
        response = client.files_upload(
            channels=channel_id,
            file=path,
            title=caption
        )
        if response["ok"]:
            print("The photo was sent.")
        else:
            for key, value in response.items():
                print(f"{key.capitalize()}: {value}")
    except SlackApiError as e:
        print(f"Error uploading file: {e.response['error']}")
def help_slack_bot():
    """
    Provides a list of resources to help users create and configure a Slack bot.
    """
    print('''
        1. Creating a slack_bot (read the first paragraph): https://medium.com/applied-data-science/how-to-build-you-own-slack-bot-714283fd16e5
        2. Getting the channel_id (read method 1): https://www.process.st/how-to/find-slack-channel-id/ 
        ''')