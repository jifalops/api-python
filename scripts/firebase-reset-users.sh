echo "Resetting local firebase auth emulator"
curl -X DELETE "http://localhost:9099/emulator/v1/projects/${FIREBASE_PROJECT_ID}/accounts"
echo