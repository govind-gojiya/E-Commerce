#!/bin/bash
set -e

# Run database migrations and seed the database
python3 manage.py migrate
python3 manage.py seed_db

