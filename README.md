# RTC Insight Engine

An AI-powered analytics platform built using RTC (Rewriting The Code) reports. The project combines Business Intelligence, Data Engineering, and Generative AI to transform static reports into interactive insights.

## Overview
<img width="1599" height="832" alt="image" src="https://github.com/user-attachments/assets/a81fd4dc-17b5-4de2-91f9-de858752fb97" />


RTC Insight Engine enables users to:

* Explore RTC impact and recruiting dashboards
* Analyze community and career outcomes
* Ask natural language questions about RTC reports
* Retrieve report-backed answers using RAG (Retrieval-Augmented Generation)
* View supporting sources for every response

## Features

### Interactive Dashboard
<img width="1600" height="829" alt="image" src="https://github.com/user-attachments/assets/2005e60c-6510-4016-8841-1e42db1bbcea" />


* Built with Looker Studio
* Community Impact analytics
* Recruiting Insights analytics
* Career outcomes and RTC metrics

### AI Assistant

* Powered by Gemini
* TF-IDF based retrieval engine
* Answers questions using RTC reports
* Source-backed responses
* RTC knowledge base integration
  <img width="601" height="741" alt="image" src="https://github.com/user-attachments/assets/23dfa614-793e-48fc-818a-17fbbcc456df" />


### Data Engineering Pipeline

* PDF extraction and processing
* Text chunking for retrieval
* Metrics extraction and cleaning
* Structured datasets for analytics

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* FastAPI
* Python

### AI & NLP

* Google Gemini
* TF-IDF Vectorization
* Scikit-Learn
* RAG Architecture

### Analytics

* Looker Studio
* CSV Data Pipeline

## Project Architecture

RTC Reports (PDFs)
↓
Data Extraction
↓
Text Chunking
↓
TF-IDF Retrieval Engine
↓
Gemini AI
↓
AI Responses with Sources


## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd rtc-project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Future Enhancements

* Semantic vector search
* Knowledge graph visualization
* Report comparison mode
* Advanced analytics dashboards
* Dashboard-aware AI responses


Built as a portfolio project demonstrating:

* Data Analytics
* Data Engineering
* Business Intelligence
* FastAPI Development
* Retrieval-Augmented Generation (RAG)
* Generative AI Applications
