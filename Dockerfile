FROM python:3.11.1-slim-bullseye

ENV PYTHONUNBUFFERED 1
WORKDIR /build

# Создаем venv, добавляем в PATH, устанавливаем зависимости из requirements.txt
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Устанавливаем uvicorn
RUN pip install uvicorn[standard]

# Копируем приложение
COPY . app

# Create new user to run app process as unprivilaged user
RUN addgroup --gid 1001 --system uvicorn && \
    adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 uvicorn

# Run init.sh script then start uvicorn
RUN chown -R uvicorn:uvicorn /build
RUN chmod +xr app/init.sh
ENTRYPOINT ["/bin/bash", "init.sh"]
EXPOSE 8000
