import os
import re
import threading

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError
)


# ==========================================================
# NYX CHROME PROFILE
# ==========================================================

NYX_CHROME_PROFILE = os.path.abspath(
    "nyx_chrome_profile"
)


# ==========================================================
# SEND WHATSAPP MESSAGE BY PHONE NUMBER
# ==========================================================

def whatsapp_send(target):

    if not isinstance(target, dict):
        return "❌ WhatsApp target must be an object."

    phone = str(
        target.get("phone", "")
    ).strip()

    message = str(
        target.get("message", "")
    ).strip()

    if not phone:
        return "❌ Phone number is required."

    if not message:
        return "❌ Message is required."

    phone = re.sub(
        r"\D",
        "",
        phone
    )

    if len(phone) < 10:
        return "❌ Invalid phone number."

    result = {
        "value": None
    }

    def worker():

        playwright = None
        context = None

        try:

            print("🌐 Starting Chrome...")

            playwright = sync_playwright().start()

            context = playwright.chromium.launch_persistent_context(

                user_data_dir=NYX_CHROME_PROFILE,

                channel="chrome",

                headless=False,

                args=[
                    "--start-maximized"
                ]
            )

            if context.pages:
                page = context.pages[0]
            else:
                page = context.new_page()

            url = (
                "https://web.whatsapp.com/send"
                f"?phone={phone}"
                f"&text={message}"
            )

            print(
                f"📱 Opening WhatsApp chat: {phone}"
            )

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(6000)

            page.keyboard.press("Enter")

            page.wait_for_timeout(1000)

            result["value"] = (
                "✅ WhatsApp message sent successfully."
            )

        except Exception as e:

            result["value"] = (
                f"❌ WhatsApp automation failed: {e}"
            )

    thread = threading.Thread(
        target=worker
    )

    thread.start()
    thread.join()

    return result["value"]


# ==========================================================
# WHATSAPP CONTACT SEARCH + MESSAGE
# ==========================================================

def whatsapp_send_contact(target):

    if not isinstance(target, dict):
        return "❌ Invalid WhatsApp target."

    contact = str(
        target.get("contact", "")
    ).strip()

    message = str(
        target.get("message", "")
    ).strip()

    if not contact:
        return "❌ Contact name is required."

    if not message:
        return "❌ Message is required."

    result = {
        "value": None
    }


    # ======================================================
    # PLAYWRIGHT WORKER
    # ======================================================

    def worker():

        playwright = None
        context = None

        try:

            # ------------------------------------------------
            # START PLAYWRIGHT
            # ------------------------------------------------

            print("🌐 Starting Chrome...")

            playwright = sync_playwright().start()

            context = playwright.chromium.launch_persistent_context(

                user_data_dir=NYX_CHROME_PROFILE,

                channel="chrome",

                headless=False,

                args=[
                    "--start-maximized"
                ]
            )


            # ------------------------------------------------
            # GET PAGE
            # ------------------------------------------------

            if context.pages:

                page = context.pages[0]

            else:

                page = context.new_page()


            # ------------------------------------------------
            # OPEN WHATSAPP
            # ------------------------------------------------

            print("📱 Opening WhatsApp Web...")

            page.goto(
                "https://web.whatsapp.com",
                wait_until="domcontentloaded"
            )


            # ------------------------------------------------
            # WAIT FOR WHATSAPP
            # ------------------------------------------------

            print("⏳ Waiting for WhatsApp...")

            try:

                page.locator(
                    'div[contenteditable="true"]'
                ).first.wait_for(
                    state="visible",
                    timeout=30000
                )

            except PlaywrightTimeoutError:

                result["value"] = (
                    "❌ WhatsApp did not become ready. "
                    "Please scan the QR code if required."
                )

                return


            print("✅ WhatsApp Web is ready.")


            # =================================================
            # FIND SEARCH BOX
            # =================================================

            print(
                f"🔎 Searching for contact: {contact}"
            )

            search_box = None

            selectors = [

                'div[contenteditable="true"][data-tab="3"]',

                'div[contenteditable="true"][aria-label*="Search"]',

                'div[contenteditable="true"][role="textbox"]'

            ]


            for selector in selectors:

                try:

                    locator = page.locator(
                        selector
                    )

                    count = locator.count()


                    for i in range(count):

                        candidate = locator.nth(i)

                        if candidate.is_visible(
                            timeout=1000
                        ):

                            search_box = candidate

                            break


                    if search_box:

                        break


                except Exception:

                    continue


            # ------------------------------------------------
            # SEARCH BOX NOT FOUND
            # ------------------------------------------------

            if search_box is None:

                result["value"] = (
                    "❌ WhatsApp search box was not found."
                )

                return


            # =================================================
            # TYPE CONTACT NAME
            # =================================================

            search_box.click()

            search_box.fill("")

            search_box.type(
                contact,
                delay=50
            )

            print(
                f"⌨️ Typed: {contact}"
            )


            # ------------------------------------------------
            # WAIT FOR RESULTS
            # ------------------------------------------------

            page.wait_for_timeout(
                2000
            )


            # =================================================
            # FIND CONTACT RESULT
            # =================================================

            contact_result = None


            try:

                candidate = page.get_by_text(
                    contact,
                    exact=True
                ).first

                candidate.wait_for(
                    state="visible",
                    timeout=5000
                )

                contact_result = candidate

            except PlaywrightTimeoutError:

                pass


            # ------------------------------------------------
            # CONTACT NOT FOUND
            # ------------------------------------------------

            if contact_result is None:

                result["value"] = (
                    f"❌ Could not find WhatsApp contact: "
                    f"{contact}"
                )

                return


            # =================================================
            # CLICK CONTACT
            # =================================================

            print(
                f"👤 Found contact: {contact}"
            )

            contact_result.click()

            page.wait_for_timeout(
                1500
            )

            print(
                "✅ Contact chat opened."
            )


            # =================================================
            # FIND MESSAGE BOX
            # =================================================

            print(
                "💬 Finding message box..."
            )

            message_box = None


            message_selectors = [

                'footer div[contenteditable="true"]',

                'div[contenteditable="true"][data-tab="10"]',

                'div[contenteditable="true"][role="textbox"]'

            ]


            for selector in message_selectors:

                try:

                    locator = page.locator(
                        selector
                    )

                    count = locator.count()


                    for i in range(count):

                        candidate = locator.nth(i)

                        if candidate.is_visible(
                            timeout=1000
                        ):

                            message_box = candidate

                            break


                    if message_box:

                        break


                except Exception:

                    continue


            # ------------------------------------------------
            # MESSAGE BOX NOT FOUND
            # ------------------------------------------------

            if message_box is None:

                result["value"] = (
                    "❌ WhatsApp message box was not found."
                )

                return


            # =================================================
            # TYPE MESSAGE
            # =================================================

            message_box.click()

            message_box.type(
                message,
                delay=30
            )

            print(
                f"⌨️ Typed message: {message}"
            )


            # =================================================
            # SEND MESSAGE
            # =================================================

            print(
                "📤 Sending message..."
            )

            message_box.press(
                "Enter"
            )

            page.wait_for_timeout(
                1000
            )


            print(
                f"✅ Message sent to {contact}"
            )

            result["value"] = (
                f"✅ Message sent successfully "
                f"to {contact}."
            )


        except Exception as e:

            result["value"] = (
                f"❌ WhatsApp automation failed: {e}"
            )


    # ======================================================
    # RUN PLAYWRIGHT IN SEPARATE THREAD
    # ======================================================

    thread = threading.Thread(
        target=worker
    )

    thread.start()

    thread.join()


    return result["value"]