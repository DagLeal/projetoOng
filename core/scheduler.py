from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import gerar_relatorio_mensal

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(gerar_relatorio_mensal, 'cron', day=1, hour=0, minute=0)  # todo dia 1 às 00:00
    scheduler.start()