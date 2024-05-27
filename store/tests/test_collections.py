# For automated testing there is unittest and pytest 
# pytest have advantage in boilerplate code, more featues and simple
# pip install pytest pytest-django
# Remember : folder name should be 'tests' and file inside start with 'test_*.py' and also method name also start with 'test_'
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from model_bakery import baker
from store.models import Collection

# Run all tests : pytest
# Run specific file: pytest store/tests/test_collections.py
# Run specific class: pytest store/tests/test_collections.py::TestCreateCollection
# Run specific function: pytest store/tests/test_collections.py::TestCreateCollection::test_if_user_is_anonymous_returns_401
# Run specific word pattern: pytest -k anonymous

# pytest-watch for continuous testing while changing/developping code
# pip install pytest-watch
# To run : ptw 


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db # For compatible to add data to database
class TestCreateCollection:

    # For skip use below decorater
    # @pytest.mark.skip(reason="Not implemented yet")
    # def test_if_user_is_anonymous_returns_401(self):
    #     # Follow AAA rule
    #     # Arrange - Where we define objects want to retrive and create or likewise we want to use in

    #     # Act - Where we define code for making request and get response
    #     client = APIClient()
    #     response = client.post('/store/collections/', {'title': 'a'})

    #     # Assert - Check that the response meets the behavior or not
    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_if_user_is_not_admin_returns_403(self):
    #     client = APIClient()
    #     # For authenticate user without info use below method with empty dict of user
    #     client.force_authenticate(user={})
    #     response = client.post('/store/collections/', {'title': 'a'})
    
    #     assert response.status_code == status.HTTP_403_FORBIDDEN

    # def test_if_data_invalid_returns_400(self):
    #     client = APIClient()
    #     # For authenticate user as staff without info use below method 
    #     client.force_authenticate(user=User(is_staff=True))
    #     response = client.post('/store/collections/', {'title': ''})

    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data['title'] is not None

    # def test_if_data_valid_returns_201(self):
    #     client = APIClient()
    #     client.force_authenticate(user=User(is_staff=True))
    #     response = client.post('/store/collections/', {'title': 'a'})

    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.data['id'] > 0



    # Using Fixture
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'}) # Act

        assert response.status_code == status.HTTP_401_UNAUTHORIZED # Assert

    def test_if_user_is_not_admin_returns_403(self, autheticate, create_collection):
        autheticate(is_staff=False) # Arrange
        # Or - autheticate()

        response = create_collection({'title': 'a'}) # Act

        assert response.status_code == status.HTTP_403_FORBIDDEN # Assert

    def test_if_data_invalid_returns_400(self, autheticate, create_collection):
        autheticate(is_staff=True)

        response = create_collection({'title': ''}) 

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_valid_returns_201(self, autheticate, create_collection):
        autheticate(is_staff=True)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        # To make dummy collection use model_bakery module
        # we can give _quantity=10 for create more collection specify attributes explictly by giving value in args
        collection = baker.make(Collection) 

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    