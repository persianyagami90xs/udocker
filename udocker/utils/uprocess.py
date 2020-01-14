# -*- coding: utf-8 -*-
"""Alternative implementations for subprocess"""

import subprocess
import sys
from udocker.msg import Msg

# Python version major.minor
PY_VER = "%d.%d" % (sys.version_info[0], sys.version_info[1])


class Uprocess(object):
    """Provide alternative implementations for subprocess"""

    def _check_output(self, *popenargs, **kwargs):
        """Alternative to subprocess.check_output"""
        process = subprocess.Popen(*popenargs, stdout=subprocess.PIPE, **kwargs)
        output, dummy = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output

    def check_output(self, *popenargs, **kwargs):
        """Select check_output implementation"""
        chk_out = ""
        if PY_VER == "2.6":
            chk_out = self._check_output(*popenargs, **kwargs)
        if PY_VER == "2.7":
            chk_out = subprocess.check_output(*popenargs, **kwargs)
        if PY_VER >= "3":
            command = subprocess.check_output(*popenargs, **kwargs)
            chk_out = command.decode()

        return chk_out

    def get_output(self, cmd):
        """Execute a shell command and get its output"""
        try:
            content = self.check_output(cmd, shell=True,
                                        stderr=Msg.chlderr,
                                        close_fds=True)
        except subprocess.CalledProcessError:
            return None
        return content.strip()