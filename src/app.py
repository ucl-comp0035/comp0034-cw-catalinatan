from dash import Dash
import dash_bootstrap_components as dbc
from layout import app_layout
from callbacks import register_callbacks
# import dash_daq as daq

# Define meta tags for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Define external stylesheets, using Bootstrap styling from
# dash_bootstrap_components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css']
external_scripts = [{'src': 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.0/html2canvas.min.js'}]

# Initialize the Dash app with external stylesheets and meta tags
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    meta_tags=meta_tags
)

# Set the layout of the app
app.layout = app_layout

# Register all callbacks
register_callbacks(app)

# Run the app in debug mode if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
