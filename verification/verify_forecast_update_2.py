
from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-web-security'])
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # Navigate to the dashboard
        page.goto('http://localhost:8000/index.html')

        # Handle login
        page.fill('#password-input', 'SSthunder!')
        page.click('#login-button')

        # Wait for loading overlay to disappear
        page.wait_for_selector('#loading-overlay', state='hidden', timeout=30000)

        # Open Sidebar
        page.click('#menu-toggle')
        time.sleep(0.5)

        # Navigate to Previsioni section
        page.click('a[href="#previsioni"]')

        # Wait for data to load and charts to appear
        # We wait for the experimental table to have rows
        try:
            page.wait_for_selector('#experimentalDataTable tbody tr', timeout=30000)
        except:
            print('Timeout waiting for experimental data table rows')
            page.screenshot(path='verification/debug_timeout_update_2.png')
            raise

        # Scroll to the new section
        element = page.locator('#experimentalForecastChart-container')
        element.scroll_into_view_if_needed()

        # Give charts a moment to render
        time.sleep(2)

        # Take screenshot
        page.screenshot(path='verification/experimental_forecast_update_2.png')
        browser.close()

if __name__ == '__main__':
    run()
