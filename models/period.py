from models import db

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    drug_name = db.Column(db.String(255), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'drug_name': self.drug_name.strip()
        }