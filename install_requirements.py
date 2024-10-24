import os
import platform
import subprocess

# Install common requirements
subprocess.check_call([os.sys.executable, "-m", "pip", "install", "-r", "requirements.in"])

# Conditionally install uvloop on non-Windows systems
if platform.system() != "Windows":
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "uvloop==0.19.0"])
