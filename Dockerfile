FROM python:3.12

WORKDIR /app

ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .  

RUN pip install --no-cache -r requirements.txt

COPY . . 

CMD ["python", "scheduler.py"]