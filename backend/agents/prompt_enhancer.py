"""
Prompt Enhancement Agent
Enhances user prompts with technical details, style guides, and best practices.
"""

import os
from typing import Dict, Any
from openai import OpenAI
from .base_agent import BaseAgent, AgentResult


class PromptEnhancerAgent(BaseAgent):
    """
    Agent responsible for enhancing user prompts with:
    - Technical photography/art terms
    - Style specifications
    - Quality improvements
    - Anatomical accuracy hints
    """
    
    def __init__(self):
        super().__init__(
            name="PromptEnhancer",
            description="Enhances user prompts with technical details and best practices"
        )
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Enhances the user's prompt with additional context and technical details.
        """
        try:
            user_prompt = input_data.get("prompt", "")
            
            if not user_prompt:
                return AgentResult(
                    success=False,
                    data={},
                    message="No prompt provided"
                )
            
            # System prompt for prompt enhancement
            enhancement_system_prompt = """You are an expert prompt engineer for AI image generation. 
Your task is to enhance user prompts to generate high-quality, anatomically correct images.

Guidelines:
1. Add technical photography/art terms (lighting, composition, perspective)
2. Include anatomical accuracy cues if the prompt involves humans/animals
3. Add style specifications (realistic, artistic, cinematic)
4. Improve clarity and specificity
5. Add quality modifiers (high detail, sharp focus, professional photography)
6. Keep the original intent while enhancing technical aspects

Return ONLY the enhanced prompt, nothing else."""

            # Call OpenAI to enhance the prompt
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": enhancement_system_prompt},
                    {"role": "user", "content": f"Enhance this prompt for image generation: {user_prompt}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            enhanced_prompt = response.choices[0].message.content.strip()
            
            return AgentResult(
                success=True,
                data={
                    "original_prompt": user_prompt,
                    "enhanced_prompt": enhanced_prompt
                },
                message="Prompt enhanced successfully",
                metadata={
                    "model": "gpt-4",
                    "enhancement_length": len(enhanced_prompt)
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                message=f"Error enhancing prompt: {str(e)}"
            )

