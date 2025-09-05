



const express = require('express');
const cors = require('cors');
const { chromium } = require('playwright');
const cheerio = require('cheerio');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Rate limiting
const requestQueue = [];
let isProcessing = false;

// Cache for recent searches
const contentCache = new Map();
const CACHE_TTL = 60 * 60 * 1000; // 1 hour

app.get('/', (req, res) => {
    res.json({ message: 'Scraper Service for AI Research Assistant', status: 'running' });
});

app.post('/scrape', async (req, res) => {
    const { query } = req.body;
    
    if (!query) {
        return res.status(400).json({ error: 'Query is required' });
    }
    
    try {
        console.log(`🔍 Scraping content for query: "${query}"`);
        
        // Check cache first
        const cacheKey = query.toLowerCase().trim();
        if (contentCache.has(cacheKey)) {
            const cached = contentCache.get(cacheKey);
            if (Date.now() - cached.timestamp < CACHE_TTL) {
                console.log('📋 Returning cached content');
                return res.json({ content: cached.content, source: 'cache' });
            }
        }
        
        // Add to queue
        const result = await processScrapingRequest(query);
        
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
        
        res.json({ content: result, source: 'scraped' });
        
    } catch (error) {
        console.error('❌ Scraping error:', error);
        res.status(500).json({ 
            error: 'Failed to scrape content', 
            details: error.message,
            fallback: generateFallbackContent(query)
        });
    }
});

async function processScrapingRequest(query) {
    let browser;
    
    try {
        // Launch browser
        browser = await chromium.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        
        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        });
        
        const page = await context.newPage();
        
        // Set viewport
        await page.setViewportSize({ width: 1920, height: 1080 });
        
        // Search for content using multiple sources
        const searchResults = await Promise.allSettled([
            searchWithGoogle(query, page),
            searchWithBing(query, page),
            searchWithDuckDuckGo(query, page)
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
        
        return combinedContent;
        
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

async function searchWithGoogle(query, page) {
    try {
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}&num=10`;
        await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 10000 });
        
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
        
        // Extract content from each URL
        const contents = [];
        for (const url of urls) {
            try {
                const content = await extractContentFromUrl(url, page);
                if (content && content.length > 100) {
                    contents.push(content);
                }
            } catch (err) {
                console.log(`Failed to extract from ${url}: ${err.message}`);
            }
        }
        
        return contents.join('\n\n');
        
    } catch (error) {
        console.log(`Google search failed: ${error.message}`);
        return null;
    }
}

async function searchWithBing(query, page) {
    try {
        const searchUrl = `https://www.bing.com/search?q=${encodeURIComponent(query)}&count=10`;
        await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 10000 });
        
        // Extract URLs
        const urls = await page.evaluate(() => {
            const links = Array.from(document.querySelectorAll('a[href^="http"]'));
            return links
                .map(link => link.href)
                .filter(href => !href.includes('bing.com') && !href.includes('microsoft.com'))
                .slice(0, 2);
        });
        
        const contents = [];
        for (const url of urls) {
            try {
                const content = await extractContentFromUrl(url, page);
                if (content && content.length > 100) {
                    contents.push(content);
                }
            } catch (err) {
                console.log(`Failed to extract from ${url}: ${err.message}`);
            }
        }
        
        return contents.join('\n\n');
        
    } catch (error) {
        console.log(`Bing search failed: ${error.message}`);
        return null;
    }
}

async function searchWithDuckDuckGo(query, page) {
    try {
        const searchUrl = `https://duckduckgo.com/?q=${encodeURIComponent(query)}&kl=us-en`;
        await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 10000 });
        
        // Wait for results and click on first result
        await page.waitForSelector('[data-result]', { timeout: 5000 }).catch(() => {});
        
        const urls = await page.evaluate(() => {
            const results = Array.from(document.querySelectorAll('[data-result] a'));
            return results
                .map(link => link.href)
                .filter(href => href.startsWith('http') && !href.includes('duckduckgo.com'))
                .slice(0, 2);
        });
        
        const contents = [];
        for (const url of urls) {
            try {
                const content = await extractContentFromUrl(url, page);
                if (content && content.length > 100) {
                    contents.push(content);
                }
            } catch (err) {
                console.log(`Failed to extract from ${url}: ${err.message}`);
            }
        }
        
        return contents.join('\n\n');
        
    } catch (error) {
        console.log(`DuckDuckGo search failed: ${error.message}`);
        return null;
    }
}

async function extractContentFromUrl(url, page) {
    try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
        
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
        
        return content;
        
    } catch (error) {
        console.log(`Content extraction failed for ${url}: ${error.message}`);
        return null;
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

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'scraper_service' });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`🌐 Scraper service running on port ${PORT}`);
});



