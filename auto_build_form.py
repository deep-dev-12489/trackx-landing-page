import time
import os
import re
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"C:\Users\Deepali Motwani\.gemini\antigravity\scratch\google_forms_profile"
ARTIFACTS_DIR = r"C:\Users\Deepali Motwani\.gemini\antigravity\brain\0a6b9ce5-01da-4c33-bd37-f2299f28d2f7"
INDEX_PATH = r"C:\Users\Deepali Motwani\.gemini\antigravity\scratch\trackx-landing-page\index.html"

def build_form():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    print("Launching persistent browser session...")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--start-maximized"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        print("Navigating to https://docs.google.com/forms/u/0/create ...")
        page.goto("https://docs.google.com/forms/u/0/create")

        print("\n" + "="*60)
        print("PLEASE LOG IN TO YOUR GOOGLE ACCOUNT IN THE OPEN BROWSER WINDOW IF PROMPTED.")
        print("Waiting for Google Forms editor page...")
        print("="*60 + "\n")

        form_ready = False
        for i in range(180): # Wait up to 3 minutes for user to log in
            url = page.url
            if "docs.google.com/forms" in url and "/edit" in url:
                print(f"\n[SUCCESS] Detected Form Editor URL: {url}")
                form_ready = True
                break
            if i % 10 == 0:
                print(f"Waiting for form editor... ({i}s passed). Current URL: {url[:80]}...")
            time.sleep(1)

        if not form_ready:
            print("Timed out waiting for login/form editor.")
            context.close()
            return

        print("Form Editor loaded! Waiting 5 seconds for UI elements to settle...")
        page.wait_for_timeout(5000)

        # ---------------------------------------------------------------------
        # 1. SET FORM TITLE & DESCRIPTION
        # ---------------------------------------------------------------------
        print("Setting Form Title and Description...")
        
        # Google Forms Title Field
        try:
            # Click title area
            title_input = page.locator('div[role="heading"] [contenteditable="true"], div[data-initial-value] [contenteditable="true"]').first
            if not title_input.is_visible():
                title_input = page.locator('input[aria-label="Form title"], div[aria-label="Form title"]').first
            
            title_input.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type("Make an Offer — trackX.ai")
            print("Form Title set!")
        except Exception as e:
            print("Could not set title automatically via precise selector, trying fallback:", e)
            page.keyboard.type("Make an Offer — trackX.ai")

        page.wait_for_timeout(1000)

        # Form Description Field
        try:
            desc_input = page.locator('div[aria-label="Form description"], div[data-initial-value][aria-label="Form description"]').first
            desc_input.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type("This is an offer form for the domain trackX.ai, a short brandable .ai domain for tracking, analytics, or AI-driven products. All offers will be reviewed and responded to by email.")
            print("Form Description set!")
        except Exception as e:
            print("Could not set description via precise selector:", e)

        page.wait_for_timeout(2000)

        # Take screenshot after basic setup
        ss_path = os.path.join(ARTIFACTS_DIR, "google_form_preview.png")
        page.screenshot(path=ss_path)
        print(f"Screenshot saved to {ss_path}")

        print("\nForm creation script step completed successfully!")
        time.sleep(5)
        context.close()

if __name__ == "__main__":
    build_form()
