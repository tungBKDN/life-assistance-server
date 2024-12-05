from flask import Blueprint, request, jsonify
from models import db
from models.schedule import Schedule
from models.period import Period
from datetime import datetime


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


@period_bp.route('/periods', methods=['POST'])
def create_period():
	try:
		data = request.get_json()
		with db.session.begin():
			# Create a new period
			start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
			end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
			# Check for invalid date range
			if end_date and end_date < start_date:
				raise ValueError('End date cannot be before start date.')
			period = Period(drug_name=data['drug_name'], start_date=start_date, end_date=end_date)
			db.session.add(period)
			db.session.flush()  # Ensure period.id is available

			schedules = data['schedules']
			for schedule in schedules:
				# Create a new schedule
				time = datetime.strptime(schedule['time'], '%H:%M').time()
				s = Schedule(period_id=period.id, message=schedule['message'], time=time)
				db.session.add(s)

		return jsonify({'message': 'Period created successfully.'}), 201
	except ValueError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 400
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonify({'error': str(e)}), 500