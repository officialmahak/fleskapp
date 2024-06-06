from flask import Flask, request, jsonify
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import boto3

app = Flask(__name__)

def validate_aws_credentials(access_key, secret_key):
    try:
        client = boto3.client(
            'sts',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        response = client.get_caller_identity()
        account_id = response['Account']
        user_arn = response['Arn']
        return True, account_id, user_arn
    except NoCredentialsError:
        return False, None, None
    except PartialCredentialsError:
        return False, None, None
    except Exception as e:
        return False, None, None

@app.route('/validate-aws-credentials', methods=['POST'])
def validate_aws_credentials_api():
    access_key = request.json.get('access_key')
    secret_key = request.json.get('secret_key')
    if not access_key or not secret_key:
        return jsonify({'error': 'Access key or secret key missing.'}), 400

    is_valid, account_id, user_arn = validate_aws_credentials(access_key, secret_key)
    if is_valid:
        return jsonify({
            'success': True,
            'account_id': account_id,
            'user_arn': user_arn,
            'message': 'Credentials are valid.'
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials provided.'}), 401

if __name__ == '__main__':
    app.run(debug=True)
