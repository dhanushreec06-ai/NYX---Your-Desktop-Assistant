from playwright.sync_api import sync_playwright
import time


def chatgpt_send(prompt):

    print("🌐 NYX Web Agent: Opening ChatGPT...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        try:

            page.goto(
                "https://chatgpt.com/",
                wait_until="domcontentloaded",
                timeout=30000
            )

            print("⏳ Waiting for ChatGPT...")

            time.sleep(5)

            print("🔎 Looking for message box...")

            # ChatGPT message box
            textbox = page.locator(
                "#prompt-textarea"
            )

            textbox.wait_for(
                state="visible",
                timeout=20000
            )

            print("✍️ Sending prompt...")

            textbox.fill(prompt)

            textbox.press("Enter")

            print("✅ Prompt sent to ChatGPT.")

            # Keep browser open for now
            time.sleep(10)

            return "✅ ChatGPT prompt sent successfully."

        except Exception as e:

            print(f"❌ ChatGPT automation failed: {e}")

            return f"❌ ChatGPT automation failed: {e}"

        finally:

            # Don't close browser yet.
            # We want to see what happened.
            pass


if __name__ == "__main__":

    result = chatgpt_send(
        "Prepare a short document explaining Artificial Intelligence."
    )

    print(result)