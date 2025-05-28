
backend avec 'fastapi-users[beanie]'

model :
  user_admin :
    - id : UUID
    - email : str
    - hashed_password : str
    - username : str

routes :

- /auth
  - /register :
    - POST: Register a new user
  - /login :
    - POST: Login a user
  - /logout :
    - POST: Logout a user
  - /profile :
    - GET: Get the current user's profile
    - PUT: Update the current user's profile
  - /change-password :
    - POST: Change the current user's password
