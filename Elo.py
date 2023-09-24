import pandas as pd
from Data import results_df, ratings_df


def compute_EY(RY, RP):
    EY = 1 / (1 + 10 ** ((RP - RY) / 1000))

    return EY


def compute_EP(EY):
    EP = 1 - EY

    return EP


def update_RY(RY, SA, EY, K):
    RY = RY + K * (SA - EY)

    return RY


def update_RP(RP, SB, EP, K):
    RP = RP + K * (SB - EP)

    return RP


def calculate_K(win_score, lose_score, game_type):
    pointDiff = win_score - lose_score

    if game_type == "2v2":
        if pointDiff < 6:
            K = 40 * (pointDiff / 3)

        else:
            K = 100

    else:
        if pointDiff < 10:
            K = 22 * (pointDiff / 3)

        else:
            K = 100

    return K


def get_game_type(YO, YD, PO, PD):
    if YO == YD and PO == PD:
        return "1v1"

    else:
        return "2v2"


def get_correct_ratings(R, YO, YD, PO, PD):
    RYO, RYD, RPO, RPD = (
        R.loc[R["Name"] == YO, "OFF Rating"],
        R.loc[R["Name"] == YD, "DEF Rating"],
        R.loc[R["Name"] == PO, "OFF Rating"],
        R.loc[R["Name"] == PD, "DEF Rating"],
    )
    return RYO, RYD, RPO, RPD


def get_average_ratings(RYO, RYD, RPO, RPD, game_type):
    if game_type == "1v1":
        RY, RP = RYO, RPO
        return RY, RP

    elif game_type == "2v2":
        RY, RP = (RYO + RYD) / 2, (RPO + RPD) / 2

        return RY, RP


def compute_ratings(DF):
    ratings_df[ratings_df.columns.difference(["Name"])] = 1000

    for (
        index,
        row,
    ) in (
        DF.iterrows()
    ):  # for each game, update the ratings based upon the result of the game
        # Extract Names From Game
        YO, YD, PO, PD = (
            results_df["Yellow Offense"].loc[index],
            results_df["Yellow Defense"].loc[index],
            results_df["Purple Offense"].loc[index],
            results_df["Purple Defense"].loc[index],
        )

        # get game type 1v1 or 2v2
        game_type = get_game_type(YO, YD, PO, PD)

        # get the game result and K

        yellow_score = int(results_df["Yellow Score"].loc[index])
        purple_score = int(results_df["Purple Score"].loc[index])

        if yellow_score - purple_score > 0:
            SY, SP = 1, 0
            K = calculate_K(yellow_score, purple_score, game_type)
        else:
            SY, SP = 0, 1
            K = calculate_K(purple_score, yellow_score, game_type)

        # get ratings
        RYO, RYD, RPO, RPD = get_correct_ratings(ratings_df, YO, YD, PO, PD)

        RY, RP = get_average_ratings(RYO, RYD, RPO, RPD, game_type)

        # calc probabilities
        EY = compute_EY(RY, RP)
        EP = compute_EP(EY)

        print(K, EY, EP)

        # update Yellow Offense
        ratings_df.loc[ratings_df["Name"] == YO, "OFF Rating"] = update_RY(
            RYO, SY, EY, K
        )

        # update yellow defense
        ratings_df.loc[ratings_df["Name"] == YD, "DEF Rating"] = update_RY(
            RYD, SY, EY, K
        )

        # update purple offense
        ratings_df.loc[ratings_df["Name"] == PO, "OFF Rating"] = update_RP(
            RPO, SP, EP, K
        )

        # update purple defense
        ratings_df.loc[ratings_df["Name"] == PD, "DEF Rating"] = update_RP(
            RPD, SP, EP, K
        )


compute_ratings(results_df)

print(ratings_df)
