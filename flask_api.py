from __future__ import print_function
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

import sys
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('userId', required=True, type=int, help='userId must be an INT')
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 401
        else:
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'expenses': [[]]
            })
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int, help='userId must be an INT')
        parser.add_argument('expenses', required=True, type=int)

        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            data['expenses'] = data['expenses'].apply(
                lambda x: ast.literal_eval(x)
            )

            user_data = data[data['userId'] == args['userId']]
            user_data['expenses'] = user_data['expenses'].values[0].append(args['expenses'])
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int, help='locationId must be an INT')
        parser.add_argument('name', required=False)
        parser.add_argument('city', required=False)

        args = parser.parse_args()

        args = {dictK: dictV for dictK, dictV in args.items() if dictV is not None}

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            user_data = data[data['userId'] == args['userId']]

            if 'name' in args:
                user_data['name'] = args['name']

            if 'city' in args:
                user_data['city'] = args['city']

            # Update data frame to updated location data
            data[data['userId'] == args['userId']] = user_data
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int, help='userId must be an INT')
        parser.add_argument('expenses', required=False, type=int, help='expenses must be an INT')

        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        user_expenses = data[data['userId'] == args['userId']]

        if str(args['expenses']) in str(user_expenses['expenses']):
            data['expenses'] = data['expenses'].apply(
                lambda x: ast.literal_eval(x)
            )
            user_expenses_update = list(data.at[(int(args['userId']) - 1), 'expenses'])
            user_expenses_update.remove(args['expenses'])

            data.at[(int(args['userId']) - 1), 'expenses'] = user_expenses_update
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        elif args['expenses'] != None:
            return {'message': f"'{args['expenses']}' expense not found."}, 401

        if args['userId'] in list(data['userId']) and args['expenses'] == None:
            data = data[data['userId'] != args['userId']]
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 401


class Expenses(Resource):
    def get(self):
        data = pd.read_csv('expenses.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('expenseId', required=True, type=int, help='expenseId must be an INT')
        parser.add_argument('name', required=True)
        parser.add_argument('location', required=False)
        parser.add_argument('date', required=False)
        parser.add_argument('expense', required=False, type=float, help='expense must be a float')

        args = parser.parse_args()

        data = pd.read_csv('expenses.csv')

        if args['expenseId'] in list(data['expenseId']):
            return {
                       'message': f"'{args['expenseId']}' already exists."
                   }, 401
        else:
            new_data = pd.DataFrame({
                'expenseId': args['expenseId'],
                'name': args['name'],
                'location': args['location'],
                'date': args['date'],
                'expense': [args['expense']]
            })
            data = data.append(new_data, ignore_index=True)
            data.to_csv('expenses.csv', index=False)
            return {'data': data.to_dict()}, 200

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('expenseId', required=True, type=int, help='expenseId must be an INT')
        parser.add_argument('name', required=False)
        parser.add_argument('location', required=False)
        parser.add_argument('date', required=False)
        parser.add_argument('expense', required=False, type=float, help='expense must be a float')

        args = parser.parse_args()

        args = {dictK: dictV for dictK, dictV in args.items() if dictV is not None}

        data = pd.read_csv('expenses.csv')

        if args['expenseId'] in list(data['expenseId']):
            expense_data = data[data['expenseId'] == args['expenseId']]

            if 'name' in args:
                expense_data['name'] = args['name']

            if 'location' in args:
                expense_data['location'] = args['location']

            if 'date' in args:
                expense_data['date'] = args['date']

            if 'expense' in args:
                expense_data['expense'] = args['expense']

            # Update data frame to updated location data
            data[data['expenseId'] == args['expenseId']] = expense_data
            data.to_csv('expenses.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['expenseId']}' expense not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('expenseId', required=True, type=int, help='expenseId must be an INT')

        args = parser.parse_args()

        data = pd.read_csv('expenses.csv')

        if args['expenseId'] in list(data['expenseId']):
            data = data[data['expenseId'] != args['expenseId']]
            data.to_csv('expenses.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['expenseId']}' expense not found."
                   }, 401

    pass


api.add_resource(Users, '/users')
api.add_resource(Expenses, '/expenses')

if __name__ == '__main__':
    app.run()
