from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

import os
import subprocess


class PrevFocus(object):
    """Store last focus per group and go back when called"""

    def __init__(self):
        self.focus = None
        self.old_focus = None
        self.groups_focus = {}
        hook.subscribe.client_focus(self.on_focus)

    def on_focus(self, window):
        group = window.group
        # only store focus if the group is set
        if not group:
            return
        group_focus = self.groups_focus.setdefault(group.name, {
            "current": None, "prev": None
        })
        # don't change prev if the current focus is the same as before
        if group_focus["current"] == window:
            return
        group_focus["prev"] = group_focus["current"]
        group_focus["current"] = window

    def __call__(self, qtile):
        group = qtile.current_group
        group_focus = self.groups_focus.get(group.name, {"prev": None})
        prev = group_focus["prev"]
        if prev and group.name == prev.group.name:
            group.focus(prev, False)

def switch_to_last_group(qtile: Qtile):
    qtile.current_screen.set_group(qtile.current_screen.previous_group)

def move_window(qtile: Qtile, *args):
    side = args[0]

    group = qtile.current_group
    windowList: List = group.windows
    if not qtile.current_window:
        return

    offset = 1 if side == "right" else -1

    windowIndex = windowList.index(qtile.current_window)

    temp = windowList[windowIndex + offset]
    windowList[windowIndex + offset] = windowList[windowIndex]
    windowList[windowIndex] = temp

    get_bar(qtile.current_screen, "top").draw()


def move_focus_to_neighbor(qtile: Qtile, *args):
    side = args[0]
    
    group = qtile.current_group
    windowList: List = group.windows

    offset = 1 if side == "right" else -1

    windowIndex = windowList.index(qtile.current_window)
    newWindowIndex = (windowIndex + offset) % len(windowList)

    group.focus(windowList[newWindowIndex])


def move_focus_to_index(qtile: Qtile, *args):
    index = args[0]
    group = qtile.current_group
    windowList: List = group.windows

    if len(windowList) > index:
        group.focus(windowList[index])


def get_bar(screen, position=None) -> bar.Bar:
    if not position:
        position = "bottom"
    bar = getattr(screen, position)
    return bar


mod = "mod4"

terminal = guess_terminal()

keys = [
    # Switch between windows
    #Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    #Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "Right", lazy.function(move_focus_to_neighbor, "right")),
    Key([mod], "Left",  lazy.function(move_focus_to_neighbor, "left")),

    Key(["mod1"], "1", lazy.function(move_focus_to_index, 0)),
    Key(["mod1"], "2", lazy.function(move_focus_to_index, 1)),
    Key(["mod1"], "3", lazy.function(move_focus_to_index, 2)),
    Key(["mod1"], "4", lazy.function(move_focus_to_index, 3)),
    Key(["mod1"], "5", lazy.function(move_focus_to_index, 4)),
    Key(["mod1"], "6", lazy.function(move_focus_to_index, 5)),
    Key(["mod1"], "7", lazy.function(move_focus_to_index, 6)),
    Key(["mod1"], "8", lazy.function(move_focus_to_index, 7)),
    Key(["mod1"], "9", lazy.function(move_focus_to_index, 8)),

    Key([mod], "d", lazy.spawn("dmenu_run -h 34")),

    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "Left", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "w", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "k", lazy.reload_config(), desc="Reload the config"),
    Key(["mod1"], "Tab", lazy.function(PrevFocus())),
    Key([mod], "Tab", lazy.function(switch_to_last_group)),

    Key(["mod1", "shift"], "Right", lazy.function(move_window, "right")),
    Key(["mod1", "shift"], "Left", lazy.function(move_window, "left")),

    Key([mod], "Escape", lazy.spawn("powerDown")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Max(),
    layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4, margin=6),
]

widget_defaults = dict(
    font='sans',
    fontsize=16,
    padding=6,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar([
            widget.TaskList(
                    highlight_method="block",
                    border="#243e80",
                    max_title_width=400
                    ),
            widget.Spacer(),
            widget.WidgetBox(widgets=[
                widget.Sep(),
                widget.TextBox(text="Network"),
                widget.NetGraph(),
                widget.Spacer(length=10),
                widget.TextBox(text="CPU"),
                widget.CPUGraph(),
                widget.Spacer(length=10),
                widget.TextBox(text="Memory"),
                widget.Memory(),

            ],
                text_closed="Sys info [>]  ",
                text_open="[>]  "

            ),
            widget.Sep(),
            widget.Net(),
            widget.Sep(),
            widget.Wttr(location={"CPH": "CPH"}, format="CPH:  %t  %c  %m  %p")
        ],
            34,
            background="#1f1d1d"
        ),
        bottom=bar.Bar(
            [
                widget.Sep(),
                widget.GroupBox(),
                widget.Sep(),
                widget.CurrentLayoutIcon(),
                widget.Sep(),
                widget.Notify(
                    default_timeout=10,
                    parse_text=lambda e: "Notification -> " + e,
                    foreground="ff0000",
                ),
                widget.Prompt(),
                widget.Spacer(),
                widget.CheckUpdates(
                    distro="Ubuntu",
                    colour_no_updates="00ff00",
                    execute="sudo apt update",
                    no_update_string="0 Updates",
                    custom_command="apt list --upgradable",
                    custom_command_modify=lambda e: e - 1,
                    mouse_callbacks={"Button1": lazy.spawn("update-manager")}
                ),
                widget.Sep(),
                widget.Battery(),
                widget.BatteryIcon(),
                widget.Sep(),
                widget.TextBox(text="Volume:"),
                widget.Volume(),
                widget.Sep(),
                widget.Clock(format='%a %d-%m-%Y - %H:%M:%S',
                             update_interval=5),
            ],
            34,
            background="#1f1d1d"
        ),
    ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    auto = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([auto])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
