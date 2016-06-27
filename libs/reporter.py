"""
Reporter will take the generated junit file and push it up
to betelguese.
"""
from libs.generator import Generator


class Reporter(Generator):
    def __init__(self, filename, results, test_id):
        super.__init__()


