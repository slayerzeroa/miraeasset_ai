# Dockerfile

# 베이스 이미지 설정
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /djangoweb

# 필요 패키지 설치
COPY requirements.txt /djangoweb/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . /djangoweb/

# 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONUNBUFFERED=1

# 포트 설정
EXPOSE 5555

# 애플리케이션 실행 명령어
CMD ["gunicorn", "--bind", "0.0.0.0:5555", "config.wsgi:application"]
