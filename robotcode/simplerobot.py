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
        self.right_shooter_piston = wp.DoubleSolenoid(1, 2)
        self.left_shooter_piston = wp.DoubleSolenoid(3, 4)
        #self.right_harvester_piston = wp.DoubleSolenoid(*ports.RIGHT_HARVESTER_SOLENOIDS)
        #self.left_harvester_piston = wp.DoubleSolenoid(*ports.LEFT_HARVESTER_SOLENOIDS)
        self.harvester_wheels = wp.Victor(5)

    def CheckRestart(self):
        if self.joystick.GetRawButton(8):
            self.Restart()

    def Restart(self):
        raise RuntimeError("Robot Restart() called")

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
            self.drive.TankDrive(-self.joystick.GetRawAxis(2), -self.joystick.GetRawAxis(5))
            shooter_direction = wp.DoubleSolenoid.kForward if self.joystick.GetRawButton(1) else wp.DoubleSolenoid.kReverse
            self.right_shooter_piston.Set(shooter_direction)
            self.left_shooter_piston.Set(shooter_direction)
            self.harvester_wheels.Set(-self.joystick.GetRawButton(2))

            self.CheckRestart()
            wp.Wait(0.04)

def run():
    robot = Robot()
    robot.StartCompetition()
