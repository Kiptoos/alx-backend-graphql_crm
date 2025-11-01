# crm/tasks.py
from celery import shared_task


@shared_task
def generatecrmreport():
    with open("/tmp/crmreportlog.txt", "a") as f:
        f.write("CRM report\n")
