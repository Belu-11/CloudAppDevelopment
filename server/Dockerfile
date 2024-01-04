FROM python:3.8

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# RUN apt-get update && apt-get install -y netcat

ENV APP=/app

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP

RUN pip install -r requirements.txt

# Copy the rest of the files
COPY . $APP

EXPOSE 8000

RUN chmod +x ./entrypoint.sh
# RUN tr -d '\r' < entrypoint.sh > entrypoint_unix.sh && mv entrypoint_unix.sh entrypoint.sh && chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash","./entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
# CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
# RUN ["python", "-m", "dotenv", "-f", ".env", "python", "manage.py", "runserver"]
