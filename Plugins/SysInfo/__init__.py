import asyncio
import platform
import psutil
import time
import datetime

from Based.Event import Event
from Based.Send_Message import send_message
from Based.Message import TextMessage


async def getSysInfo(messge: Event):
    content = messge.getEventData().Content()
    if content:
        content = content.strip()
        if (
            content.find("系统信息") != -1
            and str(messge.getEventData().SenderUin()) == "2434221948"
        ):
            # 获取平台信息
            platform_info = platform.system()

            # 获取CPU架构信息
            cpu_architecture = platform.architecture()[0]

            # 获取内存信息
            memory_info = psutil.virtual_memory()
            total_memory = memory_info.total
            used_memory = memory_info.used
            memory_percent = memory_info.percent

            # 获取当前进程占用的内存信息
            process = psutil.Process()
            process_memory_info = process.memory_info()
            process_memory = process_memory_info.rss  # Resident Set Size (进程占用的物理内存)

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
                    messge.getEventData().FromUin(),
                    messge.getEventData().FromType(),
                    info,
                )
            )
            del info
            return True

    return False


last_send_sys_info_time = 0


def is_whole_hour_or_half():
    current_time = datetime.datetime.now().time()
    return current_time.minute == 0 or current_time.minute == 30


def your_task():
    # 这里执行你的任务逻辑
    print("任务执行中...")


def send_info():
    try:
        platform_info = platform.system()

        # 获取CPU架构信息
        cpu_architecture = platform.architecture()[0]

        # 获取内存信息
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total
        used_memory = memory_info.used
        memory_percent = memory_info.percent

        # 获取当前进程占用的内存信息
        process = psutil.Process()
        process_memory_info = process.memory_info()
        process_memory = process_memory_info.rss  # Resident Set Size (进程占用的物理内存)

        info = f"""
                    系统平台：{platform_info}\nCPU信息：{cpu_architecture}\n总内存：{total_memory / (1024 ** 2):.2f} MB\n已使用：{used_memory / (1024 ** 2):.2f} MB\n已使用百分比：{memory_percent}%\n当前进程占用：{process_memory / (1024 ** 2):.2f} MB\n
                    """
        info = info.strip()

        send_message(TextMessage(721213151, 2, info))

    except Exception as e:
        print(f"An error occurred: {e}")


def periodic_send_info():
    while True:
        if is_whole_hour_or_half():
            send_info()
        time.sleep(60)
