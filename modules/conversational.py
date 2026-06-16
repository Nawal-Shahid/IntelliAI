import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

class ConversationalAnalytics:
    """Natural language conversational analytics using Groq"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.3-70b-versatile"
        self.conversation_history = []
    
    def ask_question(self, data, question):
        """Answer natural language questions about the dataset"""
        # Prepare data context
        context = self._prepare_question_context(data, question)
        
        # Build prompt
        prompt = f"""You are IntelliAI, an AI-powered business intelligence assistant. 
Answer the following question about the dataset based on the provided context.

DATASET CONTEXT:
{context}

USER QUESTION: {question}

Provide a clear, accurate, and helpful response. If you don't have enough information, 
suggest what additional data would be helpful. Include specific numbers from the data when relevant.
Be conversational but professional.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert data analyst and business intelligence assistant. Provide accurate, data-driven answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                'question': question,
                'answer': answer
            })
            
            return answer
            
        except Exception as e:
            return f"Unable to process your question at this moment. Error: {str(e)}"
    
    def _prepare_question_context(self, data, question):
        """Prepare relevant context based on the question"""
        context = f"""
Dataset Overview:
- Rows: {len(data):,}
- Columns: {len(data.columns)}
- Column Names: {', '.join(data.columns[:20])}

"""
        
        # Add relevant statistics based on question keywords
        question_lower = question.lower()
        
        # Check for specific column mentions
        mentioned_cols = [col for col in data.columns if col.lower() in question_lower]
        
        if mentioned_cols:
            context += "Relevant Column Statistics:\n"
            for col in mentioned_cols[:5]:
                if pd.api.types.is_numeric_dtype(data[col]):
                    context += f"""
{col}:
- Min: {data[col].min():.2f}
- Max: {data[col].max():.2f}
- Mean: {data[col].mean():.2f}
- Median: {data[col].median():.2f}
- Std Dev: {data[col].std():.2f}
"""
                else:
                    context += f"""
{col}:
- Unique Values: {data[col].nunique()}
- Most Common: {data[col].mode().iloc[0] if len(data[col].mode()) > 0 else 'N/A'}
- Sample Values: {', '.join(str(x) for x in data[col].dropna().head(3))}
"""
        
        # Add correlation info if asking about relationships
        if any(word in question_lower for word in ['correlation', 'relationship', 'related', 'affect', 'impact']):
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                context += "\nCorrelations:\n"
                corr_matrix = data[numeric_cols[:5]].corr()
                context += corr_matrix.to_string()
        
        # Add trend info
        if any(word in question_lower for word in ['trend', 'change', 'increase', 'decrease']):
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                context += "\nRecent Trends (last 10 rows if available):\n"
                context += data[numeric_cols[:5]].tail(10).to_string()
        
        # Add distribution info
        if any(word in question_lower for word in ['distribution', 'spread', 'outlier', 'range']):
            numeric_cols = data.select_dtypes(include=['number']).columns
            for col in numeric_cols[:3]:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                context += f"""
{col} Distribution:
- 25th Percentile: {Q1:.2f}
- 75th Percentile: {Q3:.2f}
- Range: {data[col].min():.2f} to {data[col].max():.2f}
"""
        
        # Add sample data
        context += f"\nSample Data (first 5 rows):\n{data.head(5).to_string()}\n"
        
        # Add missing data info
        missing = data.isnull().sum()
        if missing.sum() > 0:
            context += f"\nMissing Data:\n{missing[missing > 0].to_string()}\n"
        
        return context
    
    def get_conversation_summary(self):
        """Get summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        summary = "Conversation Summary:\n\n"
        for i, exchange in enumerate(self.conversation_history[-5:], 1):
            summary += f"{i}. Q: {exchange['question'][:100]}\n"
            summary += f"   A: {exchange['answer'][:100]}...\n\n"
        
        return summary
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."