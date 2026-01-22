# messenger.py
import threading
from your_original_script import FacebookMessenger

class MessengerService:
    def __init__(self):
        self.bot = FacebookMessenger()
        self.thread = None
        self.running = False

    def start(self, cookies, uid, messages, speed, haters_name=""):
        def run_bot():
            self.running = True
            self.bot.speed_seconds = speed
            self.bot.haters_name = haters_name
            self.bot.target_uid = uid
            self.bot.messages = messages

            if not self.bot.setup_driver():
                return
            if not self.bot.login_with_cookies(cookies):
                return

            self.bot.driver.get(
                f"https://www.facebook.com/messages/e2ee/t/{uid}"
            )
            self.bot.start_sending()

        self.thread = threading.Thread(target=run_bot, daemon=True)
        self.thread.start()

    def stop(self):
        if self.bot.driver:
            self.bot.driver.quit()
        self.running = False
