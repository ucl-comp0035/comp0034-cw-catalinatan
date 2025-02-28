import requests
from dash.testing.application_runners import import_app

# References: comp0034 tutorials


def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN the server is started and an HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="app")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to
    # make an HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status
    # code in the HTTP response is 200
    assert response.status_code == 200
