FROM python:3.9.18-slim
LABEL authors="tekporlipos"
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install wheel
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

RUN pytest -q ./test/unit test

RUN if [ $? -ne 0 ]; then \
        echo "Unit tests failed. Exiting..."; \
        exit 1; \
    fi

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
