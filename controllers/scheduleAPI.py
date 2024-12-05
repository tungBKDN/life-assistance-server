from flask import Blueprint, request, jsonify
from models import db
from models.schedule import Schedule
from models.period import Period

schedule_bp = Blueprint('schedule_bp', __name__)

@schedule_bp.route('/schedules', methods=['GET'])
def get_periods():
	schedules = Schedule.query.all()
	result = []
	for schedule in schedules:
		result.append(schedule.to_dict())
	return jsonify(result)