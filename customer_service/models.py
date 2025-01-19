from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    GAS_LEAK = 'Gas Leak'
    METER_ISSUE = 'Meter Issue'
    BILLING_ISSUE = 'Billing Issue'
    SERVICE_DISRUPTION = 'Service Disruption'
    GENERAL_ENQUIRY = 'General Enquiry'

    REQUEST_TYPE_CHOICES = [
        (GAS_LEAK, 'Gas Leak'),
        (METER_ISSUE, 'Meter Issue'),
        (BILLING_ISSUE, 'Billing Issue'),
        (SERVICE_DISRUPTION, 'Service Disruption'),
        (GENERAL_ENQUIRY, 'General Enquiry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(
        max_length=30,
        choices=REQUEST_TYPE_CHOICES,
        default=GENERAL_ENQUIRY,  # Default request type if not selected
    )
    details = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Add indexes to improve query performance
        indexes = [
            models.Index(fields=['status']),  # Index on the status field
            models.Index(fields=['request_type']),  # Index on the request_type field
            models.Index(fields=['created_at']),  # Index on the created_at field
            models.Index(fields=['user']),  # Index on the user field (if you query service requests by user frequently)
        ]


    def __str__(self):
        return f"Request {self.id} - {self.status}"
