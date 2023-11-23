import dash  
import dash_bootstrap_components as dbc  
from app_layout import create_app_layout  
from app_callbacks import register_callbacks
  
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
app.config.suppress_callback_exceptions = True  
create_app_layout(app)
register_callbacks(app)  # Register all the callbacks  
  
if __name__ == '__main__':  
    app.run_server(debug=True)  
