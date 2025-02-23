# AI Summarization API

## Overview
The AI Summarization API allows users to quickly summarize text or web content across various industries. Whether you need a brief overview of legal cases, financial trends, or scientific articles, this API provides tailored summaries to save time and improve understanding.

## Key Features
- **Instant Summaries**: Extract key insights from text or URLs.
- **Domain-Specific Optimization**: Get tailored summaries for different fields.
- **Flexible Input**: Provide manual text input or a webpage URL.
- **Customizable Length**: Choose between short, medium, or long summaries.

## How It Works
1. Choose a category that best fits your content (e.g., **law, finance, real estate, business, science, education, healthcare, books, politics, or technology**).
2. Provide either **text** or a **URL** to extract content from.
3. Specify the **length** of the summary you need.
4. Get a concise and relevant summary instantly!

## API Usage
### **Endpoint:**
```http
POST /summarize/{category}
```

### **Request Parameters**
| Parameter | Type  | Required | Description |
|-----------|-------|----------|-------------|
| `category` | String | ✅ Yes | The domain of the content (e.g., `law`, `business`, `science`). |
| `text` | String | Optional | The raw text you want summarized. |
| `url` | String (URL) | Optional | A webpage URL to extract and summarize content from. |
| `length` | String | Optional | Choose between `short`, `medium`, or `long` summaries (default: `short`). |

### **Example Request (Summarizing a Legal Case)**
```sh
curl -X 'POST' 
  'https://your-api-url.com/summarize/law' 
  -H 'Content-Type: application/json' 
  -d '{
    "text": "The Supreme Court ruled in favor of data privacy protections...",
    "length": "long"
  }'
```

### **Example Request (Summarizing a News Article from a URL)**
```sh
curl -X 'POST' 
  'https://your-api-url.com/summarize/technology' 
  -H 'Content-Type: application/json' 
  -d '{
    "url": "https://technews.com/latest-ai-trends",
    "length": "short"
  }'
```

### **Example Response**
```json
{
  "category": "law",
  "summary": "The Supreme Court ruled in favor of stricter data privacy laws...",
  "length": "long",
  "source": "manual input"
}
```

## Supported Categories
| Category       | Description |
|---------------|-------------|
| `financials`  | Market trends, stock insights, and economic analysis. |
| `real-estate` | Housing trends, property values, and investment insights. |
| `law`         | Legal case rulings, regulations, and case summaries. |
| `books`       | Book overviews, themes, and literature insights. |
| `technology`  | AI research, software updates, and tech innovations. |
| `healthcare`  | Medical studies, research, and healthcare policies. |
| `science`     | Summaries of scientific discoveries and research. |
| `business`    | Startup news, company reports, and industry trends. |
| `politics`    | Government policies, election updates, and political news. |
| `education`   | Academic papers, learning resources, and research articles. |

## Benefits
✅ **Saves Time** - Get instant summaries without reading full documents.
✅ **Improves Productivity** - Quickly understand important information.
✅ **Works for Various Fields** - Custom-tailored summaries for different industries.

## **Get Started**
Simply send a request with your **text or URL** and get a concise, high-quality summary instantly!

🚀 **Try it now and save time reading!**

