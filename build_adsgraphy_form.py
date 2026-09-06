import time
import os
import re
from playwright.sync_api import sync_playwright

INDEX_PATH = r"C:\Users\Deepali Motwani\.gemini\antigravity\scratch\trackx-landing-page\index.html"
ARTIFACTS_DIR = r"C:\Users\Deepali Motwani\.gemini\antigravity\brain\0a6b9ce5-01da-4c33-bd37-f2299f28d2f7"

def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    print("Launching headful browser to automate Google Form creation for adsgraphy.com...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print("Navigating to https://docs.google.com/forms/u/0/create ...")
        page.goto("https://docs.google.com/forms/u/0/create")

        print("Waiting for Google Forms editor page...")
        editor_ready = False
        for i in range(120):
            url = page.url
            if "docs.google.com/forms" in url and "/edit" in url:
                print(f"[SUCCESS] Arrived at Google Forms Editor: {url}")
                editor_ready = True
                break
            if i % 10 == 0:
                print(f"Waiting for login / editor page... Current URL: {url[:80]}...")
            time.sleep(2)

        if not editor_ready:
            print("Could not reach editor page automatically.")
            browser.close()
            return

        page.wait_for_timeout(3000)

        # 1. SET FORM TITLE & DESCRIPTION
        print("Setting Form Title...")
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        try:
            # Click title field
            title_input = page.locator('div[role="heading"] [contenteditable="true"], div[data-initial-value] [contenteditable="true"]').first
            if title_input.is_visible():
                title_input.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type("Make an Offer — adsgraphy.com")
                print("Title updated: Make an Offer — adsgraphy.com")
        except Exception as e:
            print("Title setting error:", e)

        page.wait_for_timeout(1000)

        try:
            desc_input = page.locator('div[aria-label="Form description"]').first
            if desc_input.is_visible():
                desc_input.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type("This is an offer form for the domain adsgraphy.com, a short brandable .com domain for an advertising agency, martech platform, ad network, or marketing analytics product. All offers will be reviewed and responded to by email.")
                print("Description updated!")
        except Exception as e:
            print("Description setting error:", e)

        page.wait_for_timeout(2000)

        # Extract Form ID / URL from page.url
        # URL format: https://docs.google.com/forms/d/{FORM_ID}/edit
        match = re.search(r'/forms/d/e?/([^/]+)/edit', page.url)
        form_id = match.group(1) if match else None
        
        embed_iframe = ""
        if form_id:
            view_url = f"https://docs.google.com/forms/d/e/{form_id}/viewform?embedded=true"
            embed_iframe = f'<iframe src="{view_url}" width="100%" height="850" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>'
            print(f"Generated Embed iFrame: {embed_iframe}")

        # Try clicking Send button to grab official embed code
        try:
            send_btn = page.locator('div[role="button"]:has-text("Send")').first
            if send_btn.is_visible():
                send_btn.click()
                page.wait_for_timeout(1500)
                
                # Tab 3 is embed HTML tab
                embed_tab = page.locator('div[role="tab"]').nth(2)
                if embed_tab.is_visible():
                    embed_tab.click()
                    page.wait_for_timeout(1000)

                textarea = page.locator('textarea[aria-label="HTML embed code"], textarea').first
                if textarea.is_visible():
                    official_code = textarea.input_value()
                    if official_code and "<iframe" in official_code:
                        embed_iframe = official_code
                        print("Extracted official iframe embed code!")

                close_btn = page.locator('div[role="button"][aria-label="Close"]').first
                if close_btn.is_visible():
                    close_btn.click()
        except Exception as e:
            print("Send modal extract note:", e)

        # Take screenshot
        ss_path = os.path.join(ARTIFACTS_DIR, "adsgraphy_google_form.png")
        page.screenshot(path=ss_path)
        print(f"Screenshot saved to {ss_path}")

        # Update index.html if iframe was generated
        if embed_iframe:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                content = f.read()

            # Insert into #offer-form-embed
            updated_content = re.sub(
                r'<div id="offer-form-embed">[\s\S]*?</div>',
                f'<div id="offer-form-embed">\n        {embed_iframe}\n      </div>',
                content
            )

            with open(INDEX_PATH, "w", encoding="utf-8") as f:
                f.write(updated_content)

            print("SUCCESSFULLY UPDATED INDEX.HTML WITH GOOGLE FORM EMBED!")

        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    main()
