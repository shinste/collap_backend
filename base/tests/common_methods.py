def checker(root, response, message, status):
    root.assertEqual(response.status_code, status)
    root.assertEqual(response.json(), message)