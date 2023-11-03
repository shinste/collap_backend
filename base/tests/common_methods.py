def fail_check(root, error_message):
    response = root.client.post('/event/create/', data=root.eventInfo, format="json")
    root.assertEqual(response.status_code, 400)
    root.assertEqual(response.json(), error_message)