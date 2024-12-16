from models import db
from datetime import datetime

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    pills = db.Column(db.Integer, nullable=True)
    time = db.Column(db.Time, nullable=False)

    period = db.relationship('Period', back_populates='schedules')

    def serialize(self):
        return {
            'id': self.id,
            'period_id': self.period_id,
            'pills': self.pills,
            'time': self.time.strftime('%H:%M')
        }

    @staticmethod
    def deserialize(data):
        time = datetime.strptime(data['time'], '%H:%M').time()
        return Schedule(
            period_id=data['period_id'],
            pills=data['pills'],
            time=time
        )

    def to_dict(self):
        return {
            'id': self.id,
            'period_id': self.period_id,
            'pills': self.pills,
            'time': self.time.strftime('%H:%M')
        }