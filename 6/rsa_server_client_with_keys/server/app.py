from flask import Flask, request, render_template
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

app = Flask(__name__)

messages = {}
keys = {}
private_keys = {}  # Przechowuje klucze prywatne dla wszystkich użytkowników
deadbeef_key = None


def handle_encrypted_message(uid, message):
	"""Deszyfruje wiadomość dla danego użytkownika"""
	resp = {}
	try:
		if uid not in private_keys:
			resp['errors'] = f'Nie ma klucza prywatnego dla: {uid}'
			return resp, 400
		
		encoded_message = base64.decodebytes(message.encode('utf-8'))
		decipher = PKCS1_OAEP.new(private_keys[uid])
		decrypted = decipher.decrypt(encoded_message)
		resp['decrypted'] = decrypted.decode('utf-8')
		return resp, 200
	except Exception as e:
		resp['errors'] = str(e)
		return resp, 400

@app.route('/')
def index():
	return render_template('index.html', messages=messages)


@app.route('/message/<uid>', methods = ['GET','POST'])
def message(uid):

	if request.method == 'GET':

		if uid in messages:
			message, ip = messages[uid]
			return message
		else:
			return f'Nie ma wiadomości do: {uid}', 404

	elif request.method == 'POST':

		json = request.get_json()

		if json and 'message' in json:
			# Zawsze przechowuj wiadomość (niezależnie od tego czy użytkownik ma klucz prywatny)
			messages[uid] = json['message'], request.remote_addr
			return f'Dodano wiadomość dla: {uid}', 200
		else:
			return 'Niepoprawne zapytanie', 400


@app.route('/key/<uid>', methods = ['GET','POST'])
def key(uid):

	if request.method == 'GET':

		if uid in keys:
			return keys[uid]
		else:
			return f'Nie ma klucza dla: {uid}', 404

	elif request.method == 'POST':

		if uid == 'deadbeef':
			return f'Nie można zmienić klucza', 403
		
		json = request.get_json()

		if json and 'key' in json:
			keys[uid] = json['key']
			return f'Dodano klucz dla: {uid}', 200
		else:
			return 'Niepoprawne zapytanie', 400

if __name__ == "__main__":
	print("[*] Load deadbeef keys...")
	pubkey_filename = os.getenv("DEADBEEF_KEY_1")
	privkey_filename = os.getenv("DEADBEEF_KEY_2")

	with open(pubkey_filename, 'r') as key_file:
		keys['deadbeef'] = RSA.importKey(key_file.read()).exportKey()
	with open(privkey_filename, 'r') as key_file:
		private_keys['deadbeef'] = RSA.importKey(key_file.read())

	# Załaduj klucze dla john_snow
	print("[*] Load john_snow keys...")
	john_snow_pub_path = os.path.join(os.path.dirname(__file__), "john_snow_pub.key")
	john_snow_priv_path = os.path.join(os.path.dirname(__file__), "john_snow_priv.key")
	
	with open(john_snow_pub_path, 'r') as key_file:
		keys['john_snow'] = RSA.importKey(key_file.read()).exportKey()
	with open(john_snow_priv_path, 'r') as key_file:
		private_keys['john_snow'] = RSA.importKey(key_file.read())

	# Załaduj klucze dla bob_bob
	print("[*] Load bob_bob keys...")
	bob_bob_pub_path = os.path.join(os.path.dirname(__file__), "bob_bob_pub.key")
	bob_bob_priv_path = os.path.join(os.path.dirname(__file__), "bob_bob_priv.key")
	
	with open(bob_bob_pub_path, 'r') as key_file:
		keys['bob_bob'] = RSA.importKey(key_file.read()).exportKey()
	with open(bob_bob_priv_path, 'r') as key_file:
		private_keys['bob_bob'] = RSA.importKey(key_file.read())

	app.run(host="0.0.0.0", port=5555)
