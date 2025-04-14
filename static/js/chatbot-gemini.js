// Gemini API Configuration and Helper Functions
const GEMINI_API_KEY = 'AIzaSyCYPr16pDrZ2TayEkGKyAJQrHf9mSVCAxA'; // Add your Gemini API key here
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

// Enhanced context information about the website that will be used to guide Gemini's responses
const WEBSITE_CONTEXT = `
MyDay Events is a comprehensive event management platform that specializes in:

1. EVENT TYPES:
- Weddings: Full-service wedding planning, venues, catering, photography, and decoration
- Birthdays: Theme parties, venue booking, entertainment, and catering for all ages
- Anniversaries: Romantic celebrations, renewal of vows, surprise parties, and dining experiences
- Corporate Events: Conferences, team building, product launches, and business meetings

2. SERVICES:
- Venue selection and booking
- Catering and menu planning
- Photography and videography
- Decoration and theme design
- Entertainment and music
- Transportation and accommodation
- Guest management

3. BOOKING PROCESS:
- Browse events by category
- Select date and time
- Choose additional services
- Make payment (full or partial)
- Receive confirmation
- Manage or modify booking through user dashboard

4. PRICING:
- Wedding packages start at ₹50,000
- Birthday celebrations start at ₹15,000
- Anniversary packages start at ₹25,000
- Corporate events start at ₹35,000 per day
- All prices can be customized based on requirements

5. CANCELLATION POLICY:
- Full refund if cancelled 30+ days before event
- 50% refund if cancelled 15-29 days before event
- 25% refund if cancelled 7-14 days before event
- No refund if cancelled less than 7 days before event

6. CONTACT INFORMATION:
- Customer support: support@myday.com
- Phone: +91 6397664902
- Office hours: Monday-Saturday, 9 AM - 6 PM
- Address: 123 Event Street, Bangalore, India

7. WEBSITE FEATURES:
- User accounts and profiles
- Event galleries with high-quality images
- Customer reviews and ratings
- Secure payment processing
- Real-time availability checking
- Mobile-responsive design
- Personalized recommendations
`;

// Function to generate response using Gemini API
async function generateGeminiResponse(userMessage) {
    try {
        if (!GEMINI_API_KEY) {
            console.error('Gemini API key not configured');
            throw new Error('API key not configured');
        }

        // Show loading indicator in UI
        document.getElementById('chatbotMessages').lastChild.querySelector('.message-content').innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';

        const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `${WEBSITE_CONTEXT}\n\nUser message: ${userMessage}\n\nYou are an AI assistant for MyDay Events website. Respond to the following user message in a helpful, friendly, and conversational way.\n\nIf the user's question is related to events, booking, pricing, or our platform, use the detailed context above to provide a specific and accurate response.\n\nIf the question is about general knowledge, current events, or any topic not related to our platform, please answer it to the best of your ability as a helpful AI assistant.\n\nIf you're unsure about something specific to our business that isn't in the context, you can suggest the user contact our customer support.\n\nKeep responses concise (under 150 words) but informative. Use a friendly, helpful tone. Format your response with appropriate spacing and bullet points when listing multiple items.`
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    topK: 40,
                    topP: 0.95,
                    maxOutputTokens: 1024,
                }
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(`Failed to get response from Gemini API: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Check if we have a valid response
        if (data.candidates && data.candidates.length > 0 && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts.length > 0) {
            return data.candidates[0].content.parts[0].text;
        } else {
            console.error('Invalid response structure:', data);
            throw new Error('Invalid response structure from API');
        }

    } catch (error) {
        console.error('Error generating response:', error);
        return getDefaultResponse(userMessage);
    }
}

// Fallback responses when API is not available
function getDefaultResponse(message) {
    message = message.toLowerCase();

    // Website-specific responses
    if (message.includes('book') || message.includes('reservation')) {
        return "To book an event, please browse our events page and click on 'Book Now' for the event you're interested in. Our booking process is simple and user-friendly. <a href='/events/' class='text-primary'>View Events</a>";
    }
    else if (message.includes('price') || message.includes('cost') || message.includes('fee')) {
        return "Our pricing varies by event type:<br>• Wedding packages start at ₹50,000<br>• Birthday celebrations start at ₹15,000<br>• Anniversary packages start at ₹25,000<br>• Corporate events start at ₹35,000<br><br>Would you like more details about a specific event type?";
    }
    else if (message.includes('support') || message.includes('help') || message.includes('contact')) {
        return "You can reach our support team at:<br>• Email: support@myday.com<br>• Phone: +91 6397664902<br>• Hours: Monday-Saturday, 9 AM - 6 PM<br><br>How else can I assist you today?";
    }
    else if (message.includes('cancel') || message.includes('refund')) {
        return "Our cancellation policy:<br>• Full refund: 30+ days before event<br>• 50% refund: 15-29 days before<br>• 25% refund: 7-14 days before<br>• No refund: Less than 7 days before<br><br>Need more details about cancellations?";
    }
    else if (message.includes('wedding') || message.includes('marry')) {
        return "Our wedding packages include venue selection, catering, decoration, photography, and entertainment. Prices start at ₹50,000 and can be customized to your specific needs. Would you like to see our wedding venues? <a href='/events/wedding/' class='text-primary'>View Wedding Services</a>";
    }
    else if (message.includes('birthday') || message.includes('bday')) {
        return "We offer birthday celebrations for all ages with customizable themes, venue options, catering, and entertainment. Packages start at ₹15,000. Would you like to explore our birthday packages? <a href='/events/birthday/' class='text-primary'>View Birthday Services</a>";
    }
    else if (message.includes('anniversary')) {
        return "Make your anniversary special with our romantic celebration packages including intimate dinners, renewal of vows, or surprise parties. Prices start at ₹25,000. <a href='/events/anniversary/' class='text-primary'>View Anniversary Services</a>";
    }
    else if (message.includes('corporate') || message.includes('business') || message.includes('conference')) {
        return "Our corporate event services include conferences, team building activities, product launches, and business meetings. Packages start at ₹35,000 per day. <a href='/events/corporate/' class='text-primary'>View Corporate Services</a>";
    }
    else if (message.includes('venue') || message.includes('location') || message.includes('place')) {
        return "We offer a variety of venues including banquet halls, outdoor gardens, beachfront properties, and luxury hotels. Each venue can be customized to match your event theme and requirements. Would you like to see our venue options?";
    }
    else if (message.includes('catering') || message.includes('food') || message.includes('menu')) {
        return "Our catering services offer diverse menu options including vegetarian, non-vegetarian, international cuisines, and custom menus. We can accommodate dietary restrictions and preferences. Would you like to know more about our food options?";
    }
    else if (message.includes('photography') || message.includes('video') || message.includes('photo')) {
        return "We provide professional photography and videography services for all events. Our packages include pre-event shoots, event coverage, drone photography, and professionally edited albums/videos. Would you like to see samples of our work?";
    }

    // General conversation responses
    else if (message.includes('hello') || message.includes('hi') || message.includes('hey')) {
        return "Hello! I'm your MyDay Events assistant. I can help with event bookings, pricing information, venue details, or answer any questions about our services. What can I help you with today?";
    }
    else if (message.includes('thank')) {
        return "You're welcome! I'm happy to help. Is there anything else you'd like to know about our event services?";
    }
    else if (message.includes('weather')) {
        return "I don't have access to real-time weather data, but I can help you plan indoor or outdoor events with weather contingency plans. Would you like to know about our weather backup options for outdoor events?";
    }
    else if (message.includes('joke') || message.includes('funny')) {
        const jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "How does a penguin build its house? Igloos it together!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why did the event planner go to art school? To learn how to draw a crowd!",
            "What do you call a wedding that's also a birthday party? A 'wed-day' celebration!"
        ];
        return jokes[Math.floor(Math.random() * jokes.length)];
    }
    else if (message.includes('time') || message.includes('date')) {
        const now = new Date();
        return `The current time is ${now.toLocaleTimeString()} and today's date is ${now.toLocaleDateString()}. Planning an event for a specific date? I can help you check availability!`;
    }

    // Default response for anything else
    return "I'm here to help with any questions about MyDay Events services! You can ask about our event packages, pricing, venues, or any specific services like catering or photography. If you're looking for general information, I'll do my best to assist. What would you like to know?";
}