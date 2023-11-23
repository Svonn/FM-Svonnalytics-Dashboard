import dash  
import dash_bootstrap_components as dbc  
from app_layout import create_app_layout  
from app_callbacks import register_callbacks
import sys
import os
import argparse
import configurations


parser = argparse.ArgumentParser()
parser.add_argument('--path', help='path to the folder with the exported html files')
args = parser.parse_args()

path = args.path.strip()


if not path:
    path = 'F:\\Games\\FM24 Files\\exported_html'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
app.config.suppress_callback_exceptions = True  
create_app_layout(app, html_export_path=path)
register_callbacks(app)  # Register all the callbacks  
  
if __name__ == '__main__':  
    app.run_server(debug=True)  
