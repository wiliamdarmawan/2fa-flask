# Two-Factor Authentication (2FA) API

This Flask-based API implements Two-Factor Authentication (2FA) using One-Time Passwords (OTP).

Users first log in with their username/email and password, then receive a 6-digit OTP via email.

They must enter the OTP to receive a JWT token for authentication.

## Features
- User Registration
- Login with OTP sent via email
- OTP validation and JWT authentication
- Protected route requiring authentication

## Installation

### Prerequisites
- Docker
- Docker Compose

### Setup and Run

1. Clone the repository:
   ```sh
   git clone https://github.com/wiliamdarmawan/2fa-flask.git
   cd 2fa-flask
   ```

2. Build and start the services:
   ```sh
   make docker-up
   ```

3. The API will be accessible at `http://localhost:5001`

### Unit Testing
- You can run the unit test by simply doing: `make test`

## API Endpoints

### 1. Register a New User (`POST /register`)

By hitting this API, you'll be able to create a new User by passing `email` and `password` information.

Upon success, an `username` will automatically generated for you based on the `email` you've provided
- **Request Params**
    ```json
    {
        "data": {
            "attributes": {
                "email": "user@example.com",
                "password": "securepassword"
            }
        }
    }
    ```
- **Responses**
  - 200
  ```json
  {
      "data": {
          "id": "1",
          "attributes": {
              "username": "user12345@example.com"
          }
      }
  }
  ```
  - 400
  ```json
  {
      "errors": [
          {
              "error": "Email and password required",
              "errorCode": "TFAE2",
              "errorHandling": "Please include the missing parameter."
          }
      ]
  }
  ```

### 2. Login and Get OTP (`POST /login`)
Once you've successfully created a User using `POST /register` API above, you will then be able to login with your created user to get an OTP.

For the sake of testing, it's recommended to use email with `@mailinator` suffix.

By doing that, you will be able to receive OTP in Mailinator's [Public Inbox](https://www.mailinator.com/v4/public/inboxes.jsp). Simply search your email in the right side of the page and you'll see the OTP sent to you.


- **Request Params**
    ```json
    {
        "data": {
            "attributes": {
                "email": "user@example.com",
                "password": "securepassword"
            }
        }
    }
    ```
- **Responses**
  - 201
  ```json
  { 
      "message": "OTP sent to email"
  }
  ```
  - 401
  ```json
  {
      "errors": [
          {
              "error": "Invalid credentials",
              "errorCode": "TFAE3",
              "errorHandling": "Please provide correct credentials"
          }
      ]
  }
  ```

### Verify OTP (`POST /verify-otp`)
After successfully receiving your OTP through `POST /login` API above, you will be able to exchange your OTP with JWT Access token, which you will need to provide to authorize yourself for using the protected API.
- **Request Params**
    ```json
    {
        "data": {
            "attributes": {
                "email": "user@example.com",
                "otp": "123456"
            }
        }
    }
    ```
- **Responses:**
  - 200
  ```json
  {
      "access_token": "your-jwt-token"
  }
  ```
  - 401
  ```json
  {
      "errors": [
          {
              "error": "Invalid or expired OTP",
              "errorCode": "TFAE3",
              "errorHandling": "Please provide correct credentials"
          }
      ]
  }
  ```

### Access Protected Route (`GET /dashboard`)
You will need the JWT Access Token received from `POST /verify-otp` API above, and pass it to the header to access this API.

This API will check whether you're authorized or not.

- **Headers:**
  ```json
  Authorization: Bearer your-jwt-token
  ```

- **Responses:**
  - 200
  ```json
  {
      "status": "success",
      "message": "Hey username, you are welcome"
  }
  ```
  - 401
  ```json
  {
      "errors": [
          {
              "error": "Invalid JWT Token",
              "errorCode": "TFAE3",
              "errorHandling": "Please provide correct credentials"
          }
      ]
  }
  ```