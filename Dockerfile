
FROM python:3.8-slim

# RUN apt-get update && apt-get -y install libpq-dev gcc

# RUN adduser myuser
# USER myuser

# # 
# WORKDIR /app

# # 
# COPY --chown=myuser:myuser requirements.txt .

# # 
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# # 
# ENV PATH="/home/myuser/.local/bin:${PATH}"
# COPY --chown=myuser:myuser ./app /app

# EXPOSE 8000

# #COPY --chown=myuser:myuser . .
# # 
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]