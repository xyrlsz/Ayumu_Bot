# import os


# # 白名单，避免被误删
# WHITELIST = ["pip", "setuptools"]
# # 需要删除的模块列表
# REMOVELIST = []


# # def get_requires(module_name):
# #     """
# #     查看一个模块的依赖
# #     :param module_name: 模块名
# #     :return: module_name 所依赖的模块的列表
# #     """
# #     with os.popen('pip show %s' % module_name) as p:
# #         requires = p.readlines()
# #         if not len(requires):
# #             return []

# #         reqs = ''
# #         for line in requires:
# #             if not line.startswith('Requires:'):
# #                 continue
# #             reqs = line.strip()

# #         requires = reqs.split(':')[-1].replace(' ', '').strip()
# #         if requires:
# #             requires = requires.split(',')
# #         else:
# #             requires = []
# #         return requires
# import subprocess
# import subprocess


# def get_requires(module_name):
#     result = subprocess.run(
#         ["pip", "show", module_name], capture_output=True, text=True, encoding="utf-8"
#     )
#     requires = result.stdout.splitlines()

#     if not requires:
#         return []

#     reqs = next(
#         (line.strip() for line in requires if line.startswith("Requires:")), None
#     )

#     if reqs:
#         requires = reqs.split(":")[-1].replace(" ", "").strip()
#         if requires:
#             requires = requires.split(",")
#         else:
#             requires = []
#     else:
#         requires = []

#     return requires


# def get_required_bys(module_name):
#     """
#     查看一个模块被哪些模块依赖
#     :param module_name: 模块名
#     :return: module_name 被依赖的模块的列表
#     """
#     with os.popen("pip show %s" % module_name) as p:
#         req_by = p.readlines()
#         if not len(req_by):
#             return []

#         required = ""
#         for line in req_by:
#             if not line.startswith("Required-by:"):
#                 continue
#             required = line.strip()

#         req_by = required.split(":")[-1].replace(" ", "").strip()
#         if req_by:
#             req_by = req_by.split(",")
#         else:
#             req_by = []
#         return req_by


# def install(name):
#     os.system(f"pip install {name}")


# def get_all_requires(module_name):
#     """
#     递归地获取一个模块所有的依赖
#     :param module_name: 模块名称
#     :return: None
#     """
#     dependents = get_requires(module_name)
#     for package in dependents:
#         if package in WHITELIST:
#             # print(f'[{package}] in white list')
#             continue
#         get_all_requires(package)
#     REMOVELIST.append(module_name)


# def remove(module_name):
#     print("Scanning packages...")
#     get_all_requires(module_name)
#     s_packages = ",".join(REMOVELIST)
#     print(f"[INFO]Found packages: {s_packages}\n")

#     for package in REMOVELIST:
#         req_bys = get_required_bys(package)
#         print("[INFO]removing:", package)
#         # print(package, 'is required by:', req_bys)
#         flag = True
#         for req_by in req_bys:
#             if req_by not in REMOVELIST:
#                 flag = False
#                 print(
#                     f'[NOTICE]As "{package}" is required by "{req_by}" which is not in {REMOVELIST}, skipped...\n'
#                 )
#                 break
#         if flag:
#             print("\n")
#             os.system("pip uninstall -y %s" % package)


# if __name__ == "__main__":
#     pkg_name = input("请输入要卸载的第三方模块包: ")
#     # install(pkg_name)
#     remove(pkg_name)

import os
import subprocess

WHITELIST = ["pip", "setuptools"]
REMOVELIST = []


def get_requires(module_name):
    result = subprocess.run(
        ["pip", "show", module_name], capture_output=True, text=True, encoding="utf-8"
    )
    requires = result.stdout.splitlines()

    if not requires:
        return []

    reqs = next(
        (line.strip() for line in requires if line.startswith("Requires:")), None
    )

    if reqs:
        requires = reqs.split(":")[-1].replace(" ", "").strip()
        if requires:
            requires = requires.split(",")
        else:
            requires = []
    else:
        requires = []

    return requires


def get_required_bys(module_name):
    with subprocess.Popen(
        ["pip", "show", module_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ) as p:
        try:
            req_by = p.stderr.readlines()
        except UnicodeDecodeError:
            print(
                f"Error decoding Unicode in {module_name} information. Skipping this module."
            )
            return []

    if not req_by or not len(req_by):
        return []

    required = ""
    for line in req_by:
        if not line.startswith("Required-by:"):
            continue
        required = line.strip()

    req_by = required.split(":")[-1].replace(" ", "").strip()
    if req_by:
        req_by = req_by.split(",")
    else:
        req_by = []
    return req_by


def install(name):
    os.system(f"pip install {name}")


def get_all_requires(module_name):
    """
    Recursively get all dependencies and add them to the REMOVELIST.
    :param module_name: Module name
    :return: None
    """
    dependents = get_requires(module_name)

    if module_name not in WHITELIST and module_name not in REMOVELIST:
        REMOVELIST.append(module_name)

    for package in dependents:
        if package not in WHITELIST and package not in REMOVELIST:
            get_all_requires(package)


def remove(module_name):
    print("Scanning packages...")
    get_all_requires(module_name)

    # Reverse the list for uninstalling in the correct order (dependencies first)
    REMOVELIST.reverse()

    s_packages = ", ".join(REMOVELIST)
    print(f"[INFO]Found packages to remove: {s_packages}\n")

    for package in REMOVELIST:
        req_bys = get_required_bys(package)
        print("[INFO]Removing:", package)
        flag = all(req_by in REMOVELIST for req_by in req_bys)
        if flag:
            print("\n")
            os.system("pip uninstall -y %s" % package)
        else:
            print(
                f'[NOTICE]As "{package}" is required by "{req_bys}" which is not in {REMOVELIST}, skipped...\n'
            )


if __name__ == "__main__":
    pkg_name = input("Please enter the name of the third-party module to uninstall: ")
    remove(pkg_name)
