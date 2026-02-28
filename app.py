import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from controllers.periodAPI import period_bp
from flask_cors import CORS

# On Vercel/serverless, use /tmp as instance path (only writable directory)
# Detect Vercel or Lambda environment
is_serverless = os.getenv('VERCEL') or os.getenv('AWS_LAMBDA_FUNCTION_NAME')
instance_path = '/tmp' if is_serverless else None

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