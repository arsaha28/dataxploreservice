# projectai

# Enable vertex ai API ,create a service account and download the credential,run below command in terminal
export GOOGLE_APPLICATION_CREDENTIALS="/Users/<<user>>/Downloads/<<file.json>>"

# Run postgraphile
npx postgraphile -c postgres://localhost/<<user>> --schema <<schema>> --enhance-graphiql

#start
streamlit run home.py
