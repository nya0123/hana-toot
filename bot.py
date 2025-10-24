from mastodon import Mastodon
from bs4 import BeautifulSoup
import time
import os

MASTODON_URL = os.getenv("MASTODON_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID"))
TARGET_EMOJI = os.getenv("TARGET_EMOJI", ":suzuki_hana:")
REPLY_TEXT = os.getenv("REPLY_TEXT", "鈴木羽那すき シャニマスやってません")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))

mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=MASTODON_URL
)

last_checked_id = None

while True:
    try:
        statuses = mastodon.account_statuses(TARGET_USER_ID, limit=5)
        
        for status in statuses:
            
            if last_checked_id is None:
                last_checked_id = status["id"]

            if status["id"] <= last_checked_id:
                continue

            soup = BeautifulSoup(status["content"], "html.parser")
            text = soup.get_text()

            if TARGET_EMOJI in text:
                print(f"✨ 検出: {status['url']}")
                mastodon.status_favourite(status["id"])
                mastodon.status_reblog(status["id"])
                mastodon.status_post(REPLY_TEXT)
                print("✅ いいね・ブースト・投稿完了")

            if last_checked_id is None or status["id"] > last_checked_id:
                last_checked_id = status["id"]

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print(f"⚠️ エラー発生: {e}")
        time.sleep(60)
