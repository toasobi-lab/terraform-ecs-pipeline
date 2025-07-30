#!/usr/bin/env python3
"""
ECS Playground - Simple Flask application for deployment demonstration.
"""

import os
import json
import random
import base64
import math
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 5000))
APP_ENV = os.environ.get('APP_ENV', 'production')
VERSION = os.environ.get('APP_VERSION', '2.0.0')


@app.route('/')
def home():
    """Interactive home page with web UI."""
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ECS Playground - Interactive Demo</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                padding: 20px;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 20px; 
                padding: 30px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            }
            h1 { 
                color: #333; 
                text-align: center; 
                margin-bottom: 20px; 
                font-size: 2.5em; 
            }
            .subtitle { 
                text-align: center; 
                color: #666; 
                margin-bottom: 30px; 
                font-size: 1.2em; 
            }
            .status-bar {
                background: #e8f5e8; 
                color: #2d5a2d; 
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                font-weight: bold; 
            }
            .feature-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px; 
            }
            .feature-card { 
                background: #f8f9fa; 
                border-radius: 15px; 
                padding: 25px; 
                border-left: 5px solid #007bff;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }
            .feature-card h3 { 
                color: #333; 
                margin-bottom: 15px; 
                font-size: 1.3em;
                display: flex;
                align-items: center;
            }
            .feature-card .icon {
                font-size: 1.5em;
                margin-right: 10px;
            }
            .input-group {
                margin: 15px 0;
            }
            .input-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #555;
            }
            .input-group input, .input-group select, .input-group textarea {
                width: 100%;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s ease;
            }
            .input-group input:focus, .input-group select:focus, .input-group textarea:focus {
                outline: none;
                border-color: #007bff;
            }
            button {
                background: #007bff;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: background 0.3s ease;
                width: 100%;
                margin-top: 10px;
            }
            button:hover {
                background: #0056b3;
            }
            .result {
                margin-top: 15px;
                padding: 15px;
                background: #e3f2fd;
                border-radius: 8px;
                border-left: 4px solid #2196f3;
                display: none;
            }
            .result.show {
                display: block;
            }
            .result pre {
                margin: 0;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            .info-section {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .quote-display {
                background: #f8f9fa;
                border-left: 4px solid #28a745;
                padding: 20px;
                border-radius: 8px;
                margin-top: 15px;
                font-style: italic;
            }
            .quote-text {
                font-size: 1.1em;
                margin-bottom: 10px;
            }
            .quote-author {
                text-align: right;
                font-weight: bold;
                color: #666;
            }
            @media (max-width: 768px) {
                .container { padding: 15px; }
                h1 { font-size: 2em; }
                .feature-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 ECS Playground</h1>
            <div class="subtitle">Interactive Demo - AWS Fargate Container Application</div>
            
            <div class="status-bar">
                ✅ Running on AWS Fargate in Tokyo Region | Version {{ version }} | Environment: {{ environment }}
                </div>

            <div class="info-section">
                <strong>🏗️ User Flow:</strong> User → CloudFront → ALB → Fargate (You are here!) <br>
                <strong>⚙️ Infrastructure Flow:</strong> S3 Upload → CodeBuild → ECR Push → Manual Approval → ECS Deploy → Auto-scaling <br>
                <strong>🌏 Region:</strong> ap-northeast-1 | 
                <strong>🐍 Tech:</strong> Python 3.12 + Flask + Docker
                </div>

            <div class="feature-grid">
                <!-- Currency Exchange -->
                <div class="feature-card">
                    <h3><span class="icon">💱</span>Currency Exchange</h3>
                    <div class="input-group">
                        <label>From Currency:</label>
                        <select id="fromCurrency">
                            <option value="USD">USD - US Dollar</option>
                            <option value="EUR">EUR - Euro</option>
                            <option value="GBP">GBP - British Pound</option>
                            <option value="JPY">JPY - Japanese Yen</option>
                            <option value="CNY">CNY - Chinese Yuan</option>
                            <option value="KRW">KRW - Korean Won</option>
                        </select>
                </div>
                    <div class="input-group">
                        <label>To Currency:</label>
                        <select id="toCurrency">
                            <option value="EUR">EUR - Euro</option>
                            <option value="USD">USD - US Dollar</option>
                            <option value="GBP">GBP - British Pound</option>
                            <option value="JPY">JPY - Japanese Yen</option>
                            <option value="CNY">CNY - Chinese Yuan</option>
                            <option value="KRW">KRW - Korean Won</option>
                        </select>
                </div>
                    <div class="input-group">
                        <label>Amount:</label>
                        <input type="number" id="amount" value="100" min="0" step="0.01">
                </div>
                    <button onclick="convertCurrency()">Convert Currency</button>
                    <div id="currencyResult" class="result"></div>
            </div>

                <!-- Calculator -->
                <div class="feature-card">
                    <h3><span class="icon">🧮</span>Calculator</h3>
                    <div class="input-group">
                        <label>Operation:</label>
                        <select id="operation">
                            <option value="add">Add (+)</option>
                            <option value="subtract">Subtract (-)</option>
                            <option value="multiply">Multiply (×)</option>
                            <option value="divide">Divide (÷)</option>
                            <option value="power">Power (^)</option>
                            <option value="sqrt">Square Root (√)</option>
                            <option value="log">Natural Log (ln)</option>
                        </select>
            </div>
                    <div class="input-group">
                        <label>Number A:</label>
                        <input type="number" id="numberA" value="10" step="any">
                 </div>
                    <div class="input-group">
                        <label>Number B:</label>
                        <input type="number" id="numberB" value="5" step="any">
                 </div>
                    <button onclick="calculate()">Calculate</button>
                    <div id="calcResult" class="result"></div>
                 </div>

                <!-- Text Utilities -->
                <div class="feature-card">
                    <h3><span class="icon">📝</span>Text Utilities</h3>
                    <div class="input-group">
                        <label>Enter your text:</label>
                        <textarea id="textInput" rows="4" placeholder="Type or paste your text here...">Hello from AWS Fargate in Tokyo!</textarea>
                 </div>
                    <button onclick="analyzeText()">Analyze Text</button>
                    <div id="textResult" class="result"></div>
                 </div>
                 
                <!-- Random Quote -->
                <div class="feature-card">
                    <h3><span class="icon">💬</span>Inspirational Quotes</h3>
                    <p>Get motivated with random quotes from great minds!</p>
                    <button onclick="getRandomQuote()">Get Random Quote</button>
                    <div id="quoteDisplay" class="quote-display" style="display: none;">
                        <div id="quoteText" class="quote-text"></div>
                        <div id="quoteAuthor" class="quote-author"></div>
                 </div>
                 </div>

                <!-- Base64 Encoder -->
                <div class="feature-card">
                    <h3><span class="icon">🔐</span>Base64 Encoder/Decoder</h3>
                    <div class="input-group">
                        <label>Operation:</label>
                        <select id="encodeOperation">
                            <option value="encode">Encode to Base64</option>
                            <option value="decode">Decode from Base64</option>
                        </select>
                 </div>
                    <div class="input-group">
                        <label>Text:</label>
                        <textarea id="encodeText" rows="3" placeholder="Enter text to encode/decode...">Hello AWS Fargate!</textarea>
                 </div>
                    <button onclick="processBase64()">Process</button>
                    <div id="encodeResult" class="result"></div>
             </div>

                <!-- API Information -->
                <div class="feature-card">
                    <h3><span class="icon">🔗</span>API Endpoints</h3>
                    <p>This app also provides JSON API endpoints:</p>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li><strong>GET /api/info</strong> - API information</li>
                        <li><strong>GET /api/currency</strong> - Exchange rates</li>
                        <li><strong>GET /api/quote</strong> - Random quote</li>
                        <li><strong>POST /api/calculator</strong> - Calculator</li>
                        <li><strong>POST /api/text-utils</strong> - Text analysis</li>
                        <li><strong>POST /api/encoder</strong> - Base64 operations</li>
                    </ul>
                    <button onclick="window.open('/api/info', '_blank')">View API Info</button>
                </div>
            </div>
        </div>

        <script>
            async function convertCurrency() {
                const from = document.getElementById('fromCurrency').value;
                const to = document.getElementById('toCurrency').value;
                const amount = document.getElementById('amount').value;
                
                try {
                    const response = await fetch(`/api/currency/convert?from=${from}&to=${to}&amount=${amount}`);
                    const data = await response.json();
                    
                    const resultDiv = document.getElementById('currencyResult');
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <strong>Conversion Result:</strong><br>
                            ${data.from.amount} ${data.from.currency} = 
                            <strong>${data.to.amount} ${data.to.currency}</strong><br>
                            <small>Exchange rate: 1 ${data.from.currency} = ${data.rate} ${data.to.currency}</small>
                        `;
                    } else {
                        resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                    }
                    resultDiv.classList.add('show');
                } catch (error) {
                    document.getElementById('currencyResult').innerHTML = `<strong>Error:</strong> ${error.message}`;
                    document.getElementById('currencyResult').classList.add('show');
                }
            }

            async function calculate() {
                const operation = document.getElementById('operation').value;
                const a = parseFloat(document.getElementById('numberA').value);
                const b = parseFloat(document.getElementById('numberB').value);
                
                try {
                    const response = await fetch('/api/calculator', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ operation, a, b })
                    });
                    const data = await response.json();
                    
                    const resultDiv = document.getElementById('calcResult');
                    if (response.ok) {
                        const inputs = operation === 'sqrt' || operation === 'log' ? 
                            `${operation}(${a})` : `${a} ${operation} ${b}`;
                        resultDiv.innerHTML = `
                            <strong>Calculation:</strong><br>
                            ${inputs} = <strong>${data.result}</strong>
                        `;
                    } else {
                        resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                    }
                    resultDiv.classList.add('show');
                } catch (error) {
                    document.getElementById('calcResult').innerHTML = `<strong>Error:</strong> ${error.message}`;
                    document.getElementById('calcResult').classList.add('show');
                }
            }

            async function analyzeText() {
                const text = document.getElementById('textInput').value;
                
                try {
                    const response = await fetch('/api/text-utils', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text })
                    });
                    const data = await response.json();
                    
                    const resultDiv = document.getElementById('textResult');
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <strong>Text Analysis:</strong><br>
                            • Characters: ${data.stats.characters}<br>
                            • Characters (no spaces): ${data.stats.characters_no_spaces}<br>
                            • Words: ${data.stats.words}<br>
                            • Lines: ${data.stats.lines}<br>
                            • Sentences: ${data.stats.sentences}<br><br>
                            <strong>Transformations:</strong><br>
                            • Uppercase: ${data.transformations.uppercase}<br>
                            • Lowercase: ${data.transformations.lowercase}<br>
                            • Title Case: ${data.transformations.title_case}<br>
                            • Reversed: ${data.transformations.reversed}
                        `;
                    } else {
                        resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                    }
                    resultDiv.classList.add('show');
                } catch (error) {
                    document.getElementById('textResult').innerHTML = `<strong>Error:</strong> ${error.message}`;
                    document.getElementById('textResult').classList.add('show');
                }
            }

            async function getRandomQuote() {
                try {
                    const response = await fetch('/api/quote');
                    const data = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('quoteText').textContent = `"${data.quote.text}"`;
                        document.getElementById('quoteAuthor').textContent = `— ${data.quote.author}`;
                        document.getElementById('quoteDisplay').style.display = 'block';
                    }
                } catch (error) {
                    console.error('Error fetching quote:', error);
                }
            }

            async function processBase64() {
                const operation = document.getElementById('encodeOperation').value;
                const text = document.getElementById('encodeText').value;
                
                try {
                    const response = await fetch('/api/encoder', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ operation, text })
                    });
                    const data = await response.json();
                    
                    const resultDiv = document.getElementById('encodeResult');
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <strong>${operation === 'encode' ? 'Encoded' : 'Decoded'} Result:</strong><br>
                            <pre>${data.result}</pre>
                        `;
                    } else {
                        resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                    }
                    resultDiv.classList.add('show');
                } catch (error) {
                    document.getElementById('encodeResult').innerHTML = `<strong>Error:</strong> ${error.message}`;
                    document.getElementById('encodeResult').classList.add('show');
                }
            }

            // Update operation labels based on selection
            document.getElementById('operation').addEventListener('change', function() {
                const operation = this.value;
                const numberBDiv = document.getElementById('numberB').parentElement;
                if (operation === 'sqrt' || operation === 'log') {
                    numberBDiv.style.display = 'none';
                } else {
                    numberBDiv.style.display = 'block';
                }
            });

            // Load a quote on page load
            window.addEventListener('load', getRandomQuote);
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, version=VERSION, environment=APP_ENV)


@app.route('/health')
def health_check():
    """Health check endpoint for ALB target group."""
    return jsonify({
        'status': 'healthy',
        'service': 'ecs-playground',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': VERSION,
        'environment': APP_ENV,
        'region': 'ap-northeast-1'
    }), 200


@app.route('/api/info')
def api_info():
    """API info endpoint."""
    return jsonify({
        'api_version': 'v1',
        'service': 'ecs-playground',
        'region': 'Tokyo (ap-northeast-1)',
        'user_flow': 'User → CloudFront → ALB → Fargate',
        'infrastructure_flow': 'S3 Upload → CodeBuild → ECR Push → Manual Approval → ECS Deploy → Auto-scaling',
        'features': [
            'Multi-AZ high availability',
            'Auto-scaling Fargate containers',
            'CloudFront global CDN',
            'CI/CD with manual approval',
            'Private subnet security'
        ],
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


@app.route('/api/echo', methods=['POST'])
def echo():
    """Echo endpoint that returns the request body."""
    try:
        data = request.get_json() or {}
        return jsonify({
            'echo': data,
            'method': request.method,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'region': 'ap-northeast-1',
            'service': 'ecs-playground'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 400


# Interactive Features

@app.route('/api/currency')
def currency_exchange():
    """Simple currency exchange rates (mock data for demo)."""
    # Current exchange rates relative to USD (July 2025 rates)
    rates = {
        'USD': 1.0,
        'EUR': 0.8513,
        'GBP': 0.7443,
        'JPY': 147.65,
        'CNY': 7.169,
        'KRW': 1382.7,
        'AUD': 1.523,
        'CAD': 1.370,
        'CHF': 0.7953,
        'SGD': 1.281
    }
    
    return jsonify({
        'base_currency': 'USD',
        'rates': rates,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'note': 'July 2025 market rates - demo purposes only',
        'usage': 'GET /api/currency/convert?from=USD&to=EUR&amount=100',
        'region': 'ap-northeast-1'
    })


@app.route('/api/currency/convert')
def currency_convert():
    """Convert between currencies."""
    try:
        from_currency = request.args.get('from', 'USD').upper()
        to_currency = request.args.get('to', 'EUR').upper()
        amount = float(request.args.get('amount', 100))
        
        # Current rates (July 2025)
        rates = {
            'USD': 1.0, 'EUR': 0.8513, 'GBP': 0.7443, 'JPY': 147.65,
            'CNY': 7.169, 'KRW': 1382.7, 'AUD': 1.523, 'CAD': 1.370,
            'CHF': 0.7953, 'SGD': 1.281
        }
        
        if from_currency not in rates or to_currency not in rates:
            return jsonify({'error': 'Currency not supported'}), 400
            
        # Convert via USD
        usd_amount = amount / rates[from_currency]
        converted_amount = usd_amount * rates[to_currency]
        
        return jsonify({
            'from': {'currency': from_currency, 'amount': amount},
            'to': {'currency': to_currency, 'amount': round(converted_amount, 2)},
            'rate': round(rates[to_currency] / rates[from_currency], 4),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount provided'}), 400


@app.route('/api/calculator', methods=['POST'])
def calculator():
    """Simple calculator for basic operations."""
    try:
        data = request.get_json() or {}
        operation = data.get('operation')
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        
        operations = {
            'add': a + b,
            'subtract': a - b,
            'multiply': a * b,
            'divide': a / b if b != 0 else None,
            'power': pow(a, b),
            'sqrt': math.sqrt(a) if a >= 0 else None,
            'log': math.log(a) if a > 0 else None
        }
        
        if operation not in operations:
            return jsonify({
                'error': 'Invalid operation',
                'supported': list(operations.keys())
            }), 400
            
        result = operations[operation]
        if result is None:
            return jsonify({'error': 'Invalid calculation (division by zero, negative sqrt, etc.)'}), 400
            
        return jsonify({
            'operation': operation,
            'inputs': {'a': a, 'b': b} if operation not in ['sqrt', 'log'] else {'a': a},
            'result': result,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400


@app.route('/api/text-utils', methods=['POST'])
def text_utils():
    """Text utilities like word count, character count, etc."""
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        
        if not isinstance(text, str):
            return jsonify({'error': 'Text must be a string'}), 400
            
        return jsonify({
            'original_text': text,
            'stats': {
                'characters': len(text),
                'characters_no_spaces': len(text.replace(' ', '')),
                'words': len(text.split()),
                'lines': len(text.splitlines()),
                'sentences': len([s for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()])
            },
            'transformations': {
                'uppercase': text.upper(),
                'lowercase': text.lower(),
                'title_case': text.title(),
                'reversed': text[::-1]
            },
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 400


@app.route('/api/quote')
def random_quote():
    """Get a random inspirational quote."""
    quotes = [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"text": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
        {"text": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
        {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
        {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle"},
        {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
        {"text": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
        {"text": "Don't let yesterday take up too much of today.", "author": "Will Rogers"},
        {"text": "You learn more from failure than from success.", "author": "Unknown"},
        {"text": "If you are working on something exciting that you really care about, you don't have to be pushed.", "author": "Steve Jobs"},
        {"text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
        {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
        {"text": "The best error message is the one that never shows up.", "author": "Thomas Fuchs"}
    ]
    
    quote = random.choice(quotes)
    return jsonify({
        'quote': quote,
        'total_quotes': len(quotes),
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'region': 'ap-northeast-1'
    })


@app.route('/api/encoder', methods=['POST'])
def encoder_decoder():
    """Base64 encoder and decoder."""
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        operation = data.get('operation', 'encode')  # 'encode' or 'decode'
        
        if not isinstance(text, str):
            return jsonify({'error': 'Text must be a string'}), 400
            
        if operation == 'encode':
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return jsonify({
                'operation': 'encode',
                'original': text,
                'result': encoded,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            })
        elif operation == 'decode':
            try:
                decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                return jsonify({
                    'operation': 'decode',
                    'original': text,
                    'result': decoded,
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                })
            except Exception:
                return jsonify({'error': 'Invalid base64 string'}), 400
        else:
            return jsonify({
                'error': 'Invalid operation',
                'supported': ['encode', 'decode']
            }), 400
            
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 400


@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler."""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404,
        'region': 'ap-northeast-1',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler."""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500,
        'region': 'ap-northeast-1',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 500


if __name__ == '__main__':
    print(f"🚀 Starting ECS Playground app on port {PORT}")
    print(f"🌏 Region: Tokyo (ap-northeast-1)")
    print(f"🏷️  Environment: {APP_ENV}")
    print(f"📦 Version: {VERSION}")
    print(f"🐍 Python: 3.12")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=(APP_ENV == 'development')
    ) 