import pymongo
from pymongo import MongoClient
import random
import time
import matplotlib.pyplot as plt


def create_user(db, username, password, balance):
    post = {
        'username': username,
        'password': password,
        'balance': balance,
        'trades': [balance],
    }

    db.insert_one(post)

def reset_user(db, username, balance):
    db.update_one({"username": username}, {"$set": {"balance": balance, "trades": [balance]}})

def generate_random_password(length = 16):
    random.seed(time.time())
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%&1234568901234567890.-_'

    return ''.join([random.choice(chars) for i in range(length)])

def plot_user_history(db: pymongo.collection.Collection, username):
    user = db.find_one({'username': username})
    plt.plot(user['trades'])

    # for i in range(1, len(user['trades'])):
    #     # Determine the color of the line
    #     if user['trades'][i] > prev_balance:
    #         color = 'green'
    #     elif user['trades'][i] < prev_balance:
    #         color = 'red'
        
    #     # Plot the point and connect it to the previous point with the appropriate color
    #     plt.plot([i-1, i], [prev_balance, user['trades'][i]], color=color)
        
    #     # Update the previous balance
    #     prev_balance = user['trades'][i]

    plt.show()

def main():

    cluster = MongoClient('<server-link>')
    db = cluster['options']['people']

    users = [
    ]
    balance = 1000.0

    create_users = False
    reset_users = False
    plot_users = True

    if create_users:
        for u in users:
            p_word = generate_random_password()
            create_user(
                db,
                username = u,
                password = p_word,
                balance = balance
            )
            user_json = '{"username": "' + u + '", "password": "' + p_word + '"}'
            print(f'Created user {user_json} with balance ${balance:.2f}')

    if reset_users:
        for u in users:
            print(u)
            reset_user(db, u, balance)

    if plot_users:
        for user in users:
            print(f"{user}: {db.find_one({'username': user})['balance']}")
            plot_user_history(db, user)

if __name__ == '__main__':
    main()















