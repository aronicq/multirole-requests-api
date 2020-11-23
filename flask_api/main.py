from flask import Flask, request, jsonify
import sqlalchemy
from db import db_session
from db import init_db
from models import Queries, Users, Roles

app = Flask(__name__)



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def check_rights(required_role, action):
    if required_role not in [i.name for i in db_session.query(Users).filter(Users.name == request.args.get('user')).first().role]:
        return {'result': False,
                'error': {'text': "You have to be " + required_role + " to " + action}}
    return {'result': True,
            'text': "OK"}


@app.route('/create')
def create():
    is_allowed = check_rights('User', "create Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    new_request = Queries(text=request.args.get('text'), state=1, author=request.args.get('user'))
    db_session.add(new_request)
    db_session.commit()

    res = db_session.query(Queries).get(new_request.id)
    return res.serialize


@app.route('/edit')
def edit():
    is_allowed = check_rights('User', "edit Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    query_to_edit = db_session.query(Queries).filter(Queries.id == request.args.get('id'), Queries.author == request.args.get('user')).first()

    if not query_to_edit:
        return jsonify({'text': "0 queries found. Check author and id"})

    query_to_edit.text = request.args.get('new_text')
    db_session.commit()

    res = db_session.query(Queries).get(query_to_edit.id)
    return res.serialize


@app.route('/send')
def send():
    is_allowed = check_rights('User', "send Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    query_to_update = db_session.query(Queries).filter(Queries.id == request.args.get('id'), Queries.author == request.args.get('user')).first()

    if not query_to_update:
        return jsonify({'text': "0 queries found. Check author and id"})

    if query_to_update.state == 1:
        query_to_update.state = 2
        db_session.commit()
    else:
        return "query is already sent to operator"
    return jsonify(query_to_update.serialize)


@app.route('/view')
def view():
    is_allowed = check_rights('User', "view your Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    requester_query = db_session.query(Queries).filter(Queries.author == request.args.get('user')).all()
    return jsonify([i.serialize for i in requester_query])


@app.route('/requested')
def list_req():
    is_allowed = check_rights('Operator', "view requested Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    result_list = db_session.query(Queries).filter(Queries.state == 2).order_by(sqlalchemy.desc(Queries.created)).all()
    return jsonify([i.serialize for i in result_list])


@app.route('/accept')
def accept():
    is_allowed = check_rights('Operator', "accept Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    query_to_accept = db_session.query(Queries).get(request.args.get('id'))

    if not query_to_accept:
        return jsonify({'text': "0 queries found. Check id"})

    if query_to_accept.state == 2:
        query_to_accept.state = 3
        db_session.commit()
    else:
        return jsonify({'text': "query is already processed"})

    return query_to_accept.serialize


@app.route('/decline')
def decline():
    is_allowed = check_rights('Operator', "decline Queries")
    if not is_allowed['result']:
        return is_allowed['error']

    query_to_decline = db_session.query(Queries).get(request.args.get('id'))

    if not query_to_decline:
        return jsonify({'text': "0 queries found. Check id"})

    if query_to_decline.state == 2:
        query_to_decline.state = 4
        db_session.commit()
    else:
        return jsonify({'text': "query is already processed"})

    return query_to_decline.serialize


@app.route('/list_users')
def list_users():
    is_allowed = check_rights('Admin', "view Users")
    if not is_allowed['result']:
        return is_allowed['error']

    all_users = db_session.query(Users).all()

    roles = [[i.name for i in db_session.query(Users).filter(Users.id == j.id).first().role] for j in all_users]
    users = [i.serialize for i in all_users]

    for i in range(len(users)):
        users[i]['role'] = roles[i]

    return jsonify(users)


@app.route('/define_rights')
def define_rights():
    is_allowed = check_rights('Admin', "define Roles")
    if not is_allowed['result']:
        return is_allowed['error']

    user_to_define_rights = db_session.query(Users).get(request.args.get('id'))

    if 'Operator' not in [i.name for i in user_to_define_rights.role]:
        operator_role = db_session.query(Roles).filter(Roles.name == "Operator").first()
        user_to_define_rights.role.append(operator_role)
        db_session.commit()
    else:
        return "User is already processed"
    return user_to_define_rights.serialize


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', debug=True)