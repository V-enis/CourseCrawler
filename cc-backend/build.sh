# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --noinput

# Run migrations (This ensures Supabase is up to date on every deploy)
python manage.py migrate