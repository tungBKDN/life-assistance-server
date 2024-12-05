from models import db
from enum import Enum


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    class DayOfWeek(Enum):
        MO = 1
        TU = 2
        WE = 3
        TH = 4
        FR = 5
        SA = 6
        SU = 7
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)

    drug_name = db.Column(db.String(255), nullable=True)
    remind_time = db.Column(db.Time, nullable=False)
    message = db.Column(db.String(255), nullable=False)
    # Null means it will repeat forever
    end_date = db.Column(db.Date, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'day_of_week': self.day_of_week.name,
            'remind_time': self.remind_time.strftime('%H:%M:%S'),
            'drug_name': self.drug_name.strip(),
            'message': self.message,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None
        }
