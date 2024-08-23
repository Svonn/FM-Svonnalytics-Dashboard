import dash  
import dash_bootstrap_components as dbc  
from app_layout import create_app_layout
from app_callbacks import register_callbacks
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='path to the folder with the exported html files')
args = parser.parse_args()

path = args.path

if not path:
    path = 'F:\\Games\\FM24 Files\\exported_html'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
create_app_layout(app, path)
register_callbacks(app)
  
if __name__ == '__main__':  
    app.run_server(debug=False)  
