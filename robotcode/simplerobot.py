try:
    import wpilib as wp
except:
    from pyfrc import wpilib as wp
RED_ON_THRESHOLD = 5
class Robot(wp.SimpleRobot):
    def __init__(self, *args):
        super().__init__(*args)

    def RobotInit(self):
        print(wp.DoubleSolenoid.kForward, wp.DoubleSolenoid.kReverse)
        self.drive = wp.RobotDrive(1, 2, 3, 4)
        self.joystick = wp.Joystick(1)
        self.compressor = wp.Compressor(2, 2)
        self.right_shooter_piston = wp.Solenoid(1)
        self.left_shooter_piston = wp.Solenoid(2)
        self.harvester_piston = wp.DoubleSolenoid(3, 4)
        self.harvester_wheels = wp.Victor(5)
        self.light = wp.Solenoid(6)
        self.pressure_sensor = wp.AnalogChannel(2)
        self.range_finder = wp.Ultrasonic(3, 1)
        self.lcd = wp.DriverStationLCD.GetInstance()
        self.timer = wp.Timer()
        #wp.SmartDashboard.init()
        #wp.SmartDashboard.PutNumber("Shoot Charge Time", 0)
        self.shooter_timing = False

    def CheckRestart(self):
        pass

    def Disabled(self):
        while self.IsDisabled():
            self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
            self.CheckRestart()
            wp.Wait(0.01)

    def Autonomous(self):
        self.timer.Start()
        #if wp.SmartDashboard.GetNumber("ModeCount") < RED_ON_THRESHOLD:
        #    wp.Wait(5)
        self.light.Set(True)
        while self.IsAutonomous() and self.IsEnabled():
            if self.timer.Get() < 1.27:
                self.drive.TankDrive(1, 1)
                self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
            elif self.timer.Get() < 2.3:
                self.drive.TankDrive(0,0)
                self.harvester_piston.Set(wp.DoubleSolenoid.kForward)
            elif self.timer.Get() > 3.2:
                self.drive.TankDrive(0,0)
                self.right_shooter_piston.Set(True)
                self.left_shooter_piston.Set(True)
            self.CheckRestart()
            wp.Wait(0.04)
        self.timer.Stop()
        self.timer.Reset()
    def Test(self):
        self.compressor.Start()
        while self.IsTest() and self.IsEnabled():
            wp.Wait(.01)
    def OperatorControl(self):
        self.compressor.Start()
        self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
        self.light.Set(True)
        while self.IsOperatorControl() and self.IsEnabled():
            self.drive.TankDrive(self.joystick.GetRawAxis(5), self.joystick.GetRawAxis(2))
            self.harvester_wheels.Set(-1 if self.joystick.GetRawAxis(3) < -.7 else 1 if self.joystick.GetRawAxis(3) > .7  else 0)
            # Forward moves harvester out, reverse moves it in
            piston_value = wp.DoubleSolenoid.kReverse if self.joystick.GetRawButton(3) else wp.DoubleSolenoid.kForward if self.joystick.GetRawButton(2) else self.harvester_piston.Get()
            self.harvester_piston.Set(piston_value)
            shoot = self.joystick.GetRawButton(1)
            self.left_shooter_piston.Set(shoot)
            self.right_shooter_piston.Set(shoot)

            if shoot:
                self.shooter_timing = True
                self.timer.Reset()

            if self.shooter_timing and shoot:
                self.timer.Start()
            if self.shooter_timing:
                if self.timer.Get() > 10:
                    self.timer.Stop()
                    self.timer.Reset()
                    print("Can shoot")
                    self.shooter_timing = False
            self.lcd.PrintLine(0, str((self.pressure_sensor.GetAverageVoltage()/1.91)*120))
            self.lcd.UpdateLCD()
            #wp.SmartDashboard.PutNumber("PSI", (self.pressure_sensor.GetAverageVoltage()/1.91)*120)
            self.CheckRestart()
            wp.Wait(0.04)


def run():
    robot = Robot()
    robot.StartCompetition()
