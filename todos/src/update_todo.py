import json
import pymysql
import os

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body)
    todo_id = body.pop('id', None)

    if not todo_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Todo IDが必要です'}, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    fields = []
    values = []

    for key, value in body.items():
        fields.append(f"{key}=%s")
        values.append(value)

    if not fields:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': '更新する項目が必要です'}, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    values.append(todo_id)
    set_clause = ", ".join(fields)

    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            sql = f"UPDATE todos SET {set_clause} WHERE id=%s"
            cursor.execute(sql, values)
            connection.commit()
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Todoが正常に更新されました'}, ensure_ascii=False),
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
