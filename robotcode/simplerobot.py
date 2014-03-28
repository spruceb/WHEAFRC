try:
    import wpilib as wp
except:
    from pyfrc import wpilib as wp


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
        self.pressure_sensor = wp.AnalogChannel(2)

        self.lcd = wp.DriverStationLCD.GetInstance()

    def CheckRestart(self):
        pass

    def Disabled(self):
        while self.IsDisabled():
            self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
            self.CheckRestart()
            wp.Wait(0.01)

    def Shoot(self, value):
        self.left_shooter_piston.Set(value)
        self.right_shooter_piston.Set(value)

    def Autonomous(self):
        timer = wp.Timer()
        timer.Start()
        while self.IsAutonomous() and self.IsEnabled():
            if timer.Get() < 1.275:
                self.drive.TankDrive(1, 1)
                self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
            elif timer.Get() < 2.3:
                self.harvester_piston.Set(wp.DoubleSolenoid.kForward)
            elif 4.2 > timer.Get() > 3.2:
                self.Shoot(True)
                self.CheckRestart()
            wp.Wait(0.04)

    #def Autonomous(self):
    #    timer = wp.Timer()
    #    timer.Start()
    #    self.light.Set(True)
    #    while self.IsAutonomous() and self.IsEnabled():
    #        if timer.Get() < 1.27:
    #            self.drive.TankDrive(.99, 1)
    #            self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
    #        elif timer.Get() < 2.44:
    #            self.drive.TankDrive(-.94, -1)
    #        elif timer.Get() < 2:
    #            self.harvester_piston.Set(wp.DoubleSolenoid.kForward)
    #        elif timer.Get() < 2.7:
    #            wp.Wait(.01)
    #        elif timer.Get() < 3.1:
    #            self.Shoot(True)
    #        elif timer.Get() < 3.5:
    #            self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
    #            self.Shoot(False)
    #        elif timer.Get() < 4.77:
    #            self.drive.TankDrive(-.94, -1)
    #        elif timer.Get() < 5.7:
    #            self.harvester_piston.Set(wp.DoubleSolenoid.kForward)
    #            self.harvester_wheels.Set(-1)
    #        elif timer.Get() < 6.2:
    #            self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
    #        elif timer.Get() < 7.47:
    #            self.drive.TankDrive(1,1)
    #        elif timer.Get() < 8.2:
    #            self.harvester_piston.Set(wp.DoubleSolenoid.kForward)
    #        elif timer.Get() < 10:
    #            self.Shoot(True)
    #        wp.Wait(0.04)

    def Test(self):
        self.compressor.Start()
        while self.IsTest() and self.IsEnabled():
            wp.Wait(.01)

    def OperatorControl(self):
        self.compressor.Start()
        self.harvester_piston.Set(wp.DoubleSolenoid.kReverse)
        while self.IsOperatorControl() and self.IsEnabled():
            self.drive.TankDrive(self.joystick.GetRawAxis(5), self.joystick.GetRawAxis(2))
            # -1 pulls ball in, 1 pushes out
            self.harvester_wheels.Set(
                -1 if self.joystick.GetRawAxis(3) < -.7 else 1 if self.joystick.GetRawAxis(3) > .7  else 0)
            # Forward moves harvester out, Reverse moves it in
            # 1 = kForward, 2 = kReverse
            piston_value = 1 if self.joystick.GetRawButton(3) else 2 if self.joystick.GetRawButton(
                2) else self.harvester_piston.Get()
            self.harvester_piston.Set(piston_value)
            self.Shoot(self.joystick.GetRawButton(1))

            self.lcd.PrintLine(0, "PSI: " + str(int((self.pressure_sensor.GetAverageVoltage() / 1.91) * 120)))
            self.lcd.UpdateLCD()
            self.CheckRestart()
            wp.Wait(0.04)


def run():
    robot = Robot()
    robot.StartCompetition()
