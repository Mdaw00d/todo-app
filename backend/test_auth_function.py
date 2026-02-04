#!/usr/bin/env python3
"""
Direct test of the auth login function to check for errors.
"""

import asyncio
from src.api.auth import login
from sqlalchemy.ext.asyncio import AsyncSession

async def test_login_function():
    try:
        # Create a mock session
        class MockSession:
            async def execute(self, query):
                class MockResult:
                    def scalar_one_or_none(self):
                        return None
                return MockResult()

        # Test calling the login function directly
        result = await login(email="test@example.com", password="password", session=MockSession())
        print("SUCCESS: Login function executed without error")
        print(f"Result: {result}")
    except Exception as e:
        print(f"ERROR in login function: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_login_function())