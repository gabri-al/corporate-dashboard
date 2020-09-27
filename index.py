import dash_core_components as dcc
import dash_html_components as html
import dash

from app import app
from app import server
from layouts import sales, page2, page3
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/sales-overview':
         return sales
    elif pathname == '/apps/page2':
         return page2
    elif pathname == '/apps/page3':
         return page3
    else:
        return sales # This is the "home page"

if __name__ == '__main__':
    app.run_server(debug=False)
