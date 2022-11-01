import streamlit as st
import schemdraw
from schemdraw.flow import *


country_list = [
    ' India', 'England', 'South Africa', 'Pakistan', 'New Zealand', 'Australia', 'West Indies', 'Sri Lanka',
    'Bangladesh', 'Afghanistan', 'Zimbabwe', 'Ireland', 'United Arab Emirates', 'Namibia', 'Scotland', '  Nepal',
    'Netherlands', 'Oman', 'Papua New Guinea', 'Canada', 'Hong Kong', 'Jersey', 'Qatar', 'Uganda', 'Kuwait',
    'United States', 'Singapore', 'Malaysia', 'Italy', 'Kenya', 'Tanzania', 'Bahrain', 'Saudi Arabia', 'Bermuda',
    'Germany', 'Spain', 'Denmark', 'Guernsey', 'Isle of Man', 'Belgium', 'Cayman Islands', 'Austria', 'Nigeria',
    'Botswana', 'Vanuatu', 'Portugal', 'Romania', 'Norway', 'Finland', 'France', 'Argentina', 'Malawi', 'Sweden',
    'Ghana', 'Cook Islands', 'Czech Republic', 'Switzerland', 'Indonesia', 'Malta', 'Japan', 'Luxembourg',
    'Sierra Leone', 'Bhutan', 'Fiji', 'Cyprus', 'Bahamas', 'Hungary', 'Mozambique', 'Belize', 'Panama', 'Rwanda',
    'Serbia', 'Seychelles', 'Bulgaria', 'Maldives', 'Samoa', 'Gibraltar', 'Greece', 'Thailand', 'Eswatini', 'Turkey',
    'Lesotho', 'Estonia', 'Cameroon'
]

st. set_page_config(layout="wide")
st.title("Stake Management")

with st.expander("Select Teams To Play", expanded=False):
    team_1_col, team_2_col = st.columns(2)

    team_1 = team_1_col.selectbox('Select Team 1', country_list, index=0)
    team_2 = team_2_col.selectbox('Select Team 2', country_list, index=1)

team_col, lag_col, kha_col, amount_col = st.columns(4)

team_tuple = (team_1, team_2)
team_name = team_col.radio("Team Name", team_tuple)

lag = lag_col.number_input('Lagaaya', min_value=0, max_value=98, value=7, step=1)
kha = kha_col.number_input('Khaaya', min_value=1, max_value=99, value=8, step=1)
amount = amount_col.number_input('Amount', min_value=5000, max_value=1000000000, value=10000, step=5000)


def get_value(amount, stake, action_type, team_name="Team"):
    if amount <= 0:
        raise ValueError("Cannot stake on this amount")

    if action_type == "L":
        profit = int(((round((stake/100)+1, 2))*amount) - amount)
        # print(f"If {team_name} WIN, +{profit}")
        # print(f"If {team_name} DO NOT WIN, -{amount}")
        return {"WIN": profit, "DO NOT WIN": -amount}
    elif action_type == "K":
        # print(f"If {team_name} LOOSE, +{amount}")
        loss = int(amount * stake / 100)
        # print(f"If {team_name} DO NOT LOOSE, -{loss}")
        return {"LOOSE": amount, "DO NOT LOOSE": -loss}
    else:
        raise ValueError("Invalid action type. Action type can be Back/Lay only")


lag_win_col, lag_loss_col, kha_loss_col, kha_win_col = st.columns(4)

# dict_ = get_value(amount, int(lag), "L", team_name)
# lag_win_col.metric(f"If {team_name} WIN", dict_["WIN"], "+")
# lag_loss_col.metric(f"If {team_name} DO NOT WIN", dict_["DO NOT WIN"], "-")
#
# dict_ = get_value(amount, int(kha), "K", team_name)
# kha_loss_col.metric(f"If {team_name} LOOSE", dict_["LOOSE"], "+")
# kha_win_col.metric(f"If {team_name} DO NOT LOOSE", dict_["DO NOT LOOSE"], "-")

team_1_result = get_value(amount, lag, "L", team_tuple[0])
team_2_result = get_value(amount, kha, "K", team_tuple[1])

with schemdraw.Drawing() as d:
    d += Start().label(str(amount))
    d += Arrow().down(d.unit / 2)

    d += (decision_user := Decision(w=5, h=5, W="Lagaaya", E="Khaaya").label("Lagaaya / Khaaya"))

    # If True
    d += Arrow().left(d.unit * 2).at(decision_user.W)
    d += (true := Box(w=5).label(str(lag) + " L"))

    # Add a downward arrow from the South of false box
    d += Arrow().down(d.unit).at(true.S)
    d += (decision_result_1 := Decision(w=5, h=5, W="Win", E="Loss").label("Match Result"))

    # If True
    d += Arrow().left(d.unit).at(decision_result_1.W)
    d += (true := Box(w=5).label(str(team_1_result["WIN"])))

    # If True
    d += Arrow().right(d.unit).at(decision_result_1.E)
    d += (true := Box(w=5).label(str(team_1_result["DO NOT WIN"])))

    # If False. Start the arrow from East of decision box
    d += Arrow().right(d.unit * 2).at(decision_user.E)
    d += (false := Box(w=5).label(str(kha) + " K"))

    # Add a downward arrow from the South of false box
    d += Arrow().down(d.unit).at(false.S)

    d += (decision_result_2 := Decision(w=5, h=5, W="Win", E="Loss").label("Match Result"))

    # If True
    d += Arrow().left(d.unit).at(decision_result_2.W)
    d += (true := Box(w=5).label(str(team_2_result["DO NOT LOOSE"])))

    # If True
    d += Arrow().right(d.unit).at(decision_result_2.E)
    d += (true := Box(w=5).label(str(team_2_result["LOOSE"])))

    d.save("flowchart.svg", dpi=50)


st.image("flowchart.svg")
