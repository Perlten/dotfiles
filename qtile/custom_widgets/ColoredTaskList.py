from libqtile.backend.base import Window
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.tasklist import TaskList



class ColoredTaskList(TaskList):
  

    def get_taskname(self, window: Window):
        """
        Get display name for given window.
        Depending on its state minimized, maximized and floating
        appropriate characters are prepended.
        """
        state = ''
        markup_str = self.markup_normal

        # Enforce markup and new string format behaviour when
        # at least one markup_* option is used.
        # Mixing non markup and markup may cause problems.
        if self.markup_minimized or self.markup_maximized\
                or self.markup_floating or self.markup_focused:
            enforce_markup = True
        else:
            enforce_markup = False

        if window is None:
            pass
        elif window.minimized:
            state = self.txt_minimized
            markup_str = self.markup_minimized
        elif window.maximized:
            state = self.txt_maximized
            markup_str = self.markup_maximized
        elif window.floating:
            state = self.txt_floating
            markup_str = self.markup_floating
        elif window is window.group.current_window:
            markup_str = self.markup_focused

        index = window.group.windows.index(window) + 1
        window_name = f"[{index}] " + window.name if window and window.name else "?"

        if callable(self.parse_text):
            try:
                window_name = self.parse_text(window_name)
            except:  # noqa: E722
                logger.exception("parse_text function failed:")

        # Emulate default widget behavior if markup_str is None
        if enforce_markup and markup_str is None:
            markup_str = "%s{}" % (state)

        if markup_str is not None:
            self.markup = True
            window_name = pangocffi.markup_escape_text(window_name)
            return markup_str.format(window_name)

        return "%s%s" % (state, window_name)