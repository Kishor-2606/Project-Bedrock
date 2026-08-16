import pytest

valid_expense = {
    "title": "Coffee",
    "amount": 150.0,
    "category": "Food",
    "expense_date": "2026-08-10",
}

second_expense = {
    "title": "Bus Pass",
    "amount": 400.0,
    "category": "Transport",
    "expense_date": "2026-08-11",
}


class TestCreateExpense:

    def test_create_expense_success(self, client):
        response = client.post("/expenses", json=valid_expense)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Coffee"
        assert data["amount"] == 150.0
        assert data["category"] == "Food"
        assert "id" in data
        assert data["id"] > 0

    def test_create_expense_returns_all_fields(self, client):
        response = client.post("/expenses", json=valid_expense)
        data = response.json()

        assert "id" in data
        assert "title" in data
        assert "amount" in data
        assert "category" in data
        assert "expense_date" in data
        assert "created_at" in data
        assert "is_recurring" in data
        assert "user_id" in data

    def test_create_expense_with_description(self, client):
        payload = {**valid_expense, "description": "Morning coffee at the canteen"}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 201
        assert response.json()["description"] == "Morning coffee at the canteen"

    def test_create_expense_defaults_date_to_today(self, client):
        payload = {k: v for k, v in valid_expense.items() if k != "expense_date"}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 201
        assert response.json()["expense_date"] is not None

    def test_create_expense_auto_creates_new_category(self, client):
        payload = {**valid_expense, "category": "Gaming"}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 201
        assert response.json()["category"] == "Gaming"

    def test_create_expense_title_too_short(self, client):
        payload = {**valid_expense, "title": "A"}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 422

    def test_create_expense_title_blank(self, client):
        payload = {**valid_expense, "title": "   "}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 422

    def test_create_expense_negative_amount(self, client):
        payload = {**valid_expense, "amount": -100.0}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 422

    def test_create_expense_zero_amount(self, client):
        payload = {**valid_expense, "amount": 0}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 422

    def test_create_expense_missing_required_field(self, client):
        payload = {"title": "Coffee", "category": "Food"}
        response = client.post("/expenses", json=payload)

        assert response.status_code == 422


class TestGetAllExpenses:

    def test_get_expenses_empty_database(self, client):
        response = client.get("/expenses")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_expenses_after_creating_one(self, client):
        client.post("/expenses", json=valid_expense)
        response = client.get("/expenses")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_expenses_returns_multiple(self, client):
        client.post("/expenses", json=valid_expense)
        client.post("/expenses", json=second_expense)
        response = client.get("/expenses")

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetExpenseById:

    def test_get_expense_by_id_success(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        response = client.get(f"/expenses/{expense_id}")

        assert response.status_code == 200
        assert response.json()["id"] == expense_id
        assert response.json()["title"] == "Coffee"

    def test_get_expense_not_found(self, client):
        response = client.get("/expenses/9999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_expense_invalid_id_type(self, client):
        response = client.get("/expenses/abc")

        assert response.status_code == 422


class TestUpdateExpense:

    def test_update_title(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        response = client.patch(f"/expenses/{expense_id}", json={"title": "Espresso"})

        assert response.status_code == 200
        assert response.json()["title"] == "Espresso"
        assert response.json()["amount"] == 150.0

    def test_update_amount(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        response = client.patch(f"/expenses/{expense_id}", json={"amount": 200.0})

        assert response.status_code == 200
        assert response.json()["amount"] == 200.0
        assert response.json()["title"] == "Coffee"

    def test_update_category(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        response = client.patch(f"/expenses/{expense_id}", json={"category": "Subscriptions"})

        assert response.status_code == 200
        assert response.json()["category"] == "Subscriptions"

    def test_update_not_found(self, client):
        response = client.patch("/expenses/9999", json={"title": "Ghost Expense"})

        assert response.status_code == 404

    def test_update_invalid_amount(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        response = client.patch(f"/expenses/{expense_id}", json={"amount": -50.0})

        assert response.status_code == 422


class TestDeleteExpense:

    def test_delete_expense_success(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/expenses/{expense_id}")
        assert delete_resp.status_code == 204

    def test_deleted_expense_no_longer_retrievable(self, client):
        create_resp = client.post("/expenses", json=valid_expense)
        expense_id = create_resp.json()["id"]

        client.delete(f"/expenses/{expense_id}")

        get_resp = client.get(f"/expenses/{expense_id}")
        assert get_resp.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete("/expenses/9999")

        assert response.status_code == 404


class TestAnalytics:

    def test_get_total_empty_database(self, client):
        response = client.get("/expenses/total")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0.0
        assert data["count"] == 0

    def test_get_total_with_expenses(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 100.0})
        client.post("/expenses", json={**valid_expense, "amount": 200.0, "title": "Lunch"})

        response = client.get("/expenses/total")

        assert response.status_code == 200
        assert response.json()["total"] == pytest.approx(300.0)
        assert response.json()["count"] == 2

    def test_get_highest_empty_database(self, client):
        response = client.get("/expenses/highest")

        assert response.status_code == 404

    def test_get_highest_returns_max_amount(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 150.0})
        client.post("/expenses", json={**valid_expense, "amount": 1650.0, "title": "Laptop"})
        client.post("/expenses", json={**valid_expense, "amount": 400.0, "title": "Bus Pass"})

        response = client.get("/expenses/highest")

        assert response.status_code == 200
        assert response.json()["amount"] == pytest.approx(1650.0)
        assert response.json()["title"] == "Laptop"


class TestFiltering:

    def test_filter_by_category(self, client):
        client.post("/expenses", json={**valid_expense, "category": "Food"})
        client.post("/expenses", json={**second_expense, "category": "Transport"})

        response = client.get("/expenses?category=Food")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Food"

    def test_filter_by_category_case_insensitive(self, client):
        client.post("/expenses", json={**valid_expense, "category": "Food"})

        response = client.get("/expenses?category=food")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_filter_by_min_amount(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 100.0})
        client.post("/expenses", json={**valid_expense, "amount": 500.0, "title": "Headphones"})

        response = client.get("/expenses?min_amount=300")

        data = response.json()
        assert all(e["amount"] >= 300 for e in data)
        assert len(data) == 1

    def test_filter_by_max_amount(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 100.0})
        client.post("/expenses", json={**valid_expense, "amount": 500.0, "title": "Headphones"})

        response = client.get("/expenses?max_amount=200")

        data = response.json()
        assert all(e["amount"] <= 200 for e in data)
        assert len(data) == 1

    def test_filter_combined(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 100.0, "category": "Food"})
        client.post("/expenses", json={**valid_expense, "amount": 800.0, "title": "Dinner", "category": "Food"})
        client.post("/expenses", json={**second_expense, "amount": 400.0})

        response = client.get("/expenses?category=Food&max_amount=500")

        data = response.json()
        assert all(e["category"] == "Food" for e in data)
        assert all(e["amount"] <= 500 for e in data)


class TestSorting:

    def test_sort_by_amount_ascending(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 500.0, "title": "Expensive"})
        client.post("/expenses", json={**valid_expense, "amount": 100.0, "title": "Cheap"})

        response = client.get("/expenses?sort=amount")

        amounts = [e["amount"] for e in response.json()]
        assert amounts == sorted(amounts)

    def test_sort_by_amount_descending(self, client):
        client.post("/expenses", json={**valid_expense, "amount": 100.0, "title": "Cheap"})
        client.post("/expenses", json={**valid_expense, "amount": 500.0, "title": "Expensive"})

        response = client.get("/expenses?sort=-amount")

        amounts = [e["amount"] for e in response.json()]
        assert amounts == sorted(amounts, reverse=True)


class TestPagination:

    def _create_expenses(self, client, n):
        for i in range(n):
            client.post("/expenses", json={
                **valid_expense,
                "title": f"Expense {i + 1}",
                "amount": float((i + 1) * 100),
            })

    def test_limit_restricts_results(self, client):
        self._create_expenses(client, 5)

        response = client.get("/expenses?limit=3")

        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_skip_offsets_results(self, client):
        self._create_expenses(client, 5)

        response = client.get("/expenses?skip=3&limit=10")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_skip_beyond_total_returns_empty(self, client):
        self._create_expenses(client, 3)

        response = client.get("/expenses?skip=100&limit=10")

        assert response.status_code == 200
        assert response.json() == []

    def test_default_limit_is_10(self, client):
        self._create_expenses(client, 15)

        response = client.get("/expenses")

        assert response.status_code == 200
        assert len(response.json()) == 10
