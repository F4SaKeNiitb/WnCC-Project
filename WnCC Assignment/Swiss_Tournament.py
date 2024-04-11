import random
import pandas as pd

teams_data=pd.read_excel("Codewars Data.xlsx") #extract data from excel as dataframe
teams_data.rename({'Initial Rting':'rating','Language of Code':'language'},axis='columns',inplace='True')
teams_data['score']=0
teams_data['bye']=False

# Dividing the participants on the basis of coding language
language_groups = {
    'Python': [i for i in teams_data[teams_data['language']=='P']['Team Name']],
    'C++': [i for i in teams_data[teams_data['language']=='C++']['Team Name']]
}

# Converting data to dictionary
teams_data=teams_data.set_index('Team Name')
teams_data=teams_data.to_dict('index')
for i in teams_data:
    teams_data[i]['opps']=[]
    teams_data[i]['time']=0

# Function to pair teams
def pair_teams():

    pairs = []

    # Iterating through teams on the basis of language
    for language, team_names in language_groups.items():
        # team_names.sort(key=lambda x: (teams_data[x]['score'],teams_data[x]['rating'],x), reverse=True)
        # Sorting teams on the basis of given constraints and storing the "copy" in new array
        teams=sorted(team_names,key=lambda x: (teams_data[x]['score'],(0.3*oppr(teams_data[x]['opps'])-0.7*tsum(teams_data[x]['opps']))), reverse=True)

        # Converting odd number of teams to even number by giving a player bye only once starting from botton of leaderboard
        if len(teams)%2==1:
            for i in teams[::-1]:
                if teams_data[i]['bye']==False:
                    teams.remove(i)
                    teams_data[i]['bye']=True
                    break

        # Pairing teams and appending their opponents in the opps array
        for i in range(0, len(teams), 2):
            if i + 1 < len(teams):
                pairs.append((teams[i], teams[i + 1]))
                teams_data[teams[i]]['opps'].append(teams[i + 1])
                teams_data[teams[i + 1]]['opps'].append(teams[i])

    return pairs

# Function to simulate match outcome
def simulate_match(team1, team2):

    # Adding Noise to the team ratings
    team1_rating = teams_data[team1]['rating'] + random.randint(-4, 4)
    team2_rating = teams_data[team2]['rating'] + random.randint(-4, 4)
    rating_diff=abs(team1_rating-team2_rating)

    # Choosing winner on the basis of absolute rating
    if rating_diff < 5:
        winner = random.choice([team1, team2]) 
        loser = team2 if winner == team1 else team1
    elif rating_diff <= 10:
        winner = team1 if team1_rating > team2_rating else team2
        winner_prob = 0.65
        loser = team2 if winner == team1 else team1
        if random.random() > winner_prob:
            winner, loser = loser, winner
    else:
        winner = team1 if team1_rating > team2_rating else team2
        winner_prob = 0.9
        loser = team2 if winner == team1 else team1
        if random.random() > winner_prob:
            winner, loser = loser, winner

    # Changing rating on the basis of rating of both players
    if teams_data[winner]['rating'] > teams_data[loser]['rating']:
        teams_data[winner]["rating"] += 2
        teams_data[loser]["rating"] -= 2
    else:
        teams_data[winner]["rating"] += 5
        teams_data[loser]["rating"] -= 5

    # Increasing score by 1
    teams_data[winner]['score'] += 1

    #Randomly generating time in decimals and adding it to time (overall lesser time is better)
    t=random.uniform(5,10)
    teams_data[winner]['time'] += t   # Less time gets added if player wins faster
    teams_data[loser]['time'] += 10-t  # Less time gets added if loses in a longer time

    return winner

# Function to find sum of the rating of opponents of a player
def oppr(list):
    sum=0
    for i in list:
        sum+=teams_data[i]['rating']
    return sum

# Function to find sum of the time of opponents of a player
def tsum(list):
    sum=0
    for i in list:
        sum+=teams_data[i]['time']
    return sum

# Function to update leaderboard and print it to terminal
def update_leaderboard(round):

    # Sorting teams on the basis of given constraints and storing the "copy" in new array
    leaderboard = sorted(teams_data.items(), key=lambda x: (x[1]['score'], (0.3*oppr(x[1]['opps'])-0.7*tsum(x[1]['opps']))), reverse=True)
    print(f"\nRound {round} Leaderboard:")
    print("Rank\tTeam\tScore\tRating")
    rank=0
    for i in leaderboard:
        rank+=1
        print(f"{rank}\t{i[0]}\t{i[1]['score']}\t{i[1]['rating']}")
    return leaderboard

# Main function 
def main():
    for round in range(1, 11):
        print(f"\nRound {round}")
        pairs = pair_teams()
        for team1, team2 in pairs:
            winner= simulate_match(team1, team2)
            print(f"{team1} vs {team2}: Winner - {winner}")
        update_leaderboard(round)

if __name__ == "__main__":
    main()
