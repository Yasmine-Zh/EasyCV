"""
AI processor for generating and optimizing resume content using language models.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None
    OpenAI = None

class AIProcessor:
    """AI processor for resume content generation and optimization."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize AI processor.
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
            model: OpenAI model to use
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        
        if OpenAI is None:
            raise ImportError("openai package is required for AI processing")
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_relevant_experience(self, documents_text: Dict[str, str], job_description: str) -> str:
        """
        Extract and summarize relevant experience from documents based on job description.
        
        Args:
            documents_text: Dictionary mapping file paths to extracted text
            job_description: Target job description
            
        Returns:
            Extracted and formatted relevant experience
        """
        all_text = "\n\n".join([
            f"=== {file_path} ===\n{content}" 
            for file_path, content in documents_text.items()
        ])
        
        prompt = f"""
You are an expert resume writer. Extract and summarize the most relevant experience from the user's documents to match the target job description.

TARGET JOB DESCRIPTION:
{job_description}

USER DOCUMENTS:
{all_text}

INSTRUCTIONS:
1. Focus on experiences that directly relate to the job requirements
2. Highlight quantifiable achievements and measurable results
3. Use keywords from the job description where appropriate
4. Organize the information clearly under relevant headings
5. Emphasize technical skills and tools mentioned in the job description
6. Format the response as structured markdown

Please extract and format the most relevant information under these sections:
- Experience (with specific projects and achievements)
- Skills (technical and soft skills)
- Education (relevant qualifications)
- Achievements (awards, certifications, notable accomplishments)

Focus on making the candidate's background appear as relevant as possible to the target role.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer who helps candidates highlight their most relevant experience for specific job opportunities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error in AI processing: {str(e)}")
            raise Exception(f"Failed to process content with AI: {str(e)}")
    
    def generate_profile_from_template(self, template_content: str, extracted_info: str, 
                                     profile_name: str, job_description: str) -> str:
        """
        Generate a complete profile by filling template with extracted information.
        
        Args:
            template_content: Template markdown content
            extracted_info: AI-extracted relevant information
            profile_name: Name for the profile
            job_description: Target job description
            
        Returns:
            Complete profile content in markdown format
        """
        prompt = f"""
You are creating a professional resume using a specific template format. Fill in the template with the provided extracted information.

TEMPLATE FORMAT:
{template_content}

EXTRACTED RELEVANT INFORMATION:
{extracted_info}

TARGET JOB DESCRIPTION:
{job_description}

PROFILE NAME: {profile_name}

INSTRUCTIONS:
1. Follow the exact structure and format of the template
2. Replace placeholder content with relevant information from the extracted data
3. Ensure all sections are filled appropriately
4. Maintain professional language and formatting
5. Prioritize information most relevant to the target job
6. Include quantifiable achievements where possible
7. Use keywords from the job description naturally

Please generate the complete profile following the template structure exactly.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer who creates tailored resumes based on specific templates and job requirements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating profile: {str(e)}")
            raise Exception(f"Failed to generate profile: {str(e)}")
    
    def update_existing_profile(self, old_profile: str, new_documents: Dict[str, str], 
                              new_job_description: Optional[str] = None) -> str:
        """
        Update an existing profile with new information.
        
        Args:
            old_profile: Previous profile content
            new_documents: New documents to incorporate
            new_job_description: Updated job description (optional)
            
        Returns:
            Updated profile content
        """
        new_content = "\n\n".join([
            f"=== {file_path} ===\n{content}" 
            for file_path, content in new_documents.items()
        ])
        
        jd_section = f"\n\nNEW TARGET JOB DESCRIPTION:\n{new_job_description}" if new_job_description else ""
        
        prompt = f"""
You are updating an existing resume with new information. Integrate the new content while maintaining the structure and quality of the original resume.

EXISTING RESUME:
{old_profile}

NEW INFORMATION TO INTEGRATE:
{new_content}{jd_section}

INSTRUCTIONS:
1. Keep the existing structure and format
2. Integrate new experiences, projects, and achievements
3. Update skills section with new technical skills
4. Maintain chronological order where appropriate
5. Remove or de-emphasize less relevant old information if needed
6. Ensure the updated resume remains focused on the target role
7. Keep the most impactful and recent achievements prominent

Please provide the updated resume maintaining the same format and structure.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer who helps update and improve existing resumes with new information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error updating profile: {str(e)}")
            raise Exception(f"Failed to update profile: {str(e)}")
    
    def analyze_resume_style(self, style_reference: str) -> Dict[str, Any]:
        """
        Analyze a reference resume style to extract formatting preferences.
        
        Args:
            style_reference: Reference resume content or style description
            
        Returns:
            Style analysis with formatting preferences
        """
        prompt = f"""
Analyze the following resume style reference and provide a structured analysis of its formatting characteristics.

STYLE REFERENCE:
{style_reference}

Please analyze and return the following aspects:
1. Section structure and organization
2. Font and typography preferences
3. Color scheme and visual elements
4. Layout and spacing characteristics
5. Content presentation style
6. Professional tone and language style

Format your response as a structured analysis that can guide the creation of similar styled documents.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a design analyst specializing in resume formats and professional document styling."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            # For now, return as text; could be enhanced to return structured data
            return {"analysis": response.choices[0].message.content.strip()}
            
        except Exception as e:
            self.logger.error(f"Error analyzing style: {str(e)}")
            return {"analysis": "Style analysis failed", "error": str(e)} 