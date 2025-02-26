import requests
from dash.testing.application_runners import import_app


def test_server_live(dash_duo, start_app):
    """
    GIVEN the app is running
    WHEN an HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    start_app(dash_duo)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to make an HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
    assert response.status_code == 200