import __init__
"""import sys

# ***********************************************************************
# because rpd takes over the import !!
# ***********************************************************************
subdirs = [ 'lang',
            'bricks',
            'bricks/lang',
            '../support',
            '../support/lang',
            '../Templates',
            '../Lib_Extensions',
            '../Lib_Extensions/lang' ]
for subdir in subdirs:
  if not ( subdir in sys.path ) :
    sys.path.append ( subdir )
# ***********************************************************************
"""

import rpdb2
import wx
import wx.lib.wxpTag
import wx.gizmos
import wx.html

import wx.lib.mixins.listctrl  as  listmix
import wx.stc as stc

#import webbrowser
import traceback
import cStringIO
import threading
import xmlrpclib
import tempfile
import textwrap
import keyword
import weakref
import base64
import socket
import string
import codecs
import pickle
import Queue
import time
import os
import re

#import wx.lib.flatnotebook as fnb
#from picture_support import Get_Image_List_16

MARKER_BREAKPOINT_ENABLED = 5
MARKER_BREAKPOINT_DISABLED = 6
MARKER_CURRENT_LINE = 7
MARKER_CURRENT_LINE_HIT = 8

MARKER_CALL = 0
MARKER_LINE = 1
MARKER_RETURN = 2
MARKER_EXCEPTION = 3
MARKER_RUNNING = 4

MARKER_LIST = [MARKER_BREAKPOINT_ENABLED, MARKER_BREAKPOINT_DISABLED, MARKER_CURRENT_LINE, MARKER_CURRENT_LINE_HIT, MARKER_CALL, MARKER_LINE, MARKER_RETURN, MARKER_EXCEPTION, MARKER_RUNNING]

MSG_WARNING_TRAP = "Are you sure that you want to disable the trapping of unhandled exceptions? If you click Yes unhandled exceptions will not be caught."
MSG_WARNING_UNHANDLED_EXCEPTION = "An unhandled exception was caught. Would you like to analyze it?"
MSG_WARNING_TITLE = "Warning"
MSG_WARNING_TEMPLATE = "%s\n\nClick 'Cancel' to ignore this warning in this session."
MSG_ERROR_FILE_NOT_PYTHON = "'%s' does not seem to be a Python source file. Only Python files are accepted."

STR_FILE_LOAD_ERROR = "Failed to load source file '%s' from debuggee."
STR_FILE_LOAD_ERROR2 = """Failed to load source file '%s' from debuggee.
You may continue to debug, but you will not see
source lines from this file."""
STR_BLENDER_SOURCE_WARNING = "You attached to a Blender Python script. To be able to see the script's source you need to load it into the Blender text window and launch the script from there."
STR_EMBEDDED_WARNING = "You attached to an embedded debugger. Winpdb may become unresponsive during periods in which the Python interpreter is inactive."

WINPDB_VERSION = "WINPDB_1_3.8"
VERSION = (1, 3, 8, 0, '')

BAD_FILE_WARNING_TIMEOUT_SEC = 10.0
DIRTY_CACHE = 1
POSITION_TIMEOUT = 2.0

g_ignored_warnings = {'': True}
g_fUnicode = 'unicode' in wx.PlatformInfo
assert(g_fUnicode or not rpdb2.is_py3k())


# ***********************************************************************
# ***********************************************************************
class CJobs:
  def __init__(self):
    self.__m_jobs_lock = threading.RLock()
    self.__m_n_expected_jobs = 0
    self.__m_f_shutdown = False

  # *********************************************************
  # *********************************************************
  def shutdown_jobs(self):
    #print 'SHUTDOWN'
    self.__m_f_shutdown = True
    while 1:
      try:
        self.__m_jobs_lock.acquire()
        if self.__m_n_expected_jobs == 0:
          return
      finally:
        self.__m_jobs_lock.release()
      time.sleep(0.1)

  # *********************************************************
  # *********************************************************
  def job_post(self, job, args, kwargs = {}, callback = None):
    threading.Thread(target = self.job_do, args = (job, args, kwargs, callback)).start()

  # *********************************************************
  # *********************************************************
  def job_do(self, job, args, kwargs, callback):
    try:
      self.__m_jobs_lock.acquire()
      if self.__m_f_shutdown:
        return
      if self.__m_n_expected_jobs == 0:
        wx.CallAfter ( self.Set_Cursor, wx.CURSOR_WAIT )
      self.__m_n_expected_jobs += 1
    finally:
      self.__m_jobs_lock.release()

    r = None
    exc_info = (None, None, None)

    try:
      r = job(*args, **kwargs)
    except:
      exc_info = sys.exc_info()
      if callback == None:
        rpdb2.print_debug_exception()

    if callback is not None:
      wx.CallAfter(callback, r, exc_info)

    try:
      self.__m_jobs_lock.acquire()
      self.__m_n_expected_jobs -= 1
      if self.__m_n_expected_jobs == 0:
        wx.CallAfter(self.Set_Cursor, wx.CURSOR_ARROW)
    finally:
      self.__m_jobs_lock.release()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class CAsyncSessionManagerCall:
  def __init__(self, session_manager, job_manager, f, callback, ftrace = False):
    self.m_session_manager = session_manager
    self.m_job_manager = job_manager
    self.m_f = f
    self.m_callback = callback
    self.m_ftrace = ftrace

  # *********************************************************
  # *********************************************************
  def __wrapper(self, *args, **kwargs):
    if self.m_callback != None:
      try:
        if self.m_ftrace:
          rpdb2.print_debug('Calling %s' % repr(self.m_f))
        return self.m_f(*args, **kwargs)
      finally:
        if self.m_ftrace:
          rpdb2.print_debug('Returned from %s' % repr(self.m_f))

    try:
      self.m_f(*args, **kwargs)
    except rpdb2.FirewallBlock:
      self.m_session_manager.report_exception(*sys.exc_info())
      dlg = wx.MessageDialog(self.m_job_manager, rpdb2.STR_FIREWALL_BLOCK, MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
      dlg.ShowModal()
      dlg.Destroy()
    except (socket.error, rpdb2.CConnectionException):
      self.m_session_manager.report_exception(*sys.exc_info())
    except rpdb2.CException:
      self.m_session_manager.report_exception(*sys.exc_info())
    except:
      self.m_session_manager.report_exception(*sys.exc_info())
      rpdb2.print_debug_exception(True)

  # *********************************************************
  # *********************************************************
  def __call__(self, *args, **kwargs):
    if self.m_job_manager == None:
      return
    self.m_job_manager.job_post(self.__wrapper, args, kwargs, self.m_callback)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class CAsyncSessionManager:
  # *********************************************************
  # *********************************************************
  def __init__(self, session_manager, job_manager, callback = None, ftrace = False):
    self.m_session_manager = session_manager
    self.m_callback = callback
    self.m_ftrace = ftrace
    self.m_weakref_job_manager = None
    if job_manager != None:
      self.m_weakref_job_manager = weakref.ref(job_manager)

  # *********************************************************
  # *********************************************************
  def with_callback(self, callback, ftrace = False):
    if self.m_weakref_job_manager != None:
      job_manager = self.m_weakref_job_manager()
    else:
      job_manager = None
    asm = CAsyncSessionManager(self.m_session_manager, job_manager, callback, ftrace)
    return asm

  # *********************************************************
  # *********************************************************
  def __getattr__(self, name):
    f = getattr(self.m_session_manager, name)
    if not hasattr(f, '__call__'):
      raise TypeError(repr(type(f)) + ' object is not callable')
    if self.m_weakref_job_manager != None:
      job_manager = self.m_weakref_job_manager()
    else:
      job_manager = None
    return CAsyncSessionManagerCall(self.m_session_manager, job_manager, f, self.m_callback, self.m_ftrace)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class CSourceManager:
  def __init__ ( self, job_manager, session_manager ) :
    self.m_job_manager     = job_manager
    self.m_session_manager = session_manager
    self.m_async_sm        = CAsyncSessionManager ( session_manager,
                                                    self.m_job_manager )
    self.m_files           = {}
    self.m_lock            = threading.RLock ()

  # *********************************************************
  # *********************************************************
  def _clear ( self ) :
    self.m_files = {}

  # *********************************************************
  # *********************************************************
  def mark_files_dirty ( self ) :
    for k, v in list ( self.m_files.items () ) :
      self.m_files [k] = ( DIRTY_CACHE, rpdb2.as_string('') )

  # *********************************************************
  # *********************************************************
  def is_in_files ( self, filename ) :
    for k in list ( self.m_files.keys() ) :
      if filename in k:
        return True
    return False

  # *********************************************************
  # *********************************************************
  def get_source ( self, filename ) :
    for k, v in list ( self.m_files.items() ) :
      if not filename in k:
          continue
      ( _time, source ) = v
      if _time == 0:
        return ( k, source )
      t = time.time ()
      if t - _time < BAD_FILE_WARNING_TIMEOUT_SEC:
          return ( k, source )
      #del self.m_files[k]
      raise KeyError
    raise KeyError

  # *********************************************************
  # *********************************************************
  def load_source ( self, filename, callback, args, fComplain ) :
    f = lambda r, exc_info: self.callback_load_source ( r, exc_info, filename, callback, args, fComplain)
    self.m_async_sm.with_callback ( f, ftrace = True ).get_source_file(filename, -1, -1)

  # *********************************************************
  # *********************************************************
  def callback_load_source ( self, r, exc_info, filename, callback, args, fComplain ) :
    (t, v, tb) = exc_info
    if self.m_session_manager.get_state() == rpdb2.STATE_DETACHED:
      return

    if t == None:
      _time = 0
      _filename = r [ rpdb2.DICT_KEY_FILENAME ]
      source_lines = r [ rpdb2.DICT_KEY_LINES ]
      source = string.join ( source_lines, '' )
      if not g_fUnicode:
        source = rpdb2.as_string(source, wx.GetDefaultPyEncoding())
    elif t == rpdb2.NotPythonSource and fComplain:
      dlg = wx.MessageDialog(None, MSG_ERROR_FILE_NOT_PYTHON % (filename, ), MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif t in (IOError, socket.error, rpdb2.NotPythonSource) or isinstance(v, rpdb2.CConnectionException):
      if fComplain:
        dlg = wx.MessageDialog(None, STR_FILE_LOAD_ERROR % (filename, ), MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()
        return

      if t == IOError and rpdb2.BLENDER_SOURCE_NOT_AVAILABLE in v.args and not self.is_in_files(filename):
        dlg = wx.MessageDialog(None, STR_BLENDER_SOURCE_WARNING, MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

      _time = time.time()
      _filename = filename
      source = STR_FILE_LOAD_ERROR2 % (filename, )
      if not g_fUnicode:
        source = rpdb2.as_string(source, wx.GetDefaultPyEncoding())

    else:
      rpdb2.print_debug('get_source_file() returned the following error: %s' % repr(t))
      _time = time.time()
      _filename = filename
      source = STR_FILE_LOAD_ERROR2 % (filename, )
      if not g_fUnicode:
        source = rpdb2.as_string(source, wx.GetDefaultPyEncoding())

    try:
      self.m_lock.acquire()
      fNotify = not self.is_in_files(_filename)
      self.m_files[_filename] = (_time, source)
    finally:
      self.m_lock.release()

    _args = (_filename, ) + args + (fNotify, )
    callback ( *_args )
# ***********************************************************************


