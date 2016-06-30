# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        sound.py                                  ##
##            █ █        █ █        Game_RamIt                                ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2016                        ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##
################################################################################
## Source Notice:                                                             ##
##                                                                            ##
##  _generateTone function was inspired and hacked from:                      ##
##      pitch perfect by Sean McKean                                          ##
##      https://code.google.com/archive/p/pitch-perfect/                      ##
##                                                                            ##
##  The original copyright notice is represented bellow:                      ##
##                                                                            ##
## generate.py : contains tone-generating function                            ##
##                                                                            ##
## Copyright (C) 2010  Sean McKean                                            ##
##                                                                            ##
## This program is free software: you can redistribute it and/or modify       ##
## it under the terms of the GNU General Public License as published by       ##
## the Free Software Foundation, either version 3 of the License, or          ##
## (at your option) any later version.                                        ##
##                                                                            ##
## This program is distributed in the hope that it will be useful,            ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of             ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              ##
## GNU General Public License for more details.                               ##
##                                                                            ##
## You should have received a copy of the GNU General Public License          ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>.      ##
##                                                                            ##
################################################################################


################################################################################
## Imports                                                                    ##
################################################################################
## Python ##
import sys;
import os;
import random;
## Pygame ##
import pygame;
## NumPy /SciPy ##
import numpy as np;
## Game_RamIt ##
import assets;
from constants import *;


################################################################################
## Constants                                                                  ##
################################################################################
WAVE_SQUARE = "square";
WAVE_SAW    = "saw";
WAVE_SINE   = "sine";

_VOLUME_HI  = 1.0;
_VOLUME_MED = 0.5;
_VOLUME_LOW = 0.2;


PRE_INIT_FREQUENCY = 22050;
PRE_INIT_SIZE      =   -16;
PRE_INIT_CHANNELS  =     1;
PRE_INIT_BUFFER    =   512;


################################################################################
## Private Functions                                                          ##
################################################################################
def _generateTone(freq, wave, play_frames,
                  vol       = 1,
                  add_noise = False):

    (pb_freq, pb_bits, pb_chns) = pygame.mixer.get_init();
    length = GAME_FRAME_SEC * play_frames;

    multiplier = int(freq * length);
    length     = max(1, int(float(pb_freq) / freq * multiplier));
    lin        = np.linspace(0.0, multiplier, length, endpoint=False);

    ## Generate the waves.
    if(wave == WAVE_SINE):
        ary = np.sin(lin * 2.0 * np.pi);

    elif(wave == WAVE_SAW):
        ary = 2.0 * ((lin + 0.5) % 1.0) - 1.0;

    elif(wave == WAVE_SQUARE):
        ary = np.zeros(length);
        ary[lin % 1.0 < 0.5]  = 1.0;
        ary[lin % 1.0 >= 0.5] = -1.0;


    ## Noise
    if(add_noise):
        noise = np.random.normal(0, 1, length);
        ary = ary + noise;

    ## If mixer is in stereo mode, double up the array
    ## information for each channel.
    if pb_chns == 2:
        ary = np.repeat(ary[..., np.newaxis], 2, axis=1)


    buffer = None;
    ## 8 Bits
    if(pb_bits == 8):
        snd_ary = ary * vol * 127.0;
        buffer  = (snd_ary.astype(np.uint8) + 128);
    ## 16 Bits
    elif(pb_bits == -16):
        snd_ary = ary * vol * float((1 << 15) - 1);
        buffer  = (snd_ary.astype(np.int16));

    return buffer;


def _play_buffer(channel, buffer):
    sound_buffer = pygame.sndarray.make_sound(buffer);
    channel      = pygame.mixer.Channel(channel);

    unused_channel = pygame.mixer.find_channel();
    if(unused_channel is not None):
        channel = unused_channel;
    # else:
        #print "- Cannot find a unused channel -"

    if(channel.get_busy()):
        channel.queue(sound_buffer);
    else:
        channel.play(sound_buffer);


def _play_sound(channel, frequency, wave_type,
                frames_count, add_noise, volume):

    tone = _generateTone(freq        = frequency,
                        wave        = wave_type,
                        play_frames = frames_count,
                        vol         = volume,
                        add_noise   = add_noise);

    _play_buffer(channel, tone);


################################################################################
## Init                                                                       ##
################################################################################
def pre_init():
    pygame.mixer.pre_init(PRE_INIT_FREQUENCY,
                          PRE_INIT_SIZE,
                          PRE_INIT_CHANNELS,
                          PRE_INIT_BUFFER);



################################################################################
## Stop                                                                       ##
################################################################################
def stop_all_sounds():
    pass;
    #COWTODO: Implement...


################################################################################
## Intro                                                                      ##
################################################################################
def play_intro():
    pygame.mixer.Sound(assets.build_path("amazing_intro.wav")).play();




################################################################################
##                                                                            ##
################################################################################
def play_frequency(freq, duration, wave_type = WAVE_SQUARE, noise = False):
    _play_sound(channel      = 0,
                frequency    = freq,
                wave_type    = WAVE_SQUARE,
                frames_count = GAME_FRAME_MS * duration,
                add_noise    = noise,
                volume       = _VOLUME_LOW);
