import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/lowRISC/ibex"

# Module version
version_str = "0.0.post2680"
version_tuple = (0, 0, 2680)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post2680")
except ImportError:
    pass

# Data version info
data_version_str = "0.0.post2538"
data_version_tuple = (0, 0, 2538)
try:
    from packaging.version import Version as V
    pdata_version = V("0.0.post2538")
except ImportError:
    pass
data_git_hash = "56268c675a9f160f01a0f5a1f548c0db716b2a40"
data_git_describe = "v0.0-2538-g56268c67"
data_git_msg = """\
commit 56268c675a9f160f01a0f5a1f548c0db716b2a40
Author: Canberk Topal <ctopal@lowrisc.org>
Date:   Fri Nov 4 17:44:19 2022 +0000

    [dv] Generate random writes in custom CSRs
    
    This commit adds random custom CSR writes to debug_single_step_test
    and riscv_mem_error_test.
    
    Signed-off-by: Canberk Topal <ctopal@lowrisc.org>

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_ibex."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_ibex".format(f))
    return fn
