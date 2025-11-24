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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Olympics Dashboard"


# -------------------------
# Layout
# -------------------------
app.layout = dbc.Container([
    html.H1("Olympic Games Dashboard", className="text-center mt-4 mb-4"),

    dcc.Tabs([

        # ---------------- TAB 1: HOME -------------------
        dcc.Tab(label="🏠 Home", children=[
            html.Div([
                html.H2("Välkommen till vår OS-dashboard"),

                dcc.Markdown("""
                This dashboard shows results from Great Britain and Other Countries.
                Navigate the tabs above to view different visualizations.
                """)
            ], className="p-4")
        ]),

        # ---------------- TAB 2: UPPGIFT 1 -------------------
        dcc.Tab(label="GBR", children=[
            html.Div([

                html.H2(" Great Britain (GBR)"),

                html.H4("choose visualisering"),
                dcc.Dropdown(
                    id="gbr_graph_selector",
                    options=[
                        {"label": "Top 10 Sports by Medals", "value": "sports"},
                        {"label": "Medal Breakdown (Stacked)", "value": "breakdown"},
                        {"label": "Medals Per Year", "value": "year"},
                        {"label": "Age Distribution", "value": "age"},
                    ],
                    value="sports"
                ),

                html.Br(),

                html.H4("Välj medaljtyp"),
                dcc.Dropdown(
                    id="gbr_medal_filter",
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "Gold", "value": "Gold"},
                        {"label": "Silver", "value": "Silver"},
                        {"label": "Bronze", "value": "Bronze"},
                    ],
                    value="All"
                ),

                html.Br(),

                html.H4("Choose Time Period"),
                dcc.RangeSlider(
                    id="gbr_year_slider",
                    min=int(gbr["Year"].min()),
                    max=int(gbr["Year"].max()),
                    value=[1900, 2020],
                    step=4,
                    marks={y: str(y) for y in range(1900, 2021, 20)}
                ),

                html.Hr(),

                dcc.Graph(id="gbr_dynamic_graph")

            ], className="p-4")
        ]),

        # ---------------- TAB 3: UPPGIFT 2 -------------------

        dcc.Tab(
    label="🏅 Uppgift 2 – Sporter",
    children=[
        html.Div([

            html.H2("Uppgift 2 – Sportanalys"),

            html.H4("Välj sport"),
            dcc.Dropdown(
                id="sport_selector",
                options=[
                    {"label": s, "value": s}
                    for s in sorted(df["Sport"].dropna().unique())
                    if s in ["Athletics", "Cycling", "Swimming", "Football"]
                ],
                value="Athletics"
            ),

        ], className="p-4")
    ])

    ])
], fluid=True)


# -------------------------
# CALLBACKS – REAL GRAPHS FOR UPPGIFT 1
# -------------------------
@app.callback(
    Output("gbr_dynamic_graph", "figure"),
    Input("gbr_graph_selector", "value"),
    Input("gbr_medal_filter", "value"),
    Input("gbr_year_slider", "value")
)
def update_gbr_graph(graph_type, medal_filter, year_range):

    # --- Filter by year ---
    df_local = gbr[(gbr["Year"] >= year_range[0]) & (gbr["Year"] <= year_range[1])]

    # --- Filter by medal ---
    if medal_filter != "All":
        df_local = df_local[df_local["Medal"] == medal_filter]

    # 1) Top sports
    if graph_type == "sports":
        top_sports = (
            df_local[df_local["Medal"].notna()]
            .groupby("Sport")["Medal"]
            .count()
            .reset_index(name="Medals")
            .sort_values("Medals", ascending=False)
            .head(10)
        )

        fig = px.bar(top_sports, x="Sport", y="Medals",
                     title="GBR – Top 10 Sports by Medals")
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        return fig

    # 2) Medal breakdown stacked
    if graph_type == "breakdown":
        breakdown = (
            df_local[df_local["Medal"].notna()]
            .groupby(["Year", "Medal"])["Medal"]
            .count()
            .reset_index(name="Count")
        )

        fig = px.bar(
            breakdown,
            x="Year",
            y="Count",
            color="Medal",
            title="GBR – Medal Breakdown per Year",
            barmode="stack"
        )
        return fig

    # 3) Medals per year
    if graph_type == "year":
        per_year = (
            df_local[df_local["Medal"].notna()]
            .groupby("Year")["Medal"]
            .count()
            .reset_index(name="Medals")
        )

        fig = px.line(per_year, x="Year", y="Medals", markers=True,
                      title="GBR – Medals per Year")
        return fig

    # 4) Age distribution
    if graph_type == "age":
        age_data = df_local[df_local["Age"].notna()]

        fig = px.histogram(age_data, x="Age", nbins=40,
                           title="GBR – Age Distribution")
        return fig

    return placeholder_fig("No data")


# -------------------------
# CALLBACKS – Uppgift 2 (placeholder)
# -------------------------
@app.callback(
    Output("sport_dynamic_graph", "figure"),
    Input("sport_selector", "value"),
    Input("country_selector", "value"),
    Input("sport_plot_type", "value")
)
def update_sport_graph(sport, country, plot_type):

    title = f"{sport} | {country} | {plot_type}"

    # placeholder
    return placeholder_fig(title)


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
