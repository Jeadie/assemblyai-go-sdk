

curl --request GET \
  --url "https://api.assemblyai.com/v2/transcript/$1/paragraphs" \
  --header "authorization: $ASSEMBLY_KEY" \
  --header 'content-type: application/json'