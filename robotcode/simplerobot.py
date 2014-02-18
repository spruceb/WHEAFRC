try:
    import wpilib as wp
except:
    from pyfrc import wpilib as wp

class Robot(wp.SimpleRobot):
    def __init__(self, *args):
        super().__init__(*args)

    def RobotInit(self):
        self.drive = wp.RobotDrive(1, 2, 3, 4)
        self.joystick = wp.Joystick(1)
        self.compressor = wp.Compressor(2, 2)
        self.right_shooter_piston = wp.Solenoid(1)
        self.left_shooter_piston = wp.Solenoid(2)
        self.harvester_piston = wp.DoubleSolenoid(3, 4)
        self.harvester_wheels = wp.Victor(5)
        self.timer = wp.Timer()
        wp.SmartDashboard.init()
        wp.SmartDashboard.PutNumber("Shoot Charge Time", 0)
        self.shooter_timing = False

    def CheckRestart(self):
        if self.joystick.GetRawButton(8):
            self.Restart()

    def Restart(self):
        raise SystemExit("Robot Restart() called")

    def Disabled(self):
        while self.IsDisabled():
            self.CheckRestart()
            wp.Wait(0.01)

    def Autonomous(self):
        while self.IsAutonomous() and self.IsEnabled():
            self.CheckRestart()
            wp.Wait(0.01)

    def OperatorControl(self):
        self.compressor.Start()
        while self.IsOperatorControl() and self.IsEnabled():
            self.drive.TankDrive(self.joystick.GetRawAxis(5), self.joystick.GetRawAxis(2))
            self.harvester_wheels.Set(-1 if self.joystick.GetRawAxis(3) < -.7 else 1 if self.joystick.GetRawAxis(3) > .7  else 0)
            self.harvester_piston.Set(2 if self.joystick.GetRawButton(3) else 1 if self.joystick.GetRawButton(2) else 0)
            shoot = self.joystick.GetRawButton(1)
            self.left_shooter_piston.Set(shoot)
            self.right_shooter_piston.Set(shoot)

            if shoot:
                self.shooter_timing = True
                self.timer.Reset()

            if self.shooter_timing and shoot:
                self.timer.Start()
            if self.shooter_timing:
                #wp.SmartDashboard.PutNumber("Shoot Charge Time", self.timer.Get())
                print(self.timer.Get())
                if self.timer.Get() > 10:
                    self.timer.Stop()
                    self.timer.Reset()
                    #wp.SmartDashboard.PutNumber("Shoot Charge Time", 0)
                    print(0)
                    self.shooter_timing = False

            self.CheckRestart()
            wp.Wait(0.04)

def run():
    robot = Robot()
    robot.StartCompetition()
