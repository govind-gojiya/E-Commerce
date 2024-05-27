from random import randint
from locust import HttpUser, between, task

# Locus for permfomance testing purposes
# pip install locust
# To Run : locust -f locustfiles/browse_products.py
# We can give any name to folder and file 

class WebsiteUser(HttpUser):
    wait_time = between(1, 5) # For waiting time between tasks

    def on_start(self) -> None:
        """ on_start is called when a Locust start before any task is scheduled """
        response = self.client.post("/store/carts/")

        result = response.json()
        self.cart_id = result['id']

    # task decorator show that this is the task for perfomance testing
    # number inside the task decorater show that how likely it should be run
    # As number large is most likely to be visit
    @task(2)
    def view_products(self):
        collection_id = randint(2, 9)
        self.client.get(
            f"/store/products/?collection_id={collection_id}", # Url to check
            name="/store/products" # Name to visiable on monitoring
        )

    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(
            f"/store/products/{product_id}/",
            name="/store/products/:id"
        )

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            json={"product_id": product_id, "quantity": randint(1, 10)}, # Data to send
            name="/store/carts/:id/items" 
        )
