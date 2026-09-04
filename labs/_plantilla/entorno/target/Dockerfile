# Target del lab NN. Solo biblioteca estándar de Python (o cambialo por la
# imagen vulnerable que uses: FROM vulnerables/web-dvwa, etc.)
FROM python:3.12-slim
WORKDIR /app
COPY server.py /app/server.py
EXPOSE 80
CMD ["python3", "/app/server.py"]
