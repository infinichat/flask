import mysql.connector

# Define your MySQL database connection settings
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'testdb',
}

# Function to delete all questions and answers except the first row
def delete_all_questions_and_answers_except_first():
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM qa WHERE id <> 1")  # This deletes all rows except the one with id = 1
            connection.commit()
            print("All questions and answers except the first one deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

# Usage example: Delete all questions and answers except the first one
delete_all_questions_and_answers_except_first()
