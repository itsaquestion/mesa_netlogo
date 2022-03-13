import pyNetLogo

class NL:

    def __init__(self):
        self.netlogo = pyNetLogo.NetLogoLink(gui=True)

    def load_model(self, model_path):
        # model_path = r'd:\a.nlogo'
        self.netlogo.load_model(model_path)

    def report(self, x):
        return self.netlogo.report(x)

    def cmd(self, x):
        self.netlogo.command(x)

    def clear_reset(self):
        self.cmd("clear-all")
        self.cmd("reset-ticks")

    def tick(self):
        self.cmd('tick')

    def get(self, var: str):
        return self.report(f"{var}")

    def set(self, var: str, value):
        return self.cmd(f'set {var} {value}')

    def close(self):
        self.netlogo.kill_workspace()
