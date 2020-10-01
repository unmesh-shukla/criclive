#!/usr/local/bin/python3

import argparse
import os
import sys
import requests
from print_in_colors import prRed, prGreen, prYellow, prLightPurple, prPurple, prCyan, prLightGray, prBlack

class CricInfo():


    def __init__(self):
        self.get_matches_info()


    def crawl_url(self, url):
        '''
        work with url.
        '''
        try:
            r = requests.get(url).json()
            return r
        except Exception: 
            raise


    def get_matches_info(self):
        '''
        This function get matches information.
        '''
        url = "https://mapps.cricbuzz.com/cbzios/match/livematches"
        crawled_content = self.crawl_url(url)
        self.matches = crawled_content['matches']
        
        # for match in matches:
        #     info.append(self.matchinfo(match['match_id']))
        return self.matches


    def generate_matches_list(self):
        '''
        This function genrate match list.
        '''
        self.get_matches_info()
        self.match_list = []
        for match in self.matches:
            if match.get('bat_team') is None or match.get('bow_team') is None:
                # if no scores are available for a match
                continue
            match_short_info = [match['match_id'], match['series_name'], match['header']['match_desc'], match['header']['status'], match['team1']['name'], match['team2']['name']]
            self.match_list.append(match_short_info)


    def get_match_list(self):
        '''
        This function get match list.
        '''
        self.generate_matches_list()
        return self.match_list


    def display_match_list(self):
        '''
        This function display match list.
        '''
        self.get_match_list()
        print("")
        for i, match in enumerate(self.match_list):
            print(str(i + 1) + ".\t"),
            sys.stdout.write("\b\b\b\b")
            prGreen(match[4]),
            print("vs"),
            prGreen(match[5]),
            print(" - "),
            prCyan(match[2])
            print(" - "),
            prRed(match[1])
            print("")


    def show_options_menu(self):
        '''
        This function show Menue.
        '''
        self.display_match_list()
        choice = raw_input("Select a match number : ")
        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.match_list):
                raise Exception
        except:
            print("\nInvalid choice!")
            print("Exiting program..\n")
            sys.exit(0)

        return choice


    def get_score_by_match(self, match):
        '''
        This function get score by match.
        '''
        
        def use_inning_id_as_key(inning):
            try:
                return int(inning['id'])
            except KeyError:
                print("Incorrect inning key!")
                sys.exit(0)

        team_1_id = match['team1']['id']
        team_1_name = match['team1']['name']
        short_team_1_name = match['team1']['s_name']
        team_2_id = match['team2']['id']
        team_2_name = match['team2']['name']
        short_team_2_name = match['team2']['s_name']

        if match['bat_team']['id'] == team_1_id:
            batting_team_id = team_1_id
            batting_team_name = team_1_name
            short_batting_team_name = short_team_1_name
            bowling_team_id = team_2_id
            bowling_team_name = team_2_name
            short_bowling_team_name = short_team_2_name
        else:
            batting_team_id = team_2_id
            batting_team_name = team_2_name
            short_batting_team_name = short_team_2_name
            bowling_team_id = team_1_id
            bowling_team_name = team_1_name
            short_bowling_team_name = short_team_1_name

        all_innings = []

        for inning in match['bat_team']['innings']:
            inning['team_name'] = batting_team_name
            inning['short_team_name'] = short_batting_team_name
            all_innings.append(inning)
        for inning in match['bow_team']['innings']:
            inning['team_name'] = bowling_team_name
            inning['short_team_name'] = short_bowling_team_name
            all_innings.append(inning)

        # sort the innings score by innings numbers
        all_innings.sort(key=use_inning_id_as_key)

        status = match['header']['status']
        return all_innings, status


    def display_score(self, score, status):
        '''
        This function display score.
        '''

        print("")

        for line in score:
            prLightPurple("Inning " + line['id']),
            print("->"),
            prYellow("\033[1m" + line['team_name'] + " (" + line['short_team_name'] + ")" + "\033[0;0m"),
            print("-"),
            prGreen("\033[1m" + line['score'] + "\033[0;0m"),
            print("for"),
            prGreen("\033[1m" + line['wkts'] + "\033[0;0m"),
            print("in"),
            prGreen("\033[1m" + line['overs'] + "\033[0;0m"),
            print("overs"),

            if line.get('decl') == 'true':
                print("(declared)")
            else:
                print("")

        prRed(status)
        print("")
        print("")


    def open_score_of_choice(self, choice_id=None):
        '''
        Open score of choice.
        '''

        if choice_id is None:
            print("\n Wrong choice!")
            return -1
        for match in self.matches:
            if str(match['match_id']) == str(self.match_list[choice_id - 1][0]):
                score, status = self.get_score_by_match(match=match)
                self.display_score(score, status)
                return 0


# Create the parser
my_parser = argparse.ArgumentParser(prog='criclive',
                                    usage='%(prog)s [-h]',
                                    description='Run the command without any argument to get live scores of ongoing matches.\nSelect the match number to view the scores of that match.',
                                    epilog='Enjoy!!')
my_parser.parse_args()

c = CricInfo()
choice_id = c.show_options_menu()
c.open_score_of_choice(choice_id=choice_id)
