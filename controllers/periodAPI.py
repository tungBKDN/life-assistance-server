from flask import Blueprint, request, jsonify
from models import db
from models.schedule import Schedule
from models.period import Period

period_bp = Blueprint('period_bp', __name__)
schedule_bp = Blueprint('schedule_bp', __name__)

@period_bp.route('/periods', methods=['GET'])
def get_all_periods():
	try:
		periods = Period.query.all()
		result = []
		for period in periods:
			schedule_count = Schedule.query.filter_by(period_id=period.id).count()
			period_dict = period.serialize()
			period_dict['schedule_count'] = schedule_count
			result.append(period_dict)
		return jsonify(result)
	except Exception as e:
		print(e)
		return jsonify({'error': 'An error occurred while retrieving periods.'}), 500

@period_bp.route('/periods/<int:id>', methods=['GET'])
def get_period(id):
	try:
		# Get the period by id and it associated schedules
		period = Period.query.get(id)
		schedules = Schedule.query.filter_by(period_id=id).all()
		schedule_list = []
		for schedule in schedules:
			schedule_list.append(schedule.to_dict())
		period_dict = period.serialize()
		period_dict['schedules'] = schedule_list
		return jsonify(period_dict)
	except Exception as e:
		print(e)
		return jsonify({'error': 'An error occurred while retrieving period.'}), 500