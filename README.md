# Screen Monitor with Discord Notifications

A Python script that monitors your computer screen for changes (motion detection) and sends a screenshot to a specified Discord channel whenever significant changes are detected.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Discord Bot Setup](#discord-bot-setup)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Customization](#customization)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

This script captures screenshots of your computer screen at regular intervals and detects significant changes between consecutive images. When a change exceeding a specified threshold is detected, it sends a notification along with the screenshot to a designated Discord channel.

## Features

- **Screen Monitoring**: Continuously monitors your screen for changes.
- **Motion Detection**: Uses image processing to detect significant differences between screenshots.
- **Discord Integration**: Sends alerts and screenshots to a specified Discord channel.
- **Configurable Parameters**: Customize the check interval and sensitivity threshold.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Prerequisites

- **Python 3.6 or higher**
- **Discord Account**: To set up a Discord bot and receive notifications.
- **Discord Server**: Where the bot will send messages.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes:

   ```
   discord.py
   mss
   opencv-python
   numpy
   ```

## Configuration

### Discord Bot Setup

1. **Create a New Discord Application**

   - Visit the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click **"New Application"** and enter a name.
   - Navigate to the **"Bot"** tab and click **"Add Bot"**.
   - Click **"Yes, do it!"** to confirm.

2. **Obtain Your Bot Token**

   - In the **"Bot"** section, click **"Reset Token"** and then **"Copy"**.
   - **Important**: Keep this token secure and do not share it publicly.

3. **Invite the Bot to Your Server**

   - Go to the **"OAuth2"** tab and select **"URL Generator"**.
   - Under **"Scopes"**, check **`bot`**.
   - Under **"Bot Permissions"**, check:
     - **Send Messages**
     - **Attach Files**
   - Copy the generated URL and paste it into your browser.
   - Select the server where you want to add the bot and authorize it.

4. **Enable Privileged Gateway Intents (If Necessary)**

   - In the **"Bot"** tab, under **"Privileged Gateway Intents"**, enable **"Server Members Intent"** if your bot requires it.

5. **Retrieve the Channel ID**

   - In Discord, go to **User Settings** > **Advanced** and enable **Developer Mode**.
   - Right-click on the channel where you want the bot to send messages and select **"Copy ID"**.

### Environment Variables

Store sensitive information like your bot token and channel ID in environment variables using a `.env` file.

1. **Create a `.env` File**

   ```bash
   touch .env
   ```

2. **Add Your Configuration Variables**

   Open the `.env` file in a text editor and add:

   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token
   DISCORD_CHANNEL_ID=your_channel_id
   ```

   - Replace `your_discord_bot_token` with the token you obtained from the Discord Developer Portal.
   - Replace `your_channel_id` with the ID of the Discord channel.

3. **Ensure `.env` is Ignored by Git**

   The provided `.gitignore` file already includes `.env`, so it won't be committed to your repository.

## Usage

To run the script, use the following command:

```bash
python screen_monitor.py
```

You should see output indicating that the bot has logged in and is monitoring your screen:

```
Logged in as YourBotName#1234
First screenshot captured.
```

## Customization

You can adjust the script's behavior by modifying the following variables in `screen_monitor.py`:

- **`CHECK_INTERVAL`**: Time interval in seconds between each screen capture. The default is `5`.
- **`PIXEL_DIFF_THRESHOLD`**: Minimum number of differing pixels required to detect motion. The default is `1000`.

Example:

```python
CHECK_INTERVAL = 10  # Check every 10 seconds
PIXEL_DIFF_THRESHOLD = 500  # Increase sensitivity
```

## Security Considerations

- **Keep Your Bot Token Secure**: Never share your bot token or commit it to a repository. Treat it like a password.
- **Use Environment Variables**: Store sensitive information in environment variables or a `.env` file that is not tracked by version control.
- **Be Mindful of Privacy**: The script captures and sends screenshots of your screen. Ensure no sensitive information is displayed during monitoring.

## Troubleshooting

### Bot Not Sending Messages

- **Invalid Token**: Ensure your bot token is correct and matches the one in the Discord Developer Portal.
- **Incorrect Channel ID**: Double-check the channel ID and make sure the bot has access to the channel.
- **Permissions**: Verify that the bot has the necessary permissions to send messages and attach files in the channel.
- **Intents**: Ensure that the required intents are enabled in both the code and the Discord Developer Portal.

### Screen Capture Issues

- **Permissions on macOS**: Grant screen recording permissions to your terminal or Python interpreter in **System Preferences** > **Security & Privacy** > **Privacy** > **Screen Recording**.
- **Missing Libraries**: Make sure all dependencies are installed.

### Import Errors

- **Ensure Dependencies are Installed**: Run `pip install -r requirements.txt` to install all required packages.

## Contributing

Contributions are welcome! If you'd like to contribute:

1. **Fork the Repository**

   Click the **"Fork"** button at the top-right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your_feature_name
   ```

4. **Make Your Changes**

   - Implement your feature or bug fix.
   - Write clear and concise commit messages.

5. **Commit and Push**

   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   git push origin feature/your_feature_name
   ```

6. **Create a Pull Request**

   - Go to your fork on GitHub.
   - Click on **"Compare & pull request"**.
   - Provide a detailed description of your changes and submit the pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- **[discord.py](https://discordpy.readthedocs.io/en/stable/)**: An API wrapper for Discord written in Python.
- **[mss](https://python-mss.readthedocs.io/)**: A cross-platform screenshot tool.
- **[OpenCV](https://opencv.org/)**: An open-source computer vision and machine learning software library.
- **[NumPy](https://numpy.org/)**: A library for adding support for large, multi-dimensional arrays and matrices.
