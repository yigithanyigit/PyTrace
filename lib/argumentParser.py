import argparse

class ArgumentParser:
    def __init__(self, args):
        self.args = args
        parser = argparse.ArgumentParser(description="Ray Tracer")
        parser.add_argument("--scene", type=str, help="Scene file path", required=True)
        parser.add_argument("--width", type=int, help="Width of the image", required=False, default=800)
        parser.add_argument("--height", type=int, help="Height of the image", required=False, default=600)

        self.args = parser.parse_args(self.args[1:])