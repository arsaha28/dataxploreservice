# projectai

# Enable vertex ai API ,create a service account and download the credential,run below command in terminal
export GOOGLE_APPLICATION_CREDENTIALS="/Users/replace with username/Downloads/secret file.json"

# Run postgraphile
npx postgraphile -c postgres://localhost/replace with username --schema replace with schemaname --enhance-graphiql

# Start the app
streamlit run home.py
