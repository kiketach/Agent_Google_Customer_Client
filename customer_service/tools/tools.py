import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional
import os

logger = logging.getLogger(__name__)


def send_call_companion_link(
    phone_number: str,
    date: str,
    start_time: str,
    end_time: str,
    company_email: str,
    user_email: Optional[str] = None
) -> dict:
    """
    Schedules a Google Meet call, sends the link to the user via chat, and emails the company.

    Args:
        phone_number (str): The user's phone number.
        date (str): Date of the call (YYYY-MM-DD).
        start_time (str): Start time (HH:MM, 24h).
        end_time (str): End time (HH:MM, 24h).
        company_email (str): Email to notify the company.
        user_email (str, optional): User's email (for calendar invite).

    Returns:
        dict: Status and Meet link or error message.
    """
    import pytz
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    import smtplib
    from email.mime.text import MIMEText

    logger.info("Scheduling Meet call for %s on %s from %s to %s", phone_number, date, start_time, end_time)

    # --- Google Calendar Setup ---
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
    CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'Hat trick')
    TIMEZONE = os.getenv('GOOGLE_CALENDAR_TIMEZONE', 'America/Bogota')

    # Parse datetime
    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
    tz = pytz.timezone(TIMEZONE)
    start_dt = tz.localize(start_dt)
    end_dt = tz.localize(end_dt)

    # Authenticate with Google
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        logger.error("Google API auth failed: %s", e)
        return {"status": "error", "message": "Google API authentication failed."}

    # Check for conflicting events
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        for event in events:
            if event.get('conferenceData'):
                return {"status": "conflict", "message": "There is already a video call scheduled at this time."}
    except Exception as e:
        logger.error("Error checking calendar: %s", e)
        return {"status": "error", "message": "Failed to check calendar."}

    # Create event with Meet link
    event_body = {
        'summary': 'Videollamada con cliente',
        'description': f'Videollamada agendada para {phone_number}',
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': TIMEZONE},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': TIMEZONE},
        'attendees': [{'email': company_email}],
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
    }
    if user_email:
        event_body['attendees'].append({'email': user_email})

    try:
        event = service.events().insert(
            calendarId=CALENDAR_ID,
            body=event_body,
            conferenceDataVersion=1
        ).execute()
        meet_link = event['conferenceData']['entryPoints'][0]['uri']
    except Exception as e:
        logger.error("Error creating event: %s", e)
        return {"status": "error", "message": "Failed to create Meet event."}

    # Send email to company
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')
        msg = MIMEText(f"Se ha agendado una videollamada.\n\nLink: {meet_link}\nCliente: {phone_number}\nFecha: {date} {start_time}-{end_time}")
        msg['Subject'] = 'Nueva videollamada agendada'
        msg['From'] = smtp_user
        msg['To'] = company_email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [company_email], msg.as_string())
    except Exception as e:
        logger.error("Error sending email: %s", e)
        # Not critical, continue

    # Return link for chat
    return {
        "status": "success",
        "message": f"Videollamada agendada. Link: {meet_link}",
        "meet_link": meet_link
    }


def approve_discount(discount_type: str, value: float, reason: str) -> str:
    """
    Approve the flat rate or percentage discount requested by the user.

    Args:
        discount_type (str): The type of discount, either "percentage" or "flat".
        value (float): The value of the discount.
        reason (str): The reason for the discount.

    Returns:
        str: A JSON string indicating the status of the approval.

    Example:
        >>> approve_discount(type='percentage', value=10.0, reason='Customer loyalty')
        '{"status": "ok"}'
    """
    logger.info(
        "Approving a %s discount of %s because %s", discount_type, value, reason
    )

    logger.info("INSIDE TOOL CALL")
    return '{"status": "ok"}'


def sync_ask_for_approval(discount_type: str, value: float, reason: str) -> str:
    """
    Asks the manager for approval for a discount.

    Args:
        discount_type (str): The type of discount, either "percentage" or "flat".
        value (float): The value of the discount.
        reason (str): The reason for the discount.

    Returns:
        str: A JSON string indicating the status of the approval.

    Example:
        >>> sync_ask_for_approval(type='percentage', value=15, reason='Customer loyalty')
        '{"status": "approved"}'
    """
    logger.info(
        "Asking for approval for a %s discount of %s because %s",
        discount_type,
        value,
        reason,
    )
    return '{"status": "approved"}'


def update_salesforce_crm(customer_id: str, details: dict) -> dict:
    """
    Updates the Salesforce CRM with customer details.

    Args:
        customer_id (str): The ID of the customer.
        details (str): A dictionary of details to update in Salesforce.

    Returns:
        dict: A dictionary with the status and message.

    Example:
        >>> update_salesforce_crm(customer_id='123', details={
            'appointment_date': '2024-07-25',
            'appointment_time': '9-12',
            'services': 'Planting',
            'discount': '15% off planting',
            'qr_code': '10% off next in-store purchase'})
        {'status': 'success', 'message': 'Salesforce record updated.'}
    """
    logger.info(
        "Updating Salesforce CRM for customer ID %s with details: %s",
        customer_id,
        details,
    )
    return {"status": "success", "message": "Salesforce record updated."}


def access_cart_information(customer_id: str) -> dict:
    """
    Args:
        customer_id (str): The ID of the customer.

    Returns:
        dict: A dictionary representing the cart contents.

    Example:
        >>> access_cart_information(customer_id='123')
        {'items': [{'product_id': 'soil-123', 'name': 'Standard Potting Soil', 'quantity': 1}, {'product_id': 'fert-456', 'name': 'General Purpose Fertilizer', 'quantity': 1}], 'subtotal': 25.98}
    """
    logger.info("Accessing cart information for customer ID: %s", customer_id)

    # MOCK API RESPONSE - Replace with actual API call
    mock_cart = {
        "items": [
            {
                "product_id": "soil-123",
                "name": "Standard Potting Soil",
                "quantity": 1,
            },
            {
                "product_id": "fert-456",
                "name": "General Purpose Fertilizer",
                "quantity": 1,
            },
        ],
        "subtotal": 25.98,
    }
    return mock_cart


def modify_cart(
    customer_id: str, items_to_add: list[dict], items_to_remove: list[dict]
) -> dict:
    """Modifies the user's shopping cart by adding and/or removing items.

    Args:
        customer_id (str): The ID of the customer.
        items_to_add (list): A list of dictionaries, each with 'product_id' and 'quantity'.
        items_to_remove (list): A list of product_ids to remove.

    Returns:
        dict: A dictionary indicating the status of the cart modification.
    Example:
        >>> modify_cart(customer_id='123', items_to_add=[{'product_id': 'soil-456', 'quantity': 1}, {'product_id': 'fert-789', 'quantity': 1}], items_to_remove=[{'product_id': 'fert-112', 'quantity': 1}])
        {'status': 'success', 'message': 'Cart updated successfully.', 'items_added': True, 'items_removed': True}
    """

    logger.info("Modifying cart for customer ID: %s", customer_id)
    logger.info("Adding items: %s", items_to_add)
    logger.info("Removing items: %s", items_to_remove)
    # MOCK API RESPONSE - Replace with actual API call
    return {
        "status": "success",
        "message": "Cart updated successfully.",
        "items_added": True,
        "items_removed": True,
    }


def get_product_recommendations(plant_type: str, customer_id: str) -> dict:
    """Provides product recommendations based on the type of plant.

    Args:
        plant_type: The type of plant (e.g., 'Petunias', 'Sun-loving annuals').
        customer_id: Optional customer ID for personalized recommendations.

    Returns:
        A dictionary of recommended products. Example:
        {'recommendations': [
            {'product_id': 'soil-456', 'name': 'Bloom Booster Potting Mix', 'description': '...'},
            {'product_id': 'fert-789', 'name': 'Flower Power Fertilizer', 'description': '...'}
        ]}
    """
    #
    logger.info(
        "Getting product recommendations for plant " "type: %s and customer %s",
        plant_type,
        customer_id,
    )
    # MOCK API RESPONSE - Replace with actual API call or recommendation engine
    if plant_type.lower() == "petunias":
        recommendations = {
            "recommendations": [
                {
                    "product_id": "soil-456",
                    "name": "Bloom Booster Potting Mix",
                    "description": "Provides extra nutrients that Petunias love.",
                },
                {
                    "product_id": "fert-789",
                    "name": "Flower Power Fertilizer",
                    "description": "Specifically formulated for flowering annuals.",
                },
            ]
        }
    else:
        recommendations = {
            "recommendations": [
                {
                    "product_id": "soil-123",
                    "name": "Standard Potting Soil",
                    "description": "A good all-purpose potting soil.",
                },
                {
                    "product_id": "fert-456",
                    "name": "General Purpose Fertilizer",
                    "description": "Suitable for a wide variety of plants.",
                },
            ]
        }
    return recommendations


def check_product_availability(product_id: str, store_id: str) -> dict:
    """Checks the availability of a product at a specified store (or for pickup).

    Args:
        product_id: The ID of the product to check.
        store_id: The ID of the store (or 'pickup' for pickup availability).

    Returns:
        A dictionary indicating availability.  Example:
        {'available': True, 'quantity': 10, 'store': 'Main Store'}

    Example:
        >>> check_product_availability(product_id='soil-456', store_id='pickup')
        {'available': True, 'quantity': 10, 'store': 'pickup'}
    """
    logger.info(
        "Checking availability of product ID: %s at store: %s",
        product_id,
        store_id,
    )
    # MOCK API RESPONSE - Replace with actual API call
    return {"available": True, "quantity": 10, "store": store_id}


def schedule_planting_service(
    customer_id: str, date: str, time_range: str, details: str
) -> dict:
    """Schedules a planting service appointment.

    Args:
        customer_id: The ID of the customer.
        date:  The desired date (YYYY-MM-DD).
        time_range: The desired time range (e.g., "9-12").
        details: Any additional details (e.g., "Planting Petunias").

    Returns:
        A dictionary indicating the status of the scheduling. Example:
        {'status': 'success', 'appointment_id': '12345', 'date': '2024-07-29', 'time': '9:00 AM - 12:00 PM'}

    Example:
        >>> schedule_planting_service(customer_id='123', date='2024-07-29', time_range='9-12', details='Planting Petunias')
        {'status': 'success', 'appointment_id': 'some_uuid', 'date': '2024-07-29', 'time': '9-12', 'confirmation_time': '2024-07-29 9:00'}
    """
    logger.info(
        "Scheduling planting service for customer ID: %s on %s (%s)",
        customer_id,
        date,
        time_range,
    )
    logger.info("Details: %s", details)
    # MOCK API RESPONSE - Replace with actual API call to your scheduling system
    # Calculate confirmation time based on date and time_range
    start_time_str = time_range.split("-")[0]  # Get the start time (e.g., "9")
    confirmation_time_str = (
        f"{date} {start_time_str}:00"  # e.g., "2024-07-29 9:00"
    )

    return {
        "status": "success",
        "appointment_id": str(uuid.uuid4()),
        "date": date,
        "time": time_range,
        "confirmation_time": confirmation_time_str,  # formatted time for calendar
    }


def get_available_planting_times(date: str) -> list:
    """Retrieves available planting service time slots for a given date.

    Args:
        date: The date to check (YYYY-MM-DD).

    Returns:
        A list of available time ranges.

    Example:
        >>> get_available_planting_times(date='2024-07-29')
        ['9-12', '13-16']
    """
    logger.info("Retrieving available planting times for %s", date)
    # MOCK API RESPONSE - Replace with actual API call
    # Generate some mock time slots, ensuring they're in the correct format:
    return ["9-12", "13-16"]


def send_care_instructions(
    customer_id: str, plant_type: str, delivery_method: str
) -> dict:
    """Sends an email or SMS with instructions on how to take care of a specific plant type.

    Args:
        customer_id:  The ID of the customer.
        plant_type: The type of plant.
        delivery_method: 'email' (default) or 'sms'.

    Returns:
        A dictionary indicating the status.

    Example:
        >>> send_care_instructions(customer_id='123', plant_type='Petunias', delivery_method='email')
        {'status': 'success', 'message': 'Care instructions for Petunias sent via email.'}
    """
    logger.info(
        "Sending care instructions for %s to customer: %s via %s",
        plant_type,
        customer_id,
        delivery_method,
    )
    # MOCK API RESPONSE - Replace with actual API call or email/SMS sending logic
    return {
        "status": "success",
        "message": f"Care instructions for {plant_type} sent via {delivery_method}.",
    }


def generate_qr_code(
    customer_id: str,
    discount_value: float,
    discount_type: str,
    expiration_days: int,
) -> dict:
    """Generates a QR code for a discount.

    Args:
        customer_id: The ID of the customer.
        discount_value: The value of the discount (e.g., 10 for 10%).
        discount_type: "percentage" (default) or "fixed".
        expiration_days: Number of days until the QR code expires.

    Returns:
        A dictionary containing the QR code data (or a link to it). Example:
        {'status': 'success', 'qr_code_data': '...', 'expiration_date': '2024-08-28'}

    Example:
        >>> generate_qr_code(customer_id='123', discount_value=10.0, discount_type='percentage', expiration_days=30)
        {'status': 'success', 'qr_code_data': 'MOCK_QR_CODE_DATA', 'expiration_date': '2024-08-24'}
    """
    logger.info(
        "Generating QR code for customer: %s with %s - %s discount.",
        customer_id,
        discount_value,
        discount_type,
    )
    # MOCK API RESPONSE - Replace with actual QR code generation library
    expiration_date = (
        datetime.now() + timedelta(days=expiration_days)
    ).strftime("%Y-%m-%d")
    return {
        "status": "success",
        "qr_code_data": "MOCK_QR_CODE_DATA",  # Replace with actual QR code
        "expiration_date": expiration_date,
    }
