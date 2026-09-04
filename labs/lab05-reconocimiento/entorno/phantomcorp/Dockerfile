# Target del Lab 05 — PhantomCorp. Solo biblioteca estándar de Python.
FROM python:3.12-slim
WORKDIR /app
COPY server.py /app/server.py
# Documentamos los puertos (informativo; la red interna igual los expone todos)
EXPOSE 21 80 8080 31337
CMD ["python3", "/app/server.py"]
