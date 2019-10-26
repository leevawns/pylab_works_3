# ***********************************************************************
# PyLab_Works
# ***********************************************************************
Create_Flow_Code ()

PG.App_Running = True
PG.State = PG.SS_Reset
while PG.App_Running :
  if PG.State == PG.SS_Reset :
    ReCreate_Flow_Code ()
    PG.State = PG.SS_Stop

  elif PG.State in [PG.SS_Run, PG.SS_Stop]:
    try:

      # ************************************************************
      # execfile ( PG.Simulation_Filename )
      # PyLab_Works_Simulation_File
      # ************************************************************
        PG.Bricks[1].In[0] = PG.Bricks[2].Out[0]

        PG.Bricks[0].Exec()
        # ************************************************************
        # Bricks.Exec
        # ************************************************************
        def Exec (self):
          if PG.Execution_HighLight: self.Execute_Pre ()

          # if the Brick has controls or output,
          # and the inputs has changed, we need to update them
          if self.Old_Input_Value !=  self.In:
            self.Old_Input_Value = copy.copy ( self.In )
            self.Control_Pane.Brick_2_Control ( self.In )

          try:
            self.Execute ()
            # **********************************************************************
            # **********************************************************************
            def Execute ( self ) :
              try :
                new = self.Out[0] + self.Params[3] - self.Params[2]
                delta = self.Params[3]
                # check if new value inside the given range
                if abs ( new / delta ) != new / delta :
                  self.Out[0] = self.Out[0] + self.Params[3]
                #else :
                ##  self.Out_Modified [0] = False

                print 'FOR-LOOP, Change=',self.Out_Modified[0],'   Value=',self.Out[0]
              except :
                print 'error in FOR LOOP'
            # **********************************************************************
            # ***********************************************************************
          except:
            pass

          while PG.app.My_EventLoop.Pending():
            PG.app.My_EventLoop.Dispatch()
          PG.app.ProcessIdle()

          if PG.Execution_HighLight: self.Execute_Post ()
        # ************************************************************
        # ************************************************************
      # ************************************************************
      # ************************************************************

    except PG.Reload_Exception:
      print 'Program aborted in Simulation File'
    except:
      print 'Error in Simulation File'

    if PG.State == PG.SS_Step :
      PG.State = PG.SS_Stop
    PG.Main_Form.Update_Buttons ()

  while self.My_EventLoop.Pending(): self.My_EventLoop.Dispatch()
  time.sleep(0.02)
  self.ProcessIdle()




# ***********************************************************************
# PyLab_Works_Simulation_File  (example)
# ***********************************************************************
import PyLab_Works_Globals as PG

PG.Bricks[1].In[0] = PG.Bricks[2].Out[0]
PG.Bricks[2].In[0] = PG.Bricks[3].Out[0]

PG.Bricks[0].Exec()
PG.Bricks[1].Exec()
PG.Bricks[2].Exec()
PG.Bricks[3].Exec()
