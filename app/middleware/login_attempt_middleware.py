from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import Dict

import time

class LoginAttemptMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.failed_attempts: Dict[str, int] = defaultdict(int)
        self.block_until: Dict[str, float] = defaultdict(float)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        print(self.failed_attempts)
        print(self.block_until)
        # Check if the IP is blocked
        if current_time < self.block_until.get(client_ip, 0):
            message = {"message": "Too many failed login attempts. Please try again later."}
            return JSONResponse(content=message, status_code=429)

        # Process the request
        response = await call_next(request)

        # If the request is a failed login attempt, increment the counter
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            self.failed_attempts[client_ip] += 1
            if self.failed_attempts[client_ip] >= 3:
                self.block_until[client_ip] = current_time + 3600 # Block for 1 hr
                self.failed_attempts[client_ip] = 0 # Reset the counter

        return response