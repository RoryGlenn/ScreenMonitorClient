import logging
import os
from typing import Optional
import uuid

import cv2
import discord
import mss
import numpy as np
from discord.ext import tasks

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
CHECK_INTERVAL = 10
PIXEL_DIFF_THRESHOLD = 25_000

logger = logging.getLogger(__name__)


class ScreenMonitorClient(discord.Client):
    """
    A Discord client that monitors the screen for motion and sends screenshots to a channel.
    """

    def __init__(self, **kwargs):
        """
        Initialize the ScreenMonitorClient.

        Parameters:
        - kwargs: Additional keyword arguments for discord.Client.
        """
        super().__init__(**kwargs)
        self.previous_screenshot: Optional[str] = None

    def capture_screen(self) -> str:
        """
        Capture the current screen and save it as an image file.

        Returns:
        - str: The file path of the captured screenshot.
        """
        with mss.mss() as sct:
            screenshot_path = sct.shot(output=f"current_screen{uuid.uuid4()}.png")
        return screenshot_path

    def detect_motion(
        self, image_path1: str, image_path2: str, pixel_diff_threshold: int
    ) -> bool:
        """
        Detect motion between two images by comparing pixel differences.

        Parameters:
        - image_path1 (str): Path to the first image.
        - image_path2 (str): Path to the second image.
        - pixel_diff_threshold (int): The minimum number of differing pixels to consider motion detected.

        Returns:
        - bool: True if motion is detected, False otherwise.

        Raises:
        - ValueError: If one or both images could not be loaded.

        """
        # Load images
        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)

        if image1 is None or image2 is None:
            raise ValueError("One or both images could not be loaded.")

        # Convert to grayscale
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Resize images to the same size if necessary
        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))

        # Apply Gaussian blur to reduce noise
        gray1_blur = cv2.GaussianBlur(gray1, (5, 5), 0)
        gray2_blur = cv2.GaussianBlur(gray2, (5, 5), 0)

        # Compute absolute difference between the two images
        diff = cv2.absdiff(gray1_blur, gray2_blur)

        # Threshold the difference image to get regions with significant differences
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Count the number of non-zero (differing) pixels
        non_zero_count = np.count_nonzero(thresh)

        # Debugging: Print the number of differing pixels
        logger.info(f"Differing pixels: {non_zero_count}")

        # Compare the count with the pixel difference threshold
        return non_zero_count > pixel_diff_threshold

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def check_screen_change(self) -> None:
        """
        Periodically capture the screen and check for motion.

        If motion is detected, send a screenshot to the specified Discord channel.
        """
        current_screenshot = self.capture_screen()
        try:
            if self.previous_screenshot is None:
                self.previous_screenshot = current_screenshot
                logger.info("First screenshot captured.")
            else:
                motion_detected = self.detect_motion(
                    self.previous_screenshot, current_screenshot, PIXEL_DIFF_THRESHOLD
                )
                if motion_detected:
                    # Motion detected
                    try:
                        channel = await self.fetch_channel(DISCORD_CHANNEL_ID)
                    except discord.NotFound:
                        raise ValueError(
                            "Invalid channel ID. Please check if the provided channel ID is correct."
                        ) from None
                    except discord.Forbidden:
                        raise PermissionError(
                            "Bot does not have permission to access the channel."
                        ) from None
                    except discord.HTTPException as exc:
                        raise ConnectionError(
                            f"Failed to fetch channel: {exc}"
                        ) from exc

                    if channel is not None:
                        with open(current_screenshot, "rb") as file:
                            picture = discord.File(file)
                            await channel.send(
                                "Motion detected! Here's the screenshot:", file=picture
                            )
                        logger.info("Motion detected! Screenshot sent.")
                    else:
                        raise ValueError("Channel is None after fetching.")
                else:
                    logger.info("No significant motion detected.")

                # Remove the previous screenshot
                if os.path.exists(self.previous_screenshot):
                    os.remove(self.previous_screenshot)

                # Update the previous screenshot
                self.previous_screenshot = current_screenshot
        except (ValueError, PermissionError, ConnectionError) as error:
            logger.info(f"An error occurred: {error}")
            # Clean up current screenshot if there's an error
            if os.path.exists(current_screenshot):
                os.remove(current_screenshot)

    async def on_ready(self) -> None:
        """
        Called when the bot is ready and connected to Discord.

        Starts the screen monitoring loop.

        """
        logger.info(f"Logged in as {self.user}")
        self.check_screen_change.start()


def main() -> None:
    """
    Main function to run the ScreenMonitorClient.

    """
    intents = discord.Intents.default()
    intents.guilds = True  # Enable the guilds intent
    client = ScreenMonitorClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
