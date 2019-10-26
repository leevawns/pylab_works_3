import wx


# ***********************************************************************
# ***********************************************************************
def _Wrap_No_GUI ( target ):
  def wrapper ( *args, **kwargs ) :
    ##v3print ( 'BEFORE', target.__name__ )
    # Create the Application if it doesn't exists
    _dummy_app = None
    if not (wx.GetApp () ):
      _dummy_app = wx.PySimpleApp ()

    # perform the called target function
    result = target ( *args, **kwargs )

    # Destroy the wx.App, if it was created here
    ##v3print ( 'AFTER', target.__name__ )
    if _dummy_app :
      _dummy_app.Destroy ()
      _dummy_app = None
      
    # return the result to the calling application
    return result
  
  # ???? don't know what this is for ????
  return wrapper
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def AskYesNo ( Question = 'Some Question', Title = 'Please answer this question' ) :
  """
  Yes-No Dialog,  returns :
    True   if Yes is pressed
    False  if No  is pressed
  """
  dialog = wx.MessageDialog ( None, Question, Title,
                              wx.YES_NO | wx.ICON_QUESTION)
  answer = dialog.ShowModal() == wx.ID_YES
  dialog.Destroy ()
  return answer
# ***********************************************************************

print AskYesNo ()
print AskYesNo ()
