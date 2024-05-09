import json
import pymysql
import os

# データベース接続情報
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

def lambda_handler(event, context):
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, user_name, title, description, tag1, tag2, tag3, completed FROM todos"
            cursor.execute(sql)
            result = cursor.fetchall()
        
        todos = []
        for row in result:
            todo = {
                'id': row[0],
                'user_name': row[1],
                'title': row[2],
                'description': row[3],
                'tag1': row[4],
                'tag2': row[5],
                'tag3': row[6],
                'completed': row[7]
            }
            todos.append(todo)
        
        return {
            'statusCode': 200,
            'body': json.dumps(todos, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    finally:
        connection.close()
