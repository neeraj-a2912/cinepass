import csv
from datetime import date, datetime
from celery.schedules import crontab
from jinja2 import Template
from weasyprint import HTML
from mail_configuration import send_email
from models import Show, Theatre, User, Booking
from main import celery, cache


@celery.on_after_finalize.connect
def setup_interval_task(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=12, minute=16),
        daily_mail.s(),
        name = 'Daily Reminder'
    )
    
    sender.add_periodic_task(
        crontab(day_of_month=28, hour=12, minute=16),
        monthly_mail.s(),
        name = 'Montly Report'
    )


@celery.task(name="exportTheatre")
@cache.memoize(timeout=15)
def exTheatre(theatre_id: int):
    
    email = "ticketshow@admin.com"
    attachment = './exports/All_Theatre_Details.csv'
    message = 'CSV File Containing Details of All the Theatres'
    subject = "All Theatre Details"
    
    if theatre_id != 0:
        theatre = Theatre.query.get(theatre_id)
        shows = theatre.shows
        attachment = f'./exports/{theatre.name}.csv'
        message = f'CSV File containing details of the theatre {theatre.name}'   
        subject = f'Theatre Details - {theatre.name}'
        with open(file=f'./exports/{theatre.name}.csv', mode='w') as file:
            csv_obj = csv.writer(file, delimiter=',')
            csv_obj.writerow(['Show id', 'Show Name', 'Theatre', 'Location','Timing', 'Date', 'Screen', 'Available Seats', 'Ticket Price', 'Ratings'])
            for show in shows:
                if datetime.strptime(show.show_date, "%Y-%m-%d").month == datetime.now().month:
                    csv_obj.writerow([show.id, show.name, show.theatre.name, show.theatre.place, show.show_timing, show.show_date, show.screen_number,  show.capacity, 
                                  show.ticket_price, show.ratings])
    else:
        theatres = Theatre.query.all()
        with open(file=attachment, mode='w') as file:
            csv_obj = csv.writer(file, delimiter=',')
            csv_obj.writerow(['Theatre id', 'Theatre Name', 'Theatre Location', 'Number of Shows Currently Running'])
            for theatre in theatres:
                csv_obj.writerow([ theatre.id, theatre.name, theatre.place, len(theatre.shows)])

    send_email(to_address=email, subject=subject, message=message, attachment=attachment)
    
    return attachment


@celery.task(name="exportShow")
@cache.memoize(timeout=15)
def exShow(show_id):
    
    email = "ticketshow@admin.com"

    show = Show.query.get(show_id)
    

    with open('./templates/show_details.html') as file:
        template = Template(file.read())
        message = template.render(show=show)

    send_email(to_address=email, subject=f"Show Details - { show.name }", message=message)


    return 'Show Details Sent',200


@celery.task(name="dailyReminder")
def daily_mail():
    users = User.query.all()
    active = True
    for user in users:
        if user.last_logged.day - datetime.now().day > 0:
            active = False
        else:
            print(user.last_logged.day, datetime.now().day, user.last_logged.day - datetime.now().day)
            if user.role == 'user':
                bookings = Booking.query.filter_by(user_id=user.id).all()
                print([booking.show.show_date for booking in bookings])
                daily_bookings = []
                for booking in bookings: 
                    if booking.show.show_date == str(date.today()):
                        daily_bookings.append(booking)
                with open(r"templates/daily_reminder.html") as file:
                    template = Template(file.read())
                    message = template.render(bookings=daily_bookings, active=active)
                send_email(to_address=user.email, subject="Daily reminder",
                        message=message)

    return 'Daily Reminder Sent'


@celery.task(name = "monthlyReport")
def monthly_mail():
    users = User.query.all()
    for user in users:
        if user.role == 'user':
            
            monthly_bookings = []
            genres = {}
            
            bookings = Booking.query.filter_by(user_id=user.id).all()
            for booking in bookings:
                print(booking)
                if(datetime.strptime(booking.show.show_date, "%Y-%m-%d").month == datetime.now().month):
                    tags = booking.show.tags.split(',')
                    for tag in tags:
                        tag = tag.strip()
                        if tag in genres.keys():
                            genres[tag] +=1
                        else:
                            genres[tag] = 1
                    monthly_bookings.append(booking)
                    print(genres)
            
            
            with open(r"./templates/monthly_report.html") as file:
                template = Template(file.read())
                message = template.render(monthly_bookings=monthly_bookings, genres=genres)
            
            pdf_file = f"./reports/{user.name}.pdf"
            html = HTML(string=message)
            html.write_pdf(pdf_file)


            send_email(to_address=user.email, subject="Monthly Report", attachment=pdf_file,
                    message=message)

    return "Monthly Report Sent"


