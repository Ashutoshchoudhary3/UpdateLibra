const express = require('express');
const cors = require('cors');
const { chromium } = require('playwright');
const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3002; // Different port from original

// Create logs and screenshots directories
const logsDir = path.join(__dirname, 'logs');
const screenshotsDir = path.join(__dirname, 'screenshots');
if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir);
if (!fs.existsSync(screenshotsDir)) fs.mkdirSync(screenshotsDir);

// Enhanced logging function
function log(message, data = null, type = 'INFO') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${type}] ${message}${data ? ' ' + JSON.stringify(data) : ''}\n`;
    
    console.log(logEntry.trim());
    
    // Append to log file
    const logFile = path.join(logsDir, `scraper-${new Date().toISOString().split('T')[0]}.log`);
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

// Rate limiting
const requestQueue = [];
let isProcessing = false;

// Cache for recent searches
const contentCache = new Map();
const CACHE_TTL = 60 * 60 * 1000; // 1 hour

// Active scraping sessions tracking
const activeSessions = new Map();

app.get('/', (req, res) => {
    res.json({ 
        message: 'Enhanced Scraper Service for AI Research Assistant', 
        status: 'running',
        features: [
            'Browser screenshots',
            'Detailed logging',
            'Session tracking',
            'Request source identification'
        ],
        activeSessions: activeSessions.size
    });
});

// Dashboard endpoint to view scraper activity
app.get('/dashboard', (req, res) => {
    const recentLogs = getRecentLogs();
    const screenshots = getAvailableScreenshots();
    
    res.send(`
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scraper Service Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .log-entry { font-family: monospace; font-size: 12px; margin: 5px 0; padding: 10px; background: #f8f8f8; border-left: 4px solid #007bff; }
            .screenshot { display: inline-block; margin: 10px; border: 1px solid #ddd; border-radius: 4px; }
            .screenshot img { max-width: 300px; height: auto; }
            .status { padding: 5px 10px; border-radius: 4px; font-weight: bold; }
            .status.active { background: #28a745; color: white; }
            .status.idle { background: #6c757d; color: white; }
            .session-info { background: #e3f2fd; padding: 10px; margin: 10px 0; border-radius: 4px; }
        </style>
        <meta http-equiv="refresh" content="10">
    </head>
    <body>
        <div class="container">
            <h1>🕷️ Scraper Service Dashboard</h1>
            
            <div class="card">
                <h2>Service Status</h2>
                <p>Port: <strong>${PORT}</strong></p>
                <p>Active Sessions: <span class="status ${activeSessions.size > 0 ? 'active' : 'idle'}">${activeSessions.size}</span></p>
                <p>Cache Size: <strong>${contentCache.size}</strong> entries</p>
            </div>
            
            <div class="card">
                <h2>Active Scraping Sessions</h2>
                ${activeSessions.size === 0 ? 
                    '<p>No active sessions</p>' : 
                    Array.from(activeSessions.entries()).map(([id, session]) => `
                        <div class="session-info">
                            <strong>Session ID:</strong> ${id}<br>
                            <strong>Query:</strong> ${session.query}<br>
                            <strong>Source:</strong> ${session.source || 'Unknown'}<br>
                            <strong>Started:</strong> ${new Date(session.startTime).toLocaleString()}<br>
                            <strong>Status:</strong> ${session.status}
                        </div>
                    `).join('')
                }
            </div>
            
            <div class="card">
                <h2>Recent Screenshots</h2>
                ${screenshots.length === 0 ? 
                    '<p>No screenshots available</p>' : 
                    screenshots.map(screenshot => `
                        <div class="screenshot">
                            <img src="/screenshots/${screenshot}" alt="${screenshot}">
                            <br><small>${screenshot}</small>
                        </div>
                    `).join('')
                }
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

// Serve screenshots
app.use('/screenshots', express.static(screenshotsDir));

// Enhanced scrape endpoint with source tracking
app.post('/scrape', async (req, res) => {
    const { query, source } = req.body;
    const sessionId = generateSessionId();
    
    if (!query) {
        return res.status(400).json({ error: 'Query is required' });
    }
    
    // Track session
    activeSessions.set(sessionId, {
        query,
        source: source || 'Unknown',
        startTime: Date.now(),
        status: 'Starting'
    });
    
    log(`🎯 New scraping session started`, { sessionId, query, source });
    
    try {
        activeSessions.get(sessionId).status = 'Processing';
        
        // Check cache first
        const cacheKey = query.toLowerCase().trim();
        if (contentCache.has(cacheKey)) {
            const cached = contentCache.get(cacheKey);
            if (Date.now() - cached.timestamp < CACHE_TTL) {
                log('📋 Returning cached content', { sessionId, cacheKey });
                activeSessions.delete(sessionId);
                return res.json({ 
                    content: cached.content, 
                    source: 'cache',
                    sessionId,
                    cached: true
                });
            }
        }
        
        // Process scraping request
        const result = await processScrapingRequest(query, sessionId, source);
        
        // Cache the result
        contentCache.set(cacheKey, {
            content: result,
            timestamp: Date.now()
        });
        
        // Clean up old cache entries
        if (contentCache.size > 100) {
            const oldestKey = contentCache.keys().next().value;
            contentCache.delete(oldestKey);
        }
        
        activeSessions.delete(sessionId);
        
        res.json({ 
            content: result, 
            source: 'scraped',
            sessionId,
            cached: false
        });
        
    } catch (error) {
        log('❌ Scraping error', { sessionId, error: error.message }, 'ERROR');
        activeSessions.delete(sessionId);
        
        res.status(500).json({ 
            error: 'Failed to scrape content', 
            details: error.message,
            fallback: generateFallbackContent(query),
            sessionId
        });
    }
});

async function processScrapingRequest(query, sessionId, source) {
    let browser;
    
    try {
        activeSessions.get(sessionId).status = 'Launching browser';
        log('🚀 Launching browser', { sessionId });
        
        // Launch browser with screenshot capabilities
        browser = await chromium.launch({
            headless: true, // Set to true for server environments
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            viewport: { width: 1920, height: 1080 },
            recordVideo: {
                dir: path.join(__dirname, 'videos'),
                size: { width: 1920, height: 1080 }
            }
        });
        
        const page = await context.newPage();
        
        // Set up page event logging
        page.on('console', msg => log(`🖥️  Browser console: ${msg.text()}`, { sessionId }));
        page.on('pageerror', error => log(`❌ Browser page error: ${error.message}`, { sessionId }, 'ERROR'));
        
        activeSessions.get(sessionId).status = 'Searching content';
        
        // Search for content using multiple sources
        const searchResults = await Promise.allSettled([
            searchWithGoogle(query, page, sessionId),
            searchWithBing(query, page, sessionId),
            searchWithDuckDuckGo(query, page, sessionId)
        ]);
        
        // Extract content from successful searches
        let allContent = [];
        for (const result of searchResults) {
            if (result.status === 'fulfilled' && result.value) {
                allContent.push(result.value);
            }
        }
        
        if (allContent.length === 0) {
            throw new Error('No content found from any source');
        }
        
        // Combine and clean content
        const combinedContent = combineAndCleanContent(allContent, query);
        
        activeSessions.get(sessionId).status = 'Completed';
        log('✅ Scraping completed successfully', { sessionId });
        
        return combinedContent;
        
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

async function searchWithGoogle(query, page, sessionId) {
    try {
        activeSessions.get(sessionId).status = 'Searching Google';
        log('🔍 Searching Google', { sessionId, query });
        
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}&num=10`;
        await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 10000 });
        
        // Take screenshot
        await takeScreenshot(page, sessionId, 'google_search');
        
        // Wait for results
        await page.waitForSelector('div[data-ved]', { timeout: 5000 }).catch(() => {});
        
        // Extract search result URLs
        const urls = await page.evaluate(() => {
            const links = Array.from(document.querySelectorAll('a[href^="http"]'));
            return links
                .map(link => link.href)
                .filter(href => !href.includes('google.com') && !href.includes('youtube.com'))
                .slice(0, 3); // Top 3 results
        });
        
        log('🔗 Found URLs from Google', { sessionId, urls });
        
        // Extract content from each URL
        const contents = [];
        for (const url of urls) {
            try {
                const content = await extractContentFromUrl(url, page, sessionId);
                if (content && content.length > 100) {
                    contents.push(content);
                }
            } catch (err) {
                log(`Failed to extract from ${url}: ${err.message}`, { sessionId }, 'WARN');
            }
        }
        
        return contents.join('\n\n');
        
    } catch (error) {
        log(`Google search failed: ${error.message}`, { sessionId }, 'ERROR');
        return null;
    }
}

async function searchWithBing(query, page, sessionId) {
    try {
        activeSessions.get(sessionId).status = 'Searching Bing';
        log('🔍 Searching Bing', { sessionId, query });
        
        const searchUrl = `https://www.bing.com/search?q=${encodeURIComponent(query)}&count=10`;
        await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 10000 });
        
        // Take screenshot
        await takeScreenshot(page, sessionId, 'bing_search');
        
        // Extract URLs
        const urls = await page.evaluate(() => {
            const links = Array.from(document.querySelectorAll('a[href^="http"]'));
            return links
                .map(link => link.href)
                .filter(href => !href.includes('bing.com') && !href.includes('microsoft.com'))
                .slice(0, 2);
        });
        
        log('🔗 Found URLs from Bing', { sessionId, urls });
        
        const contents = [];
        for (const url of urls) {
            try {
                const content = await extractContentFromUrl(url, page, sessionId);
                if (content && content.length > 100) {
                    contents.push(content);
                }
            } catch (err) {
                log(`Failed to extract from ${url}: ${err.message}`, { sessionId }, 'WARN');
            }
        }
        
        return contents.join('\n\n');
        
    } catch (error) {
        log(`Bing search failed: ${error.message}`, { sessionId }, 'ERROR');
        return null;
    }
}

async function searchWithDuckDuckGo(query, page, sessionId) {
    try {
        activeSessions.get(sessionId).status = 'Searching DuckDuckGo';
        log('🔍 Searching DuckDuckGo', { sessionId, query });
        
        const searchUrl = `https://duckduckgo.com/?q=${encodeURIComponent(query)}&kl=us-en`;
        await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 10000 });
        
        // Take screenshot
        await takeScreenshot(page, sessionId, 'duckduckgo_search');
        
        // Wait for results and click on first result
        await page.waitForSelector('[data-result]', { timeout: 5000 }).catch(() => {});
        
        const urls = await page.evaluate(() => {
            const results = Array.from(document.querySelectorAll('[data-result] a'));
            return results
                .map(link => link.href)
                .filter(href => href.startsWith('http') && !href.includes('duckduckgo.com'))
                .slice(0, 2);
        });
        
        log('🔗 Found URLs from DuckDuckGo', { sessionId, urls });
        
        const contents = [];
        for (const url of urls) {
            try {
                const content = await extractContentFromUrl(url, page, sessionId);
                if (content && content.length > 100) {
                    contents.push(content);
                }
            } catch (err) {
                log(`Failed to extract from ${url}: ${err.message}`, { sessionId }, 'WARN');
            }
        }
        
        return contents.join('\n\n');
        
    } catch (error) {
        log(`DuckDuckGo search failed: ${error.message}`, { sessionId }, 'ERROR');
        return null;
    }
}

async function extractContentFromUrl(url, page, sessionId) {
    try {
        activeSessions.get(sessionId).status = `Extracting from ${url}`;
        log(`📄 Extracting content from URL`, { sessionId, url });
        
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
        
        // Take screenshot of the page
        const urlDomain = new URL(url).hostname;
        await takeScreenshot(page, sessionId, `content_${urlDomain}`);
        
        // Wait a bit for dynamic content
        await page.waitForTimeout(2000);
        
        // Extract main content
        const content = await page.evaluate(() => {
            // Remove unwanted elements
            const unwanted = ['script', 'style', 'nav', 'header', 'footer', 'aside', '.advertisement', '.ads'];
            unwanted.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => el.remove());
            });
            
            // Try to find main content area
            const contentSelectors = [
                'main',
                'article',
                '.content',
                '.main-content',
                '#content',
                '.post-content',
                '.entry-content',
                '.article-content'
            ];
            
            let contentElement = null;
            for (const selector of contentSelectors) {
                contentElement = document.querySelector(selector);
                if (contentElement) break;
            }
            
            // Fallback to body if no specific content area found
            if (!contentElement) {
                contentElement = document.body;
            }
            
            // Extract text content
            const textContent = contentElement.innerText || contentElement.textContent;
            
            // Clean up the text
            return textContent
                .replace(/\s+/g, ' ')
                .replace(/\n{3,}/g, '\n\n')
                .trim();
        });
        
        log(`✅ Content extracted successfully`, { sessionId, url, contentLength: content.length });
        
        return content;
        
    } catch (error) {
        log(`Content extraction failed for ${url}: ${error.message}`, { sessionId }, 'ERROR');
        return null;
    }
}

async function takeScreenshot(page, sessionId, name) {
    try {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `${sessionId}_${name}_${timestamp}.png`;
        const filepath = path.join(screenshotsDir, filename);
        
        await page.screenshot({ 
            path: filepath, 
            fullPage: true,
            timeout: 5000
        });
        
        log(`📸 Screenshot taken`, { sessionId, filename, name });
        
    } catch (error) {
        log(`Failed to take screenshot: ${error.message}`, { sessionId }, 'WARN');
    }
}

function combineAndCleanContent(contentArray, query) {
    // Combine all content
    let combined = contentArray.join('\n\n');
    
    // Remove excessive whitespace
    combined = combined.replace(/\s+/g, ' ');
    combined = combined.replace(/\n{3,}/g, '\n\n');
    
    // Extract relevant paragraphs
    const sentences = combined.split(/[.!?]+/);
    const relevantSentences = sentences.filter(sentence => 
        sentence.toLowerCase().includes(query.toLowerCase()) ||
        isRelevantContent(sentence, query)
    );
    
    // If we have relevant content, use it
    if (relevantSentences.length > 3) {
        return relevantSentences.slice(0, 10).join('. ').trim() + '.';
    }
    
    // Otherwise, use the first few paragraphs
    const paragraphs = combined.split('\n\n').filter(p => p.trim().length > 50);
    return paragraphs.slice(0, 5).join('\n\n').trim();
}

function isRelevantContent(sentence, query) {
    const queryWords = query.toLowerCase().split(' ');
    const sentenceLower = sentence.toLowerCase();
    
    // Check if any query words appear in the sentence
    return queryWords.some(word => 
        word.length > 3 && sentenceLower.includes(word)
    );
}

function generateFallbackContent(query) {
    // Generate descriptive fallback content based on query
    return `Descriptive content related to: ${query}. This passage would typically contain rich, human-written descriptions that capture the essence and atmosphere of the scene, providing authentic details that can be woven into the narrative. The content would include sensory details, emotional resonance, and specific observations that bring the scene to life in a way that only human experience can capture.`;
}

function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function getRecentLogs() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const logFile = path.join(logsDir, `scraper-${today}.log`);
        
        if (fs.existsSync(logFile)) {
            const logs = fs.readFileSync(logFile, 'utf8');
            return logs.split('\n').filter(line => line.trim()).slice(-20); // Last 20 lines
        }
    } catch (error) {
        console.error('Error reading logs:', error);
    }
    return [];
}

function getAvailableScreenshots() {
    try {
        const files = fs.readdirSync(screenshotsDir);
        return files.filter(file => file.endsWith('.png')).slice(-10); // Last 10 screenshots
    } catch (error) {
        console.error('Error reading screenshots:', error);
    }
    return [];
}

app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        service: 'enhanced_scraper_service',
        activeSessions: activeSessions.size,
        cacheSize: contentCache.size,
        screenshots: getAvailableScreenshots().length
    });
});

// Cleanup old screenshots periodically (keep last 50)
setInterval(() => {
    try {
        const files = fs.readdirSync(screenshotsDir);
        if (files.length > 50) {
            const sortedFiles = files
                .map(file => ({
                    name: file,
                    time: fs.statSync(path.join(screenshotsDir, file)).mtime
                }))
                .sort((a, b) => a.time - b.time);
            
            const filesToDelete = sortedFiles.slice(0, files.length - 50);
            filesToDelete.forEach(file => {
                fs.unlinkSync(path.join(screenshotsDir, file.name));
                log(`🗑️  Deleted old screenshot: ${file.name}`);
            });
        }
    } catch (error) {
        log(`Error cleaning up screenshots: ${error.message}`, null, 'ERROR');
    }
}, 60 * 60 * 1000); // Run every hour

app.listen(PORT, '0.0.0.0', () => {
    log(`🌐 Enhanced scraper service running on port ${PORT}`);
    log(`📊 Dashboard available at http://localhost:${PORT}/dashboard`);
});
