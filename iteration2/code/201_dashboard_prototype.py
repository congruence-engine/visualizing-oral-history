# Dashboard prototype
# Depends on:
#     code/analysis/122_bertopic_sbertmpnet.ipynb

# Local setup
from local_dir_setup import *

# Libraries
from dash import Dash, html, dcc, State, Output, Input, ctx
import plotly.express as px
import pandas as pd
pd.set_option('display.max_columns', None)


# Load data
vis_df = pd.read_csv(dir_storage + "---transcripts-objects-topics-file---") # Output from 131_bertopic_sbertmpnet.ipynb
vis_df["start_time"] = vis_df["start_time"] / 60.0
vis_df["end_time"] = vis_df["end_time"] / 60.0
vis_df["segment_len"] = vis_df["end_time"] - vis_df["start_time"]
vis_df["vis_topic"] = "Not shown"


# Generate sorted list of topics
grouped = vis_df.groupby("bertopic_topic_name").size().reset_index(name="Count")
grouped_sorted = grouped.sort_values(by="Count", ascending=False)
vis_df_topics = grouped_sorted["bertopic_topic_name"].tolist()
vis_df_topics = [t for t in vis_df_topics if not t.startswith("-1")]

# Generate list of interviews
interviews = vis_df["transcript"].unique()

app = Dash(__name__, prevent_initial_callbacks="initial_duplicate")
selected_indices = None

app.layout = html.Div([
    html.H1(children="Title", style={"textAlign":"center"}),
    html.Div([
        dcc.Tabs(id="tabs", value="tab-1-timelines", children=[
            dcc.Tab(label="Timelines", value="tab-1-timelines"),
            dcc.Tab(label="UMAP scatterplot", value="tab-2-scatterplot"),
        ]),
        html.Div([
            dcc.Graph(
                id="graph-content"
            ),
        ])
    ], style={"width": "69%", "display": "inline-block"}),
    # Side panel
    html.Div([
        html.Div([
            dcc.Dropdown(vis_df_topics, id="topic-dropdown-selection", multi=True, placeholder="Select topic..."),
            dcc.Dropdown(interviews, id="transcript-dropdown-selection", multi=True, placeholder="Select interview..."),
            html.Div([
                html.Button("Clear lasso selection", id="clear-selection", n_clicks=0)
            ],style={"padding": "3px", "textAlign": "right"})
        ], style={
            "backgroundColor": "AliceBlue",
            "padding": "1%",
            "boxSizing": "border-box",
            "marginBottom": "25px",
            "borderRadius": "5px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
        }),
        html.Div([
            html.Div(id="output-container", children="Click on a bar section to see the transcript", style={"padding": "10px"})
        ], style={
            "backgroundColor": "AliceBlue",
            "padding": "1%",
            "boxSizing": "border-box",
            "borderRadius": "5px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            "height": "60vh",
            "overflowY": "scroll"
        })
    ], style={
        "width": "29%",
        "display": "inline-block",
        "verticalAlign": "top",
        "marginLeft": "10px"
    })
])



@app.callback(
    [Output("output-container", "children", allow_duplicate=True),
     Output("graph-content", "figure", allow_duplicate=True)],
    [Input("graph-content", "clickData")],
    [State("graph-content", "figure")],
    prevent_initial_call=True
)
def display_click_data(clickData, figure):
    if clickData is None:
        return "Click on a bar to visualise the transcript"
    else:
        print(clickData)
        point_index = clickData["points"][0]["pointIndex"]
        curve_index = clickData["points"][0]["curveNumber"]

        print(clickData["points"][0]["customdata"][1])
        if len(figure["data"])==1:
            trans_section = vis_df.copy()
        else:
            if clickData["points"][0]["customdata"][1] == "Not shown":
                figure_shown_topics = [figure["data"][c+1]["customdata"][0][0] for c in range(len(figure["data"])-1)]
                print(figure_shown_topics)
                trans_section = vis_df[
                    ~vis_df['bertopic_topic_name'].isin(figure_shown_topics)
                ].reset_index(drop=True)
            else:
                trans_section = vis_df[
                    (vis_df["bertopic_topic_name"]==clickData["points"][0]["customdata"][0])
                ].reset_index(drop=True)
        trans_section_text = trans_section["text"][point_index]
        trans_section_topic = trans_section["bertopic_topic_name"][point_index]

        if trans_section["museum_sim_mpnet"][point_index] >= 0.6:
            museum_object_matching = "Suggested matching object:"
            museum_object = trans_section["museum_desc"][point_index] + " (" + trans_section["museum_id"][point_index] + ")."
        elif trans_section["museum_sim_mpnet"][point_index] >= 0.5:
            museum_object_matching = "Suggested matching object (uncertain):"
            museum_object = trans_section["museum_desc"][point_index] + " (" + trans_section["museum_id"][point_index] + ")."
        elif trans_section["museum_sim_mpnet"][point_index] >= 0.4:
            museum_object_matching = "Suggested matching object (poor):"
            museum_object = trans_section["museum_desc"][point_index] + " (" + trans_section["museum_id"][point_index] + ")."
        elif trans_section["museum_sim_mpnet"][point_index] >= 0.3:
            museum_object_matching = "Suggested matching object (very poor):"
            museum_object = trans_section["museum_desc"][point_index] + " (" + trans_section["museum_id"][point_index] + ")."
        else:
            museum_object_matching = "No matching object."
            museum_object = ""

        for c in range(len(figure["data"])):
            figure["data"][c]["marker"]["line"]["width"] = [0] * len(vis_df)
        for i, bar in enumerate(figure["data"][curve_index]["marker"]["line"]["width"]):
            # Set the border to visible only for the clicked bar
            if i == point_index:
                figure["data"][curve_index]["marker"]["line"]["width"][i] = 1
                figure["data"][curve_index]["marker"]["line"]["color"] = "black"
            else:
                figure["data"][curve_index]["marker"]["line"]["width"][i] = 0

        return html.Div([
            html.P([html.Strong("Topic: "), trans_section_topic]),
            html.P([html.Strong("Transcript:")]),
            html.P(trans_section_text),
            html.P([html.Strong(museum_object_matching)]),
            html.P(museum_object)
        ]), figure


@app.callback(
    [Output("output-container", "children", allow_duplicate=True),
     Output("graph-content", "figure", allow_duplicate=True)],
    Input("tabs", "value"),
    Input("topic-dropdown-selection", "value"),
    Input("transcript-dropdown-selection", "value"),
    Input("graph-content", "selectedData"),
    Input("clear-selection", "n_clicks")
)
def render_content(tab, disply_topic, display_transcripts, selected_data, clear_selection_n_clicks):

    global selected_indices
    if "clear-selection" == ctx.triggered_id:
        selected_indices = None

    vis_df_to_display = vis_df.copy()

    if disply_topic is None: disply_topic = []
    colorbrewer_set1 = ["#b3cde3", "#ff7f00", "#984ea3", "#4daf4a", "#ffff33", "#a65628", "#f781bf", "#e41a1c", "#999999"]
    cmap = {
        "Not shown": "#b3cde3",
        None: "grey"
    }
    tmap = {}
    tmap["Not shown"] = 0.5
    for i in range(len(disply_topic)):
        cmap[disply_topic[i]] = colorbrewer_set1[i]
        tmap[disply_topic[i]] = 1.0
    vis_df_to_display["vis_topic"] = "Not shown"
    vis_df_to_display["vis_topic"] = vis_df_to_display.apply(lambda x: x.bertopic_topic_name if x.bertopic_topic_name in disply_topic else "Not shown", axis=1)

    if display_transcripts is not None:
        if len(display_transcripts) > 0:
            vis_df_to_display = vis_df_to_display[vis_df_to_display["transcript"].isin(display_transcripts)]


    if selected_data is not None:
        if len(selected_data["points"]) > 0:
            selected_indices = [p["pointIndex"] for p in selected_data["points"]]
    if selected_indices is not None:
        vis_df_to_display = vis_df_to_display[vis_df_to_display.index.isin(selected_indices)]

    if tab == "tab-1-timelines":

        # Based on https://stackoverflow.com/questions/66078893/plotly-express-timeline-for-gantt-chart-with-integer-xaxis

        topic_bars = px.timeline(
            vis_df_to_display,
            x_start="start_time", x_end="end_time", y="transcript", color="vis_topic", color_discrete_sequence=colorbrewer_set1,
            hover_data={"start_time": ".0f", "end_time": ".0f", "bertopic_topic_name": True, "vis_topic": True, "segment_len":True},
            labels={"transcript":"Interview", "vis_topic": "Topic"},
            height=680)
        topic_bars.update_layout(
            plot_bgcolor="white",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )
        topic_bars.update_traces(
            marker=dict(line=dict(width=0)),
            hovertemplate="<br><b>Topic</b>: %{customdata[0]}<br> Starting at about %{x:.0f} min <extra></extra>"
        )
        topic_bars.update_yaxes(autorange="reversed")

        topic_bars.layout.xaxis.type = "linear"
        for i_figdata in range(len(topic_bars.data)):
            topic_bars.data[i_figdata].x = topic_bars.data[i_figdata]["customdata"][:, 2]
        f = topic_bars.full_figure_for_development(warn=False)

        return html.Div([
            html.P("Click on a bar to visualise the transcript")
        ]), topic_bars

    elif tab == "tab-2-scatterplot":

        if display_transcripts is None:
            if len(disply_topic) == 0:
                topic_scatter = px.scatter(
                    vis_df_to_display, x="UMAP1", y="UMAP2", color_discrete_sequence=colorbrewer_set1,
                    hover_data=["vis_topic", "bertopic_topic_name", "transcript", "start_time", "end_time"],
                    labels={"vis_topic": "Topic"},
                    height=680)
            else:
                topic_scatter = px.scatter(
                    vis_df_to_display, x="UMAP1", y="UMAP2", color="vis_topic", color_discrete_sequence=colorbrewer_set1,
                    hover_data=["vis_topic", "bertopic_topic_name", "transcript", "start_time", "end_time"],
                    labels={"vis_topic": "Topic"},
                    height=680)
                topic_scatter.for_each_trace(lambda t: t.update({"marker": {"opacity": [tmap[a] for a in t["customdata"][:, 0]]}}))
        elif len(display_transcripts) == 0:
            if len(disply_topic) == 0:
                topic_scatter = px.scatter(
                    vis_df_to_display, x="UMAP1", y="UMAP2", color_discrete_sequence=colorbrewer_set1,
                    hover_data=["vis_topic", "bertopic_topic_name", "transcript", "start_time", "end_time"],
                    labels={"vis_topic": "Topic"},
                    height=680)
            else:
                topic_scatter = px.scatter(
                    vis_df_to_display, x="UMAP1", y="UMAP2", color="vis_topic", color_discrete_sequence=colorbrewer_set1,
                    hover_data=["vis_topic", "bertopic_topic_name", "transcript", "start_time", "end_time"],
                    labels={"vis_topic": "Topic"},
                    height=680)
                topic_scatter.for_each_trace(lambda t: t.update({"marker": {"opacity": [tmap[a] for a in t["customdata"][:, 0]]}}))
        else:
            vis_df_to_display = vis_df_to_display[vis_df_to_display["transcript"].isin(display_transcripts)]
            if len(disply_topic) == 0:
                topic_scatter = px.scatter(
                    vis_df_to_display, x="UMAP1", y="UMAP2", color="vis_topic", color_discrete_sequence=colorbrewer_set1,
                    hover_data=["vis_topic", "bertopic_topic_name", "transcript", "start_time", "end_time"],
                    labels={"vis_topic": "Topic"},
                    height=680)
            else:
                topic_scatter = px.scatter(
                    vis_df_to_display, x="UMAP1", y="UMAP2", color="vis_topic", color_discrete_sequence=colorbrewer_set1,
                    hover_data=["vis_topic", "bertopic_topic_name", "transcript", "start_time", "end_time"],
                    labels={"vis_topic": "Topic"},
                    height=680)
                topic_scatter.for_each_trace(lambda t: t.update({"marker": {"opacity": [tmap[a] for a in t["customdata"][:, 0]]}}))

        topic_scatter.update_layout(
            plot_bgcolor="white",
            # showlegend=False
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )
        topic_scatter.update_traces(
            marker=dict(line=dict(width=0.3, color="DarkSlateGrey")),
            hovertemplate="<br><b>Topic</b>: %{customdata[1]}<br> %{customdata[2]} at about %{customdata[3]:.0f} min  <extra></extra>"
        )

        return html.Div([
            html.P("Click on a dot to visualise the transcript")
        ]), topic_scatter

if __name__ == "__main__":
    app.run_server(debug=True)
