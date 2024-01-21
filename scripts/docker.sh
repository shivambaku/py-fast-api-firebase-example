mkdir dist
cp Dockerfile dist/
cp -R src/server dist/
cp Pipfile Pipfile.lock dist/
cp .env dist/
cp serviceAccountKey.json dist/

docker build -t testimage ./dist
docker run -p 8000:8000 testimage

rm -rf dist

