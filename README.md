# Project Name

Service requests: The application would allow customers to submit service requests online.
This would include the ability to select the type of service request, provide details about the
request, and attach files.

Request tracking: The application would allow customers to track the status of their service
requests. This would include the ability to see the status of the request, the date and time
the request was submitted, and the date and time the request was resolved.
The file structure for the given project is:
```
gas-utility-service/
├── gas_utility_service/
│ ├── **init**.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ ├── customer_service/
│ │ ├── **init**.py
│ │ ├── admin.py
│ │ ├── apps.py
│ │ ├── models.py
│ │ ├── tests.py
│ │ ├── views.py
│ │ ├── templates/
│ │ │ ├── customer_service/
│ │ │ │ ├── base.html
│ │ │ │ ├── submit_request.html
│ │ │ │ ├── request_status.html
│ │ │ │ ├── account_info.html
│ │ │ ├── registration/
│ │ │ │ ├── register.html
│ │ │ │ ├── login.html
│ │ │ │ ├── logout.html
│ │ │ ├── support/
│ │ │ │ ├── base.html
│ │ │ │ ├── dashboard.html
│ │ │ │ ├── account_info.html
│ │ │ │ ├── update_request.html
│ │ ├── urls.py
│ ├── static/
│ │ ├── css/
│ │ │ ├── styles.css
│ │ ├── js/
│ │ │ ├── scripts.js
│ ├── media/
│ │ ├── uploads/
├── manage.py
├── README.md
├── requirements.txt
├── .gitignore

## Features

- **Rate Limiting**: Prevents excessive requests to improve server performance and user experience.
- **Database Indexing**: Optimized database queries using indexing to improve performance.
```
## Performance Improvements

### Rate Limiting

To prevent excessive requests from the same user in a short time frame, **rate limiting** has been implemented. This helps ensure that the server remains responsive, and users don't overwhelm the system by submitting requests too quickly.

- **Rate Limiting Implementation**:
  - Users are limited to submitting one service request within a specific time window (e.g., 30 seconds).
  - If a user attempts to submit a request before the time window has passed, an error message is displayed to let them know they must wait before submitting another request.

This is implemented using Django’s caching mechanism, which stores the timestamp of the last request for each user. If the time difference between the current request and the last submission is less than the allowed rate limit, the user will be prompted to try again later.

Example code:

```python
last_submission_time = cache.get(RATE_LIMIT_KEY_PREFIX + str(request.user.id))

if last_submission_time:
    time_diff = timezone.now() - last_submission_time
    if time_diff < RATE_LIMIT_TIME:

        return render(request, 'customer_service/submit_request.html', {
            'form': ServiceRequestForm(),
            'error_message': 'You are submitting requests too quickly. Please wait a moment and try again.'
        })
```

- **Database Indexing**:
  Indexing has been added to the relevant fields of the models. Indexing ensures that queries on frequently filtered or sorted fields (like status, request_type, and created_at) are executed more efficiently.
  example code:
  class Meta:
  indexes = [
  models.Index(fields=['status']),
  models.Index(fields=['request_type']),
  models.Index(fields=['created_at']),
  ]
