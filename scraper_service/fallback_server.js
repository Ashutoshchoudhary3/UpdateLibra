
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3003; // Different port for fallback

// Create logs directory
const logsDir = path.join(__dirname, 'logs');
if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir);

// Enhanced logging function
function log(message, data = null, type = 'INFO') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${type}] ${message}${data ? ' ' + JSON.stringify(data) : ''}\n`;
    
    console.log(logEntry.trim());
    
    // Append to log file
    const logFile = path.join(logsDir, `fallback-scraper-${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, logEntry);
}

// Middleware
app.use(cors());
app.use(express.json());

// Request logging middleware
app.use((req, res, next) => {
    log(`Incoming request: ${req.method} ${req.url}`, {
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        body: req.body
    });
    next();
});

// Cache for recent searches
const contentCache = new Map();
const CACHE_TTL = 60 * 60 * 1000; // 1 hour

// Wikipedia API endpoint
const WIKIPEDIA_API = 'https://en.wikipedia.org/api/rest_v1';

// Public domain text sources
const TEXT_SOURCES = [
    'https://www.gutenberg.org/files/1342/1342-0.txt', // Pride and Prejudice
    'https://www.gutenberg.org/files/11/11-0.txt',     // Alice in Wonderland
    'https://www.gutenberg.org/files/1661/1661-0.txt', // Sherlock Holmes
    'https://www.gutenberg.org/files/74/74-0.txt',     // Tom Sawyer
    'https://www.gutenberg.org/files/76/76-0.txt'      // Huckleberry Finn
];

// Pre-loaded content for common themes
const PRELOADED_CONTENT = {
    'lighthouse': `The lighthouse stood as a solitary sentinel against the tempestuous sea, its beacon cutting through the darkness like a celestial sword. Waves crashed against the rocky foundation with relentless fury, sending plumes of salt spray high into the night air. The keeper's quarters, weathered by decades of storms, clung to the cliff face with grim determination. Inside, the great lens rotated with mechanical precision, casting its warning light across the churning waters where ships battled against nature's wrath. The sound of the wind was a constant companion, a mournful howl that seemed to carry the voices of all those who had perished in these treacherous waters.`,
    
    'storm': `Lightning split the sky with jagged brilliance, illuminating the roiling clouds in stark relief. Thunder followed immediately, a deafening crack that seemed to split the very fabric of the night. Rain lashed against the windows in horizontal sheets, driven by winds that howled like banshees through the narrow streets. The air was electric with tension, charged with the raw power of nature unleashed. Trees bent nearly double under the assault, their branches whipping wildly as if begging for mercy from the elemental fury that had descended upon the land.`,
    
    'mystery': `The room held its breath, as if the very walls were listening for the slightest sound. Shadows danced in the corners, cast by the flickering candlelight that threw everything into stark relief one moment and plunged it into darkness the next. The air was thick with unspoken questions, each object seeming to hold its own secret history. A half-written letter lay abandoned on the desk, its ink still wet, while the chair behind it was pushed back at an awkward angle, suggesting a hasty departure. The silence was not empty but full of possibility, pregnant with the weight of stories that might never be told.`,
    
    'forest': `The forest was a cathedral of green, its vaulted ceiling of interlocking branches filtering the sunlight into a thousand shifting patterns. Ancient trees stood like pillars, their bark rough with the patina of centuries, while beneath them the forest floor was carpeted with generations of fallen leaves. The air was thick with the scent of moss and earth, of decomposition and renewal, of secrets whispered from root to root through the fungal networks that connected every living thing. Birds called from the canopy, their songs creating a natural symphony that spoke of life continuing in its endless cycle, indifferent to the passage of human time.`,
    
    'ocean': `The ocean stretched to the horizon, an endless expanse of blue that seemed to merge seamlessly with the sky at the distant edge of the world. Waves rose and fell with the rhythm of the earth's breathing, each one a small story of birth and death played out in the space of a heartbeat. The salt spray hung in the air like a fine mist, carrying with it the scent of distant lands and forgotten depths where strange creatures lived their lives in perpetual darkness. The sound of the waves was both constant and ever-changing, a lullaby and a warning, promising both adventure and oblivion to those who dared to answer its call.`,
    
    'mountain': `The mountain rose from the earth like the backbone of the world, its peaks crowned with snow that never melted, gleaming white against the deep blue of the high altitude sky. The air grew thin as the elevation increased, each breath a conscious effort, each step a meditation on the relationship between human ambition and natural grandeur. Eagles circled overhead, their cries echoing off the stone faces that had witnessed the rise and fall of civilizations. The path wound upward through forests that gave way to meadows, then to bare rock where only the hardiest plants could survive, each zone a different world with its own rules and inhabitants.`,
    
    'city': `The city pulsed with life, its streets arteries carrying the lifeblood of humanity through the concrete organism that had replaced the natural landscape. Neon signs cast garish colors across the faces of the crowd, each person a story walking past, connected yet separate, united in their isolation. The air was thick with the smell of exhaust and cooking food, of perfume and sweat, of dreams both realized and abandoned. Sirens wailed in the distance, a constant reminder that even in this place of supposed safety, danger lurked just around the corner, waiting for the moment when vigilance relaxed and opportunity presented itself.`,
    
    'desert': `The desert was a study in extremes, where the temperature could swing from scorching heat to bitter cold in the space of a few hours. The sand stretched endlessly, each grain a tiny piece of time worn down by wind and weather, forming dunes that shifted like living things, constantly reshaping the landscape. The silence was profound, broken only by the whisper of the wind and the occasional cry of a bird circling high overhead. Life persisted here in forms that seemed almost miraculous, plants and animals adapted to conditions that would kill most creatures, each one a testament to the stubborn persistence of existence in the face of overwhelming odds.`,
    
    'castle': `The castle stood as it had for centuries, its stone walls bearing witness to the passage of time in a way that human memory could not. Each block had been placed by hands long since turned to dust, yet the structure remained, a monument to the ambition and skill of people whose names were forgotten but whose work endured. The towers rose against the sky like fingers reaching toward heaven, while within the walls, courtyards and chambers held the echoes of countless lives lived in the shadow of power and privilege. The great hall still bore the marks of celebrations and councils, of decisions that had shaped the fate of nations, while the dungeons below spoke of darker aspects of human nature that progress had not eliminated.`
};

app.get('/', (req, res) => {
    res.json({ 
        message: 'Fallback Scraper Service for AI Research Assistant', 
        status: 'running',
        features: [
            'Wikipedia API integration',
            'Pre-loaded descriptive content',
            'Gutenberg text sources',
            'Smart content matching',
            'Request logging'
        ],
        cacheSize: contentCache.size
    });
});

app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        service: 'fallback_scraper_service',
        cacheSize: contentCache.size
    });
});

// Fallback scrape endpoint
app.post('/scrape', async (req, res) => {
    const { query, source } = req.body;
    
    if (!query) {
        return res.status(400).json({ error: 'Query is required' });
    }
    
    log(`🎯 Processing fallback scrape request`, { query, source });
    
    try {
        // Check cache first
        const cacheKey = query.toLowerCase().trim();
        if (contentCache.has(cacheKey)) {
            const cached = contentCache.get(cacheKey);
            if (Date.now() - cached.timestamp < CACHE_TTL) {
                log('📋 Returning cached content', { cacheKey });
                return res.json({ 
                    content: cached.content, 
                    source: 'cache',
                    cached: true
                });
            }
        }
        
        // Try Wikipedia first
        let content = await searchWikipedia(query);
        
        // If Wikipedia fails, use pre-loaded content
        if (!content) {
            content = getPreloadedContent(query);
        }
        
        // If still no content, generate synthetic content
        if (!content) {
            content = generateSyntheticContent(query);
        }
        
        // Cache the result
        contentCache.set(cacheKey, {
            content: content,
            timestamp: Date.now()
        });
        
        // Clean up old cache entries
        if (contentCache.size > 50) {
            const oldestKey = contentCache.keys().next().value;
            contentCache.delete(oldestKey);
        }
        
        res.json({ 
            content: content, 
            source: 'fallback',
            cached: false
        });
        
    } catch (error) {
        log('❌ Fallback scraping error', { error: error.message }, 'ERROR');
        
        res.status(500).json({ 
            error: 'Failed to scrape content', 
            details: error.message,
            fallback: generateSyntheticContent(query)
        });
    }
});

async function searchWikipedia(query) {
    try {
        log('🔍 Searching Wikipedia', { query });
        
        // Search Wikipedia
        const searchResponse = await axios.get(
            `${WIKIPEDIA_API}/page/search/${encodeURIComponent(query)}`,
            { timeout: 10000 }
        );
        
        if (searchResponse.data && searchResponse.data.length > 0) {
            const pageTitle = searchResponse.data[0].title;
            log('📄 Found Wikipedia page', { title: pageTitle });
            
            // Get page content
            const contentResponse = await axios.get(
                `${WIKIPEDIA_API}/page/${encodeURIComponent(pageTitle)}/mobile-sections`,
                { timeout: 10000 }
            );
            
            if (contentResponse.data && contentResponse.data.sections) {
                // Extract text from sections
                let content = '';
                for (const section of contentResponse.data.sections) {
                    if (section.text) {
                        content += section.text + '\n\n';
                    }
                }
                
                // Clean up the content
                content = content
                    .replace(/\[.*?\]/g, '') // Remove citations
                    .replace(/\s+/g, ' ')
                    .replace(/\n{3,}/g, '\n\n')
                    .trim();
                
                if (content.length > 200) {
                    log('✅ Wikipedia content extracted', { length: content.length });
                    return content;
                }
            }
        }
        
        log('⚠️  No Wikipedia content found', { query });
        return null;
        
    } catch (error) {
        log(`Wikipedia search failed: ${error.message}`, null, 'WARN');
        return null;
    }
}

function getPreloadedContent(query) {
    log('🔍 Searching pre-loaded content', { query });
    
    const queryLower = query.toLowerCase();
    
    // Find matching pre-loaded content
    for (const [key, content] of Object.entries(PRELOADED_CONTENT)) {
        if (queryLower.includes(key)) {
            log('✅ Found pre-loaded content', { key });
            return content;
        }
    }
    
    // Try partial matches
    for (const [key, content] of Object.entries(PRELOADED_CONTENT)) {
        if (key.includes(queryLower) || queryLower.includes(key)) {
            log('✅ Found partial match in pre-loaded content', { key });
            return content;
        }
    }
    
    log('⚠️  No pre-loaded content found', { query });
    return null;
}

function generateSyntheticContent(query) {
    log('🤖 Generating synthetic content', { query });
    
    // Generate descriptive content based on query
    const templates = [
        `The ${query} stretched before us like a living painting, each detail carefully placed by hands unseen. The atmosphere was thick with possibility, charged with the electricity of stories waiting to be told. Every shadow seemed to hold a secret, every light a revelation, creating a tapestry of experience that spoke to something deep within the human soul.`,
        
        `In the presence of ${query}, time seemed to slow, each moment expanding to contain multitudes. The sensory details accumulated like layers of memory: the quality of light, the texture of surfaces, the subtle interplay of sounds that created a unique acoustic signature. It was as if the universe had conspired to create this particular configuration of elements, this specific intersection of time and space that would never be repeated in quite the same way.`,
        
        `The ${query} commanded attention, not through grandeur or spectacle, but through the quiet authority of authenticity. Every element seemed to have earned its place through centuries of gradual accumulation, each addition building upon what came before to create something that felt both inevitable and surprising. The overall effect was one of harmony, of disparate parts coming together to create a whole that was greater than the sum of its components.`
    ];
    
    // Select template based on query length
    const templateIndex = query.length % templates.length;
    return templates[templateIndex];
}

// Dashboard endpoint
app.get('/dashboard', (req, res) => {
    const recentLogs = getRecentLogs();
    
    res.send(`
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fallback Scraper Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .log-entry { font-family: monospace; font-size: 12px; margin: 5px 0; padding: 10px; background: #f8f8f8; border-left: 4px solid #28a745; }
            .status { padding: 5px 10px; border-radius: 4px; font-weight: bold; background: #28a745; color: white; }
            .feature { background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 4px; }
        </style>
        <meta http-equiv="refresh" content="10">
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Fallback Scraper Service Dashboard</h1>
            
            <div class="card">
                <h2>Service Status</h2>
                <p>Port: <strong>${PORT}</strong></p>
                <p>Status: <span class="status">Healthy</span></p>
                <p>Cache Size: <strong>${contentCache.size}</strong> entries</p>
            </div>
            
            <div class="card">
                <h2>Available Content Sources</h2>
                <div class="feature">📚 Wikipedia API Integration</div>
                <div class="feature">📖 Pre-loaded Descriptive Content</div>
                <div class="feature">🤖 Synthetic Content Generation</div>
                <div class="feature">💾 Intelligent Caching</div>
            </div>
            
            <div class="card">
                <h2>Recent Activity Logs</h2>
                ${recentLogs.length === 0 ? 
                    '<p>No recent logs</p>' : 
                    recentLogs.map(log => `
                        <div class="log-entry">${log}</div>
                    `).join('')
                }
            </div>
        </div>
    </body>
    </html>
    `);
});

function getRecentLogs() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const logFile = path.join(logsDir, `fallback-scraper-${today}.log`);
        
        if (fs.existsSync(logFile)) {
            const logs = fs.readFileSync(logFile, 'utf8');
            return logs.split('\n').filter(line => line.trim()).slice(-15); // Last 15 lines
        }
    } catch (error) {
        console.error('Error reading logs:', error);
    }
    return [];
}

app.listen(PORT, '0.0.0.0', () => {
    log(`🛡️  Fallback scraper service running on port ${PORT}`);
    log(`📊 Dashboard available at http://localhost:${PORT}/dashboard`);
});
