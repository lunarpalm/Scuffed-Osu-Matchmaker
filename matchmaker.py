#!/usr/bin/env python3

# importing the requests library
import requests
# this file is in .gitignore, create a file within this directory called
# secret.py, and add `k = [your api key]` but without the backticks of course
import secret

def get_rank(username, game_mode):
  # api-endpoint
  URL = "https://osu.ppy.sh/api/get_user"
    
  # defining a params dict for the parameters to be sent to the API
  PARAMS = {'k':secret.k, 'u':username, 'm':game_mode}
    
  # sending get request and saving the response as response object
  r = requests.get(url = URL, params = PARAMS)
    
  # extracting data in json format
  data = r.json()
  
  return int(data[0]['pp_rank'])

# Must be in descending order because of helper method below (see it's descrip)
def get_bracket(game_mode):
  # std tier brackets:
  # 7 digit | 6 digit | 300-100K | 100K-50K | 50-20K | 20K-8K | 8K-2K |
  # 2K-500 | 499-100 | 99-50 | 49-20 | 19-7 | 6-1
  if game_mode == 0:
    return [
      1e6,
      3e5, 1e5,
      5e4, 2e4,
      8e3, 2e3,
      500, 100,
      50, 20,
      7, 1
    ]
  # taiko/ctb tier brackets:
  # 7 digit | 6 digit | 300-100K | 100K-50K | 50-20K | 20K-5K | 5K-2K |
  # 2K-750 | 749-420 | 419-150 | 149-50 | 49-20 | 19-7 | 6-1
  elif game_mode == 1 or game_mode == 2:
    return [
      1e6,
      3e5, 1e5,
      5e4, 2e4,
      5e3, 2e3,
      750, 420, 150,
      50, 20,
      7, 1
    ]
  # mania tier brackets:
  # 7 digit | 6 digit | 400-200K | 200-125K | 125-75K | 75-50K | 50-30K |
  # 30-15K | 15K-5K | 5K-1K | 999-420 | 419-150 | 149-50 | 49-20 | 19-7 | 6-1
  elif game_mode == 3:
    return [
      1e6,
      4e5, 2e5, 1.25e5,
      7.5e4, 5e4, 3e4, 1.5e4,
      5e3, 1e3,
      420, 150,
      50, 20,
      7, 1
    ]

# bracket_low_thresh_desc_lst must be sorted in desc order, otherwise shit
# breaks here, and also in the main method when checking for close-rank players
def tier_finder_helper(rank, bracket_low_thresh_desc_lst):
  for i in range(len(bracket_low_thresh_desc_lst)):
    if rank >= bracket_low_thresh_desc_lst[i]:
      return i

# use protection kids
def get_std_tier(rank):
  bracket_low_thresh_desc_lst = get_bracket(0)
  return tier_finder_helper(rank, bracket_low_thresh_desc_lst)

def get_taiko_tier(rank):
  bracket_low_thresh_desc_lst = get_bracket(1)
  return tier_finder_helper(rank, bracket_low_thresh_desc_lst)

def get_ctb_tier(rank):
  bracket_low_thresh_desc_lst = get_bracket(2)
  return tier_finder_helper(rank, bracket_low_thresh_desc_lst)

def get_mania_tier(rank):
  bracket_low_thresh_desc_lst = get_bracket(3)
  return tier_finder_helper(rank, bracket_low_thresh_desc_lst)

def get_tier(rank, game_mode):
  if game_mode == 0:
    return get_std_tier(rank)
  elif game_mode == 1:
    return get_taiko_tier(rank)
  elif game_mode == 2:
    return get_ctb_tier(rank)
  elif game_mode == 3:
    return get_mania_tier(rank)

def print_mod_setup_info(tier_difference, higher_tier_player):
  if tier_difference == 0:
    print("BOTH PLAYERS ARE THE SAME TIER, DUKE IT OUT WITH WHATEVER MODS >:)")
  elif tier_difference > 0:
    print(higher_tier_player + " needs to add " + str(tier_difference)
      + " mods to satisfy requirements for the 1v1"
      + " - hope you're not too much of a dirty farmer >:)")

def main():
  anotha_one = True
  while(anotha_one):
    my_username = "LunarPalm"
    
    # tribute username from console input
    tribute_username = str(input("name of the next tribute: "))
    game_mode = int(str(input("what game mode? [0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania] : ")))
    
    tribute_rank = get_rank(tribute_username, game_mode)
    my_rank = get_rank(my_username, game_mode)
    
    tribute_tier = get_tier(tribute_rank, game_mode)
    my_tier = get_tier(my_rank, game_mode)
    
    # Remember only a max 4 of mod requirements
    tier_difference = min(abs(tribute_tier - my_tier), 4)
    higher_tier_player =(
      tribute_username if tribute_tier > my_tier else
      "" if tribute_tier == my_tier else my_username
    )
    
    # Check that both players aren't too close in rank - brackets are scuffed
    if tier_difference == 1:
      # Check that the rank difference is at least the range of the higher
      # ranked player's tier bracket. If it isn't, the players are in same tier
      mode_bracket = get_bracket(game_mode)
      max_tier = max(tribute_tier, my_tier)
      bracket_range = mode_bracket[max_tier-1] - mode_bracket[max_tier]
      if abs(tribute_rank - my_rank) <= bracket_range:
        higher_tier_player = ""
        tier_difference = 0
    
    print_mod_setup_info(tier_difference, higher_tier_player)
    
    anotha_one = True if str(input("anotha one? [y/n] : ")) == "y" else False

# run file from terminal with command `python3 matchmaker.py`
if __name__ == '__main__':
  # execute only if run as a script
  main()