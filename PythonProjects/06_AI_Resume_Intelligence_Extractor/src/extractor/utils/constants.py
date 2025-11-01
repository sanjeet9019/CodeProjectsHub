"""
Resume Intelligence Constants by Sanjeet Prasad
-----------------------------------------------
Author: Sanjeet Prasad
Email: sanjeet8.23@gmail.com
Description: Centralized constants for skill and location extraction used across the Resume Intelligence Engine.
Date: October 25, 2025

Includes:
- known_skills: Canonical list of technical skills for NLP-based skill extraction
- known_cities: Supported Indian city names for location detection
- city_aliases: Normalization map for alternate city spellings and variants

Usage:
These constants are used by field extractors to match and normalize resume content.
They support regex, spaCy, and rule-based strategies for consistent parsing.
"""

# constants.py - APPEND these new constants to the existing content

# --- Job Title Field Constants (Newly Added) ---

# SECTION_HEADERS: Keywords for identifying the work experience section
WORK_EXPERIENCE_HEADERS = [
    "work experience", "professional experience", "employment history", "career contour",
    "experience narrative", "career history", "experience summary", "professional background",
    "job history", "career summary"
]

# CURRENT_EMPLOYMENT_KEYWORDS: Keywords indicating an ongoing role
CURRENT_JOB_KEYWORDS = [
    "present", "current", "till date", "tilldate", "ongoing", 
    "till now", "to date", "todate", "now", "continuing"
]

# TITLE_NOISE_PATTERNS: Regex patterns for common noise in job titles
JOB_TITLE_NOISE_PATTERNS = [
    r'\s*[-–—]\s*grade\s+\d+', r'\s*[-–—]\s*level\s+\d+', r'\s*[-–—]\s*band\s+[a-z0-9]+',
    r'\s*\(remote\)', r'\s*\(onsite\)', r'\s*\(hybrid\)', r'\s*\(contract\)',
    r'\s*\(full[- ]?time\)', r'\s*\(part[- ]?time\)', r'\s*\(temporary\)',
    r'\s*\([A-Z]{2,3}\)', r'\s*[-–—]\s*[A-Z]{2,3}\s*$'
]

# ABBREVIATIONS: Common title abbreviations for expansion
TITLE_ABBREVIATIONS = {
    'sr.': 'Senior', 'sr': 'Senior', 'snr.': 'Senior', 'snr': 'Senior',
    'jr.': 'Junior', 'jr': 'Junior', 'mgr.': 'Manager', 'mgr': 'Manager',
    'asst.': 'Assistant', 'assoc.': 'Associate', 'exec.': 'Executive',
    'vp': 'Vice President', 'svp': 'Senior Vice President', 'evp': 'Executive Vice President',
    'avp': 'Assistant Vice President', 'cto': 'Chief Technology Officer',
    'ceo': 'Chief Executive Officer', 'cfo': 'Chief Financial Officer',
    'coo': 'Chief Operating Officer', 'cio': 'Chief Information Officer',
    'cmo': 'Chief Marketing Officer', 'sme': 'Subject Matter Expert'
}

# TITLE_INDICATORS: Keywords that strongly suggest a phrase is a job title
JOB_TITLE_INDICATORS = [
    'engineer', 'developer', 'manager', 'analyst', 'lead', 'senior', 'junior', 'architect',
    'consultant', 'specialist', 'director', 'officer', 'coordinator', 'administrator',
    'designer', 'programmer', 'scientist', 'researcher', 'advisor', 'associate', 
    'executive', 'supervisor', 'technician', 'assistant', 'head', 'chief', 'principal', 
    'practitioner', 'fellow', 'partner', 'tech',
    'trainee', 'intern', 'fresher' 
]

# ACRONYMS for title casing exceptions (from _clean_and_normalize_title)
TITLE_ACRONYMS = {'CEO', 'CTO', 'CFO', 'CIO', 'CMO', 'COO', 'VP', 'SVP', 'EVP', 'AVP', 
                  'IT', 'HR', 'QA', 'UI', 'UX', 'AI', 'ML', 'SME', 'POC', 'R&D', 'SA'}

# ✅ Canonical list of known technical skills
known_skills = {
    # Programming Languages
    "c", "c++", "java", "python", "javascript", "typescript", "go", "rust", "ruby", "kotlin", "swift", "scala","perl", "shell", "bash",

    # Query & Data Languages
    "sql", "pl/sql", "t-sql", "soql", "graphql", "sparql", "hql",

    # Databases
    "oracle", "mysql", "postgresql", "mongodb", "db2", "sybase", "sqlite", "cassandra", "redis", "dynamodb", "elasticsearch",

    # Web & Frontend
    "html", "css", "sass", "less", "bootstrap", "tailwind", "react", "angular", "vue", "next.js", "nuxt.js", "jquery",

    # Backend & Frameworks
    "spring", "spring boot", "django", "flask", "express", "fastapi", "node.js", "dotnet", "asp.net", "laravel", "rails",

    # DevOps & CI/CD
    "git", "github", "gitlab", "bitbucket", "docker", "kubernetes", "jenkins", "circleci", "travis", "ansible", "terraform", "helm", "vagrant",

    # Cloud Platforms
    "aws", "azure", "gcp", "cloud foundry", "openshift", "heroku", "firebase", "netlify",

    # Testing & QA
    "selenium", "cypress", "junit", "pytest", "testng", "postman", "soapui", "jmeter", "loadrunner",

    # Tools & IDEs
    "jira", "confluence", "eclipse", "intellij", "visual studio", "vscode", "xcode", "android studio", "makefile", "gdb", "valgrind", "wireshark",

    # CRM & Salesforce
    "salesforce", "apex", "soql", "lightning components", "omnistudio", "omniscript", "data loader", "workbench",

    # Data & Analytics
    "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "keras", "pytorch", "hadoop", "spark", "airflow", "tableau", "power bi",

    # Messaging & APIs
    "rest", "soap", "grpc", "kafka", "rabbitmq", "mqtt", "websockets",

    # Security & Monitoring
    "splunk", "prometheus", "grafana", "nagios", "zabbix", "sonarqube", "veracode", "owasp",

    # Misc
    "linux", "windows", "macos", "as400", "mainframe", "uml", "visio", "notepad++", "putty", "winscp"
}

# ✅ Known Indian cities for location detection
known_cities = {
    "gurgaon", "gurugram", "noida", "delhi", "new delhi", "bangalore", "bengaluru", "hyderabad", "pune", "mumbai", "chennai", "ranchi",
    "kolkata", "jaipur", "ahmedabad", "lucknow", "bhopal", "visakhapatnam", "indore", "chandigarh", "kochi", "coimbatore", "nagpur", "patna",
    "surat", "vadodara", "trivandrum", "goa", "dehradun", "guwahati", "amritsar", "jodhpur", "mysore", "kanpur"
}

# ✅ City aliases for normalization
city_aliases = {
    "gurugram": "gurgaon",
    "bengaluru": "bangalore",
    "new delhi": "delhi",
    "trivandrum": "thiruvananthapuram",
    "vadodara": "baroda"
}
