import platform

import psutil

from Based.Event import Event
from Based.Message import TextMessage
from Based.Send_Message import send_message
from Based.Config import super_users


async def getSysInfo(message: Event):
    if message.getEventData().isBot:
        return False
    content = message.getEventData().Content()
    if content:
        content = content.strip()
        if (
            content.find("系统信息") != -1
            and (message.getEventData().SenderUin()) in super_users
        ):
            # 获取系统
            # platform_info = platform.system()
            platform_info = platform.platform()

            # 获取CPU架构信息
            # cpu_architecture = platform.architecture()[0]
            cpu_architecture = platform.machine()
            # 获取内存信息
            memory_info = psutil.virtual_memory()
            total_memory = memory_info.total
            used_memory = memory_info.used
            memory_percent = memory_info.percent

            # 获取当前进程占用的内存信息
            process = psutil.Process()
            process_memory_info = process.memory_info()
            process_memory = (
                process_memory_info.rss
            )  # Resident Set Size (进程占用的物理内存)

            # 打印信息
            # print(f"Platform: {platform_info}")
            # print(f"CPU Architecture: {cpu_architecture}")
            # print(f"Total Memory: {total_memory / (1024 ** 3):.2f} GB")
            # print(f"Used Memory: {used_memory / (1024 ** 3):.2f} GB")
            # print(f"Memory Percent: {memory_percent}%")
            # print(f"Process Memory Usage: {process_memory / (1024 ** 2):.2f} MB")

            info = f"""
            系统平台：{platform_info}\nCPU信息：{cpu_architecture}\n总内存：{total_memory / (1024 ** 2):.2f} MB\n已使用：{used_memory / (1024 ** 2):.2f} MB\n已使用百分比：{memory_percent}%\n当前进程占用：{process_memory / (1024 ** 2):.2f} MB\n
            """
            info = info.strip()
            send_message(
                TextMessage(
                    message.getEventData().FromUin(),
                    message.getEventData().FromType(),
                    info,
                )
            )
            del info
            return True

    return False
