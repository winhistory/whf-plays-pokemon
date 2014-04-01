import irc.bot
import time

IRC_SERVER = "irc.rizon.net"
IRC_PORT   = 6667

IRC_CHANNEL = "#whfspieltpokemon"
IRC_NICKNAME = "Quappot"
IRC_ALTNICK  = "Bibot"

ANARCHY   = "anarchy"
DEMOCRACY = "democracy"

KEY_DELAY = 0.1

class XKeyEmitter:

    subprocess = __import__('subprocess')

    KEYMAP = {
        "up"    : "Up",
        "down"  : "Down",
        "left"  : "Left",
        "right" : "Right",
        "a"     : "Z",
        "b"     : "X",
        "start" : "Return",
    }
    
    # Important: xdotools must be installed and vbam-cli must be running
    def emit(self, key):
        try:
            wid = self.subprocess.check_output(
                [ "xdotool", "search", "--class", "vbam"]
            ).strip()
            self.subprocess.call(
                [ "xdotool", "keydown", "--window", wid, self.KEYMAP[key] ]
            )
            time.sleep(KEY_DELAY)
            self.subprocess.call(
                [ "xdotool", "keyup", "--window", wid, self.KEYMAP[key] ]
            )
        except self.subprocess.CalledProcessError:
            print("error: could not find window id for 'vbam'")

class UInputEmitter:

    uinput = __import__('uinput')

    KEYMAP = {
        "up"    : uinput.KEY_UP,
        "down"  : uinput.KEY_DOWN,
        "left"  : uinput.KEY_LEFT,
        "right" : uinput.KEY_RIGHT,
        "a"     : uinput.KEY_Z,
        "b"     : uinput.KEY_X,
        "start" : uinput.KEY_ENTER,
    }

    # Important: uniput module must have been loaded, and current user must
    # have write access to /dev/uinput - otherwise this will fail.
    keyboard = uinput.Device(KEYMAP.values())
    
    def emit(self, key):
        self.keyboard.emit(self.KEYMAP[key], 1)
        time.sleep(KEY_DELAY)
        self.keyboard.emit(self.KEYMAP[key], 0)

class PokemonBot(irc.bot.SingleServerIRCBot):

    def __init__(self, key_emitter):
        irc.bot.SingleServerIRCBot.__init__(
            self, [(IRC_SERVER, IRC_PORT)], 
            IRC_NICKNAME, IRC_NICKNAME
        )
        
        self.connection.buffer_class.errors = 'replace'

        self.key_emitter = key_emitter
        
        self.mode = "anarchy"
        self.democracy_ballot = {}
        self.democracy_timeout = 15

    def on_nicknameinuse(self, c, e):
        c.nick(IRC_ALTNICK)

    def on_welcome(self, c, e):
        c.join(IRC_CHANNEL)

    def on_pubmsg(self, c, e):
        # split channel message by whitespace
        args = e.arguments[0].split()
        
        # if args empty, return
        if not args: return
        
        # first word is command
        cmd = args[0].lower()
        
        # key command
        if cmd in self.key_emitter.KEYMAP:
            if self.mode == DEMOCRACY:
                self.democracy_ballot[e.source.nick] = cmd
            else:
                self.emit_key(e.source.nick, cmd)
        
        
        # !cmd for channel operators
        elif len(cmd) > 1 and cmd[0] == '!':
            # get channel object
            chan = self.channels[e.target]
            # check if source was operator
            if not chan.is_oper(e.source.nick): return
        
            # dispatch command "!foobar" to "cmd_foobar"
            cb = "cmd_" + cmd[1:]
            if hasattr(self, cb) and callable(getattr(self, cb)):
                method = getattr(self, cb)
                method(args, c, e)
                
    def emit_key(self, user, key):
        self.key_emitter.emit(key)
        print("{:>16} : {}".format(user, key))

    # Commands available for channel operators:
    
    def cmd_die(self, args, c, e):
        print(e.source.nick, "!die")
        self.die()
        
    def cmd_mode(self, args, c, e):
        if len(args) < 2 or args[1] not in (DEMOCRACY, ANARCHY):
            c.privmsg(e.target, "!mode [democracy|anarchy]")
            return
        
        c.privmsg(e.target, "set mode to: " + self.mode)
        self.mode = args[1]
        
        if self.mode == DEMOCRACY:
            self.schedule_democracy(c, e)

    def cmd_timeout(self, args, c, e):
        try:
            timeout = int(args[1])
            if timeout < 1 or timeout > 120: raise ValueError()
        except (IndexError, ValueError):
            c.privmsg(e.target, "!timeout [1-120]")
            return

        c.privmsg(e.target, 
            "set democracy timeout for next round to: {} sec".
            format(timeout)
        )
        self.democracy_timeout = timeout
        
    # Helper functions for democracy mode

    def schedule_democracy(self, c, e):
        self.democracy_ballot = {}
        c.privmsg(e.target, 
            "Neue Demokratie-Periode! {} Sekunden bis zur nächsten Wahl.".
            format(self.democracy_timeout)
        )
        self.ircobj.execute_delayed(self.democracy_timeout, self.on_democracy, (c,e))

    def on_democracy(self, c, e):
        if self.mode != DEMOCRACY: return

        # no votes? reschedule and return
        if self.democracy_ballot:
            # elect winner
            papers = list(self.democracy_ballot.values())
            winner = max(set(papers), key=papers.count)
            self.emit_key("[✘] Demokratie", winner)

        self.schedule_democracy(c, e)

#
# main
#
PokemonBot(UInputEmitter()).start()
