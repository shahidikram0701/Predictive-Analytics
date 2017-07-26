#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int select_team();
int select_venue();
int who_won_the_toss(int team1, int teaam2);
int bat_or_bowl(int team);
int who_bats_first(int team1, int team2, int toss);
int predict();
int predict_based_on_venue(int team1, int team2, int venue);
int predict_based_on_toss(int team1, int team2, int toss);
int predict_based_batsmen(int team1, int team2);
int predict_based_on_bowlers(int team1, int team2);
int predict_based_on_batting_first(int team1, int team2, int first);
void predict_based_on_proper_decision(int team1, int team2, int toss, int bat_first, int venue);
char *team_name(int team_num);
//char *venue_name(int venue_num);
