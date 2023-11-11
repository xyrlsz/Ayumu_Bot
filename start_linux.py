import os
import subprocess
from io import BytesIO


exe_path = "./OPQBot"
command = "-token"
tokne = "9846bd208263a32987069f0d87828b58"

subprocess.call([exe_path, command, tokne])
