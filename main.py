import os
import json
import asyncio
import random
import threading
from flask import Flask, request, jsonify, send_from_directory
from playwright.async_api import async_playwright

app = Flask(name)

# === Global bot state ===
BOT_THREAD = None
BOT_LOCK = threading.Lock()
STOP_EVENT = threading.Event()
BOT_STATUS = {"running": False, "current": None}

UPLOAD_FOLDER = os.getcwd()

# === Serve frontend panel ===
@app.route("/panel.html")
def serve_panel():
    return send_from_directory(os.getcwd(), "panel.html")


@app.route("/")
def home():
    return '<a href="/panel.html" style="font-family:sans-serif;font-size:20px;">➡️ Open Messenger Bot Panel</a>'


# === Upload files ===
@app.route("/upload", methods=["POST"])
def upload():
    files = {}
    for key in ["cookies", "targets", "messages", "prefix"]:
        f = request.files.get(key)
        if not f:
            return f"Missing file: {key}", 400
        filename = key + (".json" if key == "cookies" else ".txt")
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)
        files[key] = path
    return "✅ Files uploaded successfully", 200


# === Bot controls ===
@app.route("/start", methods=["POST"])
def start_bot():
    global BOT_THREAD
    with BOT_LOCK:
        if BOT_STATUS["running"]:
            return "⚠️ Bot already running", 400
        STOP_EVENT.clear()
        BOT_THREAD = threading.Thread(target=lambda: asyncio.run(bot_main()), daemon=True)
        BOT_THREAD.start()
    return "✅ Bot started", 200


@app.route("/stop", methods=["POST"])
def stop_bot():
    STOP_EVENT.set()
    return "🛑 Stop signal sent", 200


@app.route("/status")
def status():
    return jsonify(BOT_STATUS)


# === Bot core logic ===
async def bot_main():
    global BOT_STATUS
    BOT_STATUS["running"] = True
    BOT_STATUS["current"] = None

    try:
        with open("cookies.json", "r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        cookies = [c for c in raw_cookies if c.get("name") and c.get("value")]

        for c in cookies:
            if "domain" in c and not c["domain"].startswith("."):
                c["domain"] = "." + c["domain"]

        with open("targets.txt", "r", encoding="utf-8") as f:
            targets = [line.strip() for line in f if line.strip()]
        with open("messages.txt", "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
        with open("prefix.txt", "r", encoding="utf-8") as f:
            prefix = f.read().strip()

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )
            context = await browser.new_context()
            await context.add_cookies(cookies)
            page = await context.new_page()

            for tid in targets:
                if STOP_EVENT.is_set():
                    break

                BOT_STATUS["current"] = f"Opening chat: {tid}"
                url = f"https://www.facebook.com/messages/e2ee/t/{tid}"
                try:
                    await page.goto(url)
                    await page.wait_for_selector('div[role="textbox"], textarea', timeout=15000)
                    await asyncio.sleep(2)
                except Exception:
                    continue

                for msg in messages:
                    if STOP_EVENT.is_set():
                        break

                    full_msg = f"{prefix} {msg}".strip()
                    BOT_STATUS["current"] = f"Sending to {tid}: {full_msg[:30]}"

                    sent = False
                    for _ in range(3):

try:
                            sel_list = [
                                'div[aria-label="Message"]',
                                'div[contenteditable="true"]',
                                'div[role="textbox"]',
                                "textarea",
                            ]
                            input_box = None
                            for sel in sel_list:
                                el = await page.query_selector(sel)
                                if el:
                                    input_box = el
                                    break
                            if not input_box:
                                await asyncio.sleep(1)
                                continue

                            await input_box.click()
                            for ch in full_msg:
                                await input_box.type(ch, delay=random.uniform(25, 60))
                            await input_box.press("Enter")
                            sent = True
                            break
                        except Exception:
                            await asyncio.sleep(1)

                    if not sent:
                        BOT_STATUS["current"] = f"⚠️ Failed to send {tid}"
                    await asyncio.sleep(random.uniform(3, 5))

            await browser.close()

    finally:
        BOT_STATUS["running"] = False
        BOT_STATUS["current"] = None


# === Run Flask ===
if name == "main":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
