from flask import Blueprint, request, jsonify, make_response
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
		result = jsonify(result)
		result.headers['Content-Type'] = 'application/json; charset=utf-8'
		return result
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@period_bp.route('/periods/<int:id>', methods=['GET'])
def get_period(id):
	try:
		# Get the period by id and it associated schedules
		period = Period.query.get(id)
		if period is None:
			return jsonify({'error': 'Period not found.'}), 404
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
				s = Schedule(period_id=period.id, pills=schedule['pills'], time=time)
				db.session.add(s)

		return jsonify({'message': 'Period created successfully.'}), 201
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonify({'error': str(e)}), 400

@period_bp.route('/periods/<int:id>', methods=['PUT'])
def update_period(id):
	try:
		data = request.get_json()
		period = Period.query.get(id)
		if period is None:
			return jsonify({'error': 'Period not found.'}), 404

		# Delete all existing schedules for the period
		Schedule.query.filter_by(period_id=id).delete()

		# Update the period
		period.drug_name = data['drug_name']
		period.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
		period.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None

		# Check for invalid date range
		if period.end_date and period.end_date < period.start_date:
			raise ValueError('End date cannot be before start date.')

		db.session.add(period)

		# Add the new schedules
		schedules = data['schedules']
		for schedule in schedules:
			time = datetime.strptime(schedule['time'], '%H:%M').time()
			s = Schedule(period_id=id, pills=schedule['pills'], time=time)
			db.session.add(s)

		# Commit the transaction
		db.session.commit()

		return jsonify({'message': 'Period updated successfully.'}), 200
	except ValueError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 400
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonify({'error': str(e)}), 500


@period_bp.route('/periods/<int:id>', methods=['DELETE'])
def delete_period(id):
	try:
		period = Period.query.get(id)
		if period is None:
			response = make_response(jsonify({'error': 'Period not found.'}), 404)
			response.headers.add("Access-Control-Allow-Origin", "*")
			return response

		with db.session.begin():
			# Delete all schedules for the period
			Schedule.query.filter_by(period_id=id).delete()
			# Delete the period
			db.session.delete(period)
		response = make_response(jsonify({'message': 'Period deleted successfully.'}), 200)
		response.headers.add("Access-Control-Allow-Origin", "*")

		return jsonify({'message': 'Period deleted successfully.'}), 200
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonify({'error': str(e)}), 500

@period_bp.route('/periods/agenda', methods=['GET'])
def get_agenda():
	try:
		current_local_time = datetime.now()
		res = {}
		# Get the schedules joined with the periods has queried above
		schedules = Schedule.query.join(Period, Schedule.period_id == Period.id).filter(
			Period.start_date <= current_local_time.date(),
			(Period.end_date >= current_local_time.date()) | (Period.end_date == None)
		).order_by(Schedule.time.asc()).all()
		result = []
		for schedule in schedules:
			sch = schedule.serialize()
			sch["drug_name"] = schedule.period.drug_name
			time = schedule.time.strftime('%H:%M')
			hours, minutes = map(int, time.split(':'))
			total_minutes = hours * 60 + minutes
			sch["time"] = total_minutes
			result.append(sch)
		res["schedules"] = result
		hours, minutes = map(int, current_local_time.strftime('%H:%M').split(':'))
		total_minutes = hours * 60 + minutes
		res["current_local_time"] = total_minutes
		res = jsonify(res)
		res.headers['Content-Type'] = 'application/json; charset=utf-8'
		return res, 200
	except Exception as e:
		print(e)
		return jsonify({'error': 'An error occurred while retrieving agenda.'}), 500

@period_bp.route('/periods/', methods=['DELETE'])
def delete_all():
	try:
		with db.session.begin():
			# Delete all schedules
			Schedule.query.delete()
			# Delete all periods
			Period.query.delete()
		return jsonify({'message': 'All periods deleted successfully.'}), 200
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonify({'error': str(e)}), 500

@period_bp.route('/periods/unactive', methods=['DELETE'])
def delete_unactive():
	# Delete schedules and periods that have ended
	try:
		current_local_time = datetime.now()
		periods = Period.query.filter(Period.end_date < current_local_time.date()).all()

		for period in periods:
			# Delete all schedules for the period
			Schedule.query.filter_by(period_id=period.id).delete()
			# Delete the period
			db.session.delete(period)

		# Commit the transaction
		db.session.commit()

		return jsonify({'message': f'Unactive periods deleted successfully for {current_local_time.date()}.'}), 200
	except Exception as e:
		db.session.rollback()
		print(e)
		return jsonify({'error': 'An error occurred while deleting unactive periods.'}), 500
