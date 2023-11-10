import os
import subprocess
from io import BytesIO


exe_path = "./OPQBot"
command = "-token"
tokne = "7b4909d1b1af2dcaa46a28250d4f6de8"

subprocess.call([exe_path, command, tokne])
