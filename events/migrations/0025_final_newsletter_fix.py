from django.db import migrations


def ensure_default_template(apps, schema_editor):
    """Ensure a default newsletter template exists"""
    NewsletterTemplate = apps.get_model('events', 'NewsletterTemplate')
    
    # Check if any templates exist
    if NewsletterTemplate.objects.count() == 0:
        # Create a default template
        NewsletterTemplate.objects.create(
            name="Default Newsletter Template",
            subject="Newsletter from MyDay Events",
            content="""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyDay Events Newsletter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .header {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        
        .content {
            padding: 20px;
        }
        
        .footer {
            background-color: #f5f5f5;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }
        
        .button {
            display: inline-block;
            background-color: #4e73df;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 4px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ subject }}</h1>
        </div>
        
        <div class="content">
            <p>Hello {{ name|default:"there" }},</p>
            
            <div>{{ custom_message }}</div>
            
            <p>Thank you for subscribing to our newsletter!</p>
            
            <div style="text-align: center;">
                <a href="https://myday-kokr.onrender.com/events/" class="button">Visit Our Website</a>
            </div>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>MyDay Events Team</p>
            <p>&copy; 2024 MyDay Events. All rights reserved.</p>
            <p>
                <a href="{{ unsubscribe_url }}">Unsubscribe</a> from this newsletter
            </p>
        </div>
    </div>
</body>
</html>""",
            is_default=True
        )


class Migration(migrations.Migration):
    """
    This is the final migration to ensure everything is working correctly.
    It runs after the merge migration and ensures a default template exists.
    """

    dependencies = [
        ('events', '0024_merge_20240601_0001'),
    ]

    operations = [
        migrations.RunPython(ensure_default_template, migrations.RunPython.noop),
    ]
