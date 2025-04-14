// Gemini API Configuration and Helper Functions
const GEMINI_API_KEY = 'AIzaSyCYPr16pDrZ2TayEkGKyAJQrHf9mSVCAxA'; // Add your Gemini API key here
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

// Context information about the website that will be used to guide Gemini's responses
const WEBSITE_CONTEXT = `
MyDay Events is an event management platform that helps users:
- Browse and book various types of events (weddings, birthdays, anniversaries, corporate events)
- Check event pricing and availability
- Make reservations and manage bookings
- Contact support for assistance
- Get information about cancellations and refunds
- Access FAQs and help documentation

The website also has the following features:
- User accounts and profiles
- Event galleries and reviews
- Booking management
- Payment processing
- Customer support
`;

// Function to generate response using Gemini API
async function generateGeminiResponse(userMessage) {
    try {
        if (!GEMINI_API_KEY) {
            console.error('Gemini API key not configured');
            throw new Error('API key not configured');
        }

        const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `${WEBSITE_CONTEXT}\n\nUser message: ${userMessage}\n\nYou are an AI assistant for MyDay Events website. If the user's question is related to events, booking, or our platform, use the context above to provide a helpful response. If the question is about general knowledge, current events, or any other topic not related to our platform, feel free to answer it to the best of your ability. Always be helpful, friendly, and concise.`
                    }]
                }]
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get response from Gemini API');
        }

        const data = await response.json();
        return data.candidates[0].content.parts[0].text;

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
        return "To book an event, please browse our events page and click on 'Book Now' for the event you're interested in. Would you like me to show you our available events? <a href='/events/' class='text-primary'>View Events</a>";
    } else if (message.includes('price') || message.includes('cost')) {
        return "Event prices vary depending on the type and scale. You can find detailed pricing information on each event's page. Would you like to see our most popular events?";
    } else if (message.includes('support') || message.includes('help')) {
        return "I'm here to help! You can reach our support team at support@myday.com or call us at +91 6397664902 during business hours. How can I assist you today?";
    } else if (message.includes('cancel') || message.includes('refund')) {
        return "For cancellations and refunds, please check our cancellation policy in the FAQ section. Would you like me to explain our cancellation policy?";
    }

    // General conversation responses
    else if (message.includes('hello') || message.includes('hi') || message.includes('hey')) {
        return "Hello! How can I assist you today? Feel free to ask me anything about our event services or any general questions you might have.";
    } else if (message.includes('thank')) {
        return "You're welcome! Is there anything else I can help you with?";
    } else if (message.includes('weather')) {
        return "I don't have access to real-time weather data, but I can suggest checking a weather service like AccuWeather or Weather.com for the most current forecast.";
    } else if (message.includes('joke')) {
        const jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "How does a penguin build its house? Igloos it together!"
        ];
        return jokes[Math.floor(Math.random() * jokes.length)];
    } else if (message.includes('time') || message.includes('date')) {
        const now = new Date();
        return `The current time is ${now.toLocaleTimeString()} and today's date is ${now.toLocaleDateString()}.`;
    }

    // Default response for anything else
    return "I'm currently experiencing connection issues with my knowledge base. Could you try asking something about our event services, or perhaps rephrase your question? You can also use one of the quick reply options below.";
}