# API Documentation

This document provides an overview of the endpoints available in the API.

## Endpoints

### 1. `GET /auto_assign_status`

- **Description:** Retrieves the status of automatic assignment toggling.
- **Authentication:** Admin user.
- **Returns:** JSON response containing the status of automatic assignment toggling.

### 2. `POST /auto_assign_toggle/{status}`

- **Description:** Toggles the automatic assignment feature.
- **Authentication:** Admin user.
- **URL Path Parameters:**
  - `status` (bool): Boolean value indicating whether to enable (True) or disable (False) the automatic assignment feature.
- **Returns:** JSON response confirming the status of the automatic assignment feature.

### 3. `POST /create_profile`

- **Description:** Creates a profile for a technician.
- **Authentication:** Technician user.
- **Request Body (JSON):**
  - `name` (str): The name of the technician.
  - `skill_set` (str): The skill set of the technician.
  - `experience_years` (int): The number of years of experience of the technician.
  - `phoneno` (str): The phone number of the technician.
- **Returns:** JSON response confirming the successful creation of the technician's profile.

### 4. `POST /create_ticket`

- **Description:** Creates a new ticket.
- **Authentication:** Admin user.
- **Request Body (JSON):**
  - `ticket` (Ticket): The details of the ticket to be created.
- **Returns:** JSON response containing information about the created ticket.

### 5. `GET /all_generated_tickets`

- **Description:** Retrieves all generated tickets.
- **Authentication:** Admin user.
- **Returns:** JSON response containing information about all generated tickets.

### 6. `GET /get_single_ticket`

- **Description:** Retrieves information about a single ticket.
- **Authentication:** Admin user.
- **Query Parameters:**
  - `_id` (str): The unique identifier of the ticket.
- **Returns:** JSON response containing information about the specified ticket.

### 7. `GET /all_technicians`

- **Description:** Retrieves all technicians' information.
- **Authentication:** Admin user.
- **Returns:** JSON response containing information about all technicians.

### 8. `GET /nearest_technician`

- **Description:** Retrieves the nearest technician based on provided location and skill set.
- **Authentication:** Admin or Technician user.
- **Query Parameters:**
  - `lat` (float): Latitude of the location.
  - `long` (float): Longitude of the location.
  - `skill_set` (str): Skill set required for the technician.
- **Returns:** JSON response containing information about the nearest technician.

### 9. `GET /query`

- **Description:** Retrieves appropriate technician details based on a query.
- **Authentication:** Admin or Technician user.
- **Query Parameters:**
  - `query` (str): The query to be processed.
  - `lat` (float): Latitude of the location.
  - `long` (float): Longitude of the location.
- **Returns:** JSON response containing appropriate technician details based on the query.

### 10. `POST /login`

- **Description:** Logs in a user.
- **Authentication:** None.
- **Request Body (Form Data):**
  - `username` (str): The username of the user.
  - `password` (str): The password of the user.
- **Returns:** JSON response containing the access token and token type.

## Note

- `authorize_user` and `authorize_both_user` are custom dependencies used for user authentication.
- `oauth2_scheme` is the OAuth2 security scheme used for token-based authentication.
- `Ticket` and `TechnicianProfile` are Pydantic models used for request and response validation.
