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
    
    def extract_relevant_experience(self, documents_text: Dict[str, str], job_description: str, 
                                   language: str = "english") -> str:
        """
        Extract and summarize relevant experience from documents based on job description.
        
        Args:
            documents_text: Dictionary mapping file paths to extracted text
            job_description: Target job description
            language: Target language for the output (default: "english")
            
        Returns:
            Extracted and formatted relevant experience
        """
        all_text = "\n\n".join([
            f"=== {file_path} ===\n{content}" 
            for file_path, content in documents_text.items()
        ])
        
        # Language-specific instructions
        language_instructions = {
            "english": "Generate ALL content in ENGLISH only. Use professional American English terminology.",
            "chinese": "Generate ALL content in CHINESE only. Use professional Chinese terminology.",
            "bilingual": "Generate content with both English and Chinese versions where appropriate."
        }
        
        language_instruction = language_instructions.get(language.lower(), language_instructions["english"])
        
        prompt = f"""
You are an expert resume writer. Extract and summarize the most relevant experience from the user's documents to match the target job description.

LANGUAGE REQUIREMENT: {language_instruction}

TARGET JOB DESCRIPTION:
{job_description}

USER DOCUMENTS:
{all_text}

CRITICAL INSTRUCTIONS:
1. **LANGUAGE**: {language_instruction}
2. Focus on experiences that directly relate to the job requirements
3. Highlight quantifiable achievements and measurable results
4. Use keywords from the job description where appropriate
5. Organize the information clearly under relevant headings
6. Emphasize technical skills and tools mentioned in the job description
7. Format the response as structured markdown
8. ALL output must be in {language.upper()} language only

Please extract and format the most relevant information under these sections:
- Experience (with specific projects and achievements)
- Skills (technical and soft skills)
- Education (relevant qualifications)
- Achievements (awards, certifications, notable accomplishments)

Focus on making the candidate's background appear as relevant as possible to the target role.
Generate ALL content in {language.upper()} language only.
"""

        system_message = f"You are an expert resume writer who helps candidates highlight their most relevant experience for specific job opportunities. Always respond in {language.upper()} only."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error in AI processing: {str(e)}")
            raise Exception(f"Failed to process content with AI: {str(e)}")
    
    def generate_profile_from_template(self, template_content: str, extracted_info: str, 
                                     profile_name: str, job_description: str, 
                                     language: str = "english") -> str:
        """
        Generate a complete profile by filling template with extracted information.
        
        Args:
            template_content: Template markdown content
            extracted_info: AI-extracted relevant information
            profile_name: Name for the profile
            job_description: Target job description
            language: Target language for the resume (default: "english")
            
        Returns:
            Complete profile content in markdown format
        """
        
        # Language-specific instructions
        language_instructions = {
            "english": "Generate ALL content in ENGLISH only. Use professional American English terminology and formatting conventions.",
            "chinese": "Generate ALL content in CHINESE only. Use professional Chinese terminology and formatting conventions.",
            "bilingual": "Generate content with both English and Chinese versions where appropriate."
        }
        
        language_instruction = language_instructions.get(language.lower(), language_instructions["english"])
        
        prompt = f"""
You are creating a professional resume using a specific template format. Fill in the template with the provided extracted information.

LANGUAGE REQUIREMENT: {language_instruction}

TEMPLATE FORMAT:
{template_content}

EXTRACTED RELEVANT INFORMATION:
{extracted_info}

TARGET JOB DESCRIPTION:
{job_description}

PROFILE NAME: {profile_name}

CRITICAL INSTRUCTIONS:
1. **LANGUAGE**: {language_instruction}
2. Follow the exact structure and format of the template
3. Replace placeholder content with relevant information from the extracted data
4. Ensure all sections are filled appropriately
5. Maintain professional language and formatting
6. Prioritize information most relevant to the target job
7. Include quantifiable achievements where possible
8. Use keywords from the job description naturally
9. ALL output must be in {language.upper()} language only

Please generate the complete profile following the template structure exactly and in {language.upper()} language.
"""
        
        system_message = f"You are a professional resume writer who creates tailored resumes in {language.upper()} language based on specific templates and job requirements. Always respond in {language.upper()} only."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
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
    
    def generate_resume_content(self, experience_docs: str, job_description: str, 
                               style_reference: str = "", language: str = "english") -> Dict[str, Any]:
        """
        Generate structured resume content using AI.
        
        Args:
            experience_docs: Extracted content from uploaded documents
            job_description: Target job description
            style_reference: Optional style reference content
            language: Target language for the resume (default: "english")
            
        Returns:
            Dictionary containing structured resume data
        """
        try:
            # Language-specific instructions
            language_instructions = {
                "english": "Generate ALL content in ENGLISH only. Use professional American English terminology.",
                "chinese": "Generate ALL content in CHINESE only. Use professional Chinese terminology.",
                "bilingual": "Generate content with both English and Chinese versions where appropriate."
            }
            
            instruction = language_instructions.get(language, language_instructions["english"])
            
            prompt = f"""
{instruction}

Based on the following information, generate a structured resume for a job application:

TARGET JOB DESCRIPTION:
{job_description}

CANDIDATE'S BACKGROUND (from uploaded documents):
{experience_docs}

{f"STYLE REFERENCE (use as formatting guide): {style_reference}" if style_reference else ""}

Please generate a well-structured resume with the following components. Return ONLY valid JSON:

{{
    "name": "Extract or infer candidate's full name",
    "contact": "Extract contact information (email, phone, etc.)",
    "summary": "Write a compelling 2-3 sentence professional summary tailored to the target job",
    "experience": "Summarize relevant work experience, highlighting achievements that match job requirements",
    "education": "List educational background relevant to the position",
    "skills": "List key technical and soft skills that match the job requirements",
    "projects": "Highlight relevant projects or accomplishments",
    "certifications": "List any relevant certifications or licenses",
    "achievements": "Notable achievements or awards"
}}

Focus on:
1. Matching the candidate's experience to the job requirements
2. Using action verbs and quantifiable achievements
3. Maintaining professional tone and formatting
4. Emphasizing skills and experience most relevant to the target position
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert resume writer and career counselor. {instruction}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse as JSON first
            try:
                import json
                resume_data = json.loads(content)
                return resume_data
            except json.JSONDecodeError:
                # If JSON parsing fails, extract content manually
                self.logger.warning("AI response was not valid JSON, using fallback parsing")
                return self._parse_resume_content_fallback(content, language)
                
        except Exception as e:
            self.logger.error(f"Error generating resume content: {str(e)}")
            # Return fallback content based on language
            return self._get_fallback_resume_content(language)
    
    def _parse_resume_content_fallback(self, content: str, language: str) -> Dict[str, Any]:
        """
        Fallback method to parse resume content when JSON parsing fails.
        
        Args:
            content: Raw AI response content
            language: Target language
            
        Returns:
            Dictionary containing structured resume data
        """
        # Basic parsing logic - can be enhanced
        lines = content.split('\n')
        
        resume_data = {
            "name": "候选人姓名" if language == "chinese" else "Candidate Name",
            "contact": "联系方式待填写" if language == "chinese" else "Contact information to be filled",
            "summary": "个人简介待填写" if language == "chinese" else "Professional summary to be filled",
            "experience": "工作经验待填写" if language == "chinese" else "Work experience to be filled",
            "education": "教育背景待填写" if language == "chinese" else "Educational background to be filled",
            "skills": "技能列表待填写" if language == "chinese" else "Skills list to be filled",
            "projects": "项目经验待填写" if language == "chinese" else "Project experience to be filled",
            "certifications": "认证信息待填写" if language == "chinese" else "Certifications to be filled",
            "achievements": "成就奖项待填写" if language == "chinese" else "Achievements to be filled"
        }
        
        # Try to extract content from lines
        current_section = None
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                # Map common keys
                if 'name' in key or '姓名' in key:
                    resume_data['name'] = value
                elif 'contact' in key or '联系' in key:
                    resume_data['contact'] = value
                elif 'summary' in key or '简介' in key:
                    resume_data['summary'] = value
                elif 'experience' in key or '经验' in key:
                    resume_data['experience'] = value
                elif 'education' in key or '教育' in key:
                    resume_data['education'] = value
                elif 'skill' in key or '技能' in key:
                    resume_data['skills'] = value
                elif 'project' in key or '项目' in key:
                    resume_data['projects'] = value
        
        return resume_data
    
    def _get_fallback_resume_content(self, language: str) -> Dict[str, Any]:
        """
        Get fallback resume content when AI generation fails.
        
        Args:
            language: Target language
            
        Returns:
            Dictionary containing fallback resume data
        """
        if language == "chinese":
            return {
                "name": "候选人姓名",
                "contact": "邮箱: example@email.com\n电话: +86 123-4567-8900",
                "summary": "经验丰富的专业人士，具有强大的技术背景和解决问题的能力。",
                "experience": "相关工作经验，包括主要职责和成就。",
                "education": "教育背景，包括学位和主要课程。",
                "skills": "Python, JavaScript, 项目管理, 团队协作",
                "projects": "重要项目经验和取得的成果。",
                "certifications": "相关认证和证书。",
                "achievements": "主要成就和获得的奖项。"
            }
        elif language == "bilingual":
            return {
                "name": "Candidate Name / 候选人姓名",
                "contact": "Email: example@email.com / 邮箱: example@email.com\nPhone: +1 123-456-7890 / 电话: +86 123-4567-8900",
                "summary": "Experienced professional with strong technical background / 经验丰富的专业人士，具有强大的技术背景",
                "experience": "Relevant work experience / 相关工作经验",
                "education": "Educational background / 教育背景",
                "skills": "Python, JavaScript, Project Management / Python, JavaScript, 项目管理",
                "projects": "Important project experience / 重要项目经验",
                "certifications": "Relevant certifications / 相关认证",
                "achievements": "Major achievements / 主要成就"
            }
        else:  # english
            return {
                "name": "Candidate Name",
                "contact": "email: example@email.com\nphone: +1 123-456-7890",
                "summary": "Experienced professional with strong technical background and problem-solving abilities.",
                "experience": "Relevant work experience with key responsibilities and achievements.",
                "education": "Educational background including degrees and relevant coursework.",
                "skills": "Python, JavaScript, Project Management, Team Collaboration",
                "projects": "Important project experience and achieved results.",
                "certifications": "Relevant certifications and licenses.",
                "achievements": "Major achievements and awards received."
            } 