from django.db import migrations

def create_default_template(apps, schema_editor):
    NewsletterTemplate = apps.get_model('events', 'NewsletterTemplate')
    
    # Check if there are any templates already
    if NewsletterTemplate.objects.count() == 0:
        # Create default template
        default_template = NewsletterTemplate(
            name="Default Welcome Template",
            subject="Welcome to MyDay Events Newsletter!",
            content="""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyDay Events Newsletter</title>
    <style>
        /* Base styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
        
        /* Header styles */
        .header {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        /* Content styles */
        .content {
            padding: 30px;
            background-color: #ffffff;
        }
        
        .greeting {
            font-size: 18px;
            margin-bottom: 20px;
            color: #444;
        }
        
        .message {
            margin-bottom: 25px;
            color: #555;
        }
        
        /* Feature list */
        .features {
            margin: 25px 0;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .feature-icon {
            width: 36px;
            height: 36px;
            background-color: #e8f0fe;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: #2575fc;
            font-size: 16px;
        }
        
        .feature-text {
            flex: 1;
        }
        
        /* CTA button */
        .cta-container {
            text-align: center;
            margin: 30px 0;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            text-decoration: none;
            padding: 12px 30px;
            border-radius: 50px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: transform 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        
        /* Support section */
        .support {
            background-color: #f5f7fa;
            padding: 20px;
            border-radius: 6px;
            margin-top: 25px;
        }
        
        .support-title {
            font-weight: 600;
            color: #444;
            margin-bottom: 10px;
        }
        
        /* Footer */
        .footer {
            background-color: #f0f2f5;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        
        .social-links {
            margin: 15px 0;
        }
        
        .social-icon {
            display: inline-block;
            width: 32px;
            height: 32px;
            background-color: #ddd;
            border-radius: 50%;
            margin: 0 5px;
            line-height: 32px;
            color: #555;
            text-decoration: none;
        }
        
        .unsubscribe {
            color: #999;
            font-size: 12px;
        }
        
        /* Responsive styles */
        @media screen and (max-width: 480px) {
            .header {
                padding: 20px 15px;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ subject|default:"Welcome to MyDay Events Newsletter!" }}</h1>
        </div>
        
        <div class="content">
            <p class="greeting">Hello {{ name|default:"there" }},</p>
            
            <p class="message">{{ custom_message|default:"Thank you for subscribing to the MyDay Events newsletter!" }}</p>
            
            <p>You will now receive updates about:</p>
            
            <div class="features">
                <div class="feature-item">
                    <div class="feature-icon">🎉</div>
                    <div class="feature-text">Our latest event offerings</div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">💰</div>
                    <div class="feature-text">Special promotions and discounts</div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">🎁</div>
                    <div class="feature-text">Seasonal packages and themes</div>
                </div>
                
                <div class="feature-item">
                    <div class="feature-icon">💡</div>
                    <div class="feature-text">Event planning tips and inspiration</div>
                </div>
            </div>
            
            <div class="cta-container">
                <a href="{{ cta_url|default:'https://myday-kokr.onrender.com/events/' }}" class="cta-button">
                    {{ cta_text|default:"Explore Our Events" }}
                </a>
            </div>
            
            <div class="support">
                <p class="support-title">Need assistance?</p>
                <p>If you have any questions or need assistance with planning your event, feel free to reply to this email or contact our support team at +91 6397664902.</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>Aryan Sanatani<br>MyDay Events Team</p>
            
            <div class="social-links">
                <a href="https://www.facebook.com/profile.php?id=100049095782484" class="social-icon">f</a>
                <a href="https://x.com/aryansanatani01" class="social-icon">𝕏</a>
                <a href="https://www.instagram.com/__aryan__gupta01/" class="social-icon">i</a>
                <a href="https://www.linkedin.com/in/aryan-gupta-383587315/" class="social-icon">in</a>
            </div>
            
            <p>&copy; 2025 MyDay Events. All rights reserved.</p>
            
            <p class="unsubscribe">
                <a href="{{ unsubscribe_url|default:'#' }}">Unsubscribe</a> from this newsletter
            </p>
        </div>
    </div>
</body>
</html>""",
            is_default=True
        )
        default_template.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_newsletter_templates_campaigns'),
    ]

    operations = [
        migrations.RunPython(create_default_template),
    ]
