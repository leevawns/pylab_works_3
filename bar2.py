"""Code for drawing bar graphs and sliders.  This is version 2 of this software.
Implements a bar in a wxPython environment."""
import wx
import math
#import pac.ui.tickopt as tickopt
import tickopt

# Bar anchor positions
ANCHOR_LEFT = 0
ANCHOR_CENTER = 1
ANCHOR_RIGHT = 2

if __name__ == "__main__":
    app = wx.PySimpleApp()   # This statement must precede font creation (for demo program)

def fill_rect(dc,rect,color):
    """Useful function to draw a filled-in rectangle"""
    dc.SetBrush(wx.Brush(color,wx.SOLID))
    dc.SetPen(wx.Pen(color,1,wx.SOLID))
    dc.DrawRectangle(rect.x,rect.y,rect.width,rect.height)

def force_between(test,minval,maxval):
    """Returns a value guaranteed to be between min and max"""
    if test < minval:
        return minval
    if test > maxval:
        return maxval
    return test

class wxBar(wx.Panel):
    def __init__(self,parent,winid,pos=wx.DefaultPosition,size=wx.DefaultSize,flags=wx.FULL_REPAINT_ON_RESIZE,
            value=0.0,
            title='',
            **kwds):
        """
        Creates a bar display with a default value of 0.0, no title, and all the other parameters set to their defaults.
        All defaults can be changed with keyword arguments to this function; see set_additional_properties.
        """
        if size == wx.DefaultSize:
            size = (200,75)
        wx.Panel.__init__(self,parent,winid,pos,size,flags)
        self._title = title
        self._value = value
        self._tick_optimizer = None  # This object created later if necessary
        self._val_rect = None  # Rect where numerical value is shown
        self._title_height = None
        self._scale_height = None
        self._layout_valid = False
        self._enabled = True
        self._number_format = 1
        self.set_additional_properties(**kwds)
        wx.EVT_PAINT(self,self.__paint_me)

    def enable(self,a_bool):
        """Enables or disables the control."""
        if a_bool != self._enabled:
            self._enabled = a_bool
            self.Refresh(False)

    def prepare_to_render(self,rect,dc):
        """Called before rendering, giving subclasses a chance to do some setup.
        This class does nothing."""
        pass

    def __paint_me(self,_):
        dc = wx.PaintDC(self)
        w,h  = self.GetClientSizeTuple()
        bm = wx.EmptyBitmap(w,h)
        memdc = wx.MemoryDC()
        memdc.SelectObject(bm)
        memdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)))
        memdc.Clear()
        my_rect = wx.Rect(0,0,w,h)
        if not self._layout_valid:
            self.compute_layout_values(my_rect,memdc)
        self.prepare_to_render(my_rect,memdc)
        self.draw_title(self.__get_title_rect(my_rect),memdc)
        self.draw_bar(self.__get_bar_rect(my_rect),memdc)
        self.draw_scale(self.__get_scale_rect(my_rect),memdc)
        dc.Blit(0,0,w,h,memdc,0,0)

    def __get_title_rect(self,rect):
        """Given the overall rectangle for the whole control, return the rectangle for the title.
        rect - a wxRect object.
        return a wxRect object
        Assumes layout_values is current.
        """
        return wx.Rect(0,0,rect.width,self._title_height)

    def __get_bar_rect(self,rect):
        """Given the overall rectangle for the whole control, return the rectangle for the bar itself.
        rect - a wxRect object.
        return a wxRect object
        """
        return wx.Rect(0,self._title_height,rect.width,self._bar_height)

    def __get_scale_rect(self,rect):
        """Given the overall rectangle for the whole control, return the rectangle for the scale.
        rect - a wxRect object.
        return a wxRect object
        """
        return wx.Rect(0,self._title_height + self._bar_height,rect.width,self._scale_height)

    def set_additional_properties(self,
            bar_anchor=ANCHOR_LEFT,
            bar_left_inset=25,        # Distance from left edge of control to the beginning of the bar
            bar_right_inset=25,      # Distance from right edge to bar
            bar_height=20,               # Height of the bar itself (center region)
            number_format=1,        # Number of significant figures in the text display
            number_font=None,        # Font for the text display (None will use system default)
            min_value=0.0,
            max_value=100.0,
            major_increment=25.0,
            minors_per_major=5,
            use_labels=True,
            title_background_color= wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE),
            bar_background_color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DSHADOW),
            bar_color = wx.NamedColour("WHITE"),
            extra_major_ticks = None,
            extra_minor_ticks = None,
            autotick = True,
            title_font = None,
            title_color = wx.NamedColour("BLACK"),
            axis_number_font = None,
            axis_number_color = wx.NamedColour("BLACK"),
            axis_number_format = 0,
            axis_tick_color = wx.NamedColour("BLACK"),
            axis_background_color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE),
            axis_has_major_ticks = True,
            axis_has_minor_ticks = True,
            major_tick_length = 10,
            minor_tick_length = 5
            ):
        """
            bar_anchor - Fixed end position of the bar, one of the ANCHOR_X constants
            bar_left_inset - Distance from left edge of control to the beginning of the bar
            bar_right_inset - Distance from right edge to bar
            bar_height -  Height of the bar itself (center region)
            number_format - Number of significant figures in the text display
            number_font - Font for the text display (None will use system default)
            min_value - The minimum value the bar graph can have
            max_value - The maximum value
            major_increment - The numerical spacing from one major tick mark to the rest
            minors_per_major - Number of minor tick marks per major tick
            use_labels - True to allow numerical labels on the scale
            title_background_color - self explanatory,
            bar_background_color  - color of the background behind the colored bar
            bar_color - color of the bar itself
            extra_major_ticks - A list specifying the numerical position for special extra tick marks
            extra_minor_ticks - Ditto for minor tick marks
            autotick - True tells the control to calculate automatically the major and minor tick intervals
            title_font - None if you want the system default
            title_color - self explanatory
            axis_number_font - For axis numerical labels
            axis_number_color = For axis numerical labels
            axis_number_format - Number of significant figures for the axis labels; if autotick is on, this is irrelevant
            axis_tick_color - self explanatory
            axis_background_color - self explanatory
            axis_has_major_ticks - self explanatory
            axis_has_minor_ticks - self explanatory
            major_tick_length - self explanatory
            minor_tick_length - self explanatory
        """
        # pylint: disable-msg=w0201
        default_number_font = wx.Font(11,wx.SWISS,wx.NORMAL,wx.NORMAL)
        default_title_font = wx.Font(11,wx.SWISS,wx.NORMAL,wx.BOLD)
        default_axis_number_font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)

        self._bar_anchor = bar_anchor
        self._bar_left_inset = bar_left_inset
        self._bar_right_inset = bar_right_inset
        self._bar_height = bar_height
        self._number_format = number_format
        #self._number_font = (default_number_font if number_font is None else number_font)
        self._number_font = default_number_font
        self._min = min_value
        self._max = max_value
        self._major_increment = major_increment
        self._minors_per_major = minors_per_major
        self._use_labels = use_labels
        self._title_background_color = title_background_color
        self._bar_background_color = bar_background_color
        self._bar_color = bar_color
        self._extra_major_ticks = extra_major_ticks
        self._extra_minor_ticks = extra_minor_ticks
        self._autotick = autotick
        #self._title_font = (default_title_font if title_font is None else title_font)
        self._title_font = default_title_font
        self._title_color = title_color
        #self._axis_number_font = (default_axis_number_font if axis_number_font is None else axis_number_font)
        self._axis_number_font = default_axis_number_font
        self._axis_number_color = axis_number_color
        self._axis_number_format = axis_number_format
        self._axis_tick_color = axis_tick_color
        self._axis_background_color = axis_background_color
        self._axis_has_major_ticks = axis_has_major_ticks
        self._axis_has_minor_ticks = axis_has_minor_ticks
        self._major_tick_length = major_tick_length
        self._minor_tick_length = minor_tick_length

        self._layout_valid = False

    def __compute_title_height(self,dc):
        """Computes height of the title area, depending on which font
        is larger (the title or the text readout)."""
        dc.SetFont(self._number_font)
        _, y0 = dc.GetTextExtent("0.0")
        if self._title:
            dc.SetFont(self._title_font)
            _, y1 = dc.GetTextExtent(self._title)
            y0 = max(y0,y1)
        return y0 + 4  # Add a few pixels to make it look nicer

    def __compute_scale_height(self,dc):
        """Computes the height of the scale area, taking into account
        font sizes and tick lengths."""
        y = 0
        if self._use_labels:
            dc.SetFont(self._axis_number_font)
            _, y0 = dc.GetTextExtent("0.0")
            y += y0 + 2
        if self._axis_has_major_ticks:
            y += self._major_tick_length + 2
        elif self._minor_tick_length:
            y += self._minor_tick_length + 2
        return y + 4

    def compute_layout_values(self,rect,dc):
        """Computes values for the layout of the control."""
        bh = self._bar_height + 2
        th = self.__compute_title_height(dc)
        ah = self.__compute_scale_height(dc)
        if rect.height < th + ah + bh:
            ah = max(rect.height - th - bh,0)
        if rect.height < th + ah + bh:
            th = max(rect.height - bh,0)
        self._title_height = th
        self._scale_height = ah + 2
        self._layout_valid = True
        self.SetSizeHints(minW=100 + self._bar_left_inset + self._bar_right_inset,minH=bh + th + ah)

    def set_title(self,title):
        """Sets the title string, but does not force a redraw."""
        self._title = title

    def set_value(self,value,refresh=True):
        """Sets the value (number) to be displayed by the control.
        This will redraw by default."""
        self._value = value
        if refresh:
            self.Refresh(False)

    def get_value(self):
        """Returns the value currently shown by this control"""
        return self._value

    def set_limits(self,xmin=None,xmax=None):
        """Set the limits of the scale without a redraw."""
        if xmin is not None:
            self._min = xmin
        if xmax is not None:
            self._max = xmax

    def draw_title(self,rect,dc):
        """Draw the title inside the specified rectangle"""
        # Background erase
        bkcolor = self._title_background_color
        brush = wx.Brush(bkcolor,wx.SOLID)
        pen =  wx.Pen(bkcolor,1,wx.SOLID)
        dc.SetBrush(brush)
        dc.SetPen(pen)
        dc.DrawRectangle(rect.x,rect.y,rect.width,rect.height)

        if self._title:
            dc.SetFont(self._title_font)
            dc.SetTextForeground(self._title_color)
            dc.DrawText(self._title,rect.x+1,1)

        fstr = "%%.%df" % self._number_format
        valstr = fstr % float(self._value)
        dc.SetFont(self._number_font)
        xx,yx = dc.GetTextExtent(valstr)
        x = rect.x + rect.width - xx - 2
        y = (rect.height - yx) / 2
        dc.DrawText(valstr,x,y)
        self._val_rect = wx.Rect(x,y,xx,yx)

    def _bar_extent(self,rect):
        return rect.width - self._bar_left_inset - self._bar_right_inset

    def _bar_origin(self,rect):
        return rect.x + self._bar_left_inset

    def _scale(self,rect,value):
        """Given the specified rect for the bar, scale the specified value to a pixel position."""
        if self._max <= self._min:
            return 1
        xextent = self._bar_extent(rect)
        xoffset = (float)(value - self._min)/(self._max - self._min) * xextent
        if xoffset < 0: 
            xoffset = 0
        if xoffset > xextent: 
            xoffset = xextent
        return int(xoffset + 0.5) + self._bar_left_inset

    def draw_bar(self,rect,dc):
        if not self._enabled:
            dc.SetPen(wx.Pen(self._bar_color))
            dc.DrawRectangle(rect.x,rect.y,rect.width,rect.height)
        bar_origin = self._bar_origin(rect)
        bar_extent = self._bar_extent(rect)
        # Background erase
        fill_rect(dc,wx.Rect(bar_origin,rect.y,self._bar_extent(rect),rect.height),self._bar_background_color)
        bar_type = self._bar_anchor
        bar_endpoint = self._scale(rect,self._value)
        # print "Bar endpoint at: %d" % barendpoint
        if bar_type == ANCHOR_LEFT:
            bar_rect = wx.Rect(bar_origin,rect.y,bar_endpoint - bar_origin,rect.height)
        elif bar_type == ANCHOR_CENTER:
            bar_center = bar_origin + self._bar_extent(rect)/2
            if bar_endpoint <= bar_center:
                bar_rect = wx.Rect(bar_endpoint,rect.y,bar_center-bar_endpoint,rect.height)
            else:
                bar_rect = wx.Rect(bar_center,rect.y,bar_endpoint - bar_center,rect.height)
        else:
            bar_rect = wx.Rect(bar_endpoint,rect.y,bar_extent + bar_origin - bar_endpoint,rect.height)
        dc.SetBrush(wx.Brush(self._bar_color))
        dc.DrawRectangle(bar_rect.x,bar_rect.y+1,bar_rect.width,bar_rect.height-2)
        dc.SetPen(wx.Pen(self._axis_tick_color))
        #mark_position = bar_endpoint if bar_type != ANCHOR_CENTER else bar_center
        if bar_type != ANCHOR_CENTER :
          mark_position = bar_endpoint
        else : mark_position = bar_center


        dc.DrawLine(mark_position,rect.y+2,mark_position,rect.GetBottom())

    def draw_scale(self,rect,dc):
        # Compute tick marks automatically if that is enabled
        if rect.width < 5:
            return
        bar_extent = self._bar_extent(rect)
        x_offset = self._bar_left_inset + rect.x
        ticker = tickopt.tickopt(self._min,self._max,bar_extent)
        if not self._autotick:
            ticker.major_spacing = self._major_increment
            ticker.minors_per_major = self._minors_per_major
            ticker.sigfigs = self._axis_number_format
        # Erase to background
        fill_rect(dc,rect,self._axis_background_color)
        dc.SetPen(wx.Pen(self._axis_tick_color))
        dc.SetTextForeground(self._axis_number_color)
        dc.SetFont(self._axis_number_font)
        tick_start = rect.y
        if self._axis_has_major_ticks:
            tick_end = tick_start + self._major_tick_length
            text_start = tick_end + 2
            for label,pos in ticker.iter_majors():
                x = pos + x_offset
                dc.DrawLine(x,tick_start,x,tick_end)
                tx,_ = dc.GetTextExtent(label)
                dc.DrawText(label,x - tx/2,text_start)
        if self._axis_has_major_ticks:
            tick_end = tick_start + self._minor_tick_length
            for pos in ticker.iter_minors():
                x = pos + x_offset
                dc.DrawLine(x,tick_start,x,tick_end)
        self._tick_optimizer = ticker

class wxSlider(wxBar):
    def __init__(self,parent,winid,value=0.0,title='',**kwds):
        """Layout similar to a bar, but provides a slider for user setting of the value.
        Fires off events when the user changes the value, see add_listener."""
        self._state = "IDLE"             # The state of the control for responding to mouse events
        self._processed = False
        wxBar.__init__(self,parent,winid,value=value,title=title,**kwds)

        self._listeners = []
        self._bar_rect = None            # The rectangle for the bar.  Also see comments in __move_mouse
        self._ptr_rect = None            # The rectangle where the pointer is drawn
        self._rbutton = None                # Rectangle for right button
        self._lbutton = None                # Rectangle for left button
        self._counter = None            # Number of timer ticks since mouse down
        self._value_point = None        # Last x position of the pointer's mark
        self._original_value_point = None   # The pointer mark x position at the moment when mouse down occurred 
        self._original_value = None     # The value shown by the slider when mouse went down
        self._last_rect = None               # The last value for the full rectangle (used in scaling)
        self._jump_value = None         # X position of the mouse for a jump operation
        self._offset = None                     # Difference between the mouse pointer and the slider mark
        self._is_close = None             # True when the mouse was clicked close to one of the vernier buttons

        wx.EVT_LEFT_DOWN(self,self.__left_down)
        wx.EVT_LEFT_UP(self,self.__left_up)
        wx.EVT_MOTION(self,self.__move_mouse)
        wx.EVT_RIGHT_UP(self,self.__right_up)

        self._timer = wx.Timer(self,100)
        wx.EVT_TIMER(self,100,self.__tick)
        self._i_have_mouse = False

    def set_additional_properties(self,
            slider_width=11,
            slider_button_width=20,
            slider_increment=1.0,
            background_increment=10.0,
            button_increment=0.1,
            pointer_color=wx.NamedColor("RED"),
            auto_increment=True,
            max_button_increment=0.1,
            min_settable=None,
            **kwds):
        """Autoincrement overrides the values of slider_increment, background_increment,
        and button_increment.  In this mode the control calculates reasonable values for these
        parameters depending on its size.

        When the user clicks on the background, the value changes by the background_increment.
        When the user clicks on a vernier button, the value changes by the button_increment.
        When the user drags the slider, the value changes by slider increment.
        When the user right clicks on the control, a Dialog asks for text entry of the new value.
        A new value is always rounded off to the nearest whole number multiple of the relevant increment.
        The max_button increment sets an upper limit on the button increment when auto_increment is on.
        If min_settable is not none, do not fire off a new value event if the control's value is less than min_settable.
        """
        # pylint: disable-msg=w0201,w0221
        wxBar.set_additional_properties(self,**kwds)
        self._slider_width = slider_width
        self._slider_button_width = slider_button_width
        self._slider_increment = slider_increment
        self._background_increment = background_increment
        self._button_increment = button_increment
        self._pointer_color = pointer_color
        self._auto_increment = auto_increment
        self._max_button_increment = max_button_increment
        self._min_settable = min_settable

    def draw_scale(self,rect,dc):
        """Override here so that each time the scale is drawn, the auto increment values gets set"""
        wxBar.draw_scale(self,rect,dc)
        if self._auto_increment:
            self._background_increment = self._tick_optimizer.major_spacing / self._tick_optimizer.minors_per_major
            self._slider_increment = self._background_increment * 0.1
            self._button_increment = min(self._max_button_increment,self._slider_increment * 0.1)
            self._number_format = max(0,-int(math.log10(self._button_increment) - 0.5))

    def is_updating(self):
        """Returns true if the control is processing user input."""
        return self._state != "IDLE"

    def add_listener(self,listener):
        """Listener is a method taking 2 arguments: the new value, and a boolean that will be true when the
        value is finished changing.  Therefore the method signature is listener(newvalue,finished).
        When the user fiddles with the control, a series of new value events are produced.  All of them will
        have a second argument of false until the last one, which will be true.
        """
        self._listeners.append(listener)

    def remove_listener(self,listener):
        """Removes the listener from the list."""
        self._listeners.remove(listener)

    def draw_bar_background(self,dc):
        """Erase the bar to its background color"""
        fill_rect(dc,self._bar_rect,self._bar_background_color)

    def draw_slider(self,dc):
        dc.SetPen(wx.Pen(wx.NamedColor("BLACK")))
        dc.SetBrush(wx.Brush(self._pointer_color))
        dc.DrawRectangle(self._ptr_rect.x,self._ptr_rect.y,self._ptr_rect.width,self._ptr_rect.height)
        dc.DrawLine(self._value_point,self._ptr_rect.y + self._ptr_rect.height,self._value_point,self._ptr_rect.y+self._ptr_rect.height - 10)

    def draw_bar(self,rect,dc):
        """Draw the bar part of the window only."""
        # print "Drawing bar in %s" % rect
        # print "Y=%d" % rect.y
        if not self._enabled:
            wxBar.draw_bar(self,rect,dc)
            return
        bar_origin = self._bar_origin(rect)
        bar_extent = self._bar_extent(rect)
        self._bar_rect = wx.Rect(bar_origin,rect.y,bar_extent,rect.height)

        # Background erase
        self.draw_bar_background(dc)
        if self._min_settable is not None:
            minx = self._scale(rect,self._min_settable)
            fill_rect(dc,wx.Rect(bar_origin,rect.y,minx-bar_origin,rect.height),"BLACK")

        self._value_point = self._scale(rect,self._value)
        ptrw = self._slider_width
        ptrx = self._value_point - ptrw/2
        self._ptr_rect = wx.Rect(ptrx,rect.y,ptrw,rect.height)   # Rectangle for pointer
        self.draw_slider(dc)

        # Button draw
        bw = self._slider_button_width
        self._lbutton = wx.Rect(bar_origin-bw,rect.y,bw,rect.height)
        self._rbutton = wx.Rect(bar_origin+bar_extent,rect.y,bw,rect.height)
        self._draw_button(dc,self._lbutton,"left")
        self._draw_button(dc,self._rbutton,"right")

        # Save rectangles for subsequent mouse event processing
        self._last_rect = rect 

    def _notify_listeners(self,finished=False):
        for listener in self._listeners:
            listener(self._value,finished)

    def __inverse_scale(self,x):
        br = self._bar_rect
        val_offset = float(x - br.x) / br.width
        return val_offset * (self._max - self._min) + self._min

    def _process(self):
        if self._state == "JUMP":
            self._try_to_jump()
        elif self._state == "LBUTTON":
            self._button_down()
        elif self._state == "RBUTTON":
            self._button_up()
        self._processed = True

    def __tick(self,_):
        """The timer went off"""
        if self._state == "IDLE" or not self._enabled: 
            return
        self._counter += 1
        if self._counter <= 5:
            return
        self._process()

    def __step_up(self,increment):
        """Returns my new value after stepping up by the specified increment"""
        return (math.floor((self._value + increment * 0.0001) / increment) + 1.0) * increment

    def __step_down(self,increment):
        """Returns my new value after stepping up by the specified increment"""
        return (math.ceil((self._value - increment * 0.0001) / increment) - 1.0) * increment

    def _try_to_jump(self):
        jump_delta = self._jump_value - self._value_point
        if jump_delta > 0:
            new_value = self.__step_up(self._background_increment)
            new_x = self._scale(self._last_rect,new_value)
            if self._jump_value > new_x - self._slider_width/2:
                self.__set_new_val(new_value)
        elif jump_delta < 0:
            new_value = self.__step_down(self._background_increment)
            new_x = self._scale(self._last_rect,new_value)
            if self._jump_value < new_x + self._slider_width/2:
                self.__set_new_val(new_value)

    def _button_up(self):
        if self._is_close:
            self.__set_new_val(self.__step_up(self._button_increment))

    def _button_down(self):
        if self._is_close:
            self.__set_new_val(self.__step_down(self._button_increment))

    def __start_timer(self):
        self._counter = 0       # Counts elapsed ticks since the mouse button was clicked
        self._timer.Start(100)

    def __stop_timer(self):
        self._timer.Stop()

    def __left_down(self,event):
        if not self._enabled:
            return
        x = event.GetX()
        y = event.GetY()
        pt = wx.Point(x,y)
        self._original_value = self._value
        self._original_value_point = self._value_point
        self._processed = False
        if self._ptr_rect.Inside(pt):
            self._state = "SLIDE"
            self._offset = x - self._value_point 
        elif self._bar_rect.Inside(pt):
            self._state = "JUMP"
            self._jump_value = x   
            self._try_to_jump()
            self.__start_timer()
        elif self._lbutton.Inside(pt):
            self._state = "LBUTTON"
            self._is_close = True
            self._button_down()
            self.__start_timer()
            self.Refresh(False,self._lbutton)
        elif self._rbutton.Inside(pt):
            self._state = "RBUTTON"
            self._is_close = True
            self._button_up()
            self.__start_timer()
            self.Refresh(False,self._rbutton)
        else:
            self._state = "IDLE"
        self.CaptureMouse()
        self._i_have_mouse = True

    def __left_up(self,_):
        self._state = "IDLE"
        if not self._processed:
            self._process()
        self._processed = False
        if self._state.find("BUTTON") >= 0:
            if not self._is_close:
                self.__set_new_val(self._original_value)
        self.__stop_timer()
        if self._i_have_mouse: 
            self.ReleaseMouse()
            self._i_have_mouse = False
        if self._value != self._original_value:
            self._notify_listeners(True)
        self.Refresh(False)

    def __get_settable_extremes(self):
        if self._min_settable is not None:
            return min(self._min_settable,self._min),self._max
        return self._min,self._max

    def __right_up(self,_):
        d = wx.TextEntryDialog(self,
                    "Enter a number between %s and %s" % (self.__get_settable_extremes()),
                    "Enter desired setting",
                    style=wx.OK | wx.CANCEL)
        if d.ShowModal() == wx.ID_OK:
            self.__set_new_val(float(d.GetValue()),finished=True)

    def __set_new_val(self,value,finished=False):
        if value != self._value:
            self._value = force_between(value,*self.__get_settable_extremes())
            self.Refresh(False,self._bar_rect)
            self.Refresh(False,self._val_rect)
            self._notify_listeners(finished=finished)

    def __is_mouse_close(self,y):
        """Returns true if the mouse Y position is reasonably close to the bar."""
        bar = self._bar_rect
        return bar.y - 50 < y < (bar.y+bar.height) + 50

    def __move_mouse(self,event):
        """Returns true if a new value was generated"""
        # Sometimes this event occurs before the control is painted
        if self._bar_rect is None: 
            return
        if not self._enabled: 
            return

        if self._state == "SLIDE":
            if self.__is_mouse_close(event.GetY()):
                new_valuept = event.GetX() - self._offset
                value = self.__inverse_scale(new_valuept)
                sincr = self._slider_increment
                value = math.floor((value + sincr*0.5) / sincr) * sincr
                self.__set_new_val(value)
            else:
                self.__set_new_val(self._original_value)
        elif self._state == "JUMP":
            if self.__is_mouse_close(event.GetY()):
                self._jump_value = event.GetX()
            else:
                self._jump_value = self._original_value_point
                self.__set_new_val(self._original_value)
        elif self._state.find("BUTTON") >= 0:
            self._is_close = self.__is_mouse_close(event.GetY())

    def _draw_arrow(self,dc,rect,direction):
        ctext = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNTEXT)
        dc.SetPen(wx.Pen(ctext))

        # Find the center of the rectangle
        centerx = rect.x + rect.width/2
        centery = rect.y + rect.height/2
        if direction == "left":
            xr = range(-2,4)
        else:
            xr = range(2,-4,-1)
        for length,x in zip(range(1,11,2),xr):
            xpos = centerx + x
            dc.DrawLine(xpos,centery-length/2,xpos,centery+length/2)

    def _draw_button(self,dc,rect,direction):
        cface = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)
        cdark = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNSHADOW)
        clight = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        penface = wx.Pen(cface)
        pendark = wx.Pen(cdark)
        penlight = wx.Pen(clight)
        brush = wx.Brush(cface)
        dc.SetBrush(brush)
        if self._state.find("BUTTON") >= 0:
            dc.SetPen(pendark)
            dc.DrawRectangle(rect.x,rect.y,rect.width-1,rect.height-1)
            self._draw_arrow(dc,rect,direction)
            return
        dc.SetPen(penface)
        dc.DrawRectangle(rect.x,rect.y,rect.width-1,rect.height-1)
        self._draw_arrow(dc,rect,direction)
        x1m1 = rect.x+rect.width-1
        y1m1 = rect.y+rect.height-1
        dc.SetPen(pendark)
        dc.DrawLine(rect.x,y1m1,x1m1,y1m1)
        dc.DrawLine(x1m1,rect.y,x1m1,y1m1)
        dc.SetPen(penlight)
        x1 = rect.x + 1
        y1 = rect.y + 1
        dc.DrawLine(x1,y1,x1,y1m1-1)
        dc.DrawLine(x1,y1,x1m1-1,y1)

    def set_value(self,value,refresh=True):
        """Override to prevent this during user adjustment"""
        if self._state == "IDLE":
            wxBar.set_value(self,value,refresh)

if __name__ == "__main__":
    class MainWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self,None,100,"Bar test")
            self.bar = wxBar(self,-1,value=75.0,title="Bar")
            s = wxSlider(self,102,75.0,"Slider")
            bs = wx.BoxSizer(wx.VERTICAL)
            bs.Add(self.bar,1,wx.EXPAND,0)
            bs.Add(s,1,wx.EXPAND,0)
            self.SetSizer(bs)
            self.SetAutoLayout(True)
            self.SetSize(wx.Size(800,600))
            self.Centre()
            self.Show()
            s.add_listener(self.new_value)

        def new_value(self,value,_):
            self.bar.set_value(value)

    MainWindow()
    app.MainLoop()



