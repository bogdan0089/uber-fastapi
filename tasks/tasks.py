from core.celery_app import celery_app

@celery_app.task
def send_registration_email(email: str):
    print(f"Sending registration email to {email}")



    