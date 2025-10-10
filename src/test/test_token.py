from src.utils.auth import auth_function

tok = auth_function().login("test_integ@example.com", "pass1234")
print("TOKEN =", tok)