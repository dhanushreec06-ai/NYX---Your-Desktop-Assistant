from memory.usage_track import (
    get_most_used_browser,
    get_preferred_service_target,
    record_browser,
    record_service_usage
)



from tools.browser import open_url


# ==================================================
# OPEN WEBSITE
# ==================================================

def open_website(url, browser=None):

    # ------------------------------------------------
    # User explicitly selected browser
    # ------------------------------------------------

    if browser:

        selected_browser = browser.lower().strip()

    # ------------------------------------------------
    # User did not specify browser
    # Use NYX memory
    # ------------------------------------------------

    else:

        selected_browser = get_most_used_browser()

    # ------------------------------------------------
    # No browser history
    # Use Windows default browser
    # ------------------------------------------------

    if selected_browser is None:

        success = open_url(url)

        return success

    # ------------------------------------------------
    # Open using selected browser
    # ------------------------------------------------

    success = open_url(
        url,
        selected_browser
    )

    # ------------------------------------------------
    # Remember successful browser
    # ------------------------------------------------

    if success:

        record_browser(selected_browser)

    return success