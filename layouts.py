import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_table
from dash_table.Format import Format, Group
import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['superdark-green'],
    'background-color' : corporate_colors['superdark-green'],
    'box-shadow' : '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top' : '10px'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
    }

recapdiv = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'rgb(251, 251, 252, 0.1)',
    'margin-left' : '15px',
    'margin-right' : '15px',
    'margin-top' : '15px',
    'margin-bottom' : '15px',
    'padding-top' : '5px',
    'padding-bottom' : '5px',
    'background-color' : 'rgb(251, 251, 252, 0.1)'
    }

recapdiv_text = {
    'text-align' : 'left',
    'font-weight' : '350',
    'color' : corporate_colors['white'],
    'font-size' : '1.5rem',
    'letter-spacing' : '0.04em'
    }

####################### Corporate chart formatting

corporate_title = {
    'font' : {
        'size' : 16,
        'color' : corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid' : False,
    'linecolor' : corporate_colors['light-grey'],
    'color' : corporate_colors['light-grey'],
    'tickangle' : 315,
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_yaxis = {
    'showgrid' : True,
    'color' : corporate_colors['light-grey'],
    'gridwidth' : 0.5,
    'gridcolor' : corporate_colors['dark-green'],
    'linecolor' : corporate_colors['light-grey'],
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Dosis'

corporate_legend = {
    'orientation' : 'h',
    'yanchor' : 'bottom',
    'y' : 1.01,
    'xanchor' : 'right',
    'x' : 1.05,
	'font' : {'size' : 9, 'color' : corporate_colors['light-grey']}
} # Legend will be on the top right, above the graph, horizontally

corporate_margins = {'l' : 5, 'r' : 5, 't' : 45, 'b' : 15}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font = {'family' : corporate_font_family},
    title = corporate_title,
    title_x = 0.5, # Align chart title to center
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis = corporate_xaxis,
    yaxis = corporate_yaxis,
    height = 270,
    legend = corporate_legend,
    margin = corporate_margins
    )

####################################################################################################
# 000 - DATA MAPPING
####################################################################################################

#Sales mapping
sales_filepath = 'data/datasource.xlsx'

sales_fields = {
    'date' : 'Date',
    'reporting_group_l1' : 'Country',
    'reporting_group_l2' : 'City',
    'sales' : 'Sales Units',
    'revenues' : 'Revenues',
    'sales target' : 'Sales Targets',
    'rev target' : 'Rev Targets',
    'num clients' : 'nClients'
    }
sales_formats = {
    sales_fields['date'] : '%d/%m/%Y'
}

####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

###########################
#Import sales data
xls = pd.ExcelFile(sales_filepath)
sales_import=xls.parse('Static')

#Format date field
sales_import[sales_fields['date']] = pd.to_datetime(sales_import[sales_fields['date']], format=sales_formats[sales_fields['date']])
sales_import['date_2'] = sales_import[sales_fields['date']].dt.date
min_dt = sales_import['date_2'].min()
min_dt_str = str(min_dt)
max_dt = sales_import['date_2'].max()
max_dt_str = str(max_dt)

#Create L1 dropdown options
repo_groups_l1 = sales_import[sales_fields['reporting_group_l1']].unique()
repo_groups_l1_all_2 = [
    {'label' : k, 'value' : k} for k in sorted(repo_groups_l1)
    ]
repo_groups_l1_all_1 = [{'label' : '(Select All)', 'value' : 'All'}]
repo_groups_l1_all = repo_groups_l1_all_1 + repo_groups_l1_all_2

#Initialise L2 dropdown options
repo_groups_l2 = sales_import[sales_fields['reporting_group_l2']].unique()
repo_groups_l2_all_2 = [
    {'label' : k, 'value' : k} for k in sorted(repo_groups_l2)
    ]
repo_groups_l2_all_1 = [{'label' : '(Select All)', 'value' : 'All'}]
repo_groups_l2_all = repo_groups_l2_all_1 + repo_groups_l2_all_2
repo_groups_l1_l2 = {}
for l1 in repo_groups_l1:
    l2 = sales_import[sales_import[sales_fields['reporting_group_l1']] == l1][sales_fields['reporting_group_l2']].unique()
    repo_groups_l1_l2[l1] = l2

################################################################################################################################################## SET UP END

####################################################################################################
# 000 - DEFINE REUSABLE COMPONENTS AS FUNCTIONS
####################################################################################################

#####################
# Header with logo
def get_header():

    header = html.Div([

        html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Performance Dashboard',
                    style = {'textAlign' : 'center'}
            )],
            className='col-8',
            style = {'padding-top' : '1%'}
        ),

        html.Div([
            html.Img(
                    src = app.get_asset_url('logo_001c.png'),
                    height = '43 px',
                    width = 'auto')
            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '1%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' : corporate_colors['superdark-green']}
        )

    return header

#####################
# Nav bar
def get_navbar(p = 'sales'):

    navbar_sales = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Sales Overview',
                        style = navbarcurrentpage),
                href='/apps/sales-overview'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Page 2'),
                href='/apps/page2'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Page 3'),
                href='/apps/page3'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['dark-green'],
            'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    navbar_page2 = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Sales Overview'),
                href='/apps/sales-overview'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Page 2',
                        style = navbarcurrentpage),
                href='/apps/page2'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Page 3'),
                href='/apps/page3'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['dark-green'],
            'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    navbar_page3 = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Sales Overview'),
                href='/apps/sales-overview'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Page 2'),
                href='/apps/page2'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Page 3',
                        style = navbarcurrentpage),
                href='/apps/page3'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['dark-green'],
            'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    if p == 'sales':
        return navbar_sales
    elif p == 'page2':
        return navbar_page2
    else:
        return navbar_page3

#####################
# Empty row

def get_emptyrow(h='45px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

####################################################################################################
# 001 - SALES
####################################################################################################

sales = html.Div([

    #####################
    #Row 1 : Header
    get_header(),

    #####################
    #Row 2 : Nav bar
    get_navbar('sales'),

    #####################
    #Row 3 : Filters
    html.Div([ # External row

        html.Div([ # External 12-column

            html.Div([ # Internal row

                #Internal columns
                html.Div([
                ],
                className = 'col-2'), # Blank 2 columns

                #Filter pt 1
                html.Div([

                    html.Div([
                        html.H5(
                            children='Filters by Date:',
                            style = {'text-align' : 'left', 'color' : corporate_colors['medium-blue-grey']}
                        ),
                        #Date range picker
                        html.Div(['Select a date range: ',
                            dcc.DatePickerRange(
                                id='date-picker-sales',
                                start_date = min_dt_str,
                                end_date = max_dt_str,
                                min_date_allowed = min_dt,
                                max_date_allowed = max_dt,
                                start_date_placeholder_text = 'Start date',
                                display_format='DD-MMM-YYYY',
                                first_day_of_week = 1,
                                end_date_placeholder_text = 'End date',
                                style = {'font-size': '12px','display': 'inline-block', 'border-radius' : '2px', 'border' : '1px solid #ccc', 'color': '#333', 'border-spacing' : '0', 'border-collapse' :'separate'})
                        ], style = {'margin-top' : '5px'}
                        )

                    ],
                    style = {'margin-top' : '10px',
                            'margin-bottom' : '5px',
                            'text-align' : 'left',
                            'paddingLeft': 5})

                ],
                className = 'col-4'), # Filter part 1

                #Filter pt 2
                html.Div([

                    html.Div([
                        html.H5(
                            children='Filters by Reporting Groups:',
                            style = {'text-align' : 'left', 'color' : corporate_colors['medium-blue-grey']}
                        ),
                        #Reporting group selection l1
                        html.Div([
                            dcc.Dropdown(id = 'reporting-groups-l1dropdown-sales',
                                options = repo_groups_l1_all,
                                value = [''],
                                multi = True,
                                placeholder = "Select " +sales_fields['reporting_group_l1']+ " (leave blank to include all)",
                                style = {'font-size': '13px', 'color' : corporate_colors['medium-blue-grey'], 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                )
                            ],
                            style = {'width' : '70%', 'margin-top' : '5px'}),
                        #Reporting group selection l2
                        html.Div([
                            dcc.Dropdown(id = 'reporting-groups-l2dropdown-sales',
                                options = repo_groups_l2_all,
                                value = [''],
                                multi = True,
                                placeholder = "Select " +sales_fields['reporting_group_l2']+ " (leave blank to include all)",
                                style = {'font-size': '13px', 'color' : corporate_colors['medium-blue-grey'], 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
                                )
                            ],
                            style = {'width' : '70%', 'margin-top' : '5px'})
                    ],
                    style = {'margin-top' : '10px',
                            'margin-bottom' : '5px',
                            'text-align' : 'left',
                            'paddingLeft': 5})

                ],
                className = 'col-4'), # Filter part 2

                html.Div([
                ],
                className = 'col-2') # Blank 2 columns


            ],
            className = 'row') # Internal row

        ],
        className = 'col-12',
        style = filterdiv_borderstyling) # External 12-column

    ],
    className = 'row sticky-top'), # External row

    #####################
    #Row 4
    get_emptyrow(),

    #####################
    #Row 5 : Charts
    html.Div([ # External row

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

        html.Div([ # External 10-column

            html.H2(children = "Sales Performances",
                    style = {'color' : corporate_colors['white']}),

            html.Div([ # Internal row - RECAPS

                html.Div([],className = 'col-4'), # Empty column

                html.Div([
                    dash_table.DataTable(
                        id='recap-table',
                        style_header = {
                            'backgroundColor': 'transparent',
                            'fontFamily' : corporate_font_family,
                            'font-size' : '1rem',
                            'color' : corporate_colors['light-green'],
                            'border': '0px transparent',
                            'textAlign' : 'center'},
                        style_cell = {
                            'backgroundColor': 'transparent',
                            'fontFamily' : corporate_font_family,
                            'font-size' : '0.85rem',
                            'color' : corporate_colors['white'],
                            'border': '0px transparent',
                            'textAlign' : 'center'},
                        cell_selectable = False,
                        column_selectable = False
                    )
                ],
                className = 'col-4'),

                html.Div([],className = 'col-4') # Empty column

            ],
            className = 'row',
            style = recapdiv
            ), # Internal row - RECAPS

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='sales-count-day')
                ],
                className = 'col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='sales-count-month')
                ],
                className = 'col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='sales-weekly-heatmap')
                ],
                className = 'col-4')

            ],
            className = 'row'), # Internal row

            html.Div([ # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='sales-count-country')
                ],
                className = 'col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='sales-bubble-county')
                ],
                className = 'col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='sales-count-city')
                ],
                className = 'col-4')

            ],
            className = 'row') # Internal row


        ],
        className = 'col-10',
        style = externalgraph_colstyling), # External 10-column

        html.Div([
        ],
        className = 'col-1'), # Blank 1 column

    ],
    className = 'row',
    style = externalgraph_rowstyling
    ), # External row

])

####################################################################################################
# 002 - Page 2
####################################################################################################

page2 = html.Div([

    #####################
    #Row 1 : Header
    get_header(),

    #####################
    #Row 2 : Nav bar
    get_navbar('page2'),

    #####################
    #Row 3 : Filters
    html.Div([ # External row

        html.Br()

    ],
    className = 'row sticky-top'), # External row

    #####################
    #Row 4
    get_emptyrow(),

    #####################
    #Row 5 : Charts
    html.Div([ # External row

        html.Br()

    ])

])

####################################################################################################
# 003 - Page 3
####################################################################################################

page3 = html.Div([

    #####################
    #Row 1 : Header
    get_header(),

    #####################
    #Row 2 : Nav bar
    get_navbar('page3'),

    #####################
    #Row 3 : Filters
    html.Div([ # External row

        html.Br()

    ],
    className = 'row sticky-top'), # External row

    #####################
    #Row 4
    get_emptyrow(),

    #####################
    #Row 5 : Charts
    html.Div([ # External row

        html.Br()

    ])

])
