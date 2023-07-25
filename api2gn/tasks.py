from celery.schedules import crontab

from geonature.utils.celery import celery_app

from api2gn.models import ParserModel
from api2gn.utils import get_parser


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="0", hour="21"),
        run_parsers.s(),
        name="Run scheduled parser",
    )


@celery_app.task(bind=True)
def run_parsers(self):
    for parser_db in ParserModel.query.filter(
        ParserModel.schedule_frequency.isnot(None)
    ).all():
        Parser = get_parser(parser_db.name)
        Parser().run.delay()
