import sys
import time
import os
import subprocess
import re
from playwright.sync_api import sync_playwright

INDEX_PATH = r"C:\Users\Deepali Motwani\.gemini\antigravity\scratch\trackx-landing-page\index.html"
ARTIFACTS_DIR = r"C:\Users\Deepali Motwani\.gemini\antigravity\brain\0a6b9ce5-01da-4c33-bd37-f2299f28d2f7"
PROFILE_DIR = r"C:\Users\Deepali Motwani\.gemini\antigravity\scratch\edge_profile"

def main():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = "msedge"

    print("Launching Edge with remote debugging on port 9222...")
    try:
        subprocess.Popen([
            edge_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "https://docs.google.com/forms/u/0/create"
        ])
        time.sleep(3)
    except Exception as e:
        print("Error launching Edge:", e)

    print("Connecting Playwright over CDP to http://127.0.0.1:9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("Connected to Browser via CDP successfully!")
            
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()

            # Click "Confirm and continue" if Edge first-run modal appears
            try:
                confirm_btn = page.locator('button:has-text("Confirm and continue"), text="Confirm and continue"').first
                if confirm_btn.is_visible(timeout=3000):
                    confirm_btn.click()
                    print("Clicked Edge Confirm and continue!")
                    page.wait_for_timeout(2000)
            except Exception:
                pass

            # Go directly to create form
            print("Navigating to https://docs.google.com/forms/u/0/create ...")
            page.goto("https://docs.google.com/forms/u/0/create")

            print("Waiting for page URL...")
            for i in range(120):
                url = page.url
                if "docs.google.com/forms" in url and "/edit" in url:
                    print(f"Confirmed Form Editor URL: {url}")
                    break
                if "accounts.google.com" in url or "signin" in url:
                    if i % 10 == 0:
                        print("User login required in open Edge browser window...")
                time.sleep(2)

            page.wait_for_timeout(4000)
            print(f"Current page title: {page.title()}")

            # 1. SET FORM TITLE & DESCRIPTION
            print("Setting Form Title and Description...")
            
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            
            # Click title input
            title_input = page.locator('div[role="heading"] [contenteditable="true"], div[aria-label="Form title"]').first
            if title_input.is_visible():
                title_input.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type("Make an Offer — trackX.ai")
                print("Title set: Make an Offer — trackX.ai")

            page.wait_for_timeout(1000)

            desc_input = page.locator('div[aria-label="Form description"]').first
            if desc_input.is_visible():
                desc_input.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type("This is an offer form for the domain trackX.ai, a short brandable .ai domain for tracking, analytics, or AI-driven products. All offers will be reviewed and responded to by email.")
                print("Description set!")

            page.wait_for_timeout(2000)

            # Take screenshot of form editor
            os.makedirs(ARTIFACTS_DIR, exist_ok=True)
            screenshot_path = os.path.join(ARTIFACTS_DIR, "google_form_edited.png")
            page.screenshot(path=screenshot_path)
            print(f"Form editor screenshot saved to {screenshot_path}")

        except Exception as err:
            print("Automation error:", err)

if __name__ == "__main__":
    main()
