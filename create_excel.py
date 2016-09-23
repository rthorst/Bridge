import csv, bridgetools
import numpy as np

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

# given 2 hand objects, return IMP swing: positive value means NS gain IMPs.
def calc_imp_swing(hand1, hand2):

        # calculate point_swing. If negative reverse it and create boolean reverse_imp_swing = True
        point_swing = (hand1.score - hand2.score)
        reverse_imp_swing = False # if true flip the sign of point swing but return negative.
        if point_swing < 0 : # negative imp swing? reverse sign but later change.
                point_swing = -point_swing
                reverse_imp_swing = True
        # setup IMPS table.
        min_scores = [0,20,50,90,130,170,220,270,320,370,430,500,600,750,900,
                      1100,1300,1500,1750,2000,2250,2500,3000,3500,4000,99999999999]
        imps = range(0,26)

        # return IMP swing
        for (min_score, max_score, imps) in zip(min_scores[:-1], min_scores[1:], imps[:-1]):
                if ((point_swing >= min_score) & (point_swing < max_score)):
                        imp_swing = imps
                        if reverse_imp_swing:
                                imp_swing = - imps
                        return imp_swing



## VARS ##
infile = "sample.lin"
outfile = "sample_out.csv"
head_to_head_match = True # if true, expects lin of 2 tables i.e. Hand#16 table 1 -- Hand#16 table 2 --
                          #  Hand#16 table 1 etc

# Read infile and parse, reshaping parse to pairs of same hand played at both tables.
lin = open(infile, 'r').read()
parse = bridgetools.parse_linfile(lin)
parse = np.reshape(parse, (len(parse)/2, 2))

# Setup outfilie and write header.
of = open(outfile, 'wb')
w = csv.writer(of)
header = ['HAND_NUMBER','ROOM_NUMBER','OPENER_SEAT','OPENERS_SIDE_WINS_CONTRACT','OPENING_IS_AT_1_LEVEL',
          'CONTRACT','IMP_SWING','A_PLAYER_FROM_TABLE']
w.writerow(header)

# Iterate over single hand played at both tables.
hand_num = 1
for (hand_table1, hand_table2) in parse:

        # extract info pertaining to both hands, i.e. IMP swing.
        imp_swing = calc_imp_swing(hand_table1, hand_table2)

        # extract info pertaining to each hand individually and write IMP swing.
        room_num = 1
        for hand in (hand_table1, hand_table2):
                opener_seat = convert_idx_to_seat(hand, hand.opener) # range: {1,4}
                opener_side_win_contract = return_whether_opener_side_win_contract(hand) # {0 or 1}
                opened_at_1_level = int(get_opening_bid(hand)[0] == "1") # {0 or 1}
                a_player_from_table = hand.players[0]
                contract = hand.contract[0]

                # write.
                w.writerow([hand_num, room_num, opener_seat,opener_side_win_contract, opened_at_1_level, contract,
                            imp_swing, a_player_from_table])

                # increment room number
                room_num += 1

        # increment hand num
        hand_num += 1
        
        
