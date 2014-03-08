try:
    import wpilib as wp
except:
    from pyfrc import wpilib as wp

class Robot(wp.SimpleRobot):
    def __init__(self, *args):
        super().__init__(*args)

    def RobotInit(self):
        self.timer = wp.Timer()
        self.drive = wp.RobotDrive(1, 2, 3, 4)
        self.joystick = wp.Joystick(1)
        self.compressor = wp.Compressor(2, 2)
        self.right_shooter_piston = wp.Solenoid(1)
        self.left_shooter_piston = wp.Solenoid(2)
        self.harvester_piston = wp.DoubleSolenoid(3, 4)

    def CheckRestart(self):
        if self.joystick.GetRawButton(8):
            raise SystemExit("Robot Restart() called")

    def Disabled(self):
        while self.IsDisabled():
            self.CheckRestart()
            wp.Wait(0.01)

    def Test(self):
        self.compressor.Start()
        while self.IsTest() and self.IsEnabled():
            wp.Wait(.01)

    def Autonomous(self):
        self.timer.Start()
        while self.IsAutonomous() and self.IsEnabled():
            if self.timer.Get() < 1.65:
                self.drive.TankDrive(1, 1)

            else:#elif self.timer.Get() < 3.75:
                self.drive.TankDrive(0,0)
                self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
            #elif self.timer.Get() < 5:
                self.drive.TankDrive(0,0)
                #self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
                #self.right_shooter_piston.Set(True)
                #self.left_shooter_piston.Set(True)

            #else:
            #    self.right_shooter_piston.Set(False)
            #    self.right_shooter_piston.Set(False)
                #self.drive.TankDrive(0, 0)

            self.CheckRestart()
            wp.Wait(0.04)
        self.timer.Stop()
        self.timer.Reset()

    def OperatorControl(self):
        while self.IsOperatorControl() and self.IsEnabled():
            self.CheckRestart()
            wp.Wait(0.04)

def run():
    robot = Robot()
    robot.StartCompetition()
