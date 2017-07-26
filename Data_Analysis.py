
# coding: utf-8

# In[4]:

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

#Our first step will be to have an additional column,telling whether the match is a pre-qualifier,final,qualifier-1,qualifier-2,eliminator or final
matches = pd.read_csv('Desktop/ipl/matches.csv')
matches["type"] = "pre-qualifier" #making every value as pre-qualifier
for year in range(2008, 2017):
   final_match_index = matches[matches['season']==year][-1:].index.values[0] 
   matches = matches.set_value(final_match_index, "type", "final")
   matches = matches.set_value(final_match_index-1, "type", "qualifier-2")
   matches = matches.set_value(final_match_index-2, "type", "eliminator")
   matches = matches.set_value(final_match_index-3, "type", "qualifier-1")

matches.groupby(["type"])["id"].count()
matches.head(60)


# In[5]:

deliveries = pd.read_csv('Desktop/ipl/deliveries.csv')
deliveries.head(2)


# In[6]:

#adding team score and team extra columns for each match, each inning.
team_score = deliveries.groupby(['match_id', 'inning'])['total_runs'].sum().unstack().reset_index()
team_score.columns = ['match_id', 'Team1_score', 'Team2_score', 'Team1_superover_score', 'Team2_superover_score']
matches_agg = pd.merge(matches, team_score, left_on = 'id', right_on = 'match_id', how = 'outer')
team_extras = deliveries.groupby(['match_id', 'inning'])['extra_runs'].sum().unstack().reset_index()
team_extras.columns = ['match_id', 'Team1_extras', 'Team2_extras', 'Team1_superover_extras', 'Team2_superover_extras']
matches_agg = pd.merge(matches_agg, team_extras, on = 'match_id', how = 'outer')
#Reorder the columns to make the data more readable
cols = ['match_id', 'winner','season','city','date','team1','team2', 'toss_winner', 'toss_decision', 'result', 'dl_applied', 'Team1_score','Team2_score', 'win_by_runs', 'win_by_wickets', 'Team1_extras', 'Team2_extras', 'Team1_superover_score', 'Team2_superover_score', 'Team1_superover_extras', 'Team2_superover_extras', 'player_of_match', 'type', 'venue', 'umpire1', 'umpire2', 'umpire3']
matches_agg = matches_agg[cols]

RCB_winner = matches_agg[matches_agg.winner == "Royal Challengers Bangalore"]
RCB_winner.groupby('city')
#matches_agg.head(6)
RCB_winner.head(5)


# In[7]:

#batsman aggregates

batsman_grp = deliveries.groupby(["match_id", "inning", "batting_team", "batsman"])
batsmen = batsman_grp["batsman_runs"].sum().reset_index()

# Ignore the wide balls.
balls_faced = deliveries[deliveries["wide_runs"] == 0]
balls_faced = balls_faced.groupby(["match_id", "inning", "batsman"])["batsman_runs"].count().reset_index()
balls_faced.columns = ["match_id", "inning", "batsman", "balls_faced"]
batsmen = batsmen.merge(balls_faced, left_on=["match_id", "inning", "batsman"], 
                        right_on=["match_id", "inning", "batsman"], how="left")

fours = deliveries[ deliveries["batsman_runs"] == 4]
sixes = deliveries[ deliveries["batsman_runs"] == 6]

fours_per_batsman = fours.groupby(["match_id", "inning", "batsman"])["batsman_runs"].count().reset_index()
sixes_per_batsman = sixes.groupby(["match_id", "inning", "batsman"])["batsman_runs"].count().reset_index()

fours_per_batsman.columns = ["match_id", "inning", "batsman", "4s"]
sixes_per_batsman.columns = ["match_id", "inning", "batsman", "6s"]

batsmen = batsmen.merge(fours_per_batsman, left_on=["match_id", "inning", "batsman"], 
                        right_on=["match_id", "inning", "batsman"], how="left")
batsmen = batsmen.merge(sixes_per_batsman, left_on=["match_id", "inning", "batsman"], 
                        right_on=["match_id", "inning", "batsman"], how="left")
batsmen['SR'] = np.round(batsmen['batsman_runs'] / batsmen['balls_faced'] * 100, 2) #strike rate

for col in ["batsman_runs", "4s", "6s", "balls_faced", "SR"]:
    batsmen[col] = batsmen[col].fillna(0)

dismissals = deliveries[ pd.notnull(deliveries["player_dismissed"])]
dismissals = dismissals[["match_id", "inning", "player_dismissed", "dismissal_kind", "fielder"]]
dismissals.rename(columns={"player_dismissed": "batsman"}, inplace=True)
batsmen = batsmen.merge(dismissals, left_on=["match_id", "inning", "batsman"], 
                        right_on=["match_id", "inning", "batsman"], how="left")

batsmen = matches[['id','season']].merge(batsmen, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
batsmen.head(5)


# In[8]:

bowler_grp = deliveries.groupby(["match_id", "inning", "bowling_team", "bowler", "over"])
bowlers = bowler_grp["total_runs", "wide_runs", "bye_runs", "legbye_runs", "noball_runs"].sum().reset_index()

bowlers["runs"] = bowlers["total_runs"] - (bowlers["bye_runs"] + bowlers["legbye_runs"])
bowlers["extras"] = bowlers["wide_runs"] + bowlers["noball_runs"]

del( bowlers["bye_runs"])
del( bowlers["legbye_runs"])
del( bowlers["total_runs"])

dismissal_kinds_for_bowler = ["bowled", "caught", "lbw", "stumped", "caught and bowled", "hit wicket"]
dismissals = deliveries[deliveries["dismissal_kind"].isin(dismissal_kinds_for_bowler)]
dismissals = dismissals.groupby(["match_id", "inning", "bowling_team", "bowler", "over"])["dismissal_kind"].count().reset_index()
dismissals.rename(columns={"dismissal_kind": "wickets"}, inplace=True)

bowlers = bowlers.merge(dismissals, left_on=["match_id", "inning", "bowling_team", "bowler", "over"], 
                        right_on=["match_id", "inning", "bowling_team", "bowler", "over"], how="left")
bowlers["wickets"] = bowlers["wickets"].fillna(0)

bowlers_over = bowlers.groupby(['match_id', 'inning', 'bowling_team', 'bowler'])['over'].count().reset_index()
bowlers = bowlers.groupby(['match_id', 'inning', 'bowling_team', 'bowler']).sum().reset_index().drop('over', 1)
bowlers = bowlers_over.merge(bowlers, on=["match_id", "inning", "bowling_team", "bowler"], how = 'left')
bowlers['Econ'] = np.round(bowlers['runs'] / bowlers['over'] , 2)
bowlers = matches[['id','season']].merge(bowlers, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)

bowlers.head(10)


# In[302]:

#Number of wins per team
plt.figure(figsize=(12,6))
sns.countplot(x='winner', data=matches)
plt.xticks(rotation='vertical')
plt.show()


# In[220]:

#wins percentage
teams = [ "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ]  
win_percentage_arr = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_won_match = 0
 

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if((row['team1'] == x) or (row['team2'] == x)):
            total_matches += 1
            if(row['winner'] == x):
                no_of_times_won_match += 1

    a = no_of_times_won_match / float(total_matches)
    win_percentage_arr.append(a*100)


fig,ax = plt.subplots()
N = len(win_percentage_arr)
x = range(N)
width = 0.35
rects0 = plt.bar(x,win_percentage_arr,width,color = 'orange')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Winning Percentage')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
#print(result_arr_toss_won)
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects0)
plt.show()

#IF YOU LOOSE THE TOSS,WHAT IS THE PROBABILITY OF THEM WINNING


# In[304]:

#TOSS DECISION SO FAR
temp_series = matches.toss_decision.value_counts()
labels = (np.array(temp_series.index))
sizes = (np.array((temp_series / temp_series.sum())*100))
colors = ['silver', 'lightskyblue']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Toss decision percentage")
plt.show()
#temp_series


# In[222]:

plt.figure(figsize=(12,6))
sns.countplot(x='season', hue='toss_decision', data=matches)
plt.xticks(rotation='vertical')
plt.show()


# In[226]:

#TOSS WINNER IS A MATCH WINNER
import csv
teams = [ "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ]  
result = { "Chennai Super Kings" : 0, "Delhi Daredevils" : 0, "Kings XI Punjab" : 0, "Kolkata Knight Riders" : 0, "Mumbai Indians" : 0, "Royal Challengers Bangalore" : 0, "Sunrisers Hyderabad" : 0, "Gujarat Lions" : 0, "Rising Pune Supergiants" : 0 }
result_arr_toss_won = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_won_toss = 0
    won_toss_won_match = 0

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if((row['team1'] == x) or (row['team2'] == x)):
            total_matches += 1
            if(row['toss_winner'] == x):
                no_of_times_won_toss += 1
                if(row['winner'] == x):
                    won_toss_won_match += 1

    #print "Total matches played =  ", total_matches
    #print "No. of matches won the toss =  ", no_of_times_won_toss
    #print "No. of matches where won toss and won match =  ", won_toss_won_match
    #print ""
    a = won_toss_won_match / float(no_of_times_won_toss)
    result_arr_toss_won.append(a*100)

#print result_arr
fig,ax = plt.subplots()
N = len(result_arr_toss_won)
x = range(N)
width = 0.35
rects1 = plt.bar(x,result_arr_toss_won,width,color = 'blue')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Probabilty of winning,if the team has Won the Toss')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
#print(result_arr_toss_won)
autolabel(rects1)
plt.show()


# In[225]:

#TOSS LOOSER IS A MATCH WINNER
#toss_looser_is_winner = matches[matches.toss_winner != matches.winner]
import csv
teams = [ "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ]  
result = { "Chennai Super Kings" : 0, "Delhi Daredevils" : 0, "Kings XI Punjab" : 0, "Kolkata Knight Riders" : 0, "Mumbai Indians" : 0, "Royal Challengers Bangalore" : 0, "Sunrisers Hyderabad" : 0, "Gujarat Lions" : 0, "Rising Pune Supergiants" : 0 }
result_arr_toss_loss = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_loss_toss = 0
    loss_toss_won_match = 0

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if((row['team1'] == x) or (row['team2'] == x)):
            total_matches += 1
            if(row['toss_winner'] != x):
                no_of_times_loss_toss += 1
                if(row['winner'] == x):
                    loss_toss_won_match += 1

    #print "Total matches played =  ", total_matches
    #print "No. of matches won the toss =  ", no_of_times_won_toss
    #print "No. of matches where won toss and won match =  ", won_toss_won_match
    #print ""
    a = loss_toss_won_match / float(no_of_times_loss_toss)
    result_arr_toss_loss.append(a*100)

#print result_arr
fig,ax = plt.subplots()
N = len(result_arr_toss_loss)
x = range(N)
width = 0.35
rects1 = plt.bar(x,result_arr_toss_loss,width,color = 'green')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Probabilty of winning,if the team has Lost the Toss')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
print(result_arr_toss_loss)
autolabel(rects1)
plt.show()


# In[306]:

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
N = len(result_arr_toss_won)
x = range(N)
width = 0.35
rects5 = plt.bar(x,result_arr_toss_won,width,color = 'blue')

N = len(result_arr_toss_loss)
y = range(N)
width = 0.35

rects6 = plt.bar(ind+width,result_arr_toss_loss,width,color = 'green')

# add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Won the Match Winning Toss and Loosing Toss')
#ax.set_xticks(ind + width / 2)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants"))

ax.legend((rects5[0], rects6[0]), ('Toss Won', 'Toss Lost'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects5)
autolabel(rects6)
plt.xticks(rotation = 'vertical')

plt.show()


# In[307]:

temp_series = matches.toss_decision.value_counts()
labels = (np.array(temp_series.index))
sizes = (np.array((temp_series / temp_series.sum())*100))
colors = ['gold', 'lightskyblue']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Toss decision percentage")
plt.show()


# In[39]:

plt.figure(figsize=(12,6))
sns.countplot(x='season', hue='toss_decision', data=matches)
plt.xticks(rotation='vertical')
plt.show()


# In[227]:

#Percentage win of the match btting second or chasing irrespective of the venue
num_of_wins = (matches.win_by_wickets>0).sum()
num_of_loss = (matches.win_by_wickets==0).sum()
labels = ["Wins", "Loss"]
total = float(num_of_wins + num_of_loss)
sizes = [(num_of_wins/total)*100, (num_of_loss/total)*100]
colors = ['gold', 'lightskyblue']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Win percentage batting second")
plt.show()


# In[308]:

no_of_times_batted_first = []
no_of_times_won_batting_first = []
result_array_batting_first = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_bat_first = 0
    no_of_times_won_bat_first = 0

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if((row['team1'] == x) or (row['team2'] == x)):
            total_matches += 1
            if(row['toss_winner'] == x):
                if(row['toss_decision'] == 'bat'):
                    no_of_times_bat_first += 1
                    if(row['winner'] == x):
                        no_of_times_won_bat_first +=1
            else:
                if(row['toss_decision'] == 'field'):
                    no_of_times_bat_first += 1
                    if(row['winner'] == x):
                        no_of_times_won_bat_first +=1
    a = no_of_times_won_bat_first/ float(no_of_times_bat_first)
    no_of_times_batted_first.append(no_of_times_bat_first)
    no_of_times_won_batting_first.append(no_of_times_won_bat_first)
    result_array_batting_first.append(a*100)

#print(no_of_times_batted_first)
#print(no_of_times_won_batting_first)
#print(result_array_batting_first)
fig,ax = plt.subplots()
N = len(result_array_batting_first)
x = range(N)
width = 0.35
rects1 = plt.bar(x,result_array_batting_first,width,color = 'orange')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Probabilty of winning,if the Team is Batting First')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
autolabel(rects1)
plt.show()


# In[241]:

no_of_times_fielded_first = []
no_of_times_won_fielding_first = []
result_array_fielding_first = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_field_first = 0
    no_of_times_won_field_first = 0

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if((row['team1'] == x) or (row['team2'] == x)):
            total_matches += 1
            if(row['toss_winner'] == x):
                if(row['toss_decision'] == 'field'):
                    no_of_times_field_first += 1
                    if(row['winner'] == x):
                        no_of_times_won_field_first +=1
            else:
                if(row['toss_decision'] == 'bat'):
                    no_of_times_field_first += 1
                    if(row['winner'] == x):
                        no_of_times_won_field_first +=1
    b = no_of_times_won_field_first/ float(no_of_times_field_first)
    no_of_times_fielded_first.append(no_of_times_field_first)
    no_of_times_won_fielding_first.append(no_of_times_won_field_first)
    result_array_fielding_first.append(b*100)

print(no_of_times_fielded_first)
print(no_of_times_won_fielding_first)
print(result_array_fielding_first)
fig,ax = plt.subplots()
N = len(result_array_fielding_first)
x = range(N)
width = 0.35
rects1 = plt.bar(x,result_array_fielding_first,width,color = 'red')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Probabilty of winning,if the Team is Fielding First')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
autolabel(rects1)
plt.show()



# In[120]:



ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
N = len(result_array_batting_first)
x = range(N)
width = 0.35
rects1 = plt.bar(x,result_array_batting_first,width,color = 'orange')

N = len(result_array_fielding_first)
y = range(N)
width = 0.35

rects2 = plt.bar(ind+width,result_array_fielding_first,width,color = 'red')

# add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Batting first and Fielding first')
#ax.set_xticks(ind + width / 2)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants"))

ax.legend((rects1[0], rects2[0]), ('Batting First', 'Fielding First'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
plt.xticks(rotation = 'vertical')

plt.show()


# In[242]:

#WON THE MATCH AND WON THE TOSS AND ELECTED TO FIELD FIRST / WON THE TOSS AND ELECTED TO FIELD
   
no_of_times_won_toss_elected_to_field = []
no_of_times_won_toss_elected_to_field_won_match = []
result_array_won_toss_fielding_first = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_won_toss_field_first = 0
    no_of_times_won_toss_field_first_won_match = 0

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if(row['toss_winner'] == x):
            if(row['toss_decision'] == 'field'):
                no_of_times_won_toss_field_first += 1
                if(row['winner'] == x):
                    no_of_times_won_toss_field_first_won_match +=1
    b = no_of_times_won_toss_field_first_won_match/ float(no_of_times_won_toss_field_first)
    no_of_times_won_toss_elected_to_field.append(no_of_times_won_toss_field_first)
    no_of_times_won_toss_elected_to_field_won_match.append(no_of_times_won_toss_field_first_won_match)
    result_array_won_toss_fielding_first.append(b*100)

#print(1 , no_of_times_won_toss_elected_to_field)
#print(2 , no_of_times_won_toss_elected_to_field_won_match)
#print(3 , result_array_won_toss_fielding_first)
fig,ax = plt.subplots()
N = len(result_array_won_toss_fielding_first)
x = range(N)
width = 0.35
rects3 = plt.bar(x,result_array_won_toss_fielding_first,width,color = 'black')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Probabilty of winning,if the Team has elected to Fielding First')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
autolabel(rects3)
plt.show()

#TOTAL MATCHES = 131
#TOTAL MATCHES IN WHICH THEY WON AND ELECTED TO BAT = 44
#MATCHES IN WHICH THEY WON ELECTED TO BAT AND WON = 29
#TOTAL MATCHES AND ELECTED TO FIELD = 22
#AND THEY WON = 13
#65.91 FOR CHENNAI BAT FIRST
#WON THE TOSS VENUE WISE 


# In[243]:

#WON THE MATCH AND WON THE TOSS AND ELECTED TO BAT FIRST / WON THE TOSS AND ELECTED TO BAT
   
no_of_times_won_toss_elected_to_bat= []
no_of_times_won_toss_elected_to_bat_won_match = []
result_array_won_toss_batting_first = []
for x in teams:
    #print x
    total_matches = 0
    no_of_times_won_toss_bat_first = 0
    no_of_times_won_toss_bat_first_won_match = 0

    z = open('Desktop/ipl/matches.csv')
    reader = csv.DictReader(z)

    for row in reader:
        if(row['toss_winner'] == x):
            if(row['toss_decision'] == 'bat'):
                no_of_times_won_toss_bat_first += 1
                if(row['winner'] == x):
                    no_of_times_won_toss_bat_first_won_match +=1
    if(no_of_times_won_toss_bat_first == 0):
        no_of_times_won_toss_bat_first = 1
    b = no_of_times_won_toss_bat_first_won_match/ float(no_of_times_won_toss_bat_first)
    no_of_times_won_toss_elected_to_bat.append(no_of_times_won_toss_bat_first)
    no_of_times_won_toss_elected_to_bat_won_match.append(no_of_times_won_toss_bat_first_won_match)
    result_array_won_toss_batting_first.append(b*100)

#print(1 , no_of_times_won_toss_elected_to_field)
#print(2 , no_of_times_won_toss_elected_to_field_won_match)
#print(result_array_won_toss_fielding_first)
fig,ax = plt.subplots()
N = len(result_array_won_toss_batting_first)
y = range(N)
width = 0.35
rects3 = plt.bar(y,result_array_won_toss_batting_first,width,color = 'yellow')
#add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Probabilty of winning,if the Team has elected to Bat First')
#ax.set_xticks(1)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ))
#ax.set_xtickslabel(rotation = 'vertical')
plt.xticks(rotation = 'vertical')
autolabel(rects3)
plt.show()


# In[133]:

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
N = len(result_array_won_toss_batting_first)
x = range(N)
width = 0.35
rects3 = plt.bar(x,result_array_won_toss_batting_first,width,color = 'b')

N = len(result_array_won_toss_fielding_first)
y = range(N)
width = 0.35

rects4 = plt.bar(ind + width,result_array_won_toss_fielding_first,width,color = 'y')

# add some text for labels, title and axes ticks
ax.set_ylabel('Probability of winning')
ax.set_title('Batting first and Fielding first')
#ax.set_xticks(ind + width / 2)
ax.set_xticklabels(("Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants"))

ax.legend((rects3[0], rects4[0]), ('Batting First', 'Fielding First'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

autolabel(rects3)
autolabel(rects4)
plt.xticks(rotation = 'vertical')
    
plt.show()


# In[244]:

teams = [ "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ]
venues = [ "Bangalore", "Chandigarh", "Delhi", "Hyderabad", "Kanpur", "Kolkata", "Mumbai", "Pune", "Raipur", "Rajkot", "Vishakapatnam", "Ahmedabad", "Ranchi" ] #venue

result = { "Chennai Super Kings" : [], "Delhi Daredevils": [], "Kings XI Punjab" : [], "Kolkata Knight Riders" : [], "Mumbai Indians" : [], "Royal Challengers Bangalore" : [], "Sunrisers Hyderabad" : [], "Gujarat Lions" : [], "Rising Pune Supergiants" : [] }

for x in teams:
    total = 0
   # print ""
   # print x
    print_total = True
    #print ""
    array = []
    for y in venues:
        z = open('Desktop/ipl/matches.csv')
        reader = csv.DictReader(z)
        count = 0
        total_played = 0
        for row in reader:
            if((row['team1'] == x) or (row['team2'] == x)):
                total += 1
                #print(row['id'])
                if (row['city'] == y):
                    total_played += 1
                    #print(row['id'])
                    if(row['winner'] == x):
                        count += 1
        percentage = 0
        if(total_played != 0):
            percentage = int((float(count) / float(total_played)) * 100)
            #result[x].append(percentage)
        #if(print_total):
           # print "Total matches : ", total
           # print ""
           # print_total = False
        array.append(percentage)
        #print "\tVenue : ", y
        #print "\t\tTotal MAtches played here : ", total_played
        #print "\t\tMatches won here : ", count
        #print "\t\tPercentage win here : ", percentage
    print array
    fig,ax = plt.subplots()
    N = len(array)
    y = range(N)
    width = 0.5
    rects8 = plt.bar(y,array,width,color = 'yellow')
    #add some text for labels, title and axes ticks
    ax.set_ylabel('Probability of winning')
    ax.set_title('Probabilty of winning of '+x)
    ax.set_xticks(np.arange(N))
    ax.set_xticklabels(("Bangalore", "Chandigarh", "Delhi", "Hyderabad", "Kanpur", "Kolkata", "Mumbai", "Pune", "Raipur", "Rajkot", "Vishakapatnam", "Ahmedabad", "Ranchi"))
    #ax.set_xtickslabel(rotation = 'vertical')
    plt.xticks(rotation = 'vertical')
    plt.show()


# In[249]:

#No of wins by team and season in each city
x, y = 2010, 2017
while x < y:
    wins_percity = matches_agg[matches_agg['season'] == x].groupby(['winner', 'city'])['match_id'].count().unstack()
    plot = wins_percity.plot(kind='bar', stacked=True, title="Team wins in different cities\nSeason "+str(x), figsize=(7, 5))
    sns.set_palette("Paired", len(matches_agg['city'].unique()))
    plot.set_xlabel("Teams")
    plot.set_ylabel("No of wins")
    plot.legend(loc='best', prop={'size':8})
    x+=1
    plt.show()


# In[250]:

import csv
 
teams = [ "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders", "Mumbai Indians", "Royal Challengers Bangalore", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants" ]
venues = [ "Bangalore", "Chandigarh", "Delhi", "Hyderabad", "Kanpur", "Kolkata", "Mumbai", "Pune", "Raipur", "Rajkot", "Vishakapatnam", "Ahmedabad", "Ranchi" ] #venue
 
result = { "Chennai Super Kings" : [], "Delhi Daredevils": [], "Kings XI Punjab" : [], "Kolkata Knight Riders" : [], "Mumbai Indians" : [], "Royal Challengers Bangalore" : [], "Sunrisers Hyderabad" : [], "Gujarat Lions" : [], "Rising Pune Supergiants" : [] }

for x in teams:
    team_bat_first = []
    team_chasing = []
    total = 0
    #print ""
    print x
    print_total = True
    #print ""
    winning_batting_first = []
    winning_chasing = []
    for y in venues:
        z = open('Desktop/ipl/matches.csv')
        reader = csv.DictReader(z)
        bat_count = 0
        chase_count = 0
        total_played = 0
        total_batted = 0
        total_chased = 0

        winning_team = []
        for row in reader:
            if((row['team1'] == x) or (row['team2'] == x)):
                total += 1
 
                if (row['city'] == y):
                    total_played += 1
 
                    # won toss and won batting first or second
                    if(row['toss_winner'] == x):
                        if(row['toss_decision'] == 'bat'):
                            total_batted += 1
                            if(row['winner'] == x):
                                bat_count += 1
                        else:
                            total_chased += 1
                            if(row['winner'] == x):
                                chase_count += 1
 
                    '''else:
                        if(row['toss_decision'] == 'field'):
                            total_batted += 1
                            if(row['winner'] == x):
                                bat_count += 1
                        else:
                            total_chased += 1
                            if(row['winner'] == x):
                                chase_count += 1'''
 
 
        percentage1 = 0
        percentage2 = 0
         
        if(total_batted != 0):
            percentage1 = ((float(bat_count) / float(total_batted)) * 100)
        if(total_chased != 0):
            percentage2 = ((float(chase_count) / float(total_chased)) * 100)
        
        winning_team.append(percentage1)
        winning_team.append(percentage2)
            #result[x].append(percentage)
        #if(print_total):
            #print "Total matches : ", total
            #print ""
            #print_total = False
         
       # print "\tVenue : ", y
        #print "\t\tTotal MAtches played here : ", total_played
        #print "\t\tTotal no. of times elected to bat first here : ", total_batted
        #print "\t\tTotal no of matches won here after electing to bat first :  ", bat_count
        #print "\t\tTotal Matches elected to chase here : ", total_chased
        #print "\t\tTotal matched chased successfully here : ", chase_count
        #print "\t\tPercentage win bat first here : ", round(percentage1, 2)
        #print "\t\tPercentage win chasing : ", round(percentage2, 2)
        
       
        #print(winning_team)
        team_bat_first.append(winning_team[0])
        team_chasing.append(winning_team[1])
    #print(team_bat_first)
    #print(team_chasing)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    N = len(team_bat_first)
    x = range(N)
    width = 0.35
    rects9 = plt.bar(x,team_bat_first,width,color = 'b')

    N = len(team_chasing)
    y = range(N)
    width = 0.35

    rects10 = plt.bar(ind + width,team_chasing,width,color = 'y')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Probability of winning')
    ax.set_title('Batting first and Fielding first')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((venues))

    ax.legend((rects9[0], rects10[0]), ('Batting First', 'Fielding First'))


    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    autolabel(rects9)
    autolabel(rects10)
    plt.xticks(rotation = 'vertical')

    plt.show()
#print result


# In[253]:

temp_series = matches.player_of_match.value_counts()[:10]
labels = np.array(temp_series.index)
ind = np.arange(len(labels))
width = 0.9
fig, ax = plt.subplots()
rects = ax.bar(ind, np.array(temp_series), width=width, color='y')
ax.set_xticks(ind+((width)/2.))
ax.set_xticklabels(labels, rotation='vertical')
ax.set_ylabel("Count")
ax.set_title("Top player of the match awardees")
autolabel(rects)
plt.show()



# In[328]:

temp_df = deliveries.groupby('batsman')['batsman_runs'].agg('sum').reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
temp_df = temp_df.iloc[:10,:]

labels = np.array(temp_df['batsman'])
ind = np.arange(len(labels))
width = 0.5
fig, ax = plt.subplots()
rects = ax.bar(ind, np.array(temp_df['batsman_runs']), width=width, color='blue')
ax.set_xticks(ind+((width)/2.))
ax.set_xticklabels(labels, rotation='vertical')
ax.set_ylabel("Count")
ax.set_title("Top run scorers in IPL")
autolabel(rects)
plt.show()



# In[311]:

temp_df = deliveries.groupby('batsman')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).reset_index(drop=True)
temp_df = temp_df.iloc[:10,:]

labels = np.array(temp_df['batsman'])
ind = np.arange(len(labels))
width = 0.9
fig, ax = plt.subplots()
rects = ax.bar(ind, np.array(temp_df['batsman_runs']), width=width, color='green')
ax.set_xticks(ind+((width)/2.))
ax.set_xticklabels(labels, rotation='vertical')
ax.set_ylabel("Count")
ax.set_title("Batsman with most number of boundaries.!")
autolabel(rects)
plt.show()


# In[322]:

temp_df = deliveries.groupby('bowler')['total_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='total_runs', ascending=False).reset_index(drop=True)
temp_df = temp_df.iloc[:10,:]

labels = np.array(temp_df['bowler'])
ind = np.arange(len(labels))
width = 0.9
fig, ax = plt.subplots()
rects = ax.bar(ind, np.array(temp_df['total_runs']), width=width, color='yellow')
ax.set_xticks(ind+((width)/2.))
ax.set_xticklabels(labels, rotation='vertical')
ax.set_ylabel("Count")
ax.set_title("Top Bowlers - Number of dot balls bowled in IPL")
autolabel(rects)
plt.show()


# In[276]:

batsmen


# In[323]:

sns.jointplot(x = "batsman_runs",y = "balls_faced",data = batsmen)


# In[324]:

sns.jointplot(x = batsmen['SR'],y = batsmen["batsman_runs"])


# In[290]:

sns.jointplot(x = matches["win_by_runs"],y = matches['season'])


# In[291]:

sns.jointplot(x = matches["win_by_wickets"],y = matches['season'])


# In[325]:



batsman_runsperseason = batsmen.groupby(['season', 'batting_team', 'batsman'])['batsman_runs'].sum().reset_index()
batsman_runsperseason = batsman_runsperseason.groupby(['season', 'batsman'])['batsman_runs'].sum().unstack().T
batsman_runsperseason['Total'] = batsman_runsperseason.sum(axis = 1) #add total column to find batsman with the highest runs
batsman_runsperseason = batsman_runsperseason.sort_values(by = 'Total', ascending = False).drop('Total', 1)
ax = batsman_runsperseason[:5].T.plot()
#batsman_runsperseason


# In[327]:

six = deliveries[ deliveries.batsman_runs == 6 ] #Considering only those deliveries where 6 have been hit
six = six[['over', 'batting_team','batsman_runs']]  #This three columns is what we require
result = pd.pivot_table(six, index='batting_team', columns='over', values='batsman_runs', aggfunc=np.sum) #creating a pivot table for applying heat map
sns.heatmap(result, annot=False, fmt="g" , cmap='viridis')  #heat map
plt.show()


# In[ ]:



