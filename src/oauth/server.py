from flask import Flask, request, redirect, session, make_response, jsonify, render_template
import os
import json
from auth import hash_password, verify_password

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session handling

# Mock constants for client ID and secret. 
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:5000/callback"

AUTH_CODES = {}  # Temporary storage for auth codes. Use a proper database in a real-world scenario.
TOKENS = {}      # Temporary storage for access tokens.

@app.route("/")
def index():
    """
    Endpoint where the client sends the user to request their authorization.
    After authorization, user is redirected back to the client with an auth code.
    """
    response = {
        "status": "OK"
    }
    return make_response(jsonify(response), 200)

@app.route("/auth", methods=["GET", "POST"])
def auth():
    """
    Endpoint where the client sends the user to request their authorization.
    After authorization, user is redirected back to the client with an auth code.
    """
    # TODO:
    # 1. Extract 'client_id', 'redirect_uri', 'state', etc. from the request.
    # 2. Validate 'client_id' and 'redirect_uri' against registered client details.
    # 3. Display an authorization page to the user to grant permission.
    # 4. If user grants permission, generate an authorization code.
    # 5. Save the authorization code and associated data.
    # 6. Redirect the user back to 'redirect_uri' with the 'code' and 'state'.
    if request.method == "GET":
    
        params = request.args.to_dict()

        if params.get("response_type") != "code":
            return make_response(jsonify({"error": "invalid_request"}), 400)

        if params.get("client_id") != CLIENT_ID:
            return make_response(jsonify({"error": "unauthorized_client"}), 400)

        if params.get("redirect_uri") != REDIRECT_URI:
            return make_response(jsonify({"error": "invalid_request"}), 400)
        
        return render_template("authorize.html", params=params)

    params = request.args.get("get_request_params")
    params = json.loads(params.replace("'", "\""))
    print(params)
    user_consent = request.form.get("consent") == "on"

    if user_consent:
        code = generate_auth_code()
        AUTH_CODES[params.get("client_id")] = code
        return redirect(f"{params.get('redirect_uri')}?code={code}&state={params.get('state')}")
    return make_response(jsonify({"error": "Internal server error"}), 500)

@app.route("/token", methods=["POST"])
def token():
    """
    Endpoint where the client exchanges the authorization code for an access token.
    """
    # TODO:
    # 1. Extract 'code', 'redirect_uri', 'client_id', 'client_secret' from the request.
    # 2. Verify that the 'code' is valid and has not expired.
    # 3. Validate 'client_id' and 'client_secret'.
    # 4. Generate an access token (and optionally, a refresh token).
    # 5. Save the access token for later validation.
    # 6. Return the access token (and optionally, a refresh token) in a JSON response.
    params = request.args.to_dict()
    if params.get("client_id") != CLIENT_ID:
        return make_response(jsonify({"error": "unauthorized_client"}), 400)
    if params.get("client_secret") != CLIENT_SECRET:
        return make_response(jsonify({"error": "unauthorized_client"}), 400)
    if params.get("code") != AUTH_CODES.get(params.get("client_id")):
        return make_response(jsonify({"error": "invalid_grant"}), 400)
    
    access_token = generate_access_token()
    return make_response(jsonify({"access_token": access_token}), 200)

def generate_auth_code():
    """
    Generate a dummy authorization code.
    """
    return str(hash_password('notsecurecode123456'))

def generate_access_token():
    """
    Generate a dummy access token.
    """
    return str(hash_password('notsecuretoken123456'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)