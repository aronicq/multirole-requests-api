from flask import Flask, request, jsonify
import sqlalchemy
from db import db_session
from db import init_db
from models import Queries, Users

app = Flask(__name__)
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return "123"


@app.route('/create')
def create():
    new_request = Queries(text=request.args.get('text'), state=request.args.get('state'))
    db_session.add(new_request)
    db_session.commit()

    res = db_session.query(Queries).get(new_request.id)
    return res.serialize


@app.route('/send')
def send():
    query_to_update = db_session.query(Queries).get(request.args.get('id'))
    if query_to_update.state == 1:
        query_to_update.state = 2
        db_session.commit()
    else:
        return "query is already sent to operator"
    return jsonify([i.serialize for i in query_to_update])


@app.route('/view')
def view():
    requester_query = db_session.query(Queries).get(request.args.get('id'))
    return requester_query.serialize


@app.route('/list_requests')
def list_req():
    result_list = db_session.query(Queries).filter(Queries.state == 2).order_by(sqlalchemy.desc(Queries.created)).all()
    return jsonify([i.serialize for i in result_list])


@app.route('/accept')
def accept():
    query_to_accept = db_session.query(Queries).get(request.args.get('id'))
    if query_to_accept.state == 2:
        query_to_accept.state = 3
        db_session.commit()
    else:
        return "query is already processed"
    return query_to_accept.serialize


@app.route('/decline')
def decline():
    query_to_decline = db_session.query(Queries).get(request.args.get('id'))
    if query_to_decline.state == 2:
        query_to_decline.state = 4
        db_session.commit()
    else:
        return "query is already processed"
    return query_to_decline.serialize


@app.route('/list_users')
def list_users():
    all_users = db_session.query(Users).all()
    return jsonify([i.serialize for i in all_users])


@app.route('/define_rights')
def define_rights():
    user_to_define_rights = db_session.query(Users).get(request.args.get('id'))
    if user_to_define_rights.state == 2:
        user_to_define_rights.state = 4
        db_session.commit()
    else:
        return "query is already processed"
    return user_to_define_rights.serialize


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', debug=True)