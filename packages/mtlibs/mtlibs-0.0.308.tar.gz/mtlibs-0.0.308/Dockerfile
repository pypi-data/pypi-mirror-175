# syntax=docker/dockerfile:1

ARG NEXT_PUBLIC_BACKEND_URL
ARG WORKDIR=/app
#####################################################################
## 安装生产环境下必要的软件包
FROM gitgit188/base as mtcms_base
ARG WORKDIR
WORKDIR ${WORKDIR}
RUN pip install mtlibs>0.0.307 -U



#####################################################################
## 解压 测试容器
FROM gitgit188/base as test
ARG WORKDIR
WORKDIR ${WORKDIR}
RUN pip install mtlibs>0.0.307 -U
RUN echo "123" > ${WORKDIR}/hello.txt
# 加密打包应用源码
RUN mtbundler