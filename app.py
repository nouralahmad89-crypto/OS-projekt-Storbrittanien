import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from load_dataset import load_data

# --- LOAD DATA ---

merged, gbr_data = load_data()
df = merged
gbr = gbr_data["gbr"]

def placeholder_fig(title):
    fig = px.scatter(x=[0], y=[0], title=title)
    fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig

# --- APP ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Olympics Dashboard"
server= app.server
# --- NAVBAR ---
navbar = dbc.NavbarSimple(
    brand="Olympics Dashboard 🏅",
    color="primary",
    dark=True,
    fluid=True,
)

# --- TABS ---
tabs = dbc.Container([
    dcc.Tabs([

        # --- HOME TAB ---
        dcc.Tab(label="🏠 Home", children=[
            dbc.Container([
                html.H2("Welcome to the Olympics Dashboard", className="text-center mt-4 mb-4", style={"color": "#196F3D"}),
                dbc.Card(
                    dbc.CardBody([
                        dcc.Markdown("""
                            This dashboard shows results from Great Britain and Other Countries.
                            Navigate the tabs above to view different visualizations.
                        """)
                    ]),
                    className="shadow p-3 rounded",
                    style={"backgroundColor": "#F8F9F9"}
                )
            ], className="p-4")
        ]),

        # --- GBR TAB ---
        dcc.Tab(label="Great Britain", children=[
            dbc.Container([
                html.H2("Great Britain (GBR)", className="mb-4", style={"color": "#2C3E50", "textAlign": "center"}),

                # Controls Card
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Choose Graph", style={"color": "#1F618D"}),
                        dcc.Dropdown(
                            id="gbr_graph_selector",
                            options=[
                                {"label": "Top 10 Sports by Medals - Stacked Bar", "value": "top_sports"},
                                {"label": "Medals per OS - Bar Chart", "value": "medals_per_os"},
                                {"label": "Medals Over Time - Line Plot", "value": "medals_over_time"},
                                {"label": "Medal Types Distribution - Pie Chart", "value": "medal_types_pie"},
                                {"label": "Age Distribution - Histogram", "value": "age_hist"},
                                {"label": "Gender Distribution - Pie Chart", "value": "gender_pie"},
                            ],
                            value="top_sports"
                        ),
                        html.Br(),
                        html.H4("Select Time Period", style={"color": "#1F618D"}),
                        dcc.RangeSlider(
                            id="gbr_year_slider",
                            min=int(gbr["Year"].min()),
                            max=int(gbr["Year"].max()),
                            value=[1900, 2020],
                            step=4,
                            marks={y: str(y) for y in range(1900, 2021, 20)}
                        ),
                    ])
                ], className="mb-4 shadow p-2 rounded", style={"backgroundColor": "#F8F9F9"}),

                # Summary Board
                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Total Medals", style={"color":"#1F618D"}),
                            html.H3(id="gbr_total_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Gold", style={"color":"gold"}),
                            html.H3(id="gbr_gold_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Silver", style={"color":"silver"}),
                            html.H3(id="gbr_silver_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Bronze", style={"color":"saddlebrown"}),
                            html.H3(id="gbr_bronze_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                ], className="mb-3"),

                # Graph Card
                dbc.Card([
                    dbc.CardBody([dcc.Graph(id="gbr_dynamic_graph")])
                ], className="shadow p-2 rounded", style={"backgroundColor": "#FFFFFF"}),

            ], className="p-4")
        ]),

        # --- UPPGIFT 2 TAB ---
        dcc.Tab(label="Sportstatistik", children=[
            dbc.Container([
                html.H2("Sport Analysis", className="text-success mb-4", style={"textAlign": "center"}),

                # Controls Card
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Choose Graph", style={"color": "#D35400"}),
                        dcc.Dropdown(
                            id="sport_graph_selector",
                            options=[
                                {"label": "Top Athletes by Medals - Bar Chart", "value": "top_athletes"},
                                {"label": "Top 10 Countries by Medals - Bar Chart", "value": "top_countries"},
                                {"label": "Age Distribution - Histogram", "value": "age_hist"},
                                {"label": "Gender Distribution - Pie Chart", "value": "gender_pie"},
                                {"label": "Medal Types Breakdown - Stacked Bar", "value": "medal_breakdown"},
                            ],
                            value="top_athletes"
                        ),
                        html.Br(),
                        html.H4("Select Sport", style={"color": "#D35400"}),
                        dcc.Dropdown(
                            id="sport_selector",
                            options=[
                                {"label": s, "value": s}
                                for s in sorted(df["Sport"].dropna().unique())
                                if s in ["Athletics", "Cycling", "Swimming", "Football"]
                            ],
                            value="Athletics"
                        ),
                    ])
                ], className="mb-4 shadow p-2 rounded", style={"backgroundColor": "#FDFEFE"}),

                # Summary Board for Sport Tab
                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Total Medals", style={"color":"#1F618D"}),
                            html.H3(id="sport_total_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Gold", style={"color":"gold"}),
                            html.H3(id="sport_gold_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Silver", style={"color":"silver"}),
                            html.H3(id="sport_silver_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Bronze", style={"color":"saddlebrown"}),
                            html.H3(id="sport_bronze_medals", className="card-text")
                        ])
                    ], className="shadow rounded text-center", style={"backgroundColor":"#FDFEFE"}), width=3),
                ], className="mb-3"),

                # Graph Card
                dbc.Card([
                    dbc.CardBody([dcc.Graph(id="sport_dynamic_graph")])
                ], className="shadow p-2 rounded", style={"backgroundColor": "#FFFFFF"}),

            ], className="p-4")
        ])
    ])
], fluid=True)

# --- APP LAYOUT ---
app.layout = dbc.Container([navbar, tabs], fluid=True)

# --- CALLBACKS: GBR ---
@app.callback(
    Output("gbr_dynamic_graph", "figure"),
    Output("gbr_total_medals", "children"),
    Output("gbr_gold_medals", "children"),
    Output("gbr_silver_medals", "children"),
    Output("gbr_bronze_medals", "children"),
    Input("gbr_graph_selector", "value"),
    Input("gbr_year_slider", "value")
)
def update_gbr_graph(graph_type, year_range):
    df_local = gbr[(gbr["Year"] >= year_range[0]) & (gbr["Year"] <= year_range[1])]
    total = df_local["Medal"].notna().sum()
    gold = (df_local["Medal"]=="Gold").sum()
    silver = (df_local["Medal"]=="Silver").sum()
    bronze = (df_local["Medal"]=="Bronze").sum()

    if graph_type == "top_sports":
        top_sports = df_local[df_local["Medal"].notna()].groupby(["Sport","Medal"])["Medal"].count().reset_index(name="Count")
        top10 = top_sports.groupby("Sport")["Count"].sum().sort_values(ascending=False).head(10).index
        top_sports = top_sports[top_sports["Sport"].isin(top10)]
        fig = px.bar(top_sports, x="Sport", y="Count", color="Medal", barmode="stack",
                     color_discrete_map={"Gold":"gold","Silver":"silver","Bronze":"saddlebrown"},
                     title="GBR – Top 10 Sports by Medals")
    elif graph_type == "medals_per_os":
        per_os = df_local[df_local["Medal"].notna()].groupby("Year")["Medal"].count().reset_index(name="Medals")
        fig = px.bar(per_os, x="Year", y="Medals", color="Medals", color_continuous_scale=px.colors.sequential.Viridis,
                     title="GBR – Medals per Olympics")
    elif graph_type == "medals_over_time":
        per_year = df_local[df_local["Medal"].notna()].groupby("Year")["Medal"].count().reset_index(name="Medals")
        fig = px.line(per_year, x="Year", y="Medals", markers=True, line_shape='spline', color_discrete_sequence=px.colors.qualitative.Plotly,
                      title="GBR – Medals Over Time")
    elif graph_type == "medal_types_pie":
        counts = df_local[df_local["Medal"].notna()]["Medal"].value_counts().reset_index()
        counts.columns = ["Medal","Count"]
        fig = px.pie(counts, names="Medal", values="Count",
                     color="Medal", color_discrete_map={"Gold":"gold","Silver":"silver","Bronze":"saddlebrown"},
                     title="GBR – Medal Types Distribution")
    elif graph_type == "age_hist":
        age_data = df_local[df_local["Age"].notna()]
        fig = px.histogram(age_data, x="Age", nbins=40, color_discrete_sequence=px.colors.qualitative.Bold,
                           title="GBR – Age Distribution")
    elif graph_type == "gender_pie":
        gender_counts = df_local["Sex"].value_counts().reset_index()
        gender_counts.columns = ["Gender","Count"]
        fig = px.pie(gender_counts, names="Gender", values="Count",
                     color="Gender", color_discrete_map={"M":"blue","F":"pink"},
                     title="GBR – Gender Distribution")
    else:
        fig = placeholder_fig("No data")

    return fig, total, gold, silver, bronze

# --- CALLBACKS: Uppgift 2 ---
@app.callback(
    Output("sport_dynamic_graph", "figure"),
    Output("sport_total_medals", "children"),
    Output("sport_gold_medals", "children"),
    Output("sport_silver_medals", "children"),
    Output("sport_bronze_medals", "children"),
    Input("sport_selector", "value"),
    Input("sport_graph_selector", "value")
)
def update_sport_graph(sport, graph_type):
    sport_df = df[df["Sport"] == sport]
    total = sport_df["Medal"].notna().sum()
    gold = (sport_df["Medal"]=="Gold").sum()
    silver = (sport_df["Medal"]=="Silver").sum()
    bronze = (sport_df["Medal"]=="Bronze").sum()

    if graph_type == "top_athletes":
        top_athletes = sport_df[sport_df["Medal"].notna()].groupby("Name")["Medal"].count().reset_index(name="Medals").sort_values("Medals", ascending=False).head(10)
        fig = px.bar(top_athletes, x="Name", y="Medals", color="Medals", color_continuous_scale=px.colors.sequential.Viridis,
                     title=f"{sport} – Top Athletes by Medals")
    elif graph_type == "top_countries":
        top_countries = sport_df[sport_df["Medal"].notna()].groupby("NOC")["Medal"].count().reset_index(name="Medals")
        top_countries = top_countries.sort_values("Medals", ascending=False).head(10)
        fig = px.bar(top_countries, x="NOC", y="Medals", color="Medals", color_continuous_scale=px.colors.sequential.Viridis,
                     title=f"{sport} – Top 10 Countries by Medals")
    elif graph_type == "age_hist":
        age_data = sport_df[sport_df["Age"].notna()]
        fig = px.histogram(age_data, x="Age", nbins=40, color_discrete_sequence=px.colors.qualitative.Bold,
                           title=f"{sport} – Age Distribution")
    elif graph_type == "gender_pie":
        gender_counts = sport_df["Sex"].value_counts().reset_index()
        gender_counts.columns = ["Gender","Count"]
        fig = px.pie(gender_counts, names="Gender", values="Count", color="Gender",
                     color_discrete_map={"M":"blue","F":"pink"}, title=f"{sport} – Gender Distribution")
    elif graph_type == "medal_breakdown":
        breakdown = sport_df[sport_df["Medal"].notna()].groupby(["Year","Medal"])["Medal"].count().reset_index(name="Count")
        fig = px.bar(breakdown, x="Year", y="Count", color="Medal", barmode="stack",
                     color_discrete_map={"Gold":"gold","Silver":"silver","Bronze":"saddlebrown"},
                     title=f"{sport} – Medal Types Breakdown per Year")
    else:
        fig = placeholder_fig(f"{sport} – No Data")

    return fig, total, gold, silver, bronze

# --- RUN APP ---
if __name__ == "__main__":
    app.run(debug=True)