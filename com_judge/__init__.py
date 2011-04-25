
"""
The Computer judge.
"""

import os
from subprocess import Popen, PIPE
import tempfile
import unittest

SOURCE_ROOT = os.path.join(os.path.abspath(os.path.curdir), "junk")
if not os.path.exists(SOURCE_ROOT):
    os.mkdir(SOURCE_ROOT)


class ComJudge:
    """
    Generate the evaluation of source code.

    Currently supported languages for the source code:
     - Python

    Return codes for Python interpreter:
     0 - Everything went fine
     1 - Error occurred (SyntaxError, )
    """
    def __init__(self, compiler, source_code):
        self.compiler = compiler
        self.source_code = source_code
        self.temp_name = None

        self.status_code = None
        self.output = None
        self.errors = None

    def run(self):
        """
        Compile the source code.
        """
        self._create_temp_name()
        cmd = self._make_command()


        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        process.wait()

        self.status_code = process.returncode
        stdout, stderr = process.communicate()
        self.output = stdout
        self.errors = stderr

        if "python" in cmd and not(os.path.exists(self.temp_name)):
            pass # TODO

    def _make_command(self):
        cmd = ""
        if self.compiler == "python":
            cmd = self.compiler + " " + self.temp_name
        return cmd

    def _create_temp_name(self):
        """
        Create a temporary file, write the source code to it, and save the file name.
        """
        temp_name = None
        if self.compiler == "python":
            temp_name = tempfile.mktemp(".py", dir=SOURCE_ROOT)
        temp = open(temp_name, 'w')
        temp.write(self.source_code)
        temp.close()

        self.temp_name = temp_name

    def get_status(self):
        """
        Returns a tuple with the following information:
         (status_code, output, errors)
        """
        return (self.status_code, self.output, self.errors)



class TestComJudge(unittest.TestCase):

    def test_python_source_code(self):
        compiler = "python"
        source_code = """
print "Hello world in Python"
        """
        c = ComJudge(compiler, source_code)
        c.run()
        status = c.get_status()

        self.assertEquals(status[0], 0)
        self.assertNotEquals(status[1], None)
        self.assertEquals(status[2], "")

    def test_python_syntax_error(self):
        compiler = "python"
        source_code = """
prit "Hello world in Python"
        """
        c = ComJudge(compiler, source_code)
        c.run()
        status = c.get_status()
        self.assertEquals(status[0], 1)
        self.assertEquals(status[1], '')
        self.assertNotEquals(status[2], '')

    def test_python_division_by_zero_error(self):
        compiler = "python"
        source_code = """
x = 2 / 0
        """
        c = ComJudge(compiler, source_code)
        c.run()
        status = c.get_status()
        self.assertEquals(status[0], 1)
        self.assertEquals(status[1], '')
        self.assertNotEquals(status[2], '')

if __name__ == "__main__":
    unittest.main()
