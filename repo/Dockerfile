FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

#COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["streamlit","run"]
CMD ["app.py","--server.enableCORS","false","--browser.serverAddress","0.0.0.0","--browser.gatherUsageStats","false","--server.port","8080"]