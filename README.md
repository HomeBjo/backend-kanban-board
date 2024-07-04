# Kanban Project

## Overview
This is a Kanban project developed as part of the Developer Academy. It includes task and subtask management functionalities.

## Features
- User authentication and token generation
- CRUD operations for tasks and subtasks
- Token-based authentication

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/kanban-project.git

   Frontend Usage
A user is stored in the frontend, and we log in using a token.
You can post tasks by using the input fields and then clicking the "Save Task" button.
The edit function allows editing of the first-level attributes like title and description.
The delete function removes the entire task.
The editSubtask function is used to edit subtasks. Note that editing a subtask does not work via the edit button even if the subtasks are displayed.
The deleteSubtask function deletes individual subtasks.
