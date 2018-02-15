##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : taz.py                                                        ##
##  Project   : Game_Taz                                                      ##
##  Date      : Sep 02, 2015                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2015 - 2018                                      ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

################################################################################
## Imports                                                                    ##
################################################################################
## Pygame ##
import pygame.locals;
## Project ##
import assets;
import input;
from cowclock import *;

def clip(cur, min, max):
    if(cur < min): return min;
    if(cur > max): return max;

    return cur;

class Taz():
    ############################################################################
    ## Constatns                                                              ##
    ############################################################################
    ## Public ##
    STATE_ALIVE = 0;
    STATE_DYING = 1;
    STATE_DEAD  = 2;
    MAX_LIVES   = 3;

    ## Private ##
    _FRAMES                = None;
    _FRAMES_COUNT          = 2;
    _ANIMATION_INVERVAL    = 0.15;
    _CHANGE_TRACK_INTERVAL = 0.10;
    _DEATH_INTERVAL        = 1.00;
    _SPEED                 = 400;


    ############################################################################
    ## Static Methods                                                         ##
    ############################################################################
    @staticmethod
    def LoadAssets():
        if(Taz._FRAMES is not None):
            return;

        Taz._FRAMES = [];
        for i in xrange(0, Taz._FRAMES_COUNT):
            Taz._FRAMES.append(assets.load_image("TazFrame%d.png" %(i)));

    @staticmethod
    def GetFrame(index):
        return Taz._FRAMES[index];


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self,
                 min_bounds, max_bounds,
                 tracks_count, track_offset,
                 is_playable,
                 dead_animation_callback = None):
        ## Pre init
        Taz.LoadAssets();

        ## Housekeeping
        self._state       = Taz.STATE_ALIVE;
        self._lives       = Taz.MAX_LIVES;
        self._eat_count   = 0;
        self._is_playable = is_playable;

        ## Frames / Animation
        self._animation_timer         = None;
        self._death_timer             = None;
        self._frame_size              = None;
        self._dead_animation_callback = dead_animation_callback;

        ## Movement / Bounds
        self._curr_track_index   = 0;
        self._can_change_track   = False;
        self._min_bounds         = min_bounds;
        self._max_bounds         = max_bounds;
        self._tracks_count       = tracks_count;
        self._track_offset       = track_offset;
        self._position           = [max_bounds[0] * 0.5, min_bounds[1]];
        self._track_change_timer = None;

        ## Complete initialization.
        self._init_frames();
        self._init_timers();


    ############################################################################
    ## Public Functions                                                       ##
    ############################################################################
    ## Eat
    def make_eat(self):
        if(self._state != Taz.STATE_ALIVE):
            return;

        self._eat_count += 1;

    def get_eat_count(self):
        return self._eat_count;


    ## Actions
    def kill(self):
        if(self._state != Taz.STATE_ALIVE):
            return;

        self._state = Taz.STATE_DYING;
        self._death_timer.start();

    def reset(self):
        self._state = Taz.STATE_ALIVE;


    ## Lives
    def get_lives(self):
        return self._lives;


    ## State
    def set_state(self, state):
        self._state = state;

    def get_state(self):
        return self._state;


    ## Position / Size
    def set_position(self, x, y):
        self._position = [x, y];

    def get_size(self):
        return self._frame_size;

    def get_hit_box(self):
        return pygame.Rect(self._position, self._frame_size);


    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        ## Timers
        self._animation_timer.update   (dt);
        self._track_change_timer.update(dt);
        self._death_timer.update       (dt);

        ## There's anything to do if Taz is dying or dead
        ## (or if it is not playable)...
        if(self._state != Taz.STATE_ALIVE or not self._is_playable):
            return;

        ## Movement
        ## Vertical - Track Based
        if(input.is_down(input.KEY_MOVEMENT_DOWN) and self._change_track_is_ok()):
            self._curr_track_index += 1;
        elif(input.is_down(input.KEY_MOVEMENT_UP) and self._change_track_is_ok()):
            self._curr_track_index -= 1;

        ## Horizontal - Pixel/sec Based
        if(input.is_down(input.KEY_MOVEMENT_LEFT)):
            self._position[0] -= Taz._SPEED * dt;
        elif(input.is_down(input.KEY_MOVEMENT_RIGHT)):
            self._position[0] += Taz._SPEED * dt;

        ## Maintain the Taz into GameField
        self._curr_track_index = clip(self._curr_track_index,
                                      0,
                                      self._tracks_count -1);

        self._position[0] = clip(self._position  [0],
                                 self._min_bounds[0],
                                 self._max_bounds[0]);


        ## Update the vertical position based upon which track he is.
        self._position[1] = (self._curr_track_index * self._track_offset) \
                            + self._min_bounds[1];



    def draw(self, surface):
        ## Do not draw Taz when he's dead.
        if(self._state == Taz.STATE_DEAD):
            return;

        index       = self._animation_timer.get_tick_count() % Taz._FRAMES_COUNT;
        taz_surface = Taz.GetFrame(index);

        ## When is dying draw Taz scaled horizontally.
        if(self._state == Taz.STATE_DYING):
            taz_surface = pygame.transform.scale(
                                taz_surface,
                                (self._frame_size[0] * 2, self._frame_size[1])
                          );

        surface.blit(taz_surface, self._position);


    ############################################################################
    ## Private Methods                                                        ##
    ############################################################################
    ## Inits ##
    def _init_frames(self):
        self._frame_size = Taz.GetFrame(0).get_size();

        ## Update the max bounds, taking off the size of the taz sprite.
        ## this ease the calculation of taz bounds because we don't need
        ## to subtract it's size every time.
        self._max_bounds[0] -= self._frame_size[0];
        self._max_bounds[1] -= self._frame_size[1];


    def _init_timers(self):
        ## Animation
        self._animation_timer = CowClock(
                                    time         = Taz._ANIMATION_INVERVAL,
                                    repeat_count = CowClock.REPEAT_FOREVER,
                                );

        self._animation_timer.start();

        ## Track Change
        self._track_change_timer = CowClock(Taz._CHANGE_TRACK_INTERVAL);

        ## Death
        self._death_timer = CowClock(
                                time          = Taz._DEATH_INTERVAL,
                                done_callback = self._on_death_timer_done
                            );


    ## Movement
    def _change_track_is_ok(self):
        ## We only let Taz move the track if the timer
        ## has expired.
        is_ok = not self._track_change_timer.is_enabled();
        if(is_ok):
            self._track_change_timer.start();

        return is_ok;


    ## Timer Callbacks
    def _on_death_timer_done(self):
        self._state = Taz.STATE_DEAD;
        self._lives -= 1;

        self._dead_animation_callback();
