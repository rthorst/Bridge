import csv, bridgetools


# INPUT: hand   hand object
#        idx    index of a player in list of players
# RETURNS:
#        seat   seat of that player to act i.e. 3 = 3rd to act.
def convert_idx_to_seat(hand, idx):
        opener_idx = bridgetools.get_dealer(hand.hh)
        curr_idx = opener_idx
        steps = 1
        while curr_idx != idx:
                steps += 1
                curr_idx += 1
                if curr_idx > 3:
                        curr_idx = 0
                
                
        seat = steps
        return seat

def return_whether_opener_side_win_contract(hand):
        # logic: convert opener, declarer to 0,1,2,3. Since 0,2 = S,N; 1,3 = W,E, then
        # iff opener wins contract, then opener %2 == declarer %2
        declarer = hand.declarer # i.e. "W"
        declarer_mod2 = bridgetools.REVPLAYERS[declarer] % 2  # since i.e. S=0, N=2, W=1, the logic
                # is that this must match opener_mod2.
        opener_mod2 = hand.opener % 2
        return int(declarer_mod2 == opener_mod2) # if true, opener's side wins contract
        

def get_opening_bid(hand):
        bidding = bridgetools.extract_bidding(hand.hh)  # i.e. ['p','p','1s'....]
        bidding_no_passes = [x for x in bidding if x != 'p']
        if len(bidding_no_passes) == 0:
                return "PASSOUT"
        else:
                return bidding_no_passes[0]

## VARS ##
infile = "sample.lin"
outfile = "sample_out.csv"

# Read infile and parse
lin = open(infile, 'r').read()
parse = bridgetools.parse_linfile(lin)

# Setup outfilie and write header.
of = open(outfile, 'wb')
w = csv.writer(of)
header = ['OPENER_SEAT','OPENERS_SIDE_WINS_CONTRACT','OPENING_IS_AT_1_LEVEL','A_PLAYER_FROM_TABLE']
w.writerow(header)

# Iterate over hands.
for hand in parse:

        # extract some info.
        opener_seat = convert_idx_to_seat(hand, hand.opener) # range: {1,4}
        opener_side_win_contract = return_whether_opener_side_win_contract(hand) # {0 or 1}
        opened_at_1_level = int(get_opening_bid(hand)[0] == "1") # {0 or 1}
        a_player_from_table = hand.players[0]

        # write.
        w.writerow([opener_seat,opener_side_win_contract, opened_at_1_level,
                    a_player_from_table])

        
        
        
        
