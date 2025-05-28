#!/usr/bin/env python3
import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.db import User, db
from app.users import UserManager, get_user_db
from fastapi_users_db_beanie import BeanieUserDatabase

async def create_user():
    try:
        # Print environment variables for debugging
        print(f"MONGODB_URL: {os.getenv('MONGODB_URL', 'mongodb://mongodb:27017')}")
        print(f"MONGODB_DB: {os.getenv('MONGODB_DB', 'mev_form_db')}")
        print(f"ADMIN_EMAIL: {os.getenv('ADMIN_EMAIL', 'admin@example.com')}")
        
        # Connect to MongoDB
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
        db_name = os.getenv("MONGODB_DB", "mev_form_db")
        print(f"Connecting to MongoDB at {mongodb_url}, database {db_name}")
        
        client = AsyncIOMotorClient(mongodb_url)
        db_instance = client[db_name]
        
        # Initialize Beanie
        print("Initializing Beanie...")
        await init_beanie(database=db_instance, document_models=[User])
        
        # Check if any user exists
        print("Checking for existing users...")
        user_count = await User.count()
        print(f"Found {user_count} users")
        
        if user_count == 0:
            print("No users found. Creating initial admin user...")
            
            # Get default admin credentials from environment variables
            admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "adminpassword123")
            
            # Create user database
            user_db = BeanieUserDatabase(User)
            user_manager = UserManager(user_db)
            
            # Create user
            try:
                print(f"Creating user with email: {admin_email}")
                # Create UserCreate object properly
                from app.schemas import UserCreate
                # Examine what fields are available in UserCreate
                print(f"Creating UserCreate with fields: email, password")
                user_create = UserCreate(
                    email=admin_email,
                    password=admin_password,
                )
                user = await user_manager.create(user_create)
                print(f"Admin user created successfully: {user.email}")
                
                # Update user to make them a superuser and active after creation
                print("Making user a superuser and verifying them...")
                user.is_superuser = True
                user.is_verified = True
                user.is_active = True
                await user.save()
                print(f"User updated: superuser={user.is_superuser}, verified={user.is_verified}, active={user.is_active}")
                
                # Verify the user was created
                found_user = await User.find_one({"email": admin_email})
                if found_user:
                    print(f"Verified user exists: {found_user.email}, is_active: {found_user.is_active}, is_verified: {found_user.is_verified}, is_superuser: {found_user.is_superuser}")
                else:
                    print("WARNING: Could not find the user after creation")
                    
            except Exception as e:
                print(f"Error creating admin user: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"Users already exist in database. Found {user_count} users.")
            
            # List all users for debugging
            users = await User.find_all().to_list()
            for user in users:
                print(f"User: {user.email}, is_active: {user.is_active}, is_verified: {user.is_verified}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting init_user.py script...")
    asyncio.run(create_user())
    print("Finished init_user.py script.")