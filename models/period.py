from models import db
from models.schedule import Schedule

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drug_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    schedules = db.relationship('Schedule', back_populates='period', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'drug_name': self.drug_name,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'schedules': [schedule.serialize() for schedule in self.schedules]
        }