import re

with open('website/teacher_profile.html', 'r', encoding='utf-8') as f:
    teacher_html = f.read()

# Extract Sidebar
sidebar_match = re.search(r'(<aside class="sidebar">.*?</aside>)', teacher_html, re.DOTALL)
if not sidebar_match:
    print("Could not find sidebar")
    exit(1)
sidebar = sidebar_match.group(1)

# Extract CSS/fonts from <head> to be sure it has the same style
# Actually, they already link to css/style.css, but let's make sure the body has desktop-layout.

def wrap_with_layout(title, head_styles, content_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Vidhyarakshak</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
{head_styles}
    </style>
</head>
<body class="desktop-layout" style="background-color: #F8FAFC;">
    
    <!-- Sidebar -->
    {sidebar}

    <!-- Main Content -->
    <main class="main-content">
        <div class="dashboard-header" style="margin-bottom: 24px;">
            <h1 class="dashboard-title">{title}</h1>
            <p style="color: var(--text-muted); font-size: 15px; margin-top: 4px;">Information about the application</p>
        </div>

        {content_html}
    </main>
    
    <script>
        function clearSession() {{
            sessionStorage.clear();
            localStorage.clear();
            window.location.href = 'index.html';
        }}
    </script>
</body>
</html>"""

# === PRIVACY POLICY ===

privacy_styles = """
        .policy-container {
            max-width: 800px;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .header-top {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 32px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 24px;
        }
        .back-btn {
            background: none;
            border: none;
            cursor: pointer;
            color: #1E293B;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            border-radius: 50%;
            transition: background 0.2s;
            text-decoration: none;
        }
        .back-btn:hover {
            background: #F1F5F9;
        }
        .policy-title {
            font-size: 24px;
            font-weight: 700;
            color: #1E293B;
            margin: 0;
        }
        .policy-content h2 {
            font-size: 20px;
            font-weight: 700;
            color: #1E293B;
            margin-top: 32px;
            margin-bottom: 16px;
        }
        .policy-content h3 {
            font-size: 16px;
            font-weight: 700;
            color: #1E293B;
            margin-top: 24px;
            margin-bottom: 8px;
        }
        .policy-content p {
            font-size: 15px;
            color: #475569;
            line-height: 1.6;
            margin-bottom: 16px;
        }
        .last-updated {
            font-size: 14px;
            color: #94A3B8;
            margin-bottom: 32px;
        }
"""

privacy_content = """
        <div class="policy-container">
            <div class="header-top">
                <a href="javascript:history.back()" class="back-btn">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="19" y1="12" x2="5" y2="12"></line>
                        <polyline points="12 19 5 12 12 5"></polyline>
                    </svg>
                </a>
                <h2 class="policy-title" style="margin:0;">VidyaRakshak Privacy Policy</h2>
            </div>

            <div class="policy-content">
                <p class="last-updated">Last Updated: March 2024</p>

                <h3>1. Information We Collect</h3>
                <p>We collect minimal information required to manage student records and provide AI-based risk predictions. This includes student names, attendance, and marks. No personal student contact information is shared outside the institution.</p>

                <h3>2. How We Use Data</h3>
                <p>Data is used locally to identify students at risk of dropouts or academic failure. Our AI models analyze trends to provide alerts to teachers and administrators.</p>

                <h3>3. Data Protection</h3>
                <p>All student data is securely stored using industry-standard security measures. Profile access is strictly restricted through secure login credentials matching your authorized role.</p>

                <h3>4. Data Sharing</h3>
                <p>Student data is not shared with any third parties. It is solely used by authorized teachers and administrators for identifying students who need support and ensuring educational continuity.</p>

                <h3>5. Contact Information</h3>
                <p>If you have any questions about these privacy practices or need technical assistance, please contact the school administration or the designated IT department.</p>
            </div>
        </div>
"""

with open('website/privacy_policy.html', 'w', encoding='utf-8') as f:
    f.write(wrap_with_layout("Privacy Policy", privacy_styles, privacy_content))


# === ABOUT APP ===

about_styles = """
        .about-container {
            max-width: 600px;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            text-align: center;
        }
        .back-btn-container {
            text-align: left;
            margin-bottom: 24px;
        }
        .back-btn {
            background: none;
            border: none;
            cursor: pointer;
            color: #1E293B;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            border-radius: 50%;
            transition: background 0.2s;
            text-decoration: none;
        }
        .back-btn:hover {
            background: #F1F5F9;
        }
        
        .app-logo {
            width: 140px;
            height: auto;
            margin-bottom: 24px;
        }
        
        .app-title {
            font-size: 28px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 8px;
        }
        
        .app-subtitle {
            font-size: 16px;
            color: #3B82F6;
            margin-bottom: 24px;
        }
        
        .app-version {
            font-size: 14px;
            color: #64748B;
            margin-bottom: 8px;
        }
        
        .app-copyright {
            font-size: 13px;
            color: #94A3B8;
            margin-bottom: 40px;
        }
        
        .app-description {
            font-size: 15px;
            color: #475569;
            line-height: 1.7;
            margin-bottom: 40px;
            padding: 0 20px;
        }
        
        .support-email {
            font-size: 15px;
            font-weight: 700;
            color: #3B82F6;
            text-decoration: none;
            margin-bottom: 8px;
            display: block;
        }
        
        .support-contact {
            font-size: 14px;
            color: #64748B;
        }
"""

about_content = """
        <div class="about-container">
            <div class="back-btn-container">
                <a href="javascript:history.back()" class="back-btn">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="19" y1="12" x2="5" y2="12"></line>
                        <polyline points="12 19 5 12 12 5"></polyline>
                    </svg>
                </a>
            </div>

            <img src="assets/logo.png" alt="VidyaRakshak Logo" class="app-logo">
            
            <div class="app-title">VidyaRakshak</div>
            <div class="app-subtitle">Protecting Education, Securing Futures</div>
            
            <div class="app-version">Version 1.1.0</div>
            <div class="app-copyright">&copy; 2024 VidyaRakshak Inc.</div>
            
            <p class="app-description">
                VidyaRakshak is a student dropout prevention system designed for rural schools. It helps identify at-risk students early, track interventions, and support timely action by teachers and administrators.
            </p>
            
            <a href="mailto:help@vidyarakshak.edu" class="support-email">Support: help@vidyarakshak.edu</a>
            <div class="support-contact">Contact: +91 00000 00000</div>
        </div>
"""

with open('website/about_app.html', 'w', encoding='utf-8') as f:
    f.write(wrap_with_layout("About App", about_styles, about_content))

print("Successfully injected desktop layout!")
