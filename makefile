run:
	@pipenv run uvicorn server.app:app --reload

emulator:
	@cd ./helpers/firebase_emulator/ && firebase emulators:start

test:
	@pipenv run pytest

docker:
	@sh ./scripts/docker.sh