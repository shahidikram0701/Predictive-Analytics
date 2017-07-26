#include "prediction.h"

int
select_team()
{
    int team = -1;

    type_menu:
    printf("  \nSelect the team:\n");
    printf("  1 - Chennai Super Kings\n");
    printf("  2 - Delhi Daredevils\n");
    printf("  3 - Kings XI Punjab\n");
    printf("  4 - Kolkata Knight Riders\n");
    printf("  5 - Mumbai Indians\n");
    printf("  6 - Royal Challengers Bangalore\n");
    printf("  7 - Sunrisers Hyderabad\n");
    printf("  8 - Gujrat Lions\n");
    printf("  9 - Rising Pune Supergiants\n ");
    printf("  : ");
    scanf("%d", &team);

    if(team == -1 || team > 9){
        printf("\nInvalid selection\n\n");
        goto type_menu;
    }
    else{
        return team;
    }
}

int
select_venue(){
    int venue = -1;

    type_menu:
    printf("  \nVENUE:\n");
    printf("  1 - Bangalore\n");
    printf("  2 - Chandigarh\n");
    printf("  3 - Delhi\n");
    printf("  4 - Hyderabad\n");
    printf("  5 - Kanpur\n");
    printf("  6 - Kolkata\n");
    printf("  7 - Mumbai\n");
    printf("  8 - Pune\n");
    printf("  9 - Raipur\n");
    printf("  10 - Rajkot\n");
    printf("  11 - Vishakapatnam\n");
    printf("  12 - Ahmedabad\n");
    printf("  13 - Ranchi\n");
    printf("  : ");
    scanf("%d", &venue);

    if(venue == -1 || venue > 13){
        printf("\nInvalid selection\n\n");
        goto type_menu;
    }
    else{
        return venue;
    }
}

int
who_won_the_toss(int team1, int team2){
    int who;
    type_menu:
    printf("\nWho won the toss :\n");
    switch(team1){
        case 1:
            printf("  1 - Chennai Super Kings\n");
            break;
        case 2:
            printf("  2 - Delhi Daredevils\n");
            break;
        case 3:
            printf("  3 - Kings XI Punjab\n");
            break;
        case 4:
            printf("  4 - Kolkata Knight Riders\n");
            break;
        case 5:
            printf("  5 - Mumbai Indians\n");
            break;
        case 6:
            printf("  6 - Royal Challengers Bangalore\n");
            break;
        case 7:
            printf("  7 - Sunrisers Hyderabad\n");
            break;
        case 8:
            printf("  8 - Gujrat Lions\n");
            break;
        case 9:
            printf("  9 - Rising Pune Supergiants\n");
            break;
    }
    switch(team2){
        case 1:
            printf("  1 - Chennai Super Kings\n");
            break;
        case 2:
            printf("  2 - Delhi Daredevils\n");
            break;
        case 3:
            printf("  3 - Kings XI Punjab\n");
            break;
        case 4:
            printf("  4 - Kolkata Knight Riders\n");
            break;
        case 5:
            printf("  5 - Mumbai Indians\n");
            break;
        case 6:
            printf("  6 - Royal Challengers Bangalore\n");
            break;
        case 7:
            printf("  7 - Sunrisers Hyderabad\n");
            break;
        case 8:
            printf("  8 - Gujrat Lions\n");
            break;
        case 9:
            printf("  9 - Rising Pune Supergiants\n");
            break;
    }
    printf("  : ");
    scanf("%d", &who);

    if(who == team1 || who == team2){
        return who;
    }
    else{
        printf("\nInvalid selection\n\n");
        goto type_menu;
    }
}

int
bat_or_bowl(int team){
    int what;
    type_menu:
    printf("\n%s chose to : \n", team_name(team));
    printf("  1 - Bat\n");
    printf("  2 - Bowl\n");
    printf("  : ");
    scanf("%d", &what);

    if(what == 1 || what == 2){
        return what;
    }
    goto type_menu;
}

int
who_bats_first(int team1, int team2, int toss){
    int who;

    if(toss == team1){
        int team1_choice = bat_or_bowl(team1);
        if(team1_choice == 1){
            who = team1;
        }
        else{
            who = team2;
        }
    }
    else{
        int team2_choice = bat_or_bowl(team2);
        if(team2_choice == 1){
            who = team2;
        }
        else{
            who = team1;
        }
    }

    return who;
}

int
predict(){
    int team1 = select_team();
    int team2 = select_team();

    while(team1 == team2){
        printf("\nTEAM 1 is same as TEAM 2\n\n");
        team2 = select_team();
    }
    int venue = select_venue();
    int toss = who_won_the_toss(team1, team2);

    int first_bat = who_bats_first(team1, team2, toss);

    //printf("\n\nTeam 1 : %d", team1);
    //printf("\nTeam 2 : %d", team2);
    //printf("\n\nVenue: %d", venue);
    //printf("\n\nToss : %d", toss);
    //printf("\n\nBatting First : %d\n\n", first_bat);

    printf("\t\t\tPREDICTING\n\n\n");

    // Prediction based on team batting first or second

    int winner_battingFirst_chasing = predict_based_on_batting_first(team1, team2, first_bat);
    //printf("Based on who bats first -- %d\n\n", winner_battingFirst_chasing);
    printf("Based on who batting order winner must be -- \n\t%s\n\n", team_name(winner_battingFirst_chasing));

    // Prediction based on venue of the match

    int winner_venue = predict_based_on_venue(team1, team2, venue);
    if(winner_venue == -1){
        // cannot predict using this variable
        printf("Based on the venue winner must be -- ");
        printf("\n\tCannot predict using this variable\n\n");
    }
    else{
        printf("Based on the venue the winner must be -- \n\t%s\n\n", team_name(winner_venue));
    }

    // Prediction based on toss

    int winner_toss = predict_based_on_toss(team1, team2, toss);
    printf("Based on the toss the winner must be -- \n\t%s\n\n", team_name(winner_toss));

    // Prediction based on Batsmen strength

    int winner_batsmen = predict_based_batsmen(team1, team2);
    printf("Based on the Batting strength the winner must be -- \n\t%s\n\n", team_name(winner_batsmen));

    // Prediction based on Bowling strength

    int winner_bowler = predict_based_on_bowlers(team1, team2);
    printf("Based on the Bowling strength the winner must be -- \n\t%s\n\n", team_name(winner_bowler));

    // comment on the decision of the team after toss

    predict_based_on_proper_decision(team1, team2, toss, first_bat, venue);
}

char *team_name(int team_num){
    char team[60][60] =
                {
                    "Chennai Super Kings",
                    "Delhi Daredevils",
                    "Kings XI Punjab",
                    "Kolkata Knight Riders",
                    "Mumbai Indians",
                    "Royal Challengers Bangalore",
                    "Sunrisers Hyderabad",
                    "Gujrat Lions",
                    "Rising Pune Supergiants"
                };

    return(team[team_num - 1]);
}

/*char *venue_name(int venue_num){
    printf("I am here");
    char venue[60][60] =
                {
                    "Bangalore",
                    "Chandigarh",
                    "Delhi",
                    "Hyderabad",
                    "Kanpur",
                    "Kolkata",
                    "Mumbai",
                    "Pune",
                    "Raipur",
                    "Rajkot",
                    "Vishakapatnam",
                    "Ahmedabad",
                    "Ranchi"
                };

    return(venue[venue_num - 1]);
}*/

int
predict_based_on_venue(int team1, int team2, int venue){
    int winner;
    int table[10][14] =
                        {
                            { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                            { 0, 57, 75, 83, 66, 0, 44, 50, 50, 0, 0, 0, 0, 60 },
                            { 0, 42, 25, 38, 80, 0, 16, 20, 50, 66, 100, 0, 50, 0 },
                            { 0, 44, 47, 50, 57, 0, 25, 40, 20, 0, 100, 0, 100, 0 },
                            { 0, 50, 60, 57, 80, 0, 64, 30, 100, 0, 0, 0, 0, 33 },
                            { 0, 75, 57, 25, 66, 0, 80, 66, 100, 0, 0, 0, 50, 0 },
                            { 0, 51, 50, 66, 28, 0, 42, 50, 100, 100, 0, 0, 100, 33 },
                            { 0, 40, 100, 80, 60, 0, 0, 33, 100, 50, 100, 0, 100, 100 },
                            { 0, 0, 100, 50, 0, 100, 100, 100, 100, 0, 40, 0, 0, 0 },
                            { 0, 0, 0, 100, 100, 0, 0, 100, 0, 0, 0, 0, 0, 0 }
                        };

    int decimal[10][14] =
                        {
                            { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                            { 0, 14, 0, 33, 67, 0, 44, 0, 0, 0, 0, 0, 0, 0 },
                            { 0, 86, 0, 78, 0, 0, 67, 0, 0, 67, 0, 0, 0, 0 },
                            { 0, 44, 62, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                            { 0, 0, 0, 14, 0, 0, 71, 0, 0, 0, 0, 0, 0, 33 },
                            { 0, 0, 14, 0, 67, 0, 0, 67, 0, 0, 0, 0, 0, 0 },
                            { 0, 79, 0, 67, 57, 0, 86, 0, 0, 0, 0, 0, 0, 33 },
                            { 0, 0, 0, 0, 87, 0, 0, 33, 0, 0, 0, 0, 0, 0 },
                            { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                            { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                        };

    int points_team1 = table[team1][venue];
    int decimal_points_team1 = decimal[team1][venue];
    int points_team2 = table[team2][venue];
    int decimal_points_team2 = decimal[team2][venue];

    //printf("Points Team-1 : %d\n", points_team1);
    //printf("Points Team-2 : %d\n", points_team2);

    if(points_team1 > points_team2){
        winner = team1;
    }
    else if(points_team2 > points_team1){
        winner = team2;
    }
    else{
        if(decimal_points_team1 > decimal_points_team2){
            winner = team1;
        }
        else if(decimal_points_team2 > decimal_points_team1){
            winner = team2;
        }
        else{
            //printf("I'm here!");
            winner = -1;
        }
    }
    return winner;
}

int
predict_based_on_toss(int team1, int team2, int toss){
    int winner;
    int won_toss[10] = { 0, 63, 43, 40, 55, 55, 54, 46, 75, 42 };
    int decimal_won_toss[10] = { 0, 64, 75, 63, 7, 41, 10, 67, 0, 86 };
    int lost_toss[10] = { 0, 56, 40, 52, 47, 59, 47, 62, 37, 28 };
    int decimal_lost_toss[10] = { 0, 92, 58, 86, 62, 9, 44, 50, 50, 57 };

    int points_team1;
    int decimal_points_team1;
    int points_team2;
    int decimal_points_team2;

    if(toss == team1){
        // team 1 won the toss
        points_team1 = won_toss[team1];
        decimal_points_team1 = decimal_won_toss[team1];
        points_team2 = lost_toss[team2];
        decimal_points_team2 = decimal_lost_toss[team2];
    }
    else{
        //team2 won the toss
        points_team1 = lost_toss[team1];
        decimal_points_team1 = decimal_lost_toss[team1];
        points_team2 = won_toss[team2];
        decimal_points_team2 = decimal_won_toss[team2];
    }

    if(points_team1 > points_team2){
        winner = team1;
    }
    else if(points_team2 > points_team1){
        winner = team2;
    }
    else{
        if(decimal_points_team1 > decimal_points_team2){
            winner = team1;
        }
        else{
            winner = team2;
        }
    }
    return winner;
}

int
predict_based_batsmen(int team1, int team2){
    int winner;
    int strike_rates[10] = { 0, 117, 121, 122, 122, 128, 119, 121, 118, 107 };
    int decimal[10] = { 0, 79, 53, 25, 93, 34, 225, 68, 5, 93 };

    int points_team1 = strike_rates[team1];
    int points_team2 = strike_rates[team2];

    //printf("Strike rates of (team1, team2) : (%d, %d)\n", points_team1, points_team2);

    if(points_team1 > points_team2){
        winner = team1;
    }
    else if(points_team2 > points_team1){
        winner = team2;
    }
    else{
        if(decimal[team1] > decimal[team2]){
            winner = team1;
        }
        else{
            winner = team2;
        }
    }
    return winner;
}

int
predict_based_on_bowlers(int team1, int team2){
    int winner;
    int economy[10] = { 0, 7, 5, 6, 6, 7, 7, 7, 6, 6 };
    int decimal[10] = { 0, 94, 86, 63, 64, 9, 4, 45, 50, 94 };

    int points_team1 = economy[team1];
    int points_team2 = economy[team2];

    //printf("Strike rates of (team1, team2) : (%d, %d)\n", points_team1, points_team2);

    if(points_team1 < points_team2){
        winner = team1;
    }
    else if(points_team2 < points_team1){
        winner = team2;
    }
    else{
        if(decimal[team1] < decimal[team2]){
            winner = team1;
        }
        else{
            winner = team2;
        }
    }
    return winner;
}

int
predict_based_on_batting_first(int team1, int team2, int first){
    int batting_first[10] =     { 0, 58, 31, 40, 43, 56, 43, 48, 16, 0 };
    int decimal_bat_first[10] = { 0, 44, 58, 58, 55, 58, 55, 65, 67, 0 };
    int chasing[10] =       { 0, 62, 50, 53, 58, 57, 55, 64, 80, 71 };
    int decimal_chase[10] = { 0, 96, 0, 85, 57, 81, 84, 0, 0, 43 };

    int points_team1;
    int decimal_points_team1;
    int points_team2;
    int decimal_points_team2;

    int winner;

    if(first == team1){
        points_team1 = batting_first[team1];
        decimal_points_team1 = decimal_bat_first[team1];
        points_team2 = chasing[team2];
        decimal_points_team2 = decimal_chase[team2];
    }
    else{
        points_team1 = chasing[team1];
        decimal_points_team1 = decimal_chase[team1];
        points_team2 = batting_first[team2];
        decimal_points_team2 = decimal_bat_first[team2];
    }

    if(points_team1 > points_team2){
        winner = team1;
    }
    else if(points_team2 > points_team1){
        winner = team2;
    }
    else{
        if(decimal_points_team1 > decimal_points_team2){
            winner = team1;
        }
        else{
            winner = team2;
        }
    }

    return winner;
}

void
predict_based_on_proper_decision(int team1, int team2, int toss, int bat_first, int venue){
    int bat[10][14] =
                    {
                        { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                        { 0, 100, 100, 100, 0, 0, 50, 100, 50, 0, 0, 0, 0, 50 },
                        { 0, 0, 0, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                        { 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                        { 0, 0, 100, 0, 50, 0, 64, 0, 100, 0, 0, 0, 0, 0 },
                        { 0, 0, 50, 0, 0, 0, 66, 66, 100, 0, 0, 0, 50, 0 },
                        { 0, 0, 0, 0, 0, 0, 0, 100, 100, 0, 0, 0, 0, 0 },
                        { 0, 50, 0, 0, 28, 0, 0, 0, 0, 100, 0, 0, 0, 0 },
                        { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                        { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                    };

    int chase[10][14] =
                    {
                        { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
                        { 0, 33, 100, 100, 0, 0, 50, 60, 0, 0, 0, 0, 0, 100 },
                        { 0, 50, 50, 40, 100, 0, 100, 28, 0, 100, 100, 0, 50, 0 },
                        { 0, 50, 54, 66, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0 },
                        { 0, 100, 50, 33, 0, 0, 81, 50, 100, 0, 0, 0, 0, 50 },
                        { 0, 66, 33, 0, 0, 0, 100, 73, 100, 0, 0, 0, 0, 0 },
                        { 0, 60, 50, 66, 0, 0, 75, 50, 0, 100, 0, 0, 100, 0 },
                        { 0, 50, 0, 100, 75, 0, 0, 0, 0, 0, 100, 0, 0, 0 },
                        { 0, 0, 100, 0, 0, 100, 100, 100, 100, 0, 0, 0, 0, 0 },
                        { 0, 0, 0, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                    };
    int p;
    int b1 = 0;
    int c1 = 0;
    int b2 = 0;
    int c2 = 0;

    if(toss == team1){
        if(bat_first == team1){
            p = bat[team1][venue];
            b1 = 1;
        }
        else{
            p = chase[team1][venue];
            c1 = 1;
        }
    }
    else{
        if(bat_first == team2){
            p = bat[team2][venue];
            b2 = 1;
        }
        else{
            p = chase[team2][venue];
            c2 = 1;
        }
    }

    if(b1){
        if(p >= 50){
            printf("%s has taken a fairly good decision of batting first at this venue\n\n\n", team_name(team1));
        }
        else{
        }
        printf("Oops not a good decision to bat at this venue\n\n\n");
    }
    if(c1){
        if(p >= 50){
            printf("%s has taken a fairly good decision of chasing at this venue\n\n\n", team_name(team1));
        }
        else{
            printf("Oops not a good decision by %s to chase at this venue\n\n\n", team_name(team1));
        }
    }
    if(b2){
        if(p >= 50){
            printf("%s has taken a fairly good decision of batting first at this venue\n\n\n", team_name(team2));
        }
        else{
            printf("Oops not a good decision by %s to bat at this venue\n\n\n", team_name(team2));
        }
    }
    if(c2){
        if(p >= 50){
            printf("%s has taken a fairly good decision of chasing at this venue\n\n\n", team_name(team2));
        }
        else{
            printf("Oops not a good decision by %s to chase at this venue\n\n\n", team_name(team2));
        }
    }
}
