FROM python:3.10-slim
WORKDIR /ecommerce
COPY requirements.txt /ecommerce/
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py makemigrations
# Copy the entrypoint script and give it execution permissions
COPY setup.sh /ecommerce/setup.sh
RUN chmod +x /ecommerce/setup.sh

# Set the setup to the script
CMD ["/ecommerce/setup.sh"]

# Default command
# CMD ["python3", "manage.py", "runserver"]
