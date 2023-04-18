from dashFunctions import add_data, generate_bigrams, generate_trigrams, generate_plot

#Dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#Graphing
import plotly.express as px

#Generic
import pandas as pd
import base64
from io import BytesIO
import base64


data = add_data()

multi_select = {
    'Product Family': ['Other', 'ABC', 'Pull-On', 'Commission', 'Unspecified Jogger', 'License to Train', 'Surge', 'City Sweat', 'Running', 'Lab', 'Hiking', 'New Venture', 'Balancer', 'Discipline'],
    'Product Design': ['On the Move', 'Golf', 'Training', 'Running', 'Yoga', 'Hiking', 'Running and Training'],
    'Product Fabric': ['Other', 'Warpstreme Fabric', 'Utilitech Fabric', 'Stretch Fabric', 'Swift Fabric', 'Quick-Drying Fabric', 'Fleece Fabric', 'Terry Fabric', 'SenseKnit Technology', 'WovenAir Fabric', 'Luxtreme Fabric', 'Water-Repellent Fabric', 'Wool-Blend Fabric', 'Everlux Fabric', 'Nulux Fabric']
}

external_style = ['/bootstrap.css']

app = Dash(__name__, external_stylesheets=external_style)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            children = [
                html.H2(
                    children = 'Lululemon Mens Pants Dashboard',
                    style = {
                        'textAlign': 'center',
                        'fontSize': 32
                        }
                ), 

                html.P(
                    children = 'Use this dashboard to explore reviews of Lululemon mens pants posted to their official website. Data was collected on March 16, 2023.',
                    style = {
                        'textAlign': 'center',
                        'fontSize': 22
                        }
                )
            ]

        ),

        html.Br(),
        html.Hr(),
        
        html.Div(
            children = [
                html.H2(
                    children='Section 1: General Overview',
                    style={
                        'textAlign': 'left',
                        'fontSize': 26
                        }
                    ),

                    html.P(
                        children='The bar charts  show the total number of products and reviews throughout the dataset.\
                        The data can be grouped by either family, design, or fabric in order to get a better sense of trends in the data. Please note the use of a logged scale for the first bar chart.\
                        The bar chart on the left shows total number of reviews while the right shows total number of products.', 
                        style={
                            'textAlign': 'left',
                            'fontSize': 18
                        }
                    ),

                    html.Br(),
                    html.Br(),

                    html.Div(
                        [
                            html.Label('Please select one of the following categories:'),
                            html.Br(),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Product Family', 'value': 'Product Family'},
                                    {'label': 'Product Design', 'value': 'Product Design'},
                                    {'label': 'Product Fabric', 'value': 'Product Fabric'}
                                ],
                                id='column-drop-down',
                                value='Product Family'
                            ),
                            html.Div(
                                [
                                    dcc.Graph(id='review-bar-graph', style={'display': 'inline-block'}),
                                    dcc.Graph(id='product-bar-graph', style={'display': 'inline-block'})
                                ]
                            ), 
                            html.Br()
                        ]
                    )
            ],
            style={'textAlign': 'center'}
        ),
        
        html.Br(),
        html.Hr(),

        html.Div(
            children = [
                html.Div(
                    children=[
                        html.H2(
                            children='Section 2: Product Rating Analysis',
                            style={
                                'textAlign': 'left',
                                'fontSize': 26
                            }
                        ),

                        html.P(
                            children='The graph on the left is a stacked bar which highlights the relative percentage of reviews within a category. \
                                The 5 star reviews appear at the top of the bar, the 1 star reviews appear at the bottom, and the actual count of the number of reviews is displayed on the bar itself. \
                                The line graph on the right shows the average rating for the given category at different time periods. Feel free to toggle between inputs and change the date range.',
                            style={
                                'textAlign': 'left',
                                'fontSize': 18
                            }
                        )
                    ]
                ),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label('Please select one of the following inputs:'),
                                html.Br(),
                                dcc.Dropdown(
                                    options=[
                                        {'label': 'Product Family', 'value': 'Product Family'},
                                        {'label': 'Product Design', 'value': 'Product Design'},
                                        {'label': 'Product Fabric', 'value': 'Product Fabric'}
                                    ],
                                    id='category-select',
                                    value='Product Family',
                                    style={'width':'250px', 'display': 'inline-block'}
                                )
                            ],
                            width={'size': 4, 'offset': 1}
                        ),

                        html.Br(), 
                        
                        dbc.Col(
                            [
                                html.Label('Choose the date range below:'),
                                html.Br(),
                                dcc.Slider(
                                    id='year-slider',
                                    min=int(data['Year of Review'].min()),
                                    max=int(data['Year of Review'].max()),
                                    value=int(data['Year of Review'].max()),
                                    marks={str(year): str(year) for year in data['Year of Review'].unique()}
                                )
                            ],
                            width={'size': 5, 'offset': 1}
                        )
                    ],
                    justify="center",
                    align="center"
                ),

                html.Br(),

                html.Div(
                    children=[
                        dcc.Graph(id='stacked-bar', style={'display': 'inline-block'}),
                        dcc.Graph(id='moving-average', style={'display': 'inline-block'})
                    ]
                )
            ],
            style={'textAlign': 'center'}
        ), 

        html.Br(),
        html.Hr(),

        html.Div(
            children = [
                html.Div(
                    children=[
                        html.H2(
                            children='Section 3: Review Text Analysis',
                            style={
                                'textAlign': 'left',
                                'fontSize': 26
                            }
                        ),

                        html.P(
                            children='The word clouds below show the most common words and phrases that appear within the text of reviews. \
                            The first word cloud shows the most common words in reviews with ratings less than 3 starts while the second cloud shows the most common words in reviews with more than 3 stars. \
                            Toggle between options to better understand strengths and areas of improvement for each product group.',
                            style={
                                'textAlign': 'left',
                                'fontSize': 18
                            }
                        )
                    ]
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label('Please select one of the following inputs:'),
                                html.Br(),
                                dcc.RadioItems(
                                    options=list(multi_select.keys()),
                                    value = 'Product Family', 
                                    id='radio-cat-input',
                                    labelStyle={'display':'inline-block'}
                                ),
                            ],
                            width={'size': 4, 'offset': 0}
                        ),

                        html.Br(),

                        dbc.Col(
                            [
                                html.Label('Please select one of the following options:'),
                                html.Br(),
                                dcc.RadioItems(
                                    id='radio-cat-output', 
                                    labelStyle={'display':'inline-block'})
                            ],
                            width={'size': 4, 'offset': 0}
                        )
                    ],
                    justify="center",
                    align="center"
                ),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label('Please select one of the following n-gram types:'),
                                html.Br(),
                                dcc.RadioItems(
                                    id='ngram-input',
                                    options = [
                                        dict(label = 'token', value = 'token'),
                                        dict(label = 'bigram', value = 'bigram'),
                                        dict(label = 'trigram', value = 'trigram')],
                                    value = 'token',
                                    labelStyle={'display':'inline-block'}
                                )
                            ],
                            width={'size': 4, 'offset': 1}
                        ),

                        html.Br(),

                        dbc.Col(
                            [
                                html.Label('Please select number of phrases to display:'),
                                html.Br(),
                                dcc.Slider(
                                    min = 10, 
                                    max = 25, 
                                    step = 1,
                                    value = 10,
                                    id = 'ngram-count')
                            ],
                            width={'size': 4, 'offset': 1}
                        ), 
                    ]
                ),

                html.Br(),
                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label('N-grams of Negative Reviews (Rating < 3)'), 
                                html.Br(),
                                html.Img(id = 'wc-image1', style={'display': 'inline-block'})
                            ], 
                            width={'size': 4, 'offset': 1}
                        ), 

                        html.Br(),

                        dbc.Col(
                            [
                                html.Label('N-grams of Positive Reviews (Rating > 3)'), 
                                html.Br(),
                                html.Img(id = 'wc-image2', style={'display': 'inline-block'})

                            ]
                        )
                    ],
                    style={'textAlign': 'center'}
                )
            ],
            style={'textAlign': 'center'}
        ), 

        html.Br()
    ], 
    style={'padding': '5px'}
)

@app.callback(
    Output('review-bar-graph', 'figure'),
    Input('column-drop-down', 'value')
)

def update_review_bar(value):
    data1 = data.groupby(value).size().sort_values(ascending=False).reset_index(name='Number of Reviews')
    fig = px.bar(data1, x=value, y='Number of Reviews', log_y=True)
    fig.update_layout(title_text= 'Number of Reviews by ' + str(value), title_x=0.5)
    return fig

@app.callback(
    Output('product-bar-graph', 'figure'),
    Input('column-drop-down', 'value')
)

def update_product_bar(value):
    data2 = data.groupby('Product ID').nth(0).groupby(value)[value].count().sort_values(ascending=False).reset_index(name='Number of Products')
    fig = px.bar(data2, x = value, y = 'Number of Products')
    fig.update_layout(title_text= 'Number of Products by ' + str(value), title_x=0.5)
    return fig


@app.callback(
    Output('moving-average', 'figure'),
    [Input('year-slider', 'value'),
    Input('category-select', 'value')]
)

def update_line(year, value):
    df = data[data['Year of Review'] <= year]

    # Split the data before and after March 16 (a year to the day of the latest review in dataframe)
    df_before = df[df['Date of Review'] < '2022-03-16']
    df_before['YearMonth'] = df_before['Date of Review'].apply(lambda x: x.strftime('%Y-%m'))
    df_before = df_before.groupby([value, 'YearMonth'])['Rating (out of 5)'].mean().reset_index()
    df_before = df_before.rename(columns={'Rating (out of 5)': 'Avg Rating'})

    df_after = df[df['Date of Review'] >= '2022-03-16']
    df_after['YearMonth'] = df_after['Date of Review'].apply(lambda x: x.strftime('%Y-%m'))
    df_after = df_after.groupby([value, 'YearMonth'])['Rating (out of 5)'].mean().reset_index()
    df_after = df_after.rename(columns={'Rating (out of 5)': 'Avg Rating'})

    df = pd.concat([df_before, df_after], ignore_index=True)

    fig = px.line(df, x='YearMonth', y='Avg Rating', color=value)
    fig.update_layout(yaxis_title="Average Rating (out of 5)", xaxis_title = "Date", 
    title_text= 'Average Product Rating Over Time', title_x=0.5)
    return fig

@app.callback(
    Output('stacked-bar', 'figure'),
    [Input('year-slider', 'value'),
    Input('category-select', 'value')]
)

def update_stacked(year, value):
    data2 = data[data['Year of Review'] <= year]
    data2['Rating Category'] = pd.cut(data2['Rating (out of 5)'], bins=[0, 1, 2, 3, 4, 5], labels=['1', '2', '3', '4', '5'])

    grouped = data2.groupby([value, 'Rating Category']).size().reset_index(name='Count')
    grouped['Percentage'] = grouped.groupby(value)['Count'].apply(lambda x: x / x.sum() * 100)

    colors = ['#d7191c','#fdae61','#ffffbf','#a6d96a','#1a9641']

    fig = px.bar(grouped, x=value, y='Percentage', color='Rating Category', barmode='stack', text='Count', 
    color_discrete_map={'1': colors[0], '2': colors[1], '3': colors[2], '4': colors[3], '5': colors[4]})

    fig.update_layout(title='Percentage of Ratings by ' + str(value) +  ' and Rating Category', title_x=0.5, 
                    xaxis_title=value,
                    yaxis_title='Percentage of Ratings')
    return fig


@app.callback(
    Output('radio-cat-output', 'options'),
    Input('radio-cat-input', 'value'))
def display_categories(categorical_var):
    return [{'label': i, 'value': i} for i in multi_select[categorical_var]]


@app.callback(
    Output('radio-cat-output', 'value'),
    Input('radio-cat-output', 'options'))
def display_options(available_options):
    return available_options[0]['value']

@app.callback(
    Output('wc-image1', 'src'),
    [Input('radio-cat-input', 'value'),
    Input('radio-cat-output', 'value'),
    Input('ngram-input', 'value'),
    Input('ngram-count', 'value')]
)
def update_word_cloud(column_select, value_select, ngram_type, top_n):
    df = data[data['Rating (out of 5)'] < 3]
    df = df[df[column_select] == value_select]

    #Added to code
    img = BytesIO()
    generate_plot(df['Review Text Token'], ngram_type, top_n).save(img, format='PNG') #fig = ... (not including .save()); return fig if this doesn't work
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(
    Output('wc-image2', 'src'),
    [Input('radio-cat-input', 'value'),
    Input('radio-cat-output', 'value'),
    Input('ngram-input', 'value'),
    Input('ngram-count', 'value')]
)
def update_word_cloud(column_select, value_select, ngram_type, top_n):
    df = data[data['Rating (out of 5)'] > 3]
    df = df[df[column_select] == value_select]
    fig = generate_plot(df['Review Text Token'], ngram_type, top_n)
    return fig

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=8050, debug=True)
