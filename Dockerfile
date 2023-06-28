# 设置基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app
COPY . .

# 安装依赖包
RUN pip install -r requirements.txt

# 运行应用程序
CMD ["python", "main.py"]
