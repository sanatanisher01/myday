// Gemini API Configuration and Helper Functions
const GEMINI_API_KEY = 'AIzaSyCYPr16pDrZ2TayEkGKyAJQrHf9mSVCAxA'; // Add your Gemini API key here
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

// Context information about the website that will be used to guide Gemini's responses
const WEBSITE_CONTEXT = `
MyDay Events is an event management platform that helps users:
- Browse and book various types of events
- Check event pricing and availability
- Make reservations and manage bookings
- Contact support for assistance
- Get information about cancellations and refunds
- Access FAQs and help documentation
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
                        text: `${WEBSITE_CONTEXT}\n\nUser message: ${userMessage}\n\nProvide a helpful response about MyDay Events based on the context above. Keep the response concise and relevant to our event management platform.`
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
    
    if (message.includes('book') || message.includes('reservation')) {
        return "To book an event, please browse our events page and click on 'Book Now' for the event you're interested in. Would you like me to show you our available events? <a href='/events/' class='text-primary'>View Events</a>";
    } else if (message.includes('price') || message.includes('cost')) {
        return "Event prices vary depending on the type and scale. You can find detailed pricing information on each event's page. Would you like to see our most popular events?";
    } else if (message.includes('support') || message.includes('help')) {
        return "I'm here to help! You can reach our support team at support@myday.com or call us at +91 6397664902 during business hours. How can I assist you today?";
    } else if (message.includes('cancel') || message.includes('refund')) {
        return "For cancellations and refunds, please check our cancellation policy in the FAQ section. Would you like me to explain our cancellation policy?";
    } else if (message.includes('hello') || message.includes('hi')) {
        return "Hello! How can I assist you with your event planning today?";
    }
    
    return "I'm sorry, I don't understand that. Can you please rephrase or use one of the quick reply options?";
}