import json
import datetime
from django.test import TestCase
from ninja.testing import TestClient

from .models import SomeModel
from .api import some_model_router


class SomeModelAPITests(TestCase):
    """
    Test suite for the SomeModel API endpoints.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        This method is called once at the beginning of the test class run.
        """
        cls.initial_data = {
            "field_a": "initialA",
            "field_b": 100,
            "number_of_updates": 0
        }
        cls.model_instance = SomeModel.objects.create(**cls.initial_data)

        # Initialize TestClient directly with the router.
        # This is the recommended approach for unit testing routers in isolation.
        cls.client = TestClient(some_model_router)

    def test_update_some_model_success(self):
        """
        Test successful update of a SomeModel instance.
        Checks for correct field updates, incremented counter,
        and updated last_modified timestamp.
        """
        update_payload = {"field_a": "updatedA", "field_b": 200}
        
        # The URL is the path defined DIRECTLY on the `some_model_router`.
        # Prefixes like `/api/` or `/somemodel/` are not used here,
        # because TestClient(some_model_router) tests the router in isolation.
        url = f"/{self.model_instance.id}/update"

        timestamp_before_update = self.model_instance.last_modified

        response = self.client.put(
            url,
            json=update_payload # django-ninja's TestClient accepts JSON data directly
        )

        # Check status code and response content for better debugging in case of failure
        self.assertEqual(response.status_code, 200, f"Error: {response.content.decode()}")
        
        updated_data = response.json()
        self.model_instance.refresh_from_db() # Refresh the instance from the database

        # Check updated fields
        self.assertEqual(self.model_instance.field_a, update_payload["field_a"])
        self.assertEqual(updated_data["field_a"], update_payload["field_a"])

        self.assertEqual(self.model_instance.field_b, update_payload["field_b"])
        self.assertEqual(updated_data["field_b"], update_payload["field_b"])

        # Check if number_of_updates was incremented
        expected_updates = self.initial_data["number_of_updates"] + 1
        self.assertEqual(self.model_instance.number_of_updates, expected_updates)
        self.assertEqual(updated_data["number_of_updates"], expected_updates)

        # Check if last_modified timestamp was updated
        self.assertGreater(self.model_instance.last_modified, timestamp_before_update)
        
        # Check if the timestamp in response is close to the one in the database
        # (considering potential small time differences and timezones)
        response_timestamp = datetime.datetime.fromisoformat(updated_data["last_modified"])
        self.assertAlmostEqual(
            response_timestamp,
            self.model_instance.last_modified,
            delta=datetime.timedelta(seconds=2) # Allow a small delta
        )

    def test_update_some_model_not_found(self):
        """
        Test attempting to update a non-existent SomeModel instance,
        expecting a 404 error.
        """
        non_existent_id = self.model_instance.id + 999 # An ID that certainly doesn't exist
        update_payload = {"field_a": "test", "field_b": 1}
        url = f"/{non_existent_id}/update" # Path on the router

        response = self.client.put(url, json=update_payload)

        self.assertEqual(response.status_code, 404)
        # Ninja's default 404 response (via get_object_or_404) includes a "detail" key
        self.assertIn("detail", response.json())

    def test_update_some_model_invalid_payload_type(self):
        """
        Test attempting to update with an invalid payload (e.g., wrong data type),
        expecting a 422 Unprocessable Entity error.
        """
        invalid_payload = {"field_a": "validA", "field_b": "not_an_integer"} # field_b should be int
        url = f"/{self.model_instance.id}/update" # Path on the router

        response = self.client.put(url, json=invalid_payload)

        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        error_data = response.json()
        self.assertIn("detail", error_data) # Pydantic validation error response in Ninja
        # More specific assertions about the error message could be added, e.g.:
        # self.assertTrue(any("field_b" in e.get("loc", []) for e in error_data.get("detail", [])))

    def test_update_some_model_invalid_payload_max_length(self):
        """
        Test attempting to update with an invalid payload (e.g., field_a is too long),
        expecting a 422 Unprocessable Entity error.
        """
        invalid_payload = {"field_a": "thisIsStringIsWayTooLongForFieldA", "field_b": 123} # field_a has max_length=10
        url = f"/{self.model_instance.id}/update" # Path on the router

        response = self.client.put(url, json=invalid_payload)

        self.assertEqual(response.status_code, 422)
        error_data = response.json()
        self.assertIn("detail", error_data)
        # More specific assertions could be added, e.g., checking if the error pertains to 'field_a'
        # and if the message mentions maximum length.

    def test_multiple_updates_increment_robustness(self):
        """
        Test if multiple updates correctly increment the counter.
        While this is not a true concurrency test, it verifies the
        F-expression logic for sequential requests.
        """
        initial_updates_in_db = SomeModel.objects.get(id=self.model_instance.id).number_of_updates
        
        url = f"/{self.model_instance.id}/update" # Path on the router

        # First update
        payload1 = {"field_a": "update1", "field_b": 1}
        response1 = self.client.put(url, json=payload1)
        self.assertEqual(response1.status_code, 200)
        
        # Refresh the instance to get the current value from the database
        # or fetch the object again
        instance_after_update1 = SomeModel.objects.get(id=self.model_instance.id)
        self.assertEqual(instance_after_update1.number_of_updates, initial_updates_in_db + 1)
        self.assertEqual(instance_after_update1.field_a, "update1")

        # Second update
        payload2 = {"field_a": "update2", "field_b": 2}
        response2 = self.client.put(url, json=payload2)
        self.assertEqual(response2.status_code, 200)

        instance_after_update2 = SomeModel.objects.get(id=self.model_instance.id)
        self.assertEqual(instance_after_update2.number_of_updates, initial_updates_in_db + 2)
        self.assertEqual(instance_after_update2.field_a, "update2")
