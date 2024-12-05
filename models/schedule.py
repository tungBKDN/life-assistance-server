from models import db
from datetime import datetime

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    time = db.Column(db.Time, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'period_id': self.period_id,
            'message': self.message,
            'time': self.time.strftime('%H:%M')
        }

    @staticmethod
    def deserialize(data):
        time = datetime.strptime(data['time'], '%H:%M').time()
        return Schedule(
            period_id=data['period_id'],
            message=data['message'],
            time=time
        )

    def to_dict(self):
        return {
            'id': self.id,
            'period_id': self.period_id,
            'message': self.message,
            'time': self.time.strftime('%H:%M')
        }