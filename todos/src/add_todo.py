# src/commands/add_todo.py
import json
import pymysql
import os

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_name = body['user_name']
    title = body['title']
    description = body['description']
    tag1 = body['tag1']
    tag2 = body['tag2']
    tag3 = body['tag3']
    completed = body['completed']

    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO todos (user_name, title, description, tag1, tag2, tag3, completed) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_name, title, description, tag1, tag2, tag3, completed))
            connection.commit()
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Todo added successfully'}, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    finally:
        connection.close()
