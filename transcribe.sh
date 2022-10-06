echo "Transcribing '$1' with: "
echo '  "auto_highlights": true'
echo '  "iab_categories": true'
echo '  "sentiment_analysis": true'
echo '  "auto_chapters": true'
echo '  "entity_detection": true'
echo '  "speaker_labels": true'

curl --request POST \
  --url https://api.assemblyai.com/v2/transcript \
  --header 'authorization: $ASSEMBLY_KEY' \
  --header 'content-type: application/json' \
  --data '{"audio_url": "'$1'", "auto_highlights": true, "iab_categories": true, "sentiment_analysis": true, "auto_chapters": true, "entity_detection": true, "speaker_labels": true}'

