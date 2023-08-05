# syntax=docker/dockerfile:1

# 用环境变量的方式标识当前处于docker build环境中。
ARG MTX_DOCKER_BUILD=1
ARG MTX_BUNDLER_PASS
ARG WORKDIR=/app
#####################################################################
## 安装生产环境下必要的软件包
FROM gitgit188/base as base
ARG WORKDIR
WORKDIR ${WORKDIR}
RUN pip --no-cache-dir install mtlibs>0.0.310 -U



#####################################################################
## 模拟普通的docker build 在/app上正常放可执行源码
FROM gitgit188/base as builder
ARG MTX_BUNDLER_PASS
ARG MTX_DOCKER_BUILD
ARG WORKDIR
WORKDIR ${WORKDIR}
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python3 -m build
RUN pip install --editable .

#####################################################################
## 将源码打包加密
FROM base as bundler
ARG MTX_BUNDLER_PASS
ARG MTX_DOCKER_BUILD
ARG WORKDIR
WORKDIR ${WORKDIR}
# 加密打包应用源码
RUN mtbundler
RUN rm -rdf ${WORKDIR}



#####################################################################
## 将加密了的程序包单独抽取到生产环境
FROM base as prod
COPY --from=bundler /package.tar.gz.gpg /package.tar.gz.gpg
RUN echo "显示打包的结果" && ls -al /
ENTRYPOINT [ "mtbundler" ]