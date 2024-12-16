# R4C - Robots for consumers

# Requirements 
[Docker](https://www.docker.com/)

# How to start
First of all, you need to setup your `.env` file. You can simply copy `.env.example` to `.env`
```bash
cp .env.example .env
```
Then, start docker compose 
```bash
docker compose up
```

In case, if you want to use `admin/`, you need to create superuser, i've mounted all project folder to docker container, so you can simply use 
```bash
python manage.py createsuperuser
```

# Testing project

After docker will start up, you can test the project

## First task - robot create endpoint
Endpoint located at `/api/robots/`, accepts only `POST` method, and data, that you will send, should be like
```json
{
    "model":"R4",
    "version":"D4",
    "created":"2024-12-11 00:00:00" 
}
```
Data validation was made with django forms.

You can test this endpoint with:
```bash
curl -X POST http://127.0.0.1:8000/api/robots/ \
-H "Content-Type: application/json" \
-d '{
    "model": "R4",
    "version": "D4",
    "created": "2024-12-11 00:00:00"
}'
```

If data is body is valid, endpoint should return status code `200` and:
```json
{"message": "success"}
```

If not, it will return status code 400 and all errors, that exists in data(like len of model is to big, or invalid date time format):
```json
{
    "errors": {
        "model": [
            "Ensure this value has at most 2 characters (it has 3)."
        ],
        "version": [
            "Ensure this value has at most 2 characters (it has 3)."
        ],
        "created": [
            "Enter a valid date/time."
        ]
    }
}
```
I've registered all models in `django admin`, so you can check your robots at `admin/`. 

## Second task - get excel report with robots
I am using `openpyxl` for working with excel tables. Endpoint located at `report/`, accepts only `GET` method, and returns file as attachment. There is no template for this view.

For testing it, you can use
```bash
curl -I http://127.0.0.1:8000/report/
```
It will return `Content-Disposition: attachment; filename=robot_report.xlsx`, if you want download the file, just put the `http://127.0.0.1:8000/report/` in your browser.

Excel table generation happens in `celery task`(robot/tasks.py). Task get datetime.now(), and timedelta of 7 days, then just filter all robots by this range, grouping by model and version, and counts groups.

## Third task - email sending to customer
Endpoint located at `order/`. There would be a simple bootstrap form, that requires a customer email and robot serial(`R2-D2` for example). All data validation was made with django form. After successfull order, app will check, if there exists a robot with the same serial, it will create order in DB, and send email message with order data. Otherwise, it will send message that says "we don't have robot yet, and will notify you when it will appear". After every successfull creation of robot, we have a signal, that check, if any customers was interested in robot with that serial, if so, then we send an email, that robot appeared. 

For testing it, just go to `order/` and make an order. All emails coming to `mailpit` located at `localhost:8025`. Also you can check the how the signal work. Make an order for non-existing robot, and then add it to DB. 

All email sending was made with celery tasks

