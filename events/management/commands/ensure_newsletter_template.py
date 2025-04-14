from django.core.management.base import BaseCommand
from events.models import NewsletterTemplate


class Command(BaseCommand):
    help = 'Ensures that at least one default newsletter template exists'

    def handle(self, *args, **options):
        if NewsletterTemplate.objects.count() == 0:
            # Create a simple default template
            default_template = NewsletterTemplate(
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
        </div>
        
        <div class="footer">
            <p>Best regards,<br>MyDay Events Team</p>
            <p>&copy; {% now "Y" %} MyDay Events. All rights reserved.</p>
            <p>
                <a href="{{ unsubscribe_url|default:'#' }}">Unsubscribe</a> from this newsletter
            </p>
        </div>
    </div>
</body>
</html>""",
                is_default=True
            )
            default_template.save()
            self.stdout.write(self.style.SUCCESS('Successfully created default newsletter template'))
        else:
            self.stdout.write(self.style.SUCCESS('Newsletter templates already exist'))
