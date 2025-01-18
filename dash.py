import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos del archivo CSV
@st.cache
def load_data():
    file_path = '2025_LoL_esports_match_data_from_OraclesElixir.csv'
    return pd.read_csv(file_path)

data = load_data()

# Título principal
st.title("Esports Dashboard - League of Legends")

# Filtros
st.sidebar.header("Filtros")

# Filtrar filas donde la columna 'm' es 'team' para obtener los equipos
team_rows = data[data['position'] == 'team']  # Cambia 'm' por el nombre real de la columna si es diferente
teams = team_rows['teamname'].unique()  # Cambia 'p teamname' si es diferente

# Agregar opción 'Todos' al principio de la lista
selected_team = st.sidebar.selectbox("Selecciona un equipo", options=["Todos"] + list(teams))

# Filtro por jugador
players = data['player'].unique() if 'player' in data.columns else []  # Asegurarse de que 'player' exista
selected_player = st.sidebar.selectbox("Selecciona un jugador", options=["Todos"] + list(players))

# Filtro por estadísticas de equipo
team_filters = ["firstblood", "teamkills", "firstdragon", "dragons", "firsttower", "result"]
selected_team_stat = st.sidebar.selectbox("Selecciona una estadística de equipo", options=team_filters)

# Filtro por estadísticas de jugador
player_filters = ["champion", "kills", "assists", "deaths", "position"]
selected_player_stat = st.sidebar.selectbox("Selecciona una estadística de jugador", options=player_filters)

# Aplicar filtros
filtered_data = data.copy()

if selected_team != "Todos":
    filtered_data = filtered_data[filtered_data['teamname'] == selected_team]

if selected_player != "Todos" and 'player' in data.columns:
    filtered_data = filtered_data[filtered_data['player'] == selected_player]

# Mostrar estadísticas
st.header("Resultados Filtrados")

# Estadísticas de equipo
st.subheader("Estadísticas de Equipo")
if selected_team != "Todos":
    team_stats = filtered_data.groupby('p teamname')[selected_team_stat].mean()
    st.write(team_stats)

# Estadísticas de jugador
st.subheader("Estadísticas de Jugador")
if selected_player != "Todos" and 'player' in data.columns:
    player_stats = filtered_data.groupby('player')[selected_player_stat].mean()
    st.write(player_stats)

# Visualizaciones
st.header("Gráficos")

# Gráfico de estadísticas de equipo
if selected_team != "Todos":
    fig_team = px.bar(
        filtered_data.groupby('p teamname')[selected_team_stat].mean().reset_index(),
        x='p teamname', y=selected_team_stat,
        title=f"{selected_team_stat} por equipo"
    )
    st.plotly_chart(fig_team)

# Gráfico de estadísticas de jugador
if selected_player != "Todos" and 'player' in data.columns:
    fig_player = px.bar(
        filtered_data.groupby('player')[selected_player_stat].mean().reset_index(),
        x='player', y=selected_player_stat,
        title=f"{selected_player_stat} por jugador"
    )
    st.plotly_chart(fig_player)
