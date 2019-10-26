  def MainLoop(self):
    # take over the event loop, but save the old one
    self.My_EventLoop = wx.EventLoop ()
    old = wx.EventLoop.GetActive ()
    wx.EventLoop.SetActive ( self.My_EventLoop )

    PG.App_Running = True
    Previous_Time = time.time()
    Loop_Time = Previous_Time
    Previous_N    = 0

    global output_lines, output_bricks
    SI = 0
    SIN = len ( output_bricks )
    print 'YYY',output_bricks, len(output_bricks)

    while PG.App_Running :
      if PG.State in [PG.SS_Run, PG.SS_Step]:
        try:
          #print 'PIEP'
          if PG.Execution_HighLight or ( PG.State == PG.SS_Step ):
            try :
              #print ' loploploplop'
              exec ( output_lines [ SI ] )
              Brick = PG.Bricks [ output_bricks [ SI ] ]
              #print SI,output_bricks,PG.Bricks
              Brick.On = False
              Brick.BP_Flag = 2
              Brick._Redraw()

            except :
              print ' prprprprp', SIN, len (output_lines), SI
            SI += 1
            SI %= SIN

            while ( time.time() - Loop_Time ) < 3 :
              while self.My_EventLoop.Pending():
                self.My_EventLoop.Dispatch()
              self.ProcessIdle()
              time.sleep ( 0.02 )
            #time.sleep ( 3 )
            Brick.On = True
            Brick.BP_Flag = 0
            Brick._Redraw()

          else :
            execfile ( PG.Simulation_Filename )

        except PG.Reload_Exception:
          print 'Program aborted in Simulation File'
        except:
          import traceback
          traceback.print_exc ()
          print 'Error in Simulation File'

        if PG.State == PG.SS_Step :
          PG.State = PG.SS_Stop
        PG.Main_Form.Update_Buttons ()

      while self.My_EventLoop.Pending(): self.My_EventLoop.Dispatch()
      self.ProcessIdle()
      #time.sleep(0.02)
      #self.ProcessIdle()
      ddT = 0.02 - ( time.time() - Loop_Time )
      if ddT > 0 :
        time.sleep ( ddT )
      Loop_Time = time.time()


      # Every second display fps in statusbar
      # COULD BE USED TO CORRECT THE IDLE TIME !!
      Previous_N += 1
      dT = time.time() - Previous_Time

      if dT > 1.0 :
        line = str ( int ( round ( Previous_N / dT ) ) ) + ' fps'
        Previous_N = 0
        Previous_Time = time.time ()
        try : # Form may already have been removed
          PG.Final_App_Form.SetStatusText ( line, 4 )
        except :
          pass
