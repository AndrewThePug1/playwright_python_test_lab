import pytest
from playwright.sync_api import Page, expect, Playwright, BrowserContext


# Fixture for opening Chrome browser
@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


# Fixture for creating a browser context
@pytest.fixture(scope="function")
def context(browser) -> BrowserContext:
    context = browser.new_context()
    yield context
    context.close()


# Fixture for setting the testing viewports height and width
@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    page.set_viewport_size({"width": 1280, "height": 720})
    yield page
    page.close()


# Fixture for setting up the registration page
@pytest.fixture(scope="function")
def setup_registration_page(page: Page):
    # Load the registration page
    page.set_content("""
    <html>
        <head>
            <title>ABC Mobile E-commerce</title>
        </head>
        <body>
            <h1>ABC Mobile E-commerce - Registration</h1>
            <form id="registrationForm">
                <label for="lastName">Last Name:</label>
                <input type="text" id="lastName" name="lastName" required><br><br>
                <label for="cellPhone">Cell Phone Number:</label>
                <input type="text" id="cellPhone" name="cellPhone" required><br><br>
                <label for="userId">User ID (Email):</label>
                <input type="email" id="userId" name="userId" required><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br><br>
                <button type="button" id="submitBtn">Register</button>
            </form>
            <p id="successMessage" style="display:none;">Registration successful!</p>
            <script>
                document.getElementById('submitBtn').onclick = function() {
                    document.getElementById('successMessage').style.display = 'block';
                };
            </script>
        </body>
    </html>
    """)
    yield page


# Fixture for providing test data
@pytest.fixture(scope="module")
def test_data():
    return {
        "last_name": "Doe",
        "cell_phone": "1234567890",
        "user_id": "john.doe@example.com",
        "password": "SecurePass123!",
    }


# Test for New User Registration
def test_new_user_registration(page: Page, setup_registration_page, test_data):
    # Fill in the registration form
    page.fill("#lastName", test_data["last_name"])
    page.fill("#cellPhone", test_data["cell_phone"])
    page.fill("#userId", test_data["user_id"])
    page.fill("#password", test_data["password"])

    # Submit the form
    page.click("#submitBtn")

    # Verify the success message is displayed
    success_message = page.inner_text("#successMessage")
    assert success_message == "Registration successful!"

    # Additional assertions to verify the form behavior
    expect(page.locator("#lastName")).to_have_value(test_data["last_name"])
    expect(page.locator("#cellPhone")).to_have_value(test_data["cell_phone"])
    expect(page.locator("#userId")).to_have_value(test_data["user_id"])
    expect(page.locator("#password")).to_have_value(test_data["password"])


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
