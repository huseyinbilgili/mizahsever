from mizahsever.celery import app


@app.task
def upload_video(video_id):
    pass
