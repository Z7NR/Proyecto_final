from src.crud.usuarios_crud import user_crud


crud = user_crud()

uid = crud.create_user(
    "Test",            
    "User",             
    30,                 
    "000000000",       
    "test_integ@example.com",  
    "pass1234",        
    "Ciudad",           
    "Pais" 
)

print("USUARIO CREADO id:", uid)