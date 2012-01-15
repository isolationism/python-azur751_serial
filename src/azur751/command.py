#!/usr/bin/python

"""
A library for controlling a Cambridge Audio Azur 751BD Blu-Ray Player.
"""

# Python modules
from time import sleep
from sys import exit

# Third-party modules
import serial


class CommandError(ValueError):
    """Raised if a command is not accepted by the unit"""
    pass


class Azur751BD(object):
    """
    Class for controlling a Cambridge Audio Azur 751BD model blu-ray player.
    """

    command_interval = 0.07

    verbose_mode = {
        '0': 'Off',
        '1': 'Echo Commands',
        '2': 'Report major status changes (unsolicited)',
        '3': 'Report playback time every second (unsolicited)',
    }

    repeat_mode = {
        '00': 'Off',
        '01': 'Repeat once',
        '02': 'Repeat chapter',
        '03': 'Repeat All',
        '04': 'Repeat Title',
        '05': 'Shuffle',
        '06': 'Random',
    }

    zoom_mode = {
        '00': 'Off',
        '01': 'Stretch',
        '02': 'Full',
        '03': 'Underscan',
        '04': '1.2',
        '05': '1.3',
        '06': '1.5',
        '07': '2',
        '08': '3',
        '09': '4',
        '10': '1/2',
        '11': '1/3',
        '12': '1/4',
        '13': 'Pillar Box',
    }

    hdmi_resolutions = {
        'SDI': "Standard Definition (interlaced)",
        'SDP': "Standard Definition (progressive)",
        '720P': "720 vertical lines (progressive)",
        "1080I": "1080 vertical lines (interlaced)",
        "1080P": "1080 vertical lines (progressive)",
        "SRC": "Source direct",
        "AUTO": "Automatic",
    }

    def __init__(self, serial_port='/dev/ttyS0'):
        # Creates an (active) serial connection.
        self.__conn = serial.Serial(port=serial_port, baudrate=9600,
                                    bytesize=8, parity='N', stopbits=1,
                                    timeout=0.2)

    def _cmd(self, command, parameters=None):
        """Issues a low-level command to the player, returning the response
        code. CommandError is raised if the command encounters an error."""
        if len(command) != 3:
            raise ValueError("command must be exactly 3 bytes")

        # Commands begin with a hash header
        cmd = "#%s" % (command.upper(),)

        # Not all cmds have params; if they do, separate from cmd with a space
        if parameters: cmd = "%s %s" % (cmd, parameters)

        self.__conn.write("%s\r" % cmd)
        self.__conn.flush()

        # Retrieve the command response; promises to be max 25 bytes
        response = self.__conn.read(25)

        # If an @ symbol is present but isn't the first character, slice.
        if response.find('@') > 0:
            response = response[response.find('@'):]

            # Incomplete response? Try to get the end.
            if response.find('\r') == -1: response += self.__conn.read(25)

        # The response is valid because it has both @ (start) and \r (done)
        try:
            valid = response[0] == '@' and response[-1:] == '\r'
        except IndexError:
            valid = False

        if not valid:
            self.__conn.timeout = 10 # Explicit max-reply timeout from manual.
            response = self.__conn.read(25)
            self.__conn.timeout = self.command_interval

        # If we still didn't get a response, raise an error.
        if not response: raise CommandError("No response received")

        # Get the result code, raising an error if one was received
        if response[1:2].upper() == 'ER':
            raise CommandError("Error: %s" % (response[3:-1],))

        # Return the contents of the response
        return response[3:-1].strip()

    def sleep(self, seconds=1):
        """Suspends operation for the defined number of seconds"""
        sleep(seconds)

    def power_toggle(self):
        """Toggles power mode"""
        return self._cmd('pow')

    def power_on(self):
        """Turns on power"""
        result = self._cmd('pon')
        self.sleep(25)
        return result

    def power_off(self):
        """Turns off power"""
        result = self._cmd('pof')
        self.sleep(10) # All lights go off around 9 seconds.
        return result

    def source(self):
        """Go to Internet Menu to select internet applications"""
        return self._cmd('src')

    def eject_toggle(self):
        """Toggles the eject status of the drive"""
        return self._cmd('ejt')

    def system_cycle(self):
        """Cycle through available TV output systems (NTSC, PAL, MULTI)"""
        return self._cmd('sys')

    def dim_cycle(self):
        """Cycle through dimmer states (ON, DIM, OFF)"""
        return self._cmd('dim')

    def pureaudio_toggle(self):
        """Toggle the pure audio mode"""
        return self._cmd('pur')

    def num1(self):
        """Numeric Key"""
        return self._cmd('nu1')

    def num2(self):
        """Numeric Key"""
        return self._cmd('nu2')

    def num3(self):
        """Numeric Key"""
        return self._cmd('nu3')

    def num4(self):
        """Numeric Key"""
        return self._cmd('nu4')

    def num5(self):
        """Numeric Key"""
        return self._cmd('nu5')

    def num6(self):
        """Numeric Key"""
        return self._cmd('nu6')

    def num7(self):
        """Numeric Key"""
        return self._cmd('nu7')

    def num8(self):
        """Numeric Key"""
        return self._cmd('nu8')

    def num9(self):
        """Numeric Key"""
        return self._cmd('nu9')

    def num0(self):
        """Numeric Key"""
        return self._cmd('nu0')

    def clr(self):
        """Clear numeric input"""
        return self._cmd('clr')

    def goto(self):
        """Play from a specific location"""
        return self._cmd('got')

    def home(self):
        """Go to the home menu to select a media source"""
        return self._cmd('hom')

    def page_up(self):
        """Go to previous page"""
        return self._cmd('pup')

    def page_down(self):
        """Go to next page"""
        return self._cmd('pdn')

    def osd_toggle(self):
        """Toggle OSD presence"""
        return self._cmd('osd')

    def top_menu(self):
        """Go to top menu"""
        return self._cmd('ttl')

    def menu(self):
        """Go to BD (pop-up) or DVD (main) menu"""
        return self._cmd('mnu')

    def up(self):
        """Up arrow"""
        return self._cmd('nup')

    def left(self):
        """Left arrow"""
        return self._cmd('nlt')

    def right(self):
        """Right arrow"""
        return self._cmd('nrt')

    def down(self):
        """Down arrow"""
        return self._cmd('ndn')

    def enter(self):
        """Enter/select button"""
        return self._cmd('sel')

    def setup(self):
        """Player setup"""
        return self._cmd('set')

    def previous(self):
        """Return to previous menu"""
        return self._cmd('ret')

    def red(self):
        """Red button"""
        return self._cmd('red')

    def green(self):
        """Green button"""
        return self._cmd('grn')

    def blue(self):
        """Blue button"""
        return self._cmd('blu')

    def yellow(self):
        """Yellow button"""
        return self._cmd('ylw')

    def stop(self):
        """Stop playback"""
        return self._cmd('stp')

    def play(self):
        """Start/resume playback"""
        return self._cmd('pla')

    def pause(self):
        """Pause playback"""
        return self._cmd('pau')

    def previous(self):
        """Skip to previous [track/chapter]"""
        return self._cmd('pre')

    def next(self):
        """Skip to next [track/chapter]"""
        return self._cmd('nxt')

    def fast_reverse(self):
        """Fast reverse play"""
        return self._cmd('rev')

    def fast_forward(self):
        """Fast forward play"""
        return self._cmd('fwd')

    def audio_language_cycle(self):
        """Cycles through available audio languages"""
        return self._cmd('aud')

    def subtitle_language_cycle(self):
        """Cycles through available subtitle languages"""
        return self._cmd('sub')

    def angle_cycle(self):
        """Cycles through available camera angles"""
        return self._cmd('ang')

    def zoom_cycle(self):
        """Zoom in/out and adjust aspect ratio"""
        return self._cmd('zom')

    def toggle_sap(self):
        """Toggle secondary audio program on/off"""
        return self._cmd('sap')

    def ab_repeat_cycle(self):
        """Repeat-play the selected section"""
        return self._cmd('atb')

    def repeat_cycle(self):
        """Repeat play"""
        return self._cmd('rpt')

    def pip_toggle(self):
        """Show/hide picture-in-picture"""
        return self._cmd('pip')

    def resolution_cycle(self):
        """Toggle through available output resolution(s)"""
        return self._cmd('hdm')

    def subtitle_shift(self):
        """Equivalent to pressing and holding the subtitle button; shifts the
        subtitle position"""
        return self._cmd('suh')

    def query_verbose_mode(self):
        """What is the current verbosity level"""
        return self._cmd('qvm')

    def query_power_status(self):
        return self._cmd('qpw')

    def query_firmware_version(self):
        return self._cmd('qvr')

    def query_hdmi_resolution(self):
        return self._cmd('qhd')

    def query_playback_status(self):
        return self._cmd('qpl')

    def query_track_title(self):
        return self._cmd('qtk')

    def query_chapter(self):
        return self._cmd('qch')

    def query_track_elapsed(self):
        return self._cmd('qte')

    def query_track_remaining(self):
        return self._cmd('qtr')

    def query_chapter_elapsed(self):
        return self._cmd('qce')

    def query_chapter_remaining(self):
        return self._cmd('qcr')

    def query_total_elapsed(self):
        return self._cmd('qel')

    def query_total_remaining(self):
        return self._cmd('qre')

    def query_disc_type(self):
        return self._cmd('qdt')

    def query_audio_type(self):
        return self._cmd('qat')

    def query_subtitle_type(self):
        return self._cmd('qst')

    def query_subtitle_shift(self):
        return self._cmd('qsh')

    def query_osd_position(self):
        return self._cmd('qop')

    def query_repeat_mode(self):
        return self._cmd('qrp')

    def query_zoom_mode(self):
        return self._cmd('qzm')

    def query_region_code(self):
        return self._cmd('qrg')

    def query_model_number(self):
        return self._cmd('qmd')

    def set_verbose_mode(self, mode):
        if mode not in [0, '0', 1, '1', 2, '2', 3, '3']:
            raise ValueError("Verbose mode not supported")
        return self._cmd('svm', mode)

    def set_hdmi_resolution(self, resolution):
        if resolution not in self.hdmi_resolutions.keys():
            raise ValueError("HDMI Resolution not supported")
        return self._cmd('shd', resolution)

    def set_output_system(self, output_system):
        if output_system not in ['NTSC', 'PAL', 'AUTO']:
            raise ValueError("Output System not supported")
        return self._cmd('spn', output_system)

    def set_zoom_ratio(self, ratio):
        if ratio not in ['1', 'AR', 'FS', 'US', '1.2', '1.3', '1.5', '2',
                         '1/2', '3', '4', '1/3', '1/4']:
            raise ValueError("Zoom ratio not supported")
        return self._cmd('szm', ratio)

    def set_repeat(self, repeat_mode):
        if repeat_mode not in ['CH', 'TT', 'ALL', 'OFF', 'SHF', 'RND']:
            raise ValueError("Repeat mode not supported")
        return self._cmd('srp', repeat_mode)

    def search(self, query):
        """Search mode. Multiple formats are accepted (but not validated):

        T3 - Search to Title 3
        C10 - Search to Chapter 10
        C 0:00:34 - Search to 0h 00m 34s of the current chapter/track
        T 0:12:13 - Search to 0h 12m 13s of the current title/disc
        0:12:13 - Same as immediately above
        """
        return self._cmd('srh', query)

    def direct_play(self):
        """No idea what this does."""
        return self._cmd('dpl')

    def reset(self):
        """Resets the current RS232 command; clears the command buffer."""
        return self._cmd('rst')

    def set_subtitle_shift(self, shift_value):
        """Sets the subtitle shift to an integer from -5 through 5."""
        if not isinstance(shift_value, int):
            raise TypeError("Subtitle shift must be an integer")
        if shift_value > 5 or shift_value < -5:
            raise ValueError("Subtitle shift must be between -5 and +5")
        return self._cmd('ssh', shift_value)

    def set_osd_position(self, osd_position):
        """Sets the OSD position"""
        if not isinstance(osd_position, int):
            raise TypeError("OSD position must be an integer")
        if osd_position > 5 or osd_position < 0:
            raise ValueError("OSD position must be between 0 and 5")

