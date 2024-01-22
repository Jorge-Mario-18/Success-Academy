import streamlit as st
import pandas as pd
import plotly.express as px

st.image("SA.png")

st.title("Soccer Fall Season 2023")
st.divider()
success_manhattan = pd.read_csv('success_manhattan.csv')
success_harlem = pd.read_csv('success_harlem.csv')
success_joint = pd.read_csv('success_girls.csv')

option = st.selectbox(
    'Select the Team',
    ('All', 'SA Harlem', 'SA Girls', 'SA Manhattan'))

if option == 'SA Girls':
    value_counts_g = success_joint['Game Result'].value_counts
    fig = px.bar(success_joint, x = value_counts_g().index, y = value_counts_g().values, 
                 title="Results of SA Girls Games", labels={'x': '(Wins, Losses, or Ties)', 'y':'Count of Games'})
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    st.write(fig)

if option == 'SA Harlem':
    value_counts_h = success_harlem['Game Result'].value_counts
    fig = px.bar(success_harlem, x = value_counts_h().index, y = value_counts_h().values, 
                 title="Results of SA Harlem Games", labels={'x': '(Wins, Losses, or Ties)', 'y':'Count of Games'})
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    st.write(fig)

if option == 'SA Manhattan':
    value_counts_m = success_manhattan['Game Result'].value_counts
    fig = px.bar(success_manhattan, x = value_counts_m().index, y = value_counts_m().values, 
                 title="Results of SA Manhattan Games", labels={'x': '(Wins, Losses, or Ties)', 'y':'Count of Games'})
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    st.write(fig)

if option == 'All':
    value_counts_g = success_joint['Game Result'].value_counts()
    value_counts_h = success_harlem['Game Result'].value_counts()
    value_counts_m = success_manhattan['Game Result'].value_counts()
    team1_df = pd.DataFrame([value_counts_g], columns=['W', 'L', 'T'])
    team2_df = pd.DataFrame([value_counts_h], columns=['W', 'L', 'T'])
    team3_df = pd.DataFrame([value_counts_m], columns=['W', 'L', 'T'])
    team1_df['Team'] = 'Girls'
    team2_df['Team'] = 'Harlem'
    team3_df['Team'] = 'Manhattan'
    team1_df['Goals Scored'] = sum(success_joint['Girls Score'])
    team2_df['Goals Scored'] = sum(success_harlem['Harlem Score'])
    team3_df['Goals Scored'] = sum(success_manhattan['Manhattan Score'])
    team1_df['Goals Conceded'] = sum(success_joint['Opposition Score'])
    team2_df['Goals Conceded'] = sum(success_harlem['Opposition Score'])
    team3_df['Goals Conceded'] = sum(success_manhattan['Opposition Score'])
    result_df = pd.concat([team1_df, team2_df, team3_df], ignore_index=True)
    result_df = result_df[['Team', 'W', 'L', 'T', 'Goals Scored', 'Goals Conceded']]
    fig = px.bar(result_df, x='Team', y=['W', 'L', 'T'], custom_data=['Goals Scored', 'Goals Conceded'], barmode='group',
                labels={'value': 'Count', 'variable': 'Result'},
                title='Team Results')
    fig.update_traces(
        hovertemplate="<br>".join([
            "Goals Scored: %{customdata[0]}",
            "Goals Conceded: %{customdata[1]}"
        ])
    )
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    st.write(fig)

def load_table(conf, a, b):
    x=conf['Date']
    y=b
    fig = px.line(conf, 
             x=x, 
             y=y, 
             custom_data=['Opposition Score', 'Game Result', 'Opponent']
    )

    fig.update_traces(
    hovertemplate="<br>".join([
        "Opponent: %{customdata[2]}",
        "Game Result: %{customdata[1]}",
        "Success Academy Score: %{y}",
        "Opposition Score: %{customdata[0]}"
    ])
)
    fig.update_traces(name=a, showlegend = True)

    fig.add_scatter(x=conf['Date'], 
                y=conf['Opposition Score'], 
                mode='lines',
                hovertemplate=None,
                name='Opponent')


    fig.update_layout(xaxis_title="Date of Game",
                  yaxis_title="Goals Scored", 
                  hovermode="x")
    fig.update_traces(mode="markers+lines")
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    st.write(fig)



(
    tab1,
    tab2,
    tab3

) = st.tabs(
    [
        "Success Academy Manhattan",
        "Success Academy Harlem",
        "Success Academy Girls"
    ]
)


with tab1:
    st.header("Success Acdemy Manhattan")
    load_table(success_manhattan, "Manhattan", success_manhattan['Manhattan Score'])

with tab2:
    st.header("Success Acdemy Harlem")
    load_table(success_harlem, "Harlem", success_harlem['Harlem Score'])

with tab3:
    st.header("Success Acdemy Girls")
    load_table(success_joint, "Girls", success_joint['Girls Score'])

st.divider()

def load_pie(conf, a, b):
    fig = px.pie(conf, values=a, names="Opponent", title="Share of total Goals " + b)
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    st.write(fig)


on = st.toggle('Goals Scored or Conceded')

if on:
    b = 'Concedeed'
    team = st.radio(
        "Select the team:",
        ("SA Manhattan", "SA Harlem", "SA Girls"),
        index=0,
        horizontal=True,
    )

    if team == "SA Manhattan":
        load_pie(success_manhattan, "Opposition Score", b)

    if team == "SA Harlem":
        load_pie(success_harlem, "Opposition Score", b)

    if team == "SA Girls":
        load_pie(success_joint, "Opposition Score", b)
else:
    b = 'Scored'
    team = st.radio(
        "Select the team:",
        ("SA Manhattan", "SA Harlem", "SA Girls"),
        index=0,
        horizontal=True,
    )

    if team == "SA Manhattan":
        load_pie(success_manhattan, "Manhattan Score", b)

    if team == "SA Harlem":
        load_pie(success_harlem, "Harlem Score", b)

    if team == "SA Girls":
        load_pie(success_joint, "Girls Score", b)



