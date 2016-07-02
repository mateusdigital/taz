################################################################################
## Imports                                                                    ##
################################################################################
## Pygame ##
import pygame;
## Game_Taz ##
import assets;
import director;
from cowclock import *;


class Enemy:
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    _SPEED      = 120;
    _NEXT_SPEED = 120;

    _SURFACES = None;

    _SURFACE_TYPE_FOOD   = 0;
    _SURFACE_TYPE_CAUGHT = 1;
    _SURFACE_TYPE_BOMB   = 2;

    _OUT_OF_BOUNDS_INTERVAL_MIN = 0.4; #COWTODO: TWEAK
    _OUT_OF_BOUNDS_INTERVAL_MAX = 2.5; #COWTODO: TWEAK
    _CAUGHT_INTERVAL            =   1; #COWTODO: TWEAK


    ############################################################################
    ## Static Methods                                                         ##
    ############################################################################
    @staticmethod
    def LoadAssets():
        if(Enemy._SURFACES is None):
            print "LOADING ENEMY SURFACE"
            Enemy._SURFACES = [
                assets.load_image("Food.png"  ),
                assets.load_image("Caught.png"),
                assets.load_image("Bomb.png"  )
            ];

    @staticmethod
    def GetSurface(type):
        return Enemy._SURFACES[type];

    @staticmethod
    def Accelerate(ammount):
        Enemy._NEXT_SPEED += ammount;

    @staticmethod
    def GetNextSpeed():
        return Enemy._NEXT_SPEED;


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def __init__(self,
                 min_bounds, max_bounds,
                 tracks_count, track_offset,
                 track_index):
        ## Pre init
        Enemy.LoadAssets();

        ## Housekeeping
        self._type                      = None;
        self._reset_out_of_bounds_timer = None;
        self._reset_caught_timer        = None;

        ## Surface
        self._surface = None;

        ## Movement / Bounds
        self._position     = [0, 0];
        self._speed        = Enemy.GetNextSpeed();
        self._min_bounds   = min_bounds;
        self._max_bounds   = max_bounds;
        self._tracks_count = tracks_count;
        self._track_offset = track_offset;
        self._track_index  = track_index;

        ## Complete initialization.
        self._init_timers();
        self.reset();



    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def check_collision(self, other_rect):
        ## We can pass through the caught foods.
        if(self._type == Enemy._SURFACE_TYPE_CAUGHT):
            return False;

        this_rect = pygame.Rect(self._position, self._surface.get_size());
        collided  = this_rect.colliderect(other_rect);

        ## Collision with the Food.
        ## Make it a Food Caught
        if(collided and self._type == Enemy._SURFACE_TYPE_FOOD):
            self._type = Enemy._SURFACE_TYPE_CAUGHT;
            self._reset_caught_timer.start();

        return collided;


    def is_fatal(self):
        return self._type == Enemy._SURFACE_TYPE_BOMB;


    def reset(self):
        self._speed = Enemy.GetNextSpeed();

        self._decide_type     ();
        self._decide_direction();


        ## Reset the Out of Bounds timer.
        out_time = director.randfloat(
                        Enemy._OUT_OF_BOUNDS_INTERVAL_MIN,
                        Enemy._OUT_OF_BOUNDS_INTERVAL_MAX
                   );

        self._reset_out_of_bounds_timer = CowClock(
            time          = out_time,
            done_callback = self.reset
        );

        print "Now speed is:", self._speed;


    ############################################################################
    ## Update / Draw                                                          ##
    ############################################################################
    def update(self, dt):
        ## Timers
        self._reset_out_of_bounds_timer.update(dt);
        self._reset_caught_timer.update       (dt);

        ## Enemy reset cooldown is active, we don't need to anything more...
        if(self._reset_out_of_bounds_timer.is_enabled() or \
           self._reset_caught_timer.is_enabled()):
            return;

        ## Position
        self._position[0] += (self._speed * dt);

        ## Check Boundaries
        if(self._speed > 0 and self._position[0] > self._max_bounds[0]):
            self._reset_out_of_bounds_timer.start();

        elif(self._speed < 0 and self._position[0] < self._min_bounds[0]):
            self._reset_out_of_bounds_timer.start();


    def draw(self, surface):
        if(self._reset_out_of_bounds_timer.is_enabled()):
            return;

        self._surface = Enemy.GetSurface(self._type);
        surface.blit(self._surface, self._position);


    ############################################################################
    ## Private Methods                                                        ##
    ############################################################################
    def _init_timers(self):
        ## Caught
        self._reset_caught_timer = CowClock(
            time          = Enemy._CAUGHT_INTERVAL,
            done_callback = self.reset
        );


    def _decide_type(self):
        is_bomb = director.randbool();
        if(is_bomb):
            self._type = Enemy._SURFACE_TYPE_BOMB;
        else:
            self._type = Enemy._SURFACE_TYPE_FOOD;


    def _decide_direction(self):
        ## Y Position
        self._position[1] = (self._track_index * self._track_offset) \
                            + self._min_bounds[1];

        ## X Position, depends on the direction of movement.
        ## If Enemy is moving to Right it starts on LEFT
        ## If Enemy is moving to Left  it starts on Right
        move_to_right = director.randbool();
        if(move_to_right):
            self._position[0] = self._min_bounds[0];
            self._speed       = abs(self._speed);
        else:
             self._position[0] = self._max_bounds[0];
             self._speed     = -(abs(self._speed));
