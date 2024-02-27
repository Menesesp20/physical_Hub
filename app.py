# Libraries for data handling and manipulation
import streamlit as st
import pandas as pd
import numpy as np

# Libraries for visualizations
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

from highlight_text import  ax_text, fig_text

# Libraries for signal processing
from scipy.signal import butter, lfilter

# Libraries for spatial calculations
from scipy.spatial import ConvexHull, distance

import matplotlib.image as mpimg

import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap

from soccerplots.utils import add_image

# Libraries for system-related operations
import os

from matplotlib.font_manager import FontProperties

#font_path = 'C:/Users/menes/Documents/Data Hub/Fonts/Gagalin-Regular.otf'
#font_manager.fontManager.addfont(font_path)
#prop = font_manger.FontProperties(fname=font_path)
#plt.rcParams['font.sans-serif'] = prop.get_name()

# FONT FAMILY
# Set the Lato font file path
lato_path = 'C:/Users/menes/Documents/Data Hub/Fonts/Lato-Black.ttf'

# Register the Lato font with Matplotlib
custom_font = FontProperties(fname=lato_path)

st.set_option('deprecation.showPyplotGlobalUse', False)

# USE THIS TO GET THE FONT FAMILY: fontproperties=custom_font

st.title('GPS Análise Jogo')

# GET DATA FROM THE CURRENT MATCH
# Upload CSV file for data_intervalo
uploaded_file_intervalo = st.file_uploader("Choose a CSV file for interval data", type="csv")
if uploaded_file_intervalo is not None:
    data_intervalo = pd.read_csv(uploaded_file_intervalo, skiprows=14, delimiter=";", decimal=",")
    data_intervalo['Alta Intensidade'] = data_intervalo['V6 Dist'] + data_intervalo['V8 Dist'] + data_intervalo['V8 Dist']
    data_intervalo['Sprint'] = data_intervalo['V8 Dist'] + data_intervalo['V8 Dist']
    data_intervalo = data_intervalo.rename({'Acc2 To3 Eff' : 'Aceleração',
                                            'Dec2 To3 Eff' : 'Desaceleração',
                                            'Interval,Time,First Name' : 'First Name'}, axis=1)
    # and a list of names
    names = ['Aylon', 'Bahia', 'Castilho', 'David', 'Facundo', 'Jorge',
            'Matheus', 'Pulga', 'Rai', 'Richardson', 'Fernando']

    # Filter the DataFrame
    data_intervalo = data_intervalo[data_intervalo['First Name'].isin(names)]

# Upload CSV file for data_maximo
uploaded_file_maximo = st.file_uploader("Choose a CSV file for maximum data", type="csv")
if uploaded_file_maximo is not None:
    # DATA WITH THE MAX VALUE FOR EACH PLAYER DURING THE SEASON
    data_maximo = pd.read_csv(uploaded_file_maximo, skiprows=14, delimiter=";", decimal=",")
    data_maximo['Alta Intensidade'] = data_maximo['V6 Dist'] + data_maximo['V8 Dist'] + data_maximo['V8 Dist']
    data_maximo['Sprint'] = data_maximo['V8 Dist'] + data_maximo['V8 Dist']
    data_maximo = data_maximo.rename({'Acc2 To3 Eff' : 'Aceleração',
                                            'Dec2 To3 Eff' : 'Desaceleração'}, axis=1)

if (uploaded_file_maximo is not None) & (uploaded_file_intervalo is not None):
    # MERGE THE TWO DATAFRAMES INTO ONE UNIQUE DATAFRAME
    # Merging dataframes to calculate percentages
    merged_data = pd.merge(data_intervalo, data_maximo, on="First Name", suffixes=('_intervalo', '_maximo'))

    # Selecting columns to calculate percentages for, excluding non-numeric and non-comparable columns
    columns = ["Total Distance", "Max Velocity", "Alta Intensidade", "Sprint", "Aceleração", "Desaceleração"]

    cols_intervalo = [f'{col}_intervalo' for col in columns]
    cols_maximo = [f'{col}_maximo' for col in columns]
    columns = cols_intervalo + cols_maximo
    columns.insert(0, 'First Name')
    merged_data = merged_data[columns]

    # Creating a new column "Total Distance" by combining "Total Distance_intervalo" and "Total Distance_maximo"
    merged_data["Total Distance"] = merged_data["Total Distance_intervalo"].astype(str) + " / " + merged_data["Total Distance_maximo"].astype(str)

    # Creating a new column "Max Velocity" by combining "Max Velocity_intervalo" and "Max Velocity_maximo"
    merged_data["Max Velocity"] = merged_data["Max Velocity_intervalo"].astype(str) + " / " + merged_data["Max Velocity_maximo"].astype(str)

    # Creating a new column "Alta Intensidade" by combining "Alta Intensidade_intervalo" and "Alta Intensidade_maximo"
    merged_data["Alta Intensidade"] = merged_data["Alta Intensidade_intervalo"].astype(str) + " / " + merged_data["Alta Intensidade_maximo"].astype(str)

    # Creating a new column "Sprint" by combining "Sprint_intervalo" and "Sprint_maximo"
    merged_data["Sprint"] = merged_data["Sprint_intervalo"].astype(str) + " / " + merged_data["Sprint_maximo"].astype(str)

    # Creating a new column "Aceleração" by combining "Aceleração_intervalo" and "Aceleração_maximo"
    merged_data["Aceleração"] = merged_data["Aceleração_intervalo"].astype(str) + " / " + merged_data["Aceleração_maximo"].astype(str)

    # Creating a new column "Desaceleração" by combining "Desaceleração_intervalo" and "Desaceleração_maximo"
    merged_data["Desaceleração"] = merged_data["Desaceleração_intervalo"].astype(str) + " / " + merged_data["Desaceleração_maximo"].astype(str)

    # Dropping the original columns
    merged_data = merged_data.drop(columns=["Total Distance_intervalo", "Total Distance_maximo", 
                            'Max Velocity_intervalo', 'Max Velocity_maximo',
                            "Alta Intensidade_intervalo", "Alta Intensidade_maximo",
                            "Sprint_intervalo", "Sprint_maximo",
                            "Aceleração_intervalo", "Aceleração_maximo",
                            "Desaceleração_intervalo", "Desaceleração_maximo"], axis=1)

    # DATAFRAME WITH THE PERCENTAGE VALUES
    # Merging dataframes to calculate percentages
    merged_data_Percentage = pd.merge(data_intervalo, data_maximo, on="First Name", suffixes=('_intervalo', '_maximo'))

    # Selecting columns to calculate percentages for, excluding non-numeric and non-comparable columns
    columns_to_calculate = ["Total Distance", "Max Velocity", "Alta Intensidade", "Sprint", "Aceleração", "Desaceleração"]

    # Calculating percentages
    for col in columns_to_calculate:
        merged_data_Percentage[f'{col} %'] = round((merged_data_Percentage[f'{col}_intervalo'] / merged_data_Percentage[f'{col}_maximo']) * 100, 2)

    # Selecting columns for final output (percentage columns + First Name)
    percentage_columns = [f'{col} %' for col in columns_to_calculate]
    output_columns = ['First Name'] + percentage_columns
    result_Percentage = merged_data_Percentage[output_columns]

    # GET THE NAME OF THE PLAYERS TO ANALYZE

    # Allow users to upload multiple CSV files
    uploaded_files = st.file_uploader("Choose player GPS data files", accept_multiple_files=True, type='csv')
    all_dfs = []  # To store all player DataFrames

    if uploaded_files is not None and len(uploaded_files) > 0:
        player_names = [os.path.splitext(os.path.basename(file.name))[0] for file in uploaded_files]
        player_names = [item.split("for ")[1].split(' ')[0] for item in player_names]
        for uploaded_file in uploaded_files:
            # Assuming you want to extract player names from the file names
            player_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]
            player_names.append(player_name.split("for ")[1].split(' ')[0])
            print('uploaded_file: ', uploaded_file)
            # Read the CSV file directly from the uploaded file object
            df = pd.read_csv(uploaded_file, skiprows=8, delimiter=";", decimal=",")
            # Add a column for player name
            df['Player'] = player_name.split("for ")[1].split(' ')[0]
            all_dfs.append(df)

        # Concatenate all DataFrames into a single DataFrame
        combined_df = pd.concat(all_dfs, ignore_index=True)

with st.form("select-buttons"):     
    # Filtrando os jogadores que serão analisados
    unique_players = ['Aylon', 'Bahia', 'Castilho', 'David', 'Facundo', 'Jorge',
                      'Matheus', 'Pulga', 'Rai', 'Richardson', 'Fernando']
    
    # SET THE HOUR THE GAME STARTED AND ENDED
    # Definindo os tempos de início e fim do jogo para análise
    game_start = st.sidebar.text_input('Enter the game start time (DD-MM-DD YYYY:MM:SS):', '16:41:00 17-02-2024')
    game_end = st.sidebar.text_input('Enter the game end time (DD-MM-DD YYYY HH:MM:SS):', '17:31:02 17-02-2024')

    # Convert game_start and game_end to datetime
    game_start = pd.to_datetime('17-02-2024 16:41:00')
    game_end = pd.to_datetime('17-02-2024 17:31:02')

    # Definindo as coordenadas dos pontos de referência do estádio
    reference_points = {
        'A': (-3.806759,-38.522709),
        'B': (-3.807700,-38.522789),
        'C': (-3.807753,-38.522184),
        'D': (-3.806811,-38.522105)
    }

    print("Configurações definidas!")

    # FUNCTIONS TO HANDLE THE GPS COORDINATES FOR A CARTESIAN PLAN (FOOTBALL PITCH)
    # Função para o filtro Butterworth passa-baixa
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = lfilter(b, a, data)
        return y

    def convert_to_cartesian(lat, long):
        def map_from_to(x, a, b, c, d):
            y = (x - a) / (b - a) * (d - c) + c
            return y
        x = map_from_to(long, reference_points['A'][1], reference_points['C'][1], 0, 68)
        y = map_from_to(lat, reference_points['A'][0], reference_points['B'][0], 0, 105)
        return x, y

    cutoff_frequency = 2.0
    sampling_frequency = 10
    order = 3

    # Assuming 'players_to_analyze' is a list of player names you're interested in
    #filtered_files = [file for file in uploaded_files if os.path.splitext(os.path.basename(file.name))[0] in players_to_analyze]
    #print('files list: ', filtered_files)
    pitch_length = 105
    pitch_width = 68

    btn1 = st.form_submit_button(label='Mapas de calor')

    if btn1:
        def players_HeatMap(pitch_length, pitch_width):
            # Assumindo que você deseja analisar apenas o primeiro tempo.
            for half, start_time, end_time in [('Fisiologia', game_start, game_end)]:
                fig, axes = plt.subplots((len(unique_players) + 3) // 4, 4, figsize=(20, 20), dpi=300)

                for ax, player_name in zip(axes.flatten(), unique_players):
                    try:
                        # Adjusting pandas read_csv to handle potential issues
                        data = combined_df[combined_df['Player'] == player_name]
                        print(f'{player_name} data: ', len(data))
                        data['Y'], data['X'] = zip(*data.apply(lambda row: convert_to_cartesian(row['Latitude'], row['Longitude']), axis=1))
                        if not isinstance(data['Timestamp'].iloc[0], pd.Timestamp):
                            data['Timestamp'] = pd.to_datetime(data['Timestamp'])

                        half_data = data[(data['Timestamp'] >= start_time) & (data['Timestamp'] <= end_time)]

                        # Plotagem
                        pitch = Pitch(pitch_type='custom', line_color='black', pitch_color='white', stripe=False,
                                        pitch_length=pitch_length, pitch_width=pitch_width)
                        
                        pitch.draw(ax=ax)

                        #Params for the text inside the <> this is a function to highlight text
                        highlight_textprops_40_60 =\
                            [{"color": '#19bb16',"fontweight": 'bold'}]
                        
                        highlight_textprops_61_80 =\
                            [{"color": '#f3e015',"fontweight": 'bold'}]
                        
                        highlight_textprops_81_100 =\
                            [{"color": '#e01818',"fontweight": 'bold'}]

                        result_Percentage_Player = result_Percentage[(result_Percentage['First Name'] == player_name)]
                        result_Player = data_intervalo[(data_intervalo['First Name'] == player_name)]

                        total_Distance_Percentage = round(float(result_Percentage_Player['Total Distance %'].values[0]), 2)
                        total_Distance = round(float(result_Player['Total Distance'].values[0]), 2)

                        if (total_Distance_Percentage > 40) and (total_Distance_Percentage <= 60):
                            highlight_textprops_Choice = highlight_textprops_40_60

                        elif (total_Distance_Percentage > 60) and total_Distance_Percentage <= 80:
                            highlight_textprops_Choice = highlight_textprops_61_80

                        elif total_Distance_Percentage > 80:
                            highlight_textprops_Choice = highlight_textprops_81_100

                        ax_text(s = f'DT: {total_Distance} | <{(total_Distance_Percentage)}> %',
                                highlight_textprops = highlight_textprops_Choice,
                                x = 25, y = 95, color='black', ha='center', fontproperties=custom_font,
                                fontsize=12, ax=ax);

                        ############################################################################################################################################

                        max_velocity_Percentage = round(float(result_Percentage_Player['Max Velocity %'].values[0]), 2)
                        max_velocity = round(float(result_Player['Max Velocity'].values[0]), 2)

                        if (max_velocity_Percentage > 40) & (max_velocity_Percentage <= 60):
                            highlight_textprops_Choice = highlight_textprops_40_60

                        elif (max_velocity_Percentage > 60) & (max_velocity_Percentage <= 80):
                            highlight_textprops_Choice = highlight_textprops_61_80

                        elif max_velocity_Percentage > 80:
                            highlight_textprops_Choice = highlight_textprops_81_100

                        ax_text(s = f'VEL: {max_velocity} | <{max_velocity_Percentage}> %',
                                highlight_textprops = highlight_textprops_Choice,
                                x = 25, y = 89, color='black', ha='center', fontproperties=custom_font,
                                fontsize=12, ax=ax);

                        ############################################################################################################################################

                        alta_Intensidade_Percentage = round(float(result_Percentage_Player['Alta Intensidade %'].values[0]), 2)
                        alta_Intensidade = round(float(result_Player['Alta Intensidade'].values[0]), 2)

                        if (alta_Intensidade_Percentage > 40) & (alta_Intensidade_Percentage <= 60):
                            highlight_textprops_Choice = highlight_textprops_40_60

                        elif (alta_Intensidade_Percentage > 60) & (alta_Intensidade_Percentage <= 80):
                            highlight_textprops_Choice = highlight_textprops_61_80

                        elif alta_Intensidade_Percentage > 80:
                            highlight_textprops_Choice = highlight_textprops_81_100

                        ax_text(s = f'DAI: {alta_Intensidade} | <{alta_Intensidade_Percentage}> %',
                                highlight_textprops = highlight_textprops_Choice,
                                x = 25, y = 83, color='black', ha='center', fontproperties=custom_font,
                                fontsize=12, ax=ax);
                        ############################################################################################################################################

                        sprint_Percentage = round(float(result_Percentage_Player['Sprint %'].values[0]), 2)
                        sprint = round(float(result_Player['Sprint'].values[0]), 2)

                        if (sprint_Percentage > 40) & (sprint_Percentage <= 60):
                            highlight_textprops_Choice = highlight_textprops_40_60

                        elif (sprint_Percentage > 60) & (sprint_Percentage <= 80):
                            highlight_textprops_Choice = highlight_textprops_61_80

                        elif sprint_Percentage > 80:
                            highlight_textprops_Choice = highlight_textprops_81_100

                        ax_text(s = f'DS: {sprint} <{sprint_Percentage}> %',
                                highlight_textprops = highlight_textprops_Choice,
                                x = 95, y = 95, color='black', ha='center', fontproperties=custom_font,
                                fontsize=12, ax=ax);
                        ############################################################################################################################################

                        aceleracao_Percentage = round(float(result_Percentage_Player['Aceleração %'].values[0]), 2)
                        aceleracao = round(float(result_Player['Aceleração'].values[0]), 2)

                        if (aceleracao_Percentage > 40) & (aceleracao_Percentage <= 60):
                            highlight_textprops_Choice = highlight_textprops_40_60

                        elif (aceleracao_Percentage > 60) & (aceleracao_Percentage <= 80):
                            highlight_textprops_Choice = highlight_textprops_61_80

                        elif aceleracao_Percentage > 80:
                            highlight_textprops_Choice = highlight_textprops_81_100

                        ax_text(s = f'ACC: {aceleracao} <{aceleracao_Percentage}> %',
                                highlight_textprops = highlight_textprops_Choice,
                                x = 105, y = 89, color='black', ha='center', fontproperties=custom_font,
                                fontsize=12, ax=ax);

                        ############################################################################################################################################

                        desaceleracao_Percentage = round(float(result_Percentage_Player['Desaceleração %'].values[0]), 2)
                        desaceleracao = round(float(result_Player['Desaceleração'].values[0]), 2)

                        if (desaceleracao_Percentage > 40) & (desaceleracao_Percentage <= 60):
                            highlight_textprops_Choice = highlight_textprops_40_60

                        elif (desaceleracao_Percentage > 60) & (desaceleracao_Percentage <= 80):
                            highlight_textprops_Choice = highlight_textprops_61_80

                        elif desaceleracao_Percentage > 80:
                            highlight_textprops_Choice = highlight_textprops_81_100

                        ax_text(s = f'DCC: {desaceleracao} <{desaceleracao_Percentage}> %',
                                highlight_textprops = highlight_textprops_Choice,
                                x = 105, y = 83, color='black', ha='center', fontproperties=custom_font,
                                fontsize=12, ax=ax);
                        ############################################################################################################################################

                        # GRADIENT COLOR
                        pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                                            ['#E8E8E8', '#3d0000', '#ff0000'], N=10)

                        # PATH EFFECTS OF THE HEAT MAP
                        path_eff = [path_effects.Stroke(linewidth=3, foreground='#181818'),
                                    path_effects.Normal()]

                        # BINS FOR THE HEAT MAP
                        bs1 = pitch.bin_statistic_positional(half_data['X'], half_data['Y'],  statistic='count', positional='full', normalize=True)

                        # HEAT MAP POSITIONAL PITCH (WAY OF PLAY FOOTBALL)
                        pitch.heatmap_positional(bs1, edgecolors='#181818', ax=ax, cmap=pearl_earring_cmap, alpha=0.8)

                        # LABEL HEATMAP
                        pitch.label_heatmap(bs1, color='#E8E8E8', fontsize=18,
                                                    ax=ax, ha='center', va='center',
                                                    str_format='{:.0%}', fontproperties=custom_font, path_effects=path_eff, zorder=5)

                        ax.set_title(player_name, fontproperties=custom_font, y=1.7, size=35)

                        #add_image(image=f'C:/Users/menes/Documents/Data Hub/Images/Players/Serie_B/{player_name}.png', fig=fig, left=0.11, bottom=0.589, width=0.05, height=0.05)

                    except Exception as e:
                        print(f"Erro ao processar o arquivo {uploaded_file}. Erro: {e}")

                # Removendo os gráficos vazios
                for i in range(len(unique_players), len(axes.flatten())):
                    axes.flatten()[i].axis('off')

                plt.suptitle(f'Mapa de Calor dos jogadores - {half}', fontproperties=custom_font, fontsize=40)
                plt.tight_layout(rect=[0, 0.03, 1, 0.95])
                return plt.show()
            
        heatMap_Viz = players_HeatMap(pitch_length, pitch_width)

        st.pyplot(heatMap_Viz)






