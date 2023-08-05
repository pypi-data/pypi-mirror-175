#!/usr/bin/env python3
# 用于docker build 文件的加密打包，容器启动的解密解压
import sys
import os
from docker_helper import isInContainer
import process_helper
from pathlib import Path
import logging
from dotenv import load_dotenv, find_dotenv
from github import gitup
import time
import argparse
import docker_helper
import os
import subprocess
from subprocess import run

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#默认密码
DEFAULT_BUNDlER_PASS="secretpassword";

def build_bundle(password):
    target_dir = os.getcwd()
    logger.info(f"app dir: {target_dir}")
    cmd = f"""cd / && tar -czf - "{target_dir}" | gpg -c --passphrase "{password}" --symmetric --batch > /package.tar.gz.gpg"""
    logger.info(f"shell 命令：{cmd}")
    subprocess.run(cmd, shell=True)


def container_up(password, entry="bin/entry"):
    logger.info("容器启动，开始解密，")
    cmd = f"""gpg --batch --passphrase "{password}" -d /package.tar.gz.gpg | tar -xvzf -"""
    logger.info(f"解压命令: {cmd}")
    subprocess.run(cmd, shell=True)
    logger.info(f"启动命令入口程序 {entry}")
    cmd_entry = f"""cd /app && bash -c "{entry}" """
    subprocess.run(cmd_entry, shell=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("password", default=None, nargs="*")
    args = parser.parse_args()

    password = os.environ.get("MTX_BUNDLER_PASS",DEFAULT_BUNDlER_PASS)
    logger.info(f"password: {password}")


    is_mtx_build = os.environ.get("MTX_DOCKER_BUILD",False)
    is_docker = docker_helper.is_docker()
    if not is_mtx_build:
        container_up(password)
    else:
        #构建阶段
        build_bundle(password)
if __name__ == "__main__":
    main()