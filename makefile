run:
	@pipenv run uvicorn server.app:app --reload

emulator:
	@cd ./helpers/firebase_emulator/ && firebase emulators:start

test:
	@pipenv run pytest

docker:
	@pipenv requirements > requirements.txt && docker compose up --build
