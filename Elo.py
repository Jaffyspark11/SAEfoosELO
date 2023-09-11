import pandas as pd


def compute_EA(RA, RB):

    EA = 1/(1+10**((RB-RA)/400))
    
    return EA


def compute_EB(EA):
    
    EB = 1-EA
    
    return EB


def update_RA(RA, SA, EA, K=16):

    RA = RA + K*(SA-EA)
    
    return RA


def update_RB(RB, SB, EB, K=16):
    
    RB = RB + K*(SB-EB)
    
    return RB


def compute_ratings(G, n, K=16):
    R = [400]*n # initialize the ratings of all players with 400
    for index, row in G.iterrows(): # for each game, update the ratings based upon the result of the game
        A,B = row["win_ID"], row["lose_ID"] # # extract the player IDs as A and B
        SA,SB = 1,0 # the game result: Player A wins, Player B loses
        
        RA, RB = R[A], R[B]

        EA = compute_EA(RA, RB)
        EB = compute_EB(EA)

        R[A] = update_RA(RA, SA, EA, K)
        R[B] = update_RB(RB, SB, EB, K)
    
    return R