import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from controllers.periodAPI import period_bp
from flask_cors import CORS

# Detect if running in serverless/read-only environment (like Vercel)
# and use /tmp for instance path (the only writable directory)
instance_path = None
try:
    # Try to write to current directory to detect read-only filesystem
    test_file = os.path.join(os.getcwd(), '.write_test')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
except (OSError, IOError):
    # Read-only filesystem detected, use /tmp
    instance_path = '/tmp'

app = Flask(__name__, instance_path=instance_path)
database_url = os.getenv('DATABASE_URL')

if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:////tmp/schedules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(period_bp, url_prefix='/api')

@app.route('/health')
def health():
    """Health check endpoint for monitoring and deployment verification."""
    return {'status': 'healthy', 'database': app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}, 200

if __name__ == '__main__':
    app.run(debug=True)