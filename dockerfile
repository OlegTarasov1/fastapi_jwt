FROM python

WORKDIR /jwt_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY jwt_app .

CMD [ "python3", "main.py" ]