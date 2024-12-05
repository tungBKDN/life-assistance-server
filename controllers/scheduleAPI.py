from flask import Blueprint, request, jsonify
from models import db
from models.schedule import Schedule

schedule_bp = Blueprint('schedule_bp', __name__)

@schedule_bp.route('/schedules', methods=['GET'])
def get_schedules():
	try:
		schedules = Schedule.query.all()
		return jsonify([schedule.serialize() for schedule in schedules]), 200
	except Exception as e:
		print(e.with_traceback())
		return jsonify({'error': 'Internal Server Error'}), 500

@schedule_bp.route('/schedules', methods=['POST'])
def add_schedule():
	try:
		data = request.get_json()
		schedule = Schedule(**data)
		db.session.add(schedule)
		db.session.commit()
		return jsonify(schedule.serialize())
	except Exception as e:
		print(e.with_traceback())
		return jsonify({'error': 'Invalid input'}), 400