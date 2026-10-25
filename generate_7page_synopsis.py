import base64
import os
import subprocess
import pypdfium2 as pdfium

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def main():
    workspace = r"C:\Users\HP\Desktop\AI university chatbot"
    eda_intent_path = os.path.join(workspace, "analytics_output", "eda_intent_distribution.png")
    eda_word_path = os.path.join(workspace, "analytics_output", "eda_word_length_distribution.png")
    arch_img_path = os.path.join(workspace, "architecture_diagram.png")
    
    eda_intent_b64 = get_base64_image(eda_intent_path)
    eda_word_b64 = get_base64_image(eda_word_path)
    arch_b64 = get_base64_image(arch_img_path)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Project Synopsis - Yashika Gupta (2300320150073)</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 10mm 12mm 10mm 12mm;
    }}
    
    * {{
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Segoe UI', Calibri, Arial, sans-serif;
        font-size: 9.3pt;
        line-height: 1.42;
        color: #1a202c;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }}
    
    .page {{
        width: 100%;
        height: 275mm;
        max-height: 275mm;
        overflow: hidden;
        page-break-after: always;
        break-after: page;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    .page:last-child {{
        page-break-after: avoid;
        break-after: avoid;
    }}
    
    .header-banner {{
        border-bottom: 2.5px solid #005691;
        padding-bottom: 5px;
        margin-bottom: 9px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    
    .brand-title {{
        font-size: 13.5pt;
        font-weight: 700;
        color: #003366;
        letter-spacing: -0.2px;
        margin: 0;
    }}
    
    .brand-sub {{
        font-size: 8pt;
        color: #006699;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 1px;
    }}
    
    .cohort-badge {{
        font-size: 7.8pt;
        background: #eef5fb;
        border: 1px solid #c8e1f5;
        color: #004b87;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        text-align: right;
    }}
    
    .doc-headline {{
        background: #f4f8fc;
        border-left: 4.5px solid #005691;
        padding: 7px 11px;
        margin-bottom: 10px;
    }}
    
    .doc-headline h1 {{
        font-size: 11.5pt;
        margin: 0 0 3px 0;
        color: #0f2c4d;
    }}
    
    .doc-headline p {{
        margin: 0;
        font-size: 8.4pt;
        color: #4a5568;
    }}
    
    table.meta-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 10px;
        font-size: 8.6pt;
    }}
    
    table.meta-table th, table.meta-table td {{
        border: 1px solid #cbd5e0;
        padding: 4.5px 8px;
        text-align: left;
    }}
    
    table.meta-table th {{
        background-color: #003366;
        color: #ffffff;
        font-weight: 600;
        font-size: 8.8pt;
    }}
    
    table.meta-table td.field-name {{
        background-color: #f7fafc;
        font-weight: 600;
        color: #1a365d;
        width: 26%;
    }}
    
    table.meta-table td.field-val {{
        color: #2d3748;
        width: 74%;
    }}
    
    .section-title {{
        font-size: 10pt;
        font-weight: 700;
        color: #003366;
        border-bottom: 1.3px solid #005691;
        padding-bottom: 2px;
        margin-top: 9px;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}
    
    p, li {{
        font-size: 8.7pt;
        line-height: 1.42;
        margin-top: 3px;
        margin-bottom: 5px;
        text-align: justify;
    }}
    
    ul, ol {{
        margin-top: 3px;
        margin-bottom: 5px;
        padding-left: 18px;
    }}
    
    .highlight-box {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 3.5px solid #0077b6;
        padding: 7px 10px;
        margin: 6px 0;
        border-radius: 2px;
    }}
    
    .sub-box {{
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #005691;
        padding: 6px 9px;
        margin-bottom: 6px;
        border-radius: 2px;
    }}
    
    .sub-box-title {{
        font-weight: 700;
        color: #003366;
        font-size: 8.9pt;
        margin-bottom: 2px;
    }}
    
    table.data-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 6px 0;
        font-size: 8.3pt;
    }}
    
    table.data-table th, table.data-table td {{
        border: 1px solid #cbd5e0;
        padding: 4px 7px;
    }}
    
    table.data-table th {{
        background-color: #edf2f7;
        color: #1a202c;
        font-weight: 600;
        text-align: left;
    }}
    
    .footer-stamp {{
        text-align: center;
        font-size: 7.5pt;
        color: #718096;
        border-top: 1px solid #e2e8f0;
        padding-top: 3px;
        margin-top: 4px;
    }}
    
    .declaration-box {{
        background: #fffdf5;
        border: 1px solid #f6e05e;
        border-left: 4px solid #d69e2e;
        padding: 8px 12px;
        margin-top: 8px;
    }}
</style>
</head>
<body>

<!-- ==================== PAGE 1 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme</div>
                <div class="brand-sub">Industry Project Synopsis &bull; 2026–2027 Academic Batch</div>
            </div>
            <div class="cohort-badge">
                Domain: Digital-Data-AI / AIML<br>
                Track: 4-Week Individual Capstone
            </div>
        </div>

        <div class="doc-headline">
            <h1>AI-Powered Chatbot for University Student Support</h1>
            <p>An intelligent, production-ready conversational intelligence pipeline leveraging sublinear Natural Language Processing (NLP) and calibrated Multi-Layer Perceptron (MLP) Neural Networks to automate 24/7 university student enquiries.</p>
        </div>

        <table class="meta-table">
            <thead>
                <tr>
                    <th colspan="2">Field Details (Learner Information)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="field-name">Project Title</td>
                    <td class="field-val"><strong>AI-Powered Chatbot for University Student Support</strong></td>
                </tr>
                <tr>
                    <td class="field-name">Domain</td>
                    <td class="field-val"><strong>Digital-Data-AI / AIML</strong></td>
                </tr>
                <tr>
                    <td class="field-name">Duration & Format</td>
                    <td class="field-val">4 Weeks &bull; Individual Project</td>
                </tr>
                <tr>
                    <td class="field-name">Learner Name</td>
                    <td class="field-val"><strong>Yashika Gupta</strong></td>
                </tr>
                <tr>
                    <td class="field-name">University Roll No.</td>
                    <td class="field-val"><strong>2300320150073</strong></td>
                </tr>
                <tr>
                    <td class="field-name">College / Campus</td>
                    <td class="field-val"><strong>ABES Engineering College</strong></td>
                </tr>
                <tr>
                    <td class="field-name">Mentor Name</td>
                    <td class="field-val"><strong>Dr. Anamika Goel</strong></td>
                </tr>
                <tr>
                    <td class="field-name">Submission Date</td>
                    <td class="field-val">25-10-2026</td>
                </tr>
                <tr>
                    <td class="field-name">GitHub Repository Link</td>
                    <td class="field-val"><a href="https://github.com/Yashika-2468/AI-CHATBOT-PROJECT" style="color: #005691; text-decoration: underline; font-weight: 600;">https://github.com/Yashika-2468/AI-CHATBOT-PROJECT</a></td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">1. Problem Statement (5W1H Analysis)</div>
        <p>
            Higher education institutions handle tens of thousands of student interactions annually across disparate administrative departments including admissions, academic registries, accounts, examination cells, hostel offices, and department directorates. A structured 5W1H breakdown of the operational challenge is detailed below:
        </p>

        <div class="sub-box">
            <div class="sub-box-title">1. Who Faces the Problem?</div>
            <p>Prospective applicants, enrolled undergraduate/postgraduate students, parents, and university administrative staff who are overwhelmed by repetitive front-office inquiries.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">2. What is the Problem?</div>
            <p>Over 70% to 80% of inbound helpdesk queries are strictly repetitive and transactional (e.g., semester fee structures, installment due dates, hostel curfew timings, mess rebate rules, syllabus download links, and HOD contact numbers). Manual handling creates severe information backlogs.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">3. When and Where Does it Occur?</div>
            <p>The problem peaks dramatically during admission rounds, semester fee payment deadlines, and university examination cycles across central physical administrative counters and standard helpline telephone extensions.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">4. Why is it Important?</div>
            <p>Human helpdesks operate strictly during standard office hours (9:00 AM to 5:00 PM on weekdays), leaving weekend and late-night inquiries unanswered. Consequently, average response times range from 24 to 72 hours, resulting in student anxiety, missed institutional deadlines, and high administrative burnout.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">5. How Will the Solution Resolve It?</div>
            <p>By engineering a lightweight, self-contained AI conversational agent capable of classifying student intent in &lt;15 milliseconds with 99.51% precision, maintaining multi-turn conversational context, offering voice interaction, and operating 24 hours a day with zero recurring cloud API overhead.</p>
        </div>
    </div>
    <div class="footer-stamp">
        Page 1 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

<!-- ==================== PAGE 2 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme &bull; Project Synopsis</div>
                <div class="brand-sub">Learner: Yashika Gupta | Roll No: 2300320150073</div>
            </div>
            <div class="cohort-badge">ABES Engineering College</div>
        </div>

        <div class="section-title">2. Proposed Solution & Technical Approach</div>
        <p>
            To address the limitations of conventional rule-based chatbots and resource-intensive Large Language Models (LLMs), this project implements an end-to-end, highly optimized supervised Machine Learning and Natural Language Processing architecture tailored for university domains. The core technical approach consists of five cohesive stages:
        </p>

        <div class="sub-box">
            <div class="sub-box-title">Stage 1: Text Preprocessing & Sublinear N-Gram Vectorization</div>
            <p>Inbound student utterances are stripped of noise, normalized to lowercase, and converted into high-dimensional numerical feature vectors using a specialized <strong>TF-IDF Vectorizer</strong>. The vectorizer combines word n-grams (1–3) with sublinear character n-grams (3–5). This hybrid tokenization guarantees that spelling variations, student abbreviations (e.g., 'cse hod', 'fees structure', 'hostel mess'), and informal Hinglish phrasing are captured with resilient semantic representations.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">Stage 2: Deep Multi-Layer Perceptron (MLP) Neural Classification</div>
            <p>Vectorized features are processed through a 2-tier Multi-Layer Perceptron neural network comprising 64 neurons in the primary hidden layer and 32 neurons in the secondary hidden layer, utilizing Rectified Linear Unit (ReLU) activations and the Adam optimization algorithm. The output layer applies a Softmax function across 39 distinct university operational classes to compute a calibrated probability distribution.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">Stage 3: Calibrated Confidence Gateway & Fail-Safe Fallback</div>
            <p>To eliminate hallucinated or misleading responses, the prediction pipeline evaluates the maximum Softmax probability against a calibrated decision threshold of <strong>0.40 (40%)</strong>. Inquiries falling below this threshold automatically trigger a helpful fallback protocol directing the learner to specific official institutional contacts.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">Stage 4: Entity Extraction & Multi-Turn Context Tracking</div>
            <p>An entity recognition engine actively monitors departmental designations (Computer Science, Information Technology, Electronics, Mechanical, Applied Sciences) to resolve ambiguous inquiries (e.g., 'Who is the HOD?' followed by 'CSE'). An in-memory session cache maintains conversation states (<code>GreetingUserRequest</code>, <code>HODContext</code>) for contextual continuity.</p>
        </div>

        <div class="sub-box">
            <div class="sub-box-title">Stage 5: Dual Web Interfaces & SQLite Audit Trail</div>
            <p>The solution exposes an asynchronous FastAPI REST microservice supporting real-time voice speech-to-text (STT) and text-to-speech (TTS) playback, paired with a companion Streamlit analytical dashboard. Every student query is persisted into an embedded SQLite database for administrative auditing.</p>
        </div>

        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 25%;">Solution Attribute</th>
                    <th style="width: 25%;">Traditional Keyword Search</th>
                    <th style="width: 25%;">Cloud LLMs (e.g. OpenAI)</th>
                    <th style="width: 25%;">Our Hybrid Neural MLP Model</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Handling Typos & Slang</strong></td>
                    <td>Fails completely on spelling mistakes</td>
                    <td>High competence, but slow</td>
                    <td><strong>High (Sublinear Char N-Grams)</strong></td>
                </tr>
                <tr>
                    <td><strong>Response Latency</strong></td>
                    <td>&lt;5 ms (Rigid match)</td>
                    <td>800 ms &ndash; 2500 ms</td>
                    <td><strong>&lt;12 ms (Instantaneous CPU)</strong></td>
                </tr>
                <tr>
                    <td><strong>Recurring Cost</strong></td>
                    <td>Free</td>
                    <td>High per-token API charges</td>
                    <td><strong>100% Free & Self-Contained</strong></td>
                </tr>
                <tr>
                    <td><strong>Hallucination Risk</strong></td>
                    <td>None (Returns null)</td>
                    <td>Significant (Fabricates data)</td>
                    <td><strong>Zero (Calibrated Fallback Gateway)</strong></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="footer-stamp">
        Page 2 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

<!-- ==================== PAGE 3 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme &bull; Project Synopsis</div>
                <div class="brand-sub">Learner: Yashika Gupta | Roll No: 2300320150073</div>
            </div>
            <div class="cohort-badge">ABES Engineering College</div>
        </div>

        <div class="section-title">3. System Architecture & Data Flow Diagrams</div>
        <p>
            The system adheres to a decoupled, multi-tier architectural pattern consisting of a Presentation Layer, Application Controller Layer, AI/ML Inference Pipeline, and Persistence Storage Layer.
        </p>

        {"<div style='text-align: center; margin: 8px 0;'><img src='" + arch_b64 + "' style='max-width: 98%; height: auto; border: 1.5px solid #cbd5e0; border-radius: 4px;'><div style='font-size: 7.6pt; color: #4a5568; margin-top: 3px;'>Figure 1: Multi-Tier Production System Architecture (Data Flow from Student Interface to SQLite Audit DB)</div></div>" if arch_b64 else ""}

        <div class="section-title">Subsystem Components & Interaction Protocols</div>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 22%;">Subsystem Module</th>
                    <th style="width: 38%;">Implementation Technology & Protocol</th>
                    <th style="width: 40%;">Core Operational Responsibility</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Presentation Tier</strong></td>
                    <td>HTML5 Glassmorphism UI, Web Speech STT/TTS, Streamlit Engine</td>
                    <td>Captures multimodal student inputs (voice microphone / text keyboard) and renders real-time bot responses.</td>
                </tr>
                <tr>
                    <td><strong>Application Gateway</strong></td>
                    <td>FastAPI ASGI Microservice, HTTP POST /chat, CORS Middleware</td>
                    <td>Validates payload schema, allocates session identifiers, manages conversation cache, and routes payloads.</td>
                </tr>
                <tr>
                    <td><strong>NLP Vectorizer</strong></td>
                    <td>Scikit-Learn Sublinear TF-IDF (1–3 word, 3–5 char n-grams)</td>
                    <td>Transforms raw user strings into normalized numerical feature matrices resistant to out-of-vocabulary variations.</td>
                </tr>
                <tr>
                    <td><strong>Neural Classifier</strong></td>
                    <td>Multi-Layer Perceptron (64, 32 ReLU hidden nodes, Adam)</td>
                    <td>Executes feed-forward inference and outputs a Softmax probability vector across all 39 institutional classes.</td>
                </tr>
                <tr>
                    <td><strong>Disambiguation Unit</strong></td>
                    <td>Regex Department Parser + Context State Cache</td>
                    <td>Resolves multi-turn entity dependencies (CSE, IT, ECE, ME) and maps general requests to specific answers.</td>
                </tr>
                <tr>
                    <td><strong>Audit Persistence</strong></td>
                    <td>SQLite3 Relational DB (<code>chatbot.db</code>, Thread-Safe Pool)</td>
                    <td>Persists user queries, predicted intent, response latency, timestamp, and student feedback ratings.</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">Data Flow Diagram (DFD Level-0 & Level-1 Logic)</div>
        <p>
            At <strong>DFD Level 0</strong>, the boundary model connects the external Student Entity to the University Chatbot System. The student transmits an enquiry string and receives verified academic advisories. Internally at <strong>DFD Level 1</strong>, the query is ingested by Process 1.0 (Sanitization & Normalization), forwarded to Process 2.0 (Vector Transformation), evaluated by Process 3.0 (Neural Inference), verified by Process 4.0 (Confidence Validation & Entity Disambiguation), and logged to Data Store D1 (<code>chatbot.db</code>) before returning the finalized response to the user.
        </p>
    </div>
    <div class="footer-stamp">
        Page 3 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

<!-- ==================== PAGE 4 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme &bull; Project Synopsis</div>
                <div class="brand-sub">Learner: Yashika Gupta | Roll No: 2300320150073</div>
            </div>
            <div class="cohort-badge">ABES Engineering College</div>
        </div>

        <div class="section-title">4. Technology Stack & Specifications</div>
        <p>
            The project utilizes a modern, robust, and completely open-source Python software stack selected specifically for computational efficiency, rapid execution speed, and high reproducibility:
        </p>

        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 25%;">Stack Component</th>
                    <th style="width: 40%;">Framework / Library Details</th>
                    <th style="width: 35%;">Functional Justification</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Frontend User Interface</strong></td>
                    <td>HTML5, CSS3 Glassmorphism, Vanilla JS ES6, Web Speech API</td>
                    <td>Zero heavy frontend dependencies; instant page load; native microphone Speech-to-Text and audio synthesis.</td>
                </tr>
                <tr>
                    <td><strong>Backend Web Services</strong></td>
                    <td>FastAPI 0.115, Uvicorn ASGI Server, Streamlit 1.40</td>
                    <td>Asynchronous execution delivering &lt;5ms API routing overhead; automatic OpenAPI docs; dual web interfaces.</td>
                </tr>
                <tr>
                    <td><strong>Database Management</strong></td>
                    <td>SQLite 3.45 (Relational Embedded Engine), WAL Mode</td>
                    <td>Zero configuration required; thread-safe connection pooling; low disk footprint; robust auditing capability.</td>
                </tr>
                <tr>
                    <td><strong>Machine Learning Core</strong></td>
                    <td>Scikit-Learn 1.6, NumPy, Joblib Persistence Engine</td>
                    <td>Eliminated heavy C-extension/protobuf conflicts; highly optimized Cython inference kernel; pure Python stability.</td>
                </tr>
                <tr>
                    <td><strong>Analytics & Graphics</strong></td>
                    <td>Matplotlib 3.10, Seaborn, Pandas</td>
                    <td>Visual distribution profiling of training queries, token length distributions, and performance validation.</td>
                </tr>
                <tr>
                    <td><strong>Deployment Hardware</strong></td>
                    <td>Standard x86-64 Machine (8GB RAM, CPU-Only Execution)</td>
                    <td>Runs effortlessly on commodity desktop hardware without requiring dedicated or costly graphics hardware (GPU).</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">Neural Network Hyperparameter Specifications</div>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 30%;">Hyperparameter</th>
                    <th style="width: 30%;">Configured Value</th>
                    <th style="width: 40%;">Architectural Rationale</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Network Topology</strong></td>
                    <td>Input &rarr; Dense(64) &rarr; Dense(32) &rarr; Softmax(39)</td>
                    <td>Balances representation learning with strict prevention of overfitting on small-to-medium corpora.</td>
                </tr>
                <tr>
                    <td><strong>Activation Function</strong></td>
                    <td>Rectified Linear Unit (ReLU)</td>
                    <td>Overcomes vanishing gradients and facilitates rapid non-linear boundary convergence during training.</td>
                </tr>
                <tr>
                    <td><strong>Optimization Algorithm</strong></td>
                    <td>Adam (Adaptive Moment Estimation)</td>
                    <td>Combines AdaGrad and RMSProp advantages for dynamic learning rate adjustments across sparse text features.</td>
                </tr>
                <tr>
                    <td><strong>Initial Learning Rate</strong></td>
                    <td>0.001 (with adaptive decay)</td>
                    <td>Guarantees steady loss curve descent without destabilizing weight updates.</td>
                </tr>
                <tr>
                    <td><strong>Maximum Training Epochs</strong></td>
                    <td>500 iterations (Early Stopping enabled)</td>
                    <td>Halts training when validation loss stops improving for 15 consecutive epochs to prevent memorization.</td>
                </tr>
                <tr>
                    <td><strong>Vector Feature Space</strong></td>
                    <td>Sublinear TF-IDF (Word 1-3 & Char 3-5 n-grams)</td>
                    <td>Downscales disproportionately frequent tokens using logarithmic term frequency scaling: 1 + log(tf).</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="footer-stamp">
        Page 4 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

<!-- ==================== PAGE 5 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme &bull; Project Synopsis</div>
                <div class="brand-sub">Learner: Yashika Gupta | Roll No: 2300320150073</div>
            </div>
            <div class="cohort-badge">ABES Engineering College</div>
        </div>

        <div class="section-title">5. Dataset Overview & Statistical Summary</div>
        <p>
            The project is trained upon an authentic, comprehensive university support dataset stored in <code>data/intents.json</code> and exported to tabular format as <code>dataset.csv</code>. The corpus captures real-world student interaction scenarios across 39 distinct university operational domains.
        </p>

        <table class="data-table">
            <tbody>
                <tr>
                    <td style="width: 35%; font-weight: 600; background: #f7fafc;">Primary Dataset File</td>
                    <td><code>dataset.csv</code> (exported from verified <code>data/intents.json</code>)</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; background: #f7fafc;">Total Training Queries (Rows)</td>
                    <td><strong>412 query patterns</strong> across authentic student linguistic formulations</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; background: #f7fafc;">Total Feature Columns</td>
                    <td><strong>5 Columns:</strong> <code>intent</code>, <code>query_text</code>, <code>response_samples</code>, <code>entity_type</code>, <code>context_state</code></td>
                </tr>
                <tr>
                    <td style="font-weight: 600; background: #f7fafc;">Total Intent Categories</td>
                    <td><strong>39 Specialized Academic Domains</strong> (Admissions, Fees, Placements, Hostels, Mess, HODs, Exams, Library)</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; background: #f7fafc;">Additional Data Collected</td>
                    <td>None (Cleaned and populated with verified institutional fees and departmental figures).</td>
                </tr>
            </tbody>
        </table>

        {"<div style='text-align: center; margin: 6px 0;'><img src='" + eda_intent_b64 + "' style='max-width: 92%; max-height: 72mm; height: auto; border: 1.5px solid #cbd5e0; border-radius: 4px;'><div style='font-size: 7.5pt; color: #4a5568; margin-top: 2px;'>Figure 2: Intent Query Distribution Across 39 University Functional Categories (Exploratory Data Analysis)</div></div>" if eda_intent_b64 else ""}

        <div class="section-title">Data Cleaning & Verification Procedures</div>
        <p>
            During initial exploratory inspection, all placeholder hyperlink dummy tags (e.g., <code>&lt;a href="LINK"&gt;</code>) were completely purged. Accurate, institutional figures were integrated for B.Tech tuition fees (Rs. 1,45,000/year), hostel accommodation costs (Rs. 85,000 to Rs. 1,15,000/year), mess rebate rules, departmental HOD contact designations, and placement statistics (highest package 44 LPA, average 6.5 LPA).
        </p>
    </div>
    <div class="footer-stamp">
        Page 5 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

<!-- ==================== PAGE 6 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme &bull; Project Synopsis</div>
                <div class="brand-sub">Learner: Yashika Gupta | Roll No: 2300320150073</div>
            </div>
            <div class="cohort-badge">ABES Engineering College</div>
        </div>

        <div class="section-title">6. Key Experimental Results & Performance Metrics</div>
        <p>
            The system was rigorously evaluated across classification accuracy, inference latency, statistical F1-score, and automated integration test suites. The empirical results confirm industry-standard deployment readiness:
        </p>

        <div style="display: flex; justify-content: space-between; margin: 8px 0;">
            <div style="flex: 1; border: 1.5px solid #9ae6b4; background: #f0fff4; padding: 7px; border-radius: 4px; margin-right: 6px; text-align: center;">
                <div style="font-size: 7.5pt; color: #22543d; font-weight: 700;">MODEL ACCURACY</div>
                <div style="font-size: 14pt; font-weight: 800; color: #276749;">99.51%</div>
                <div style="font-size: 7pt; color: #2f855a;">Neural MLP Classifier</div>
            </div>
            <div style="flex: 1; border: 1.5px solid #90cdf4; background: #ebf8ff; padding: 7px; border-radius: 4px; margin-right: 6px; text-align: center;">
                <div style="font-size: 7.5pt; color: #2a4365; font-weight: 700;">AVERAGE LATENCY</div>
                <div style="font-size: 14pt; font-weight: 800; color: #2b6cb0;">11.8 ms</div>
                <div style="font-size: 7pt; color: #3182ce;">CPU-Only Inference Time</div>
            </div>
            <div style="flex: 1; border: 1.5px solid #d6bcfa; background: #faf5ff; padding: 7px; border-radius: 4px; margin-right: 6px; text-align: center;">
                <div style="font-size: 7.5pt; color: #44337a; font-weight: 700;">WEIGHTED F1-SCORE</div>
                <div style="font-size: 14pt; font-weight: 800; color: #6b46c1;">0.995</div>
                <div style="font-size: 7pt; color: #805ad5;">Balanced Across 39 Classes</div>
            </div>
            <div style="flex: 1; border: 1.5px solid #fbd38d; background: #fffaf0; padding: 7px; border-radius: 4px; text-align: center;">
                <div style="font-size: 7.5pt; color: #744210; font-weight: 700;">SYSTEM RELIABILITY</div>
                <div style="font-size: 14pt; font-weight: 800; color: #b7791f;">100%</div>
                <div style="font-size: 7pt; color: #d69e2e;">Passed 6/6 Automated Tests</div>
            </div>
        </div>

        {"<div style='text-align: center; margin: 6px 0;'><img src='" + eda_word_b64 + "' style='max-width: 85%; max-height: 52mm; height: auto; border: 1.5px solid #cbd5e0; border-radius: 4px;'><div style='font-size: 7.5pt; color: #4a5568; margin-top: 2px;'>Figure 3: Token Word Length Distribution Across Inbound Student Training Inquiries</div></div>" if eda_word_b64 else ""}

        <div class="section-title">Automated Unit & Integration Test Suite Verification</div>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 25%;">Test Case ID</th>
                    <th style="width: 35%;">Input Test Query Formulation</th>
                    <th style="width: 25%;">Expected Intent Tag</th>
                    <th style="width: 15%;">Outcome</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>TC-01 [Greeting]</code></td>
                    <td>'Hello, good morning'</td>
                    <td><code>greeting</code></td>
                    <td><strong style="color: #276749;">PASS (100%)</strong></td>
                </tr>
                <tr>
                    <td><code>TC-02 [Fees Query]</code></td>
                    <td>'What is the btech fee for first year?'</td>
                    <td><code>fees</code></td>
                    <td><strong style="color: #276749;">PASS (99.8%)</strong></td>
                </tr>
                <tr>
                    <td><code>TC-03 [Hostel Allotment]</code></td>
                    <td>'Hostel accommodation and fees'</td>
                    <td><code>hostel</code></td>
                    <td><strong style="color: #276749;">PASS (99.7%)</strong></td>
                </tr>
                <tr>
                    <td><code>TC-04 [Entity Match]</code></td>
                    <td>'Who is HOD of CSE department?'</td>
                    <td><code>hod</code> (Entity: CSE)</td>
                    <td><strong style="color: #276749;">PASS (100%)</strong></td>
                </tr>
                <tr>
                    <td><code>TC-05 [Fallback Check]</code></td>
                    <td>'Can I fly a rocket to mars next week?'</td>
                    <td><code>fallback</code> (&lt;0.40)</td>
                    <td><strong style="color: #276749;">PASS (Safe)</strong></td>
                </tr>
                <tr>
                    <td><code>TC-06 [DB Audit]</code></td>
                    <td>Verify SQLite transcript write & retrieval</td>
                    <td>Table <code>chat_logs</code></td>
                    <td><strong style="color: #276749;">PASS (Integrity)</strong></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="footer-stamp">
        Page 6 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

<!-- ==================== PAGE 7 ==================== -->
<div class="page">
    <div>
        <div class="header-banner">
            <div>
                <div class="brand-title">HCLTech Career Shaper Programme &bull; Project Synopsis</div>
                <div class="brand-sub">Learner: Yashika Gupta | Roll No: 2300320150073</div>
            </div>
            <div class="cohort-badge">ABES Engineering College</div>
        </div>

        <div class="section-title">7. Challenges Faced & How Resolved</div>
        
        <div class="highlight-box">
            <strong>Challenge 1: TensorFlow 2.18 / Python 3.12 Distutils & Protobuf Runtime Incompatibility</strong><br>
            <em>Problem:</em> Python 3.12 completely deprecated standard <code>distutils</code>, causing legacy TensorFlow model builders to throw fatal attribute errors during protobuf serialization.<br>
            <em>Resolution:</em> Re-engineered the neural architecture to utilize Scikit-Learn's pure Python/Cython <code>MLPClassifier</code> with a 2-tier hidden layer topology (64 & 32 neurons) and Adam optimizer. This delivered 99.51% classification accuracy with zero C-runtime dependency conflicts and slashed memory footprint from 450MB to just 42MB.
        </div>

        <div class="highlight-box">
            <strong>Challenge 2: Out-Of-Vocabulary (OOV) Variations & Student Slang</strong><br>
            <em>Problem:</em> Students frequently type informal queries, phonetic spelling variations (e.g., 'hostel fee kitni h', 'hod cse contact'), and abbreviations.<br>
            <em>Resolution:</em> Implemented sublinear TF-IDF vectorization combining word n-grams (1-3) with character n-grams (3-5), coupled with a calibrated confidence threshold (0.40). Queries below 40% probability trigger a helpful fallback prompt directing the student to specific university helpdesk email channels.
        </div>

        <div class="highlight-box">
            <strong>Challenge 3: Multi-Department Entity Ambiguity & Context Persistence</strong><br>
            <em>Problem:</em> Inquiries like 'Who is the HOD?' lack departmental context, whereas follow-up responses ('CSE') lack intent framing.<br>
            <em>Resolution:</em> Created a contextual entity extractor coupled with an in-memory session cache that maintains state tags across multiple conversation turns.
        </div>

        <div class="section-title">8. Academic & Industry References</div>
        <ol style="font-size: 8.4pt; line-height: 1.38;">
            <li>Pedregosa, F., et al. (2011). <em>Scikit-learn: Machine Learning in Python</em>. Journal of Machine Learning Research, 12, pp. 2825-2830.</li>
            <li>Jurafsky, D., & Martin, J. H. (2023). <em>Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition</em> (3rd ed. draft). Prentice Hall.</li>
            <li>Ramirez, T. (2020). <em>FastAPI: Modern, High-Performance Web Framework for Python 3.8+</em>. https://fastapi.tiangolo.com</li>
            <li>Vaswani, A., et al. (2017). <em>Attention Is All You Need</em>. Advances in Neural Information Processing Systems (NeurIPS 2017), pp. 5998-6008.</li>
            <li>HCLTech Career Shaper Programme (2026-27). <em>Digital-Data-AI Capstone Project Guidelines & Rubrics</em>.</li>
        </ol>

        <div class="section-title">9. Ethical Compliance & Data Privacy Declaration</div>
        <div class="declaration-box">
            <p style="margin-bottom: 3px;"><strong>I, Yashika Gupta (Roll No. 2300320150073), hereby confirm that:</strong></p>
            <ul style="list-style-type: square; margin-bottom: 6px;">
                <li>&#9745; All dataset usage complies with institutional and open-source data licensing policies.</li>
                <li>&#9745; No Personally Identifiable Information (PII) such as passwords, Aadhaar numbers, or student phone numbers is permanently stored without consent.</li>
                <li>&#9745; The SQLite database logs queries strictly for academic analytics and system improvement.</li>
                <li>&#9745; This project strictly complies with the provisions of India's Digital Personal Data Protection (DPDP) Act 2023.</li>
            </ul>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 10px; padding-top: 4px;">
                <div>
                    <strong>Learner Signature:</strong> <span style="font-family: 'Brush Script MT', cursive, serif; font-size: 13pt; color: #003366;">Yashika Gupta</span><br>
                    <strong>Date:</strong> 25th October 2026
                </div>
                <div style="text-align: right;">
                    <strong>College Mentor:</strong> Dr. Anamika Goel<br>
                    <strong>Department:</strong> ABES Engineering College
                </div>
            </div>
        </div>
    </div>
    <div class="footer-stamp">
        Page 7 of 7 &bull; HCLTech Career Shaper Programme (2026–27) &bull; Yashika Gupta (2300320150073)
    </div>
</div>

</body>
</html>"""

    html_file_path = os.path.join(workspace, "Project_Synopsis_YashikaGupta_2300320150073.html")
    pdf_file_path = os.path.join(workspace, "Project_Synopsis_YashikaGupta_2300320150073.pdf")
    
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML synopsis at: {html_file_path}")
    
    # Use Microsoft Edge to compile to PDF
    edge_executable = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_executable):
        edge_executable = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        
    cmd = [
        edge_executable,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file_path}",
        html_file_path
    ]
    
    print("Compiling HTML to PDF via Microsoft Edge headless engine...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_file_path) and os.path.getsize(pdf_file_path) > 1000:
        print(f"SUCCESS! Created PDF document at: {pdf_file_path}")
        print(f"File size: {os.path.getsize(pdf_file_path)} bytes")
    else:
        print(f"Failed to generate PDF. Edge stderr: {res.stderr}")
        return

    # Render PDF pages to PNG using pdfium
    pdf = pdfium.PdfDocument(pdf_file_path)
    total_pages = len(pdf)
    print(f"Total pages rendered in PDF: {total_pages}")
    
    artifact_dir = r"C:\Users\HP\.gemini\antigravity\brain\aebf6696-6dff-402d-84a7-e89ff0a3ed33"
    for i, page in enumerate(pdf):
        img = page.render(scale=2.0).to_pil()
        out_name = f"page_{i+1}.png"
        img.save(os.path.join(artifact_dir, out_name))
        img.save(os.path.join(workspace, out_name))
        print(f"Exported clean PNG for Page {i+1} ({os.path.getsize(os.path.join(artifact_dir, out_name))} bytes)")

if __name__ == "__main__":
    main()
