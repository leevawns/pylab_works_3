# ***********************************************************************
# This code must be here, otherwise we don't have the global "visual"
# when we run through PG.P_Globals this could be placed anywhere
# ***********************************************************************
class _tScenery_Base2 ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    GUI = """
      self.p1  ,wx.Panel
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.Script_Error     = False
    self.Init_Code_Before = None
    self.Init_Code_After  = None
    self.Loop_Code_Before = None
    self.Loop_Code_After  = None


  # *********************************************************
  # *********************************************************
  def Start_Script ( self, Code ) :
    Init_Code, self.VPC_Code, self.Loop_Code = \
      Split_Init_Code ( Code, self, self.Code_Globals )

    """
    v3print ( '======= INIT ======' )
    v3print ( Init_Code )
    v3print ( '======= VPython Control Code ======' )
    v3print ( self.VPC_Code )
    v3print ( '======= Loop ======' )
    v3print ( self.Loop_Code )
    v3print ( '======= END Loop ======' )
    """

    # Add own Library directory to the namespace
    path = os.path.join ( Application.Dir, PG.Active_Project_Filename, 'Libs' )
    self.Code_Globals [ 'My_Path' ] = path + '/'

    # The Pre-Init code is executed separately
    # to get the correct line number for error messages
    if self.Init_Code_Before :
      try :
        exec ( self.Init_Code_Before, self.Code_Globals )
      except :
        pass

    try :
      exec ( Init_Code, self.Code_Globals )
      self.Script_Error = False
    except :
      import traceback
      traceback.print_exc ( 5 )
      print '******** SCENE Code Editor, ERROR: *********'

  # *********************************************************
  # *********************************************************
  def Execute_Script ( self ) :
    # The Pre-Loop code is executed separately
    # to get the correct line number for error messages
    if self.Loop_Code_Before :
      try :
        exec ( self.Loop_Code_Before, self.Code_Globals )
      except :
        pass

    if self.Loop_Code :
      try :
        exec ( self.Loop_Code, self.Code_Globals )
        self.Script_Error = False
      except :
        if not  ( self.Script_Error ) :
          self.Script_Error = True
          import traceback
          traceback.print_exc ( 5 )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#from control_vpython import _tScenery_Base
class t_C_2D_Scene ( _tScenery_Base2 ):
  def __init__ ( self, *args, **kwargs ):
    _tScenery_Base2.__init__ ( self, *args, **kwargs )

    self.Code_Globals = {}
    self.Code_Globals [ 'self'              ] = self
    self.Code_Globals [ 'Set_Coordinates'   ] = self.Set_Coordinates
    self.Code_Globals [ 'Create_Axis'       ] = self.Create_Axis
    self.Code_Globals [ 'Create_Grid'       ] = self.Create_Grid
    self.Code_Globals [ 'Create_Text'       ] = self.Create_Text
    self.Code_Globals [ 'Create_Points'     ] = self.Create_Points
    self.Code_Globals [ 'Create_Function'   ] = self.Create_Function
    self.Code_Globals [ 'Create_Line'       ] = self.Create_Line
    self.Code_Globals [ 'Create_Arrow'      ] = self.Create_Arrow
    self.Code_Globals [ 'Create_Circle'     ] = self.Create_Circle
    self.Code_Globals [ 'Create_Button'     ] = self.Create_Button
    self.Code_Globals [ 'Create_Rectangle'  ] = self.Create_Rectangle
    self.Code_Globals [ 'Create_Free_Shape' ] = self.Create_Free_Shape

    self.Init_Code_Before  = 'self._Trail_Count = -1 \n'
    self.Init_Code_Before += 'self.Trail_Count = 5\n'

    self.Loop_Code_Before  = 'self._Trail_Count += 1 \n'
    self.Loop_Code_Before += 'if (self._Trail_Count % self.Trail_Count) == 0 :\n'
    self.Loop_Code_Before += '  self.Canvas.Add_Trail ()\n'

    self.Loop_Code_After   = 'self.Canvas.Refresh()\n'
