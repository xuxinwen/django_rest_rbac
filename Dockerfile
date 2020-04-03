FROM python:3.6.8

# 设置环境变量
ENV APP_ROOT /app
ENV TIME_ZONE=UTC

# 工作目录
WORKDIR ${APP_ROOT}/

# 阿里源
COPY conf/source/sources.list /etc/apt/sources.list

RUN deps='net-tools supervisor gettext git vim' \
    && set -x \
    && apt update -y \
    && apt-get install -y $deps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN deps='build-essential python3-dev python3-pip python3-setuptools' \
    && set -x \
    && apt update -y \
    && apt-get install -y $deps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 环境准备
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

# 安装依赖，requirements.txt变化少，pip层就容易被缓存，如果项目全部拷贝的话，这一层需要经常重新制作
COPY requirements.txt ${APP_ROOT}/
RUN pip install --no-cache-dir --trusted-host pypi.douban.com -i http://pypi.douban.com/simple/ -r requirements.txt

# 拷贝全部文件，在这主要是Docker是分层的，这一个经常容易变化，所以需要在后面拷贝进来
COPY . ${APP_ROOT}

# 配置 supervisor gunicorn
RUN cp conf/supervisord.conf /etc/supervisor/ \
    && cp conf/supervisor/* /etc/supervisor/conf.d \
    && python manage.py collectstatic --no-input \
    && chmod u+x run.sh

# 执行前台脚本
CMD ["./run.sh"]
