import sys
import time
import os
from playwright.sync_api import sync_playwright

def main():
    print("Launching headful browser for Google Forms creation...")
    with sync_playwright() as p:
        # Launch Chromium visually
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        page.goto("https://docs.google.com/forms/u/0/create")

        print("Checking page URL...")
        # Wait up to 120s for user to be logged in and on the form editor page
        form_ready = False
        for i in range(60):
            url = page.url
            if "docs.google.com/forms" in url and "/edit" in url:
                print("Confirmed: On Google Forms Editor page!")
                form_ready = True
                break
            else:
                if i % 5 == 0:
                    print(f"Waiting for form editor... Current URL: {url}")
            time.sleep(2)

        if not form_ready:
            print("Timed out waiting for Google Forms editor page. Please make sure you are logged in.")
            browser.close()
            return

        page.wait_for_timeout(3000)

        # Print current title and page structure for debugging selectors
        print("Page title:", page.title())
        
        # Take screenshot of blank form for verification
        screenshot_path = r"C:\Users\Deepali Motwani\.gemini\antigravity\brain\0a6b9ce5-01da-4c33-bd37-f2299f28d2f7\editor_opened.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Keep browser open briefly to allow interaction
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    main()
