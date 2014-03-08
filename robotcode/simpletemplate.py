try:
    import wpilib as wp
except:
    from pyfrc import wpilib as wp

class Robot(wp.SimpleRobot):
    def __init__(self, *args):
        super().__init__(*args)

    def RobotInit(self):
        pass

    def CheckRestart(self):
        pass

    def Disabled(self):
        while self.IsDisabled():
            self.CheckRestart()
            wp.Wait(0.01)

    def Autonomous(self):
        while self.IsAutonomous() and self.IsEnabled():
            self.CheckRestart()
            wp.Wait(0.01)

    def OperatorControl(self):
        while self.IsOperatorControl() and self.IsEnabled():
            self.CheckRestart()
            wp.Wait(0.04)

def run():
    robot = Robot()
    robot.StartCompetition()

if __name__ == "__main__":
    import frcupload
    frcupload.run(__file__)