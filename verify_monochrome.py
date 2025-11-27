
import os
from playwright.sync_api import sync_playwright

def verify_monochrome_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-web-security"]
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        try:
            # Navigate to the dashboard
            page.goto("http://localhost:8000/index.html")

            # Wait for login overlay and handle it
            page.wait_for_selector("#login-overlay")
            page.fill("#password-input", "SSthunder!")
            page.click("#login-button")

            # Wait for dashboard to load
            page.wait_for_selector("#loading-overlay", state="hidden", timeout=15000)
            page.wait_for_selector("#overview", state="visible")

            # Wait a bit for rendering
            page.wait_for_timeout(3000)

            # Create verification directory
            os.makedirs("/home/jules/verification", exist_ok=True)

            # Screenshot 1: Overview Dashboard (Monochrome check)
            page.screenshot(path="/home/jules/verification/monochrome_overview.png", full_page=True)
            print("Screenshot taken: monochrome_overview.png")

            # Check light mode as well to ensure it's not broken
            # Toggle light mode (using JS evaluation to trigger the switch or click the button)
            # Assuming the settings modal needs to be opened first
            page.click("#settings-btn")
            page.wait_for_selector("#settings-modal.active")
            page.wait_for_timeout(500)

            # Take screenshot of settings (should be monochrome)
            page.screenshot(path="/home/jules/verification/monochrome_settings.png")
            print("Screenshot taken: monochrome_settings.png")

            # Find and click theme toggle
            page.click("label[for='theme-toggle']")
            page.wait_for_timeout(1000) # Wait for transition

            # Close modal
            page.click("#close-settings-modal")
            page.wait_for_timeout(500)

            # Screenshot 2: Light Mode Overview
            page.screenshot(path="/home/jules/verification/monochrome_light_mode.png", full_page=True)
            print("Screenshot taken: monochrome_light_mode.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/error_monochrome.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_monochrome_ui()
