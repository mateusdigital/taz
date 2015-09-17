class GameFieldConstants:
    FIELD_TRACKS_Y   = [62, 94, 126, 158, 190, 222, 254, 285]; #The field tracks.
    FIELD_TRACKS_LEN = len(FIELD_TRACKS_Y);

    FIELD_HARD_LEFT  = -22;  #Right most positions when other stuff can go.
    FIELD_HARD_RIGHT = 500;  #Left  most positions when other stuff can go.

    FIELD_SOFT_LEFT  = 33;   #Left  most position that Taz can go.
    FIELD_SOFT_RIGHT = 440;  #Right most position that Taz can go.


    TAZ_INITIAL_TRACK_INDEX = (FIELD_TRACKS_LEN / 2);
    TAZ_INITIAL_POSITION_X  = (FIELD_HARD_RIGHT + FIELD_SOFT_LEFT) / 2;
    TAZ_INITIAL_POSITION_Y  = FIELD_TRACKS_Y[TAZ_INITIAL_TRACK_INDEX];
