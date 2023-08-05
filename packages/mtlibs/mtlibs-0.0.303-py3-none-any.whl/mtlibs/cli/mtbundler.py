#!/usr/bin/env python3
# 用于docker build 文件的加密打包，容器启动的解密解压
import sys
import os
from mtlibs.docker_helper import isInContainer
from mtlibs import process_helper
from pathlib import Path
import logging
from dotenv import load_dotenv, find_dotenv
from mtlibs.github import gitup
import time
import argparse  
from mtlibs import docker_helper

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#默认密码
DEFAULT_BUNDlER_PASS="secret----DEFAULT_BUNDlER_PASS------19199";
def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", default=None, nargs="*") 
    args = parser.parse_args()
    logger.info(f"urls: {args.urls}")
    
    password = os.environ.get("MTX_BUNDLER_PASS",DEFAULT_BUNDlER_PASS)
    logger.info(f"密码: {password}")
    if docker_helper.isInContainer():
        logger.info(f"在容器中，TODO，解压并运行主程序")
        
    else:
        logger.info(f"在构建阶段，TODO：压缩加密 workdir 下的文件")
    

if __name__ == "__main__":
    main()



